from argparse import ArgumentParser, Action, RawDescriptionHelpFormatter, \
    ArgumentTypeError, BooleanOptionalAction
from collections import namedtuple
from itertools import zip_longest
from functools import partial, reduce
from warnings import warn
import h5py
import numpy as np
from scipy.spatial.transform import Rotation as R
import hpc_suite as hpc
from .basis import parse_termsymbol, couple, unitary_transform
from .multi_electron import Ion
from .crystal import SpinHamiltonian, ZeemanHamiltonian, read_params, \
    zeeman_hamiltonian, HARTREE2INVCM, print_basis, make_operator_storage, \
    MagneticSusceptibilityFromFile, EPRGtensorFromFile, \
    TintFromFile
import jax.numpy as jnp
from jax import vmap, pmap, jit


# Action for secondary help message
class SecondaryHelp(hpc.SecondaryHelp):
    def __init__(self, option_strings, dest=None, const=None, default=None,
                 help=None):
        super().__init__(option_strings, dest=dest, const=const,
                         default=default, help=help)

    def __call__(self, parser, values, namespace, option_string=None):
        read_args([self.const, '--help'])


class QuaxAction(Action):
    def __init__(self, option_strings, dest, nargs=1, default=None, type=None,
                 choices=None, required=False, help=None, metavar=None):

        super().__init__(
            option_strings=option_strings, dest=dest, nargs=nargs,
            default=default, type=type, choices=choices, required=required,
            help=help, metavar=metavar
        )

    def __call__(self, parser, namespace, value, option_string=None):

        try:  # import from HDF5 database
            with h5py.File(value[0], 'r') as h:
                quax = h["quax"][...]
        except FileNotFoundError:  # choose coordinate system axis
            # cyclic permutation
            perm = {"x": [1, 2, 0], "y": [2, 0, 1], "z": [0, 1, 2]}[value[0]]
            quax = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])[perm]
        except OSError:
            quax = np.loadtxt(value[0])
        except:
            raise ValueError("Invalid QUAX specification.")

        setattr(namespace, self.dest, quax)


def parse_coupling(string):
    j, j1j2 = hpc.make_parse_dict(str, str)(string)
    j1, j2 = tuple(j1j2.split(','))

    if not j2:
        raise ArgumentTypeError("Expected comma separated angmom symbols.")

    return (j, (j1, j2))


def parse_term(string):
    term, ops = hpc.make_parse_dict(str, str)(string)
    return (term, tuple(ops.split(',')))


def parse_index(x):
    return int(x) - 1


proj_parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        add_help=False
)

proj_parser.add_argument(
    '--model_space',
    type=parse_termsymbol,
    help='Symbol of the model space.'
)

proj_parser.add_argument(
    '--coupling',
    nargs='*',
    default={},
    action=hpc.action.ParseKwargs,
    type=parse_coupling,
    metavar="j=j1,j2",
    help='Coupling dictionary connecting the basis space to the model space.'
)

proj_parser.add_argument(
    '--basis',
    default='l',
    choices=['l', 'j'],
    help='Intermediate ab initio basis representation.'
)

proj_parser.add_argument(
    '--truncate',
    type=int,
    help='Truncate ab initio space before constucting the angmom basis.'
)

proj_parser.add_argument(
    '--terms',
    nargs='*',
    default={},
    action=hpc.action.ParseKwargsAppend,
    type=parse_term,
    metavar="term=j1,j2,...",
    help='Dictionary of spin Hamiltonian terms.'
)

proj_parser.add_argument(
    '--k_max',
    type=int,
    default=6,
    help='Maximum Stevens operator rank.'
)

proj_parser.add_argument(
    '--theta',
    action='store_true',
    help='Factor out operator equivalent factors.'
)

proj_parser.add_argument(
    '--ion',
    type=Ion.parse,
    # choices=[Ion.parse('Dy3+')],
    help='Central ion.'
)

proj_parser.add_argument(
    '--iso_soc',
    action='store_true',
    help='Assume isotropic spin-orbit coupling.'
)

proj_parser.add_argument(
    '--quax',
    action=QuaxAction,
    help='Quantisation axes. Given either as x, y or z,'
         'or as a 3x3 matrix in a text file using SINGLE_ANISO format.'
         'That is, (Rz(a)Ry(b)Rz(g))^T, where Rz and Ry are rotation'
         'matrices around z and y, and a, b, g are the Euler angles.'
         'e.g. --quax quax.txt'
)

proj_parser.add_argument(
    '--zeeman',
    action='store_true',
    help=('By default construct the Zeeman Hamiltonian from the canonical '
          'total spin and orbital angular momentum operators. '
          'Alternatively, Hzee may be constructed using the effective '
          'g-values of the model angular momentum operators.')
)


def model_func(args, unknown_args):

    model = SpinHamiltonian(
        args.model_space,
        **args.terms,
        k_max=args.k_max,
        theta=args.theta,
        ion=args.ion,
        time_reversal_symm="even",
        iso_soc=args.iso_soc,
        diag=False
    )

    # read parameters
    params = dict(p for f, m in zip_longest(args.input, args.map, fillvalue={})
                  for p in read_params(f, **dict(m)))

    basis_space, cg_vec = couple(args.model_space, **args.coupling)

    # compute trafo from model basis to coupled (and rotated) angmom basis
    # ===================================================================
    # The aim of the quax rotation is to redefine the coordinate frame, and in particular the orientation of the z-axis
    # First approach: Active rotation of the physical system, i.e. all vector operators (angm, spin) via:
    #                 quax * vector = D^dagger(quax) vector D(quax)
    #                 -> The basis states remain eigenstates of the angular momentum operators of the unrotated system!
    # Second approach: Passive rotation (= "unrotation") of the Hamiltonian basis via: D^dagger(quax.T) H D(quax.T),
    #                  and leaving the angular momentum operators untouched.
    # The second approach corresponds effectively to the overall rotation of the physical system AND basis through:
    # D^dagger(quax.T) D^dagger(quax) vector D(quax) D(quax.T).
    # The advantage is that the rotated angular momentum operators in the rotated basis have the same structure
    # as the unrotated angular momentum operators in the unrotated basis
    # (e.g. correspondence between third component of rotated operator and z-component of original operator).
    # This facilitates a straightforward interpretation of the state composition and direct analogy
    # to the calculation with the quax rotation applied at the proj stage. Hence, the second approach is employed.

    def trafo(op, rot=False):
        if args.quax is not None and rot:  # compute basis change from basis rotation
            rotation = args.model_space.rotate(R.from_matrix(args.quax.T))
            return unitary_transform(op, rotation @ cg_vec)
        else:
            return unitary_transform(op, cg_vec)

    hamiltonian = model.parametrise(
        params, scale=args.scale, verbose=args.verbose) / HARTREE2INVCM

    if args.zeeman:
        spin, angm = ZeemanHamiltonian(args.model_space).resolve_zeeman_ops(params, verbose=True)

    else:
        spin = np.sum([args.model_space.get_op(op)
                       for op in args.model_space.elementary_ops('spin')], axis=0)

        if spin.size == 1:
            warn("No spin momenta present assuming S=0!")

        angm = np.sum([args.model_space.get_op(op)
                       for op in args.model_space.elementary_ops('angm')], axis=0)

        if angm.size == 1:
            warn("No orbital momenta present assuming L=0!")

    # print trafo from diagonal basis to coupled + rotated angmom basis
    print_basis(trafo(hamiltonian, rot=True), trafo(spin), trafo(angm),
                basis_space, comp_thresh=args.comp_thresh, shift=args.shift,
                field=args.field)

    store_args = hpc.read_args(['store'] + unknown_args)

    ops = {"hamiltonian": trafo(hamiltonian, rot=True), "spin": trafo(spin), "angm": trafo(angm)}

    hpc.store_func(store_args, make_operator_storage, list(ops.keys()), **ops)


def sus_func(args, unknown_args):

    store_args = hpc.read_args(['store'] + unknown_args)
    kwargs = hpc.filter_parser_args(args)

    hpc.store_func(store_args, lambda f, store, **kwargs: store(f, **kwargs),
                   (MagneticSusceptibilityFromFile,), **kwargs)


def eprg_func(args, unknown_args):

    store_args = hpc.read_args(['store'] + unknown_args)
    kwargs = hpc.filter_parser_args(args)

    hpc.store_func(store_args, lambda f, store, **kwargs: store(f, **kwargs),
                   (EPRGtensorFromFile,), **kwargs)


def tint_func(args, unknown_args):

    store_args = hpc.read_args(['store'] + unknown_args)
    kwargs = hpc.filter_parser_args(args)

    hpc.store_func(store_args, lambda f, store, **kwargs: store(f, **kwargs),
                   (TintFromFile,), **kwargs)


def read_args(arg_list=None):

    description = '''
    A package for angular momentum related functionalities.
    '''

    epilog = '''
    Lorem ipsum.
    '''

    parser = ArgumentParser(
            description=description,
            epilog=epilog,
            formatter_class=RawDescriptionHelpFormatter
            )

    subparsers = parser.add_subparsers(dest='prog')

    subparsers.add_parser('proj', parents=[proj_parser])

    ham = subparsers.add_parser('model', parents=[proj_parser])
    ham.set_defaults(func=model_func)

    ham.add_argument(
        '--input', '-i',
        default=[],
        nargs='+',
        help='HDF5 data bases containing the spin Hamiltonian parameters.'
    )

    ham.add_argument(
        '--map',
        nargs='+',
        type=hpc.make_parse_dict(str, str),
        default=[],
        action='append',
        help=('Mapping of angular momentum quantum numbers to unique '
              'identifiers in order of input files. Necessary when combining '
              'parameter files with overlapping identifiers.')
    )

    ham.add_argument(
        '--scale',
        nargs='*',
        default={},
        action=hpc.action.ParseKwargs,
        type=hpc.make_parse_dict(str, float),
        help='Scale model term by factor.'
    )

    ham.add_argument(
        '--comp_thresh',
        default=0.05,
        type=float,
        help='Amplitude threshold for composition contribution printing.'
    )

    ham.add_argument(
        '--field',
        default=0.0,
        type=float,
        help='Apply magnetic field (in mT) to split basis states.'
    )

    ham.add_argument(
        '--verbose',
        action='store_true',
        help='Print out extra information.'
    )

    ham.add_argument(
        '--shift',
        action=BooleanOptionalAction,
        default=True,
        help='Shift eigenvalues in basis print-out.'
    )

    sus = subparsers.add_parser('sus')
    sus.set_defaults(func=sus_func)

    sus.add_argument(
        '--temperatures',
        nargs='+',
        type=float,
        help='Temperatures at which chi is calculated.'
    )

    sus.add_argument(
        '--field',
        default=0.0,
        type=float,
        help=('Determine susceptibility at finite field (in mT). '
              'If zero calculate differential susceptibility.')
    )

    sus.add_argument(
        '--differential',
        action=BooleanOptionalAction,
        help='Calculate differential susceptibility.'
    )

    sus.add_argument(
        '--iso',
        action='store_true',
        help='Compute isotropic susceptibility from full tensor.'
    )

    sus.add_argument(
        '--chi_T',
        action=BooleanOptionalAction,
        help='Calculate susceptibility times temperature.'
    )

    eprg = subparsers.add_parser('eprg')
    eprg.set_defaults(func=eprg_func)

    eprg_output = eprg.add_mutually_exclusive_group(required=True)

    eprg.add_argument(
        '--multiplets',
        nargs='+',
        type=int,
        help='Manually define multiplets of the ground electronic manifold.'
    )

    eprg_output.add_argument(
        '--eprg_values',
        action='store_true',
        help='Compute principal values of the G-tensor'
    )

    eprg_output.add_argument(
        '--eprg_vectors',
        action='store_true',
        help='Compute principal axes of the G-tensor'
    )

    eprg_output.add_argument(
        '--eprg_tensors',
        action='store_true',
        help='Compute G-tensor in the Cartesian frame'
    )

    tint = subparsers.add_parser('tint')
    tint.set_defaults(func=tint_func)

    tint.add_argument(
        '--field',
        default=0.,
        type=float,
        help='Determine tint at finite field (in mT along z).'
    )

    tint.add_argument(
        '--states',
        type=parse_index,
        nargs='+',
        help='Subset of states for which the tint will be computed.'
    )

    # read sub-parser
    parser.set_defaults(func=lambda args: parser.print_help())
    args, hpc_args = parser.parse_known_args(arg_list)

    # select parsing option based on sub-parser

    if arg_list:
        return hpc.filter_parser_args(args)

    if args.prog in ['model', 'sus', 'eprg', 'tint']:
        args.func(args, hpc_args)

    else:
        args.func(args)


def main():
    read_args()
