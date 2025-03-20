"""
This module contains functions for working with crystal field Hamiltonians
"""

from functools import reduce, lru_cache, partial
from itertools import product, zip_longest, combinations, accumulate
from collections import namedtuple
from fractions import Fraction
import warnings
from operator import mul, add
import h5py

from jax import numpy as jnp
from jax import scipy as jscipy
from jax import grad, jacfwd, jit, vmap
from jax.lax import stop_gradient
from jax import config

import numpy as np

import jax.numpy.linalg as la

from sympy.physics.wigner import wigner_3j, wigner_6j
import scipy.special as ssp
from scipy import integrate
from scipy.optimize import minimize

from hpc_suite.store import Store

from . import utils as ut
from .basis import unitary_transform, cartesian_op_squared, rotate_cart, perturb_doublets, \
    sfy, calc_ang_mom_ops, make_angmom_ops_from_mult, project_irrep_basis, project_function_basis, \
    Symbol, Term, Level, couple, sf2ws, sf2ws_amfi, extract_blocks, from_blocks, \
    dissect_array, SPIN_SYMBOLS, ANGM_SYMBOLS, TOTJ_SYMBOLS, wigner_eckart_reduce, \
    print_sf_term_content, print_so_term_content, sph_comps, cart_comps, we_reduce_term_blocks, we_reduce_blocks



N_TOTAL_CFP_BY_RANK = {2: 5, 4: 14, 6: 27}
RANK_BY_N_TOTAL_CFP = {val: key for key, val in N_TOTAL_CFP_BY_RANK.items()}
HARTREE2INVCM = 219474.6

config.update("jax_enable_x64", True)


@lru_cache(maxsize=None)
def recursive_a(k, q, m):
    """
    Given k,q,m this function
    calculates and returns the a(k,q-1,m)th
    Ryabov coefficient by recursion

    Parameters
    ----------
    k : int
        k value (rank)
    q : int
        q value (order)
    m : int
        m value

    Returns
    -------
    np.ndarray
        a(k,q,m) values for each power of X=J(J+1) (Ryabov) up to k+1
    """

    coeff = np.zeros(k+1)

    # Catch exceptions/outliers and end recursion
    if k == q-1 and m == 0:
        coeff[0] = 1
    elif q-1 + m > k:
        pass
    elif m < 0:
        pass
    else:
        # First and second terms
        coeff += (2*q+m-1)*recursive_a(k, q+1, m-1)
        coeff += (q*(q-1) - m*(m+1)/2) * recursive_a(k, q+1, m)

        # Third term (summation)
        for n in range(1, k-q-m+1):
            # First term in sum of third term
            coeff[1:] += (-1)**n * (
                            ut.binomial(m+n, m) * recursive_a(k, q+1, m+n)[:-1]
                        )
            # Second and third term in sum
            coeff += (-1)**n * (
                        - ut.binomial(m+n, m-1) - ut.binomial(m+n, m-2)
                    ) * recursive_a(k, q+1, m+n)

    return coeff


def get_ryabov_a_coeffs(k_max):

    """
    Given k_max this function calculates all possible values
    of a(k,q,m) for each power (i) of X=J(J+1)

    Parameters
    ----------
    k_max : int
        maximum k (rank) value

    Returns
    -------
    np.ndarray
        All a(k,q,m,i)
    np.ndarray
        Greatest common factor of each a(k,q,:,:)
    """

    a = np.zeros([k_max, k_max+1, k_max+1, k_max+1])
    f = np.zeros([k_max, k_max+1])

    # Calculate all a coefficients
    for k in range(1, k_max + 1):
        for qit, q in enumerate(range(k, -1, -1)):
            for m in range(k-q + 1):
                a[k-1, qit, m, :k+1] += recursive_a(k, q+1, m)

    # Calculate greatest common factor F for each a(k,q) value
    for k in range(1, k_max + 1):
        for qit, q in enumerate(range(k, -1, -1)):
            allvals = a[k-1, qit, :, :].flatten()
            nzind = np.nonzero(allvals)
            if np.size(nzind) > 0:
                f[k-1, qit] = reduce(ut.GCD, allvals[nzind])

    return a, f


def calc_stev_ops(k_max, J, jp, jm, jz):
    """
    Calculates all Stevens operators Okq with k even and odd from k=1 to k_max
    k_max must be <= 12 (higher rank parameters require quad precision floats)

    Parameters
    ----------
    k_max : int
        maximum k value (rank)
    J : int
        J quantum number
    jp : np.array
        Matrix representation of angular momentum operator
    jm : np.array
        Matrix representation of angular momentum operator
    jz : np.array
        Matrix representation of angular momentum operator

    Returns
    -------
    np.ndarray
        Stevens operators shape = (n_k, n_q, (2J+1), (2J+1))
            ordered k=1 q=-k->k, k=2 q=-k->k ...
    """

    # Only k <= 12 possible at double precision
    # k_max = min(k_max, 12)
    if k_max > 12:
        warnings.warn("Stevens operator with k > 12 requested. This will "
                      "likely lead to numerical errors at double precision!")

    # Get a(k,q,m,i) coefficients and greatest common factors
    a, f = get_ryabov_a_coeffs(k_max)

    # Sum a(k,q,m,i) coefficients over powers of J to give a(k,q,m)
    a_summed = np.zeros([k_max, k_max+1, k_max+1])

    for i in range(0, k_max+1):
        a_summed += a[:, :, :, i] * float(J*(J+1))**i

    _jp = np.complex128(jp)
    _jm = np.complex128(jm)
    _jz = np.complex128(jz)

    n_states = int(2*J+1)

    okq = np.zeros([k_max, 2*k_max+1, n_states, n_states], dtype=np.complex128)

    # Calulate q operators both + and - at the same time
    for kit, k in enumerate(range(1, k_max + 1)):
        # New indices for q ordering in final okq array
        qposit = 2*k + 1
        qnegit = -1
        for qit, q in enumerate(range(k, -1, -1)):
            qposit -= 1
            qnegit += 1
            if k % 2:  # Odd k, either odd/even q
                alpha = 1.
            elif q % 2:  # Even k, odd q
                alpha = 0.5
            else:  # Even k, even q
                alpha = 1.

            # Positive q
            for m in range(k-q + 1):
                okq[kit, qposit, :, :] += a_summed[kit, qit, m]*(
                    (
                        la.matrix_power(_jp, q)
                        + (-1.)**(k-q-m)*la.matrix_power(_jm, q)
                    ) @ la.matrix_power(_jz, m)
                )

            okq[kit, qposit, :, :] *= alpha/(2*f[kit, qit])

            # Negative q
            if q != 0:
                for m in range(k-q + 1):
                    okq[kit, qnegit, :, :] += a_summed[kit, qit, m]*(
                        (
                            la.matrix_power(_jp, q)
                            - (-1.)**(k-q-m)*la.matrix_power(_jm, q)
                        ) @ la.matrix_power(_jz, m)
                    )

                okq[kit, qnegit, :, :] *= alpha/(2j*f[kit, qit])

    return okq


def load_CFPs(f_name, style="phi", k_parity="even"):
    """
    Loads Crystal Field Parameters (CFPs) from file

    Parameters
    ----------
    f_name : str
        file name to load CFPs from
    style : str {'phi','raw'}
        Style of CFP file:
            Phi = Chilton's PHI Program input file
            raw = list of CFPs arranged starting with smallest value of k
                  following the scheme k=k_min q=-k->k, k=k_min+1 q=-k->k ...
    k_parity : str {'even', 'odd', 'both'}
        Indicates type of k values
            e.g. k=2,4,6,... or k=1,3,5,... or k=1,2,3...

    Returns
    -------
    np.ndarray
        CFPs with shape = (n_k, n_q)
            ordered k=k_min q=-k->k, k=k_min+mod q=-k->k ...
            where mod is 1 or 2 depending upon k_parity
    """

    _CFPs = []
    if style == "phi":
        # PHI does not support odd rank cfps
        k_parity = "even"
        # Read in CFPs, and k and q values
        kq = []
        # site, k, q, Bkq
        with open(f_name, 'r') as f:
            for line in f:
                if '****crystal' in line.lower():
                    line = next(f)
                    while "****" not in line:
                        kq.append(line.split()[1:3])
                        _CFPs.append(line.split()[3])
                        line = next(f)
                    break
        kq = [[int(k), int(q)] for [k, q] in kq]
        _CFPs = np.array([float(CFP) for CFP in _CFPs])

        # Include zero entries for missing CFPs
        # and reorder since PHI files might be in wrong order

        # find largest k and use to set size of array
        k_max = np.max(kq[0])
        n_cfps = np.sum([2*k + 1 for k in range(k_max, 0, -1)])
        CFPs = np.zeros([n_cfps])
        if k_parity == "even":
            for CFP, [k, q] in zip(_CFPs, kq):
                CFPs[_even_kq_to_num(k, q)] = CFP
        elif k_parity == "odd":
            for CFP, [k, q] in zip(_CFPs, kq):
                CFPs[_odd_kq_to_num(k, q)] = CFP
        else:
            for CFP, [k, q] in zip(_CFPs, kq):
                CFPs[_kq_to_num(k, q)] = CFP

    elif style == "raw":
        CFPs = np.loadtxt(f_name)

    return CFPs


def calc_HCF(J, cfps, stev_ops, k_max=False, oef=[]):
    """
    Calculates and diagonalises crystal field Hamiltonian (HCF)
    using CFPs Bkq and Stevens operators Okq, where k even and ranges 2 -> 2j

    Hamiltonian is sum_k (sum_q (oef_k*Bkq*Okq))

    Parameters
    ----------
    J : float
        J quantum number
    cfps : np.array
        Even k crystal Field parameters, size = (n_k*n_q)
        ordered k=2 q=-k->k, k=4 q=-k->k ...
    np.ndarray
        Stevens operators, shape = (n_k, n_q, (2J+1), (2J+1))
        ordered k=2 q=-k->k, k=4 q=-k->k ...
    k_max : int, default = 2*J
        Maximum value of k to use in summation
    oef : np.ndarray, optional
        Operator equivalent factors for each CFP i.e. 27 CFPs = 27 OEFs
        size = (n_k*n_q), ordered k=2 q=-k->k, k=4 q=-k->k ...

    Returns
    -------
    np.array
        Matrix representation of Crystal Field Hamiltonian (HCF)
    np.array
        Eigenvalues of HCF (lowest eigenvalue is zero)
    np.array
        Eigenvectors of HCF
    """

    if not k_max:
        k_max = int(2*J)
        k_max -= k_max % 2
        k_max = min(k_max, 12)

    if not len(oef):
        oef = np.ones(cfps.size)

    # calculate number of states
    n_states = int(2 * J + 1)

    # Form Hamiltonian
    HCF = np.zeros([n_states, n_states], dtype=np.complex128)
    for kit, k in enumerate(range(2, k_max+1, 2)):
        for qit, q in enumerate(range(-k, k+1)):
            HCF += stev_ops[kit, qit, :, :] * cfps[_even_kq_to_num(k, q)] \
                    * oef[_even_kq_to_num(k, q)]

    # Diagonalise
    CF_val, CF_vec = la.eigh(HCF)

    # Set ground energy to zero
    CF_val -= CF_val[0]

    return HCF, CF_val, CF_vec


def calc_oef(n, J, L, S):
    """
    Calculate operator equivalent factors for Stevens Crystal Field
    Hamiltonian in |J, mJ> basis

    Using the approach of
    https://arxiv.org/pdf/0803.4358.pdf

    Parameters
    ----------
    n : int
        number of electrons in f shell
    J : float
        J Quantum number
    L : int
        L Quantum number
    S : float
        S Quantum number

    Returns
    -------
    np.ndarray
        operator equivalent factors for each parameter, size = (n_k*n_q)
        ordered k=2 q=-k->k, k=4 q=-k->k ...
    """

    def _oef_lambda(p, J, L, S):
        lam = (-1)**(J+L+S+p)*(2*J+1)
        lam *= wigner_6j(J, J, p, L, L, S)/wigner_3j(p, L, L, 0, L, -L)
        return lam

    def _oef_k(p, k, n):
        K = 7. * wigner_3j(p, 3, 3, 0, 0, 0)
        if n <= 7:
            n_max = n
        else:
            n_max = n-7
            if k == 0:
                K -= np.sqrt(7)

        Kay = 0
        for j in range(1, n_max+1):
            Kay += (-1.)**j * wigner_3j(k, 3, 3, 0, 4-j, j-4)

        return K*Kay

    def _oef_RedJ(J, p):
        return 1./(2.**p) * (ssp.factorial(2*J+p+1)/ssp.factorial(2*J-p))**0.5

    # Calculate OEFs and store in array
    # Each parameter Bkq has its own parameter
    oef = np.zeros(27)
    k_max = np.min([6, int(2*J)])
    shift = 0
    for k in range(2, k_max+2, 2):
        oef[shift:shift + 2*k+1] = float(_oef_lambda(k, J, L, S))
        oef[shift:shift + 2*k+1] *= float(_oef_k(k, k, n) / _oef_RedJ(J, k))
        shift += 2*k + 1

    return oef


def calc_order_strength(params: list[float]) -> list[float]:
    """
    Calculates per-order strength parameter S_q for a set of Stevens parameters
    up to rank 6
    """

    max_rank = get_max_rank(params)

    # Convert Stevens parameters to Wybourne scheme
    wparams = abs(stevens_to_wybourne(params, max_rank))

    square_params = wparams ** 2

    # Calculate strength within order (S_q)

    sq = np.zeros(len(params))

    # Rank 2 contributions
    sq[0] = 1./5. * square_params[2]
    sq[1] = 1./5. * square_params[3]
    sq[2] = 1./5. * square_params[4]

    # Rank 4 contributions
    if max_rank > 2:
        sq[0] += 1./9. * square_params[9]
        sq[1] += 1./9. * square_params[10]
        sq[2] += 1./9. * square_params[11]
        sq[3] += 1./9. * square_params[12]
        sq[4] += 1./9. * square_params[13]

    # Rank 6 contributions
    if max_rank > 4:
        sq[6] += 1./13. * square_params[26]
        sq[5] += 1./13. * square_params[25]
        sq[4] += 1./13. * square_params[24]
        sq[3] += 1./13. * square_params[23]
        sq[2] += 1./13. * square_params[22]
        sq[1] += 1./13. * square_params[21]
        sq[0] += 1./13. * square_params[20]

    sq = np.sqrt(sq)

    return sq


def calc_rank_strength(params: list[float]) -> list[float]:
    """
    Calculates per-rank strength parameter S^k for a set of Stevens parameters
    up to rank 6
    """

    max_rank = get_max_rank(params)

    # Convert Stevens parameters to Wybourne scheme
    wparams = abs(stevens_to_wybourne(params, max_rank))

    # Calculate strength within rank (S^k)
    sk2 = np.sqrt(np.sum(wparams[:5]**2) / 5.)
    sk4 = np.sqrt(np.sum(wparams[5:14]**2) / 9.)
    sk6 = np.sqrt(np.sum(wparams[14:]**2) / 13.)

    sk = np.array([sk2, sk4, sk6])

    return sk


def calc_total_strength(params: list[float]) -> float:
    """
    Calculates strength parameter S for a set of Stevens parameters up to
    rank 6
    """

    sk = calc_rank_strength(params)

    # Calculate overall strength as weighted sum of S^k values
    S = np.array(np.sqrt(1./3.*(sk[0]**2 + sk[1]**2 + sk[2]**2)))

    return S


def get_max_rank(params):
    """
    Finds maximum rank in a set of parameters, assumes parameters are ordered
    k=2, q=-2...2, k=4, q=-4, ..., 4...
    """

    try:
        max_rank = RANK_BY_N_TOTAL_CFP[len(params)]
    except ValueError:
        raise ValueError("Incorrect number of CFPs")

    return max_rank


def stevens_to_wybourne(CFPs, k_max):
    """
    Transforms Crystal Field parameters from Wybourne notation to
    Stevens notation

    Assumes only even Ranks (k) are present

    Parameters
    ----------
        CFPs : np.ndarray
            CFPs in Stevens notation, shape = (n_k, n_q)
            ordered k=1 q=-k->k, k=2 q=-k->k ...
        k_max : int
            maximum value of k (rank)

    Returns
    -------
        np.ndarray, dtype=complex128
            CFPs in Wybourne notation, shape = (n_k, n_q)
    """

    if k_max > 6:
        raise ValueError("Cannot convert k>6 parameters to Wybourne")

    # Taken from Mulak and Gajek
    lmbda = [
        np.sqrt(6.)/3.,
        -np.sqrt(6.)/6.,
        2.,
        -np.sqrt(6.)/6.,
        np.sqrt(6.)/3.,
        4.*np.sqrt(70.)/35.,
        -2.*np.sqrt(35.)/35.,
        2.*np.sqrt(10.)/5.,
        -2*np.sqrt(5.)/5.,
        8.,
        -2.*np.sqrt(5.)/5.,
        2.*np.sqrt(10.)/5.,
        -2.*np.sqrt(35.)/35.,
        4.*np.sqrt(70.)/35.,
        16.*np.sqrt(231.)/231.,
        -8.*np.sqrt(77.)/231.,
        8.*np.sqrt(14.)/21.,
        -8.*np.sqrt(105.)/105.,
        16.*np.sqrt(105.)/105.,
        -4.*np.sqrt(42.)/21.,
        16.,
        -4.*np.sqrt(42.)/21.,
        16.*np.sqrt(105.)/105.,
        -8.*np.sqrt(105.)/105.,
        8.*np.sqrt(14.)/21.,
        -8.*np.sqrt(77.)/231.,
        16.*np.sqrt(231.)/231.
    ]

    w_CFPs = np.zeros(N_TOTAL_CFP_BY_RANK[k_max], dtype=np.complex128)

    for k in range(2, k_max + 2, 2):
        for q in range(-k, k + 1):
            ind = _even_kq_to_num(k, q)
            neg_ind = _even_kq_to_num(k, -q)
            if q == 0:
                w_CFPs[ind] = lmbda[ind] * CFPs[ind]
            elif q > 0:
                w_CFPs[ind] = lmbda[ind]*(CFPs[ind] + 1j*CFPs[neg_ind])
            elif q < 0:
                w_CFPs[ind] = lmbda[ind]*(-1)**q*(CFPs[neg_ind] - 1j*CFPs[ind])

    return w_CFPs


def _even_kq_to_num(k, q):
    """
    Converts Rank (k) and order (q) to array index
    Assuming that only even ranks are present

    Parameters
    ----------
        k : int
            Rank k
        q : int
            Order q

    Returns
    -------
        int
            Array index
    """

    index = k + q
    for kn in range(1, int(k/2)):
        index += 2*(k-2*kn) + 1

    return index


def _odd_kq_to_num(k, q):
    """
    Converts Rank (k) and order (q) to array index
    Assuming that only odd ranks are present

    Parameters
    ----------
        k : int
            Rank k
        q : int
            Order q

    Returns
    -------
        int
            Array index
    """

    index = 0
    for kn in range(1, k, 2):
        index += 2*kn + 1

    index += q + k + 1

    return index


def _kq_to_num(k, q):
    """
    Converts Rank (k) and order (q) to array index
    Assuming that all ranks are present

    Parameters
    ----------
        k : int
            Rank k
        q : int
            Order q

    Returns
    -------
        int
            Array index
    """

    index = -1
    for kn in range(1, k):
        index += 2*kn + 1
    index += q + k + 1

    return index


K_MAX = 15

stevens_kq_indices = tuple(
        (k, q)
        for k in range(2, K_MAX, 2)
        for q in range(-k, k+1)
)


def print_basis(hamiltonian, spin, angm, space, comp_thresh=0.05, field=None, plot=False, shift=True, **ops):
    """Print information of basis transformation and plot transformed angmom
    operators.

    Parameters
    ----------
    hamiltonian : np.array
        Array containing the total Hamiltonian in the angmom basis.
    spin : np.array
        Array containing the total spin operator in the angm basis.
    angm : np.array
        Array containing the total orbital angmom operator in the angmom basis.
    space : list of obj
        List of Symbol objects specifing the input space, e.g. terms/levels.
    comp_thresh : float
        Maximum amplitude of a given angular momentum state to be printed in
        the composition section.

    Returns
    -------
    None
    """

    if plot:
        titles = [comp + "-component" for comp in ["x", "y", "z"]]
        ut.plot_op([hamiltonian], 'hamiltonian' + ".png")
        for lab, op in ops.items():
            ut.plot_op(op, lab + ".png", sq=True, titles=titles)

    # print angmom basis and composition of the electronic states
    basis = space[0].basis

    qn_dict = {op + comp: np.sqrt(
        1/4 + np.diag(cartesian_op_squared(ops[op]).real)) - 1/2
        if comp == '2' else np.diag(ops[op][2]).real
        for op, comp in basis if op in ops and ops[op] is not None}

    def form_frac(rat, signed=True):
        return ('+' if rat > 0 and signed else '') + str(Fraction(rat))

    print("Angular momentum basis:")
    hline = 12 * "-" + "----".join([13 * "-"] * len(basis))

    print(hline)
    print(12 * " " + " || ".join(["{:^13}".format(op) for op in basis]))

    def states():
        for symbol in space:
            for state in symbol.states:
                yield state

    print(hline)
    for idx, state in enumerate(states()):
        print(f"state {idx + 1:4d}: " + " || ".join(
            ["{:>5} ({:5.2f})".format(
                form_frac(getattr(state, op + comp),
                          signed=False if comp == '2' else True),
                qn_dict[op + comp][idx] if op + comp in qn_dict else np.nan)
             for op, comp in basis]))

    print(hline)
    print("Basis labels - state N: [[<theo qn> (<approx qn>)] ...]")

    print()

    print("-----------------------------------------------------------")
    print("Diagonal basis energy, <S_z>, <L_z>, <J_z> and composition:")
    print("( angular momentum kets - " + "|" + ', '.join(basis) + "> )")
    print("-----------------------------------------------------------")

    if field:
        zeeman = zeeman_hamiltonian(spin, angm, [0, 0, field])
        eig, vec_total = np.linalg.eigh(hamiltonian + zeeman)

    else:
        eig, vec = np.linalg.eigh(hamiltonian)

        if field is None:
            vec_total = vec
        else:
            vec_total = vec @ perturb_doublets(
                eig, unitary_transform(spin + angm, vec))

    if shift:
        eners = (eig - eig[0]) * HARTREE2INVCM
    else:
        eners = eig * HARTREE2INVCM


    expectation = zip(*[np.diag(unitary_transform(op[2], vec_total).real)
                        for op in (spin, angm, spin + angm)])

    composition = np.real(vec_total * vec_total.conj())

    def format_state(state, op):
        return form_frac(getattr(state, op), signed=op[1] == 'z')

    for idx, (ener, exp, comp) in enumerate(
            zip(eners, expectation, composition.T), start=1):
        # generate states and sort by amplitude
        super_position = sorted(
            ((amp * 100, tuple(format_state(state, op) for op in basis))
             for state, amp in zip(states(), comp) if amp > comp_thresh),
            key=lambda item: item[0],
            reverse=True)

        print(f"State {idx:4d} {ener:8.4f}  " +
              " ".join([f"{val:+4.2f}" for val in exp]) + " : " +
              '  +  '.join("{:.2f}% |{}>".format(amp, ', '.join(state))
                           for amp, state in super_position))

    print("------------------------")
    print()


def make_operator_storage(op, **ops):

    description_dict = {
        "hamiltonian": "Hamiltonian matrix elements",
        "angm": "Orbital angular momentum matrix elements",
        "spin": "Spin angular momentum matrix elements"
    }

    return StoreOperator(ops[op], op, description_dict[op])


class StoreOperator(Store):

    def __init__(self, op, *args, units='au', fmt='% 20.13e'):

        self.op = op

        super().__init__(*args, label=(), units=units, fmt=fmt)

    def __iter__(self):
        yield (), self.op


class ProjectModelHamiltonian(Store):

    def __init__(self, ops, sf_mult, model_space=None, coupling=None,
                 basis='l', truncate=None, quax=None, terms=None, k_max=6,
                 theta=None, ion=None, iso_soc=True, zeeman=False,
                 verbose=False, units='cm^-1', fmt='% 20.13e'):

        self.ops = ops
        self.sf_mult = sf_mult
        self.spin_mults = np.repeat(*zip(*self.sf_mult.items()))

        # basis options
        self.model_space = model_space
        self.coupling = coupling
        self.quax = quax

        # model options
        self.terms = terms
        self.k_max = k_max
        self.theta = theta
        self.ion = ion
        self.iso_soc = iso_soc

        self.basis = basis
        self.truncate = truncate

        self.zeeman = zeeman

        if self.model_space is None:
            smult = np.repeat(list(self.sf_mult.keys()), list(self.sf_mult.values()))

            ws_angm = sf2ws(ops['sf_angm'], self.sf_mult)
            ws_spin = np.array(make_angmom_ops_from_mult(smult)[0:3])
            ws_hamiltonian = sf2ws(ops['sf_mch'], self.sf_mult) + \
                sf2ws_amfi(ops['sf_amfi'], self.sf_mult)

            eig, vec = np.linalg.eigh(ws_hamiltonian)
            so_eners = (eig - eig[0]) * HARTREE2INVCM

            sf_eners = [(np.diag(eners) - eners[0, 0]) * HARTREE2INVCM
                        for eners in ops['sf_mch']]

            print_sf_term_content(ops['sf_angm'], sf_eners, self.sf_mult)
            print_so_term_content(unitary_transform(ws_spin, vec),
                                  unitary_transform(ws_angm, vec),
                                  so_eners, self.sf_mult)
            exit()

        if self.basis == 'l':
            self.basis_space, self.cg_vecs = \
                evaluate_term_space(model_space, coupling=coupling)
        elif self.basis == 'j':
            self.basis_space, self.cg_vecs = \
                evaluate_level_space(model_space, coupling=coupling)

        # raise ValueError(f"Unknown intermediate basis: {self.basis}!")

        self.verbose = verbose

        description = \
            f"Spin Hamiltonian parameters of the {model_space} multiplet."

        super().__init__('parameters', description,
                         label=("term", "operators"), units=units, fmt=fmt)

    def evaluate(self, **ops):

        if self.verbose:
            print("Ab initio angular momentum basis space:")
            print(self.basis_space)

        # rotation of quantisation axis
        def rot_cart(ops):
            return rotate_cart(ops, self.quax)

        if self.quax is not None:
            ops['sf_amfi'] = sfy(rot_cart, sf=2)(ops['sf_amfi'])
            ops['sf_angm'] = sfy(rot_cart, sf=1)(ops['sf_angm'])

        if self.basis == 'l':
            ws_basis_vecs = self.evaluate_sf_term_trafo(ops)

        elif self.basis == 'j':
            ws_basis_vecs = self.evaluate_level_trafo(ops)

        ws_vecs = ws_basis_vecs @ self.cg_vecs

        # ut.plot_op(np.abs(from_blocks(*unitary_transform(ops['sf_angm'], sf_term_vecs, sf=1))), "sf_angm_abs.png", sq=True)
        # ut.plot_op([sf2ws(sf_term_vecs, self.sf_mult)], "sf_vecs.png")

        ws_spin = np.array(make_angmom_ops_from_mult(self.spin_mults)[0:3])
        ws_angm = sf2ws(ops['sf_angm'], self.sf_mult)

        if self.verbose:

            ws_compl_vecs, rmat = jnp.linalg.qr(ws_vecs, mode='complete')
            ws_compl_vecs = ws_compl_vecs.at[:, :rmat.shape[1]].multiply(jnp.diag(rmat))

            hamiltonian = unitary_transform(sf2ws_amfi(ops['sf_amfi'], self.sf_mult) +
                                            sf2ws(ops['sf_mch'], self.sf_mult), ws_compl_vecs)

            spin = unitary_transform(ws_spin, ws_compl_vecs)
            angm = unitary_transform(ws_angm, ws_compl_vecs)

            print_basis(hamiltonian, spin, angm,
                        [self.model_space], comp_thresh=self.comp_thresh,
                        field=self.field, plot=self.verbose,
                        S=spin, L=angm, J=spin + angm)

        model = SpinHamiltonian(self.model_space, k_max=self.k_max, theta=self.theta,
                                ion=self.ion, time_reversal_symm="even",
                                iso_soc=self.iso_soc, **self.terms)

        hamiltonian = unitary_transform(sf2ws_amfi(ops['sf_amfi'], self.sf_mult) +
                                        sf2ws(ops['sf_mch'], self.sf_mult), ws_vecs)

        spin = unitary_transform(ws_spin, ws_vecs)
        angm = unitary_transform(ws_angm, ws_vecs)

        param_dict = model.project(hamiltonian, verbose=self.verbose)

        if self.zeeman:
            zeeman_dict = ZeemanHamiltonian(self.model_space).project(spin, angm, verbose=self.verbose)
            param_dict |= zeeman_dict

        return list(param_dict.values()), list(param_dict.keys())

    def evaluate_sf_term_trafo(self, ops):

        labs = ["L"]

        def term_trafo(terms, *ops):
            return project_irrep_basis(terms, **dict(zip(labs, ops)))

        sf_terms = [[Symbol(L=term.qn['L']) for term in self.basis_space if term.mult['S'] == mult]
                    for mult in self.sf_mult]

        sf_term_vecs = list(map(term_trafo, sf_terms, ops['sf_angm']))

        if 'soc' in self.terms and (len(sf_terms) > 1 or any(len(terms) > 1 for terms in sf_terms)):

            sf_term_phases = self.relative_sf_term_phase(unitary_transform(ops['sf_amfi'], sf_term_vecs, sf=2))

            sf_term_vecs = [np.repeat(ph, [term.mult['L'] for term in terms]) * vecs
                            for terms, ph, vecs in zip(sf_terms, sf_term_phases, sf_term_vecs)]

        ws_term_vecs = sf2ws(sf_term_vecs, self.sf_mult)

        if self.verbose:
            ut.plot_op(np.block(unitary_transform(ops['sf_amfi'], sf_term_vecs, sf=2)), "sf_amfi_phased.png")
            ut.plot_op(from_blocks(*unitary_transform(ops['sf_angm'], sf_term_vecs, sf=1)), "sf_angm.png", sq=True)

        return ws_term_vecs

    def evaluate_level_trafo(self, ops):

        ws_spin = np.array(make_angmom_ops_from_mult(self.spin_mults)[0:3])
        ws_angm = sf2ws(ops['sf_angm'], self.sf_mult)

        if self.truncate is None:
            level_vecs = project_irrep_basis(self.basis_space, J=ws_spin + ws_angm)
        else:
            hamiltonian = sf2ws_amfi(ops['sf_amfi'], self.sf_mult) + sf2ws(ops['sf_mch'], self.sf_mult)
            _, so_vecs = np.linalg.eigh(hamiltonian)
            so_spin = unitary_transform(ws_spin, so_vecs[:, :self.truncate])
            so_angm = unitary_transform(ws_angm, so_vecs[:, :self.truncate])
            so_level_vecs = project_irrep_basis(self.basis_space, J=so_spin + so_angm)

            level_vecs = so_vecs[:, :self.truncate] @ so_level_vecs

        # if self.verbose:
        #     ut.plot_op([unitary_transform(sf2ws_amfi(ops['sf_amfi'], self.sf_mult), level_vecs)], "h_amfi_unphased.png")
        #     ut.plot_op(unitary_transform(ws_spin, level_vecs), "spin_unphased.png")
        #     ut.plot_op(unitary_transform(ws_angm, level_vecs), "angm_unphased.png")

        if len(self.basis_space) > 1:

            level_phases = self.relative_level_phase(
                unitary_transform(sf2ws_amfi(ops['sf_amfi'], self.sf_mult), level_vecs),
                unitary_transform(ws_spin, level_vecs), unitary_transform(ws_angm, level_vecs))

            level_vecs = np.repeat(level_phases, [lvl.multiplicity for lvl in self.basis_space]) * level_vecs

        # if self.verbose:
        #     ut.plot_op([unitary_transform(sf2ws_amfi(ops['sf_amfi'], self.sf_mult), level_vecs)], "h_amfi_phased.png")
        #     ut.plot_op(unitary_transform(ws_spin, level_vecs), "spin_phased.png")
        #     ut.plot_op(unitary_transform(ws_angm, level_vecs), "angm_phased.png")

        return level_vecs

    def make_hso_ops(self, hso_ops, tensor=True):

        if hso_ops[0].upper() in ANGM_SYMBOLS and hso_ops[1].upper() in SPIN_SYMBOLS:
            angm, spin = hso_ops
        elif hso_ops[0].upper() in SPIN_SYMBOLS and hso_ops[1].upper() in ANGM_SYMBOLS:
            spin, angm = hso_ops
        else:
            raise ValueError(("Spin-orbit coupling operator needs to be "
                              "composed of one spin and one orbital "
                              f"angular momentum symbol! Got {hso_ops}"))

        hso_tensor = (sph_comps(self.model_space.get_op(angm)) @
                      sph_comps(self.model_space.get_op(spin))[::-1])

        if tensor:
            return unitary_transform(hso_tensor, self.cg_vecs.T)

        hso = np.sum([(-1)**q * comp for q, comp in zip((-1, 0, 1), hso_tensor)], axis=0)
        return unitary_transform(hso, self.cg_vecs.T)


    def relative_sf_term_phase(self, sf_amfi):
        """evaluate relative term phase

        """

        # Account for (mysterious) extra minus sign for s2 > s1 amfi blocks
        amfi = 1.j * np.block([[-a if s > s_row else a for s, a in zip(self.sf_mult, row)]
                               for s_row, row in zip(self.sf_mult, sf_amfi)])
        # ut.plot_op(amfi, "amfi.png")

        states = [state for term in self.basis_space for state in term.states]

        amfi_red = \
            np.mean(we_reduce_term_blocks(sph_comps(amfi), states, ['S', 'L'], [None, (-1, 0, 1)]), axis=0)

        hso_red = \
            [np.mean(we_reduce_term_blocks(self.make_hso_ops(hso_ops), states, ['S', 'L'], [(1, 0, -1), (-1, 0, 1)]), axis=0)
             for hso_ops in self.terms['soc']]

        sf_term_phases = list(dissect_array(find_relative_block_phases((amfi_red, hso_red)),
                                            [term.qn['S'] for term in self.basis_space]))

        # Hamfi = sf2ws_amfi(sf_amfi, self.sf_mult)
        # print([np.trace(np.sum([(-1)**q * comp for q, comp in zip((-1, 0, 1), self.make_hso_tensor(hso_ops))], axis=0).conj().T
        #                 @ Hamfi) for hso_ops in self.terms['soc']])
        # print([np.sum(amfi_red * red) / 3 for red in hso_angm_red])

        return sf_term_phases

    def relative_level_phase(self, hso_amfi, spin, angm):

        if 'soc' in self.terms:

            amfi_red = we_reduce_blocks([hso_amfi], self.basis_space)[0]

            hso_red = \
                [we_reduce_blocks([self.make_hso_ops(hso_ops)], self.basis_space)[0]
                 for hso_ops in self.terms['soc']]

        ai_spin_red = np.mean(we_reduce_blocks(sph_comps(spin), self.basis_space), axis=0)
        ai_angm_red = np.mean(we_reduce_blocks(sph_comps(angm), self.basis_space), axis=0)

        spin_red = np.mean(we_reduce_blocks(unitary_transform(sph_comps(self.model_space.get_op("spin")), self.cg_vecs.T), self.basis_space), axis=0)
        angm_red = np.mean(we_reduce_blocks(unitary_transform(sph_comps(self.model_space.get_op("angm")), self.cg_vecs.T), self.basis_space), axis=0)

        level_phases = find_relative_block_phases((ai_spin_red, (spin_red,)), (ai_angm_red, (angm_red,)))

        return level_phases

    def __iter__(self):
        yield from map(lambda val, lab: (self.format_label(lab), val),
                       *self.evaluate(**self.ops))

    def format_label(self, label):
        return (label[0], '_'.join(label[1]))


def evaluate_term_space(model_space, coupling=None):
    """Connects model space with space of L,S terms"""

    def reorder(terms):
        """Reorder term basis of model-term transformation to match S, L, M_L, M_S ordering"""
        terms, perms = zip(*map(lambda term: term.reduce(ops=('L', 'S'), cls=Term, return_perm=True), terms))
        start_idc = accumulate([term.multiplicity for term in terms], initial=0)
        _terms, _start_idc, _perms = \
            zip(*sorted(zip(terms, start_idc, perms), key=lambda x: (x[0].qn['S'], x[0].qn['L'])))
        return _terms, [start + idx for start, perm in zip(_start_idc, _perms) for idx in perm]

    if coupling:
        cpld_space, cg_vec = couple(model_space, **coupling)
        term_space, order = reorder(cpld_space)
        trafo = cg_vec[:, order].T

    elif isinstance(model_space, Level):
        term_space = [Term(L=model_space.qn['L'], S=model_space.qn['S'])]
        _, trafo = term_space[0].couple('J', 'L', 'S', levels=[model_space])

    elif isinstance(model_space, Term):
        term_space = [model_space]
        trafo = np.identity(model_space.multiplicity)

    else:
        raise ValueError(f"Invalid model_space {model_space}!")

    return term_space, trafo


def evaluate_level_space(model_space, coupling=None):
    """Connects model space with space of J levels"""

    def reorder(levels):
        """Reorder level basis of model-level transformation to match J, M_J ordering"""
        levels, perms = zip(*map(lambda term: term.reduce(ops=('J',), return_perm=True), levels))
        start_idc = accumulate([level.multiplicity for level in levels], initial=0)
        _levels, _start_idc, _perms = \
            zip(*sorted(zip(levels, start_idc, perms), key=lambda x: x[0].qn['J']))
        return _levels, [start + idx for start, perm in zip(_start_idc, _perms) for idx in perm]

    if coupling:
        cpld_space, cg_vec = couple(model_space, **coupling)
        level_space, order = reorder(cpld_space)
        trafo = cg_vec[:, order].T

    elif isinstance(model_space, Level):
        level_space = [model_space]
        trafo = np.identity(model_space.multiplicity)

    else:
        raise ValueError(f"Invalid model_space {model_space}!")

    return level_space, trafo


def find_relative_block_phases(*ops):
    """Compute term phase correction from WE-reduced amfi and model ops"""

    def cost(phase_angles):
        phases = np.exp(1.j * phase_angles)
        return -np.sum([np.abs(np.trace(phases.conj()[:, np.newaxis] * ref * phases[np.newaxis, :] @ op.T.conj()) /
                               np.trace(op @ op.T.conj()))**2 for ref, op_list in ops for op in op_list])

    res = minimize(cost, np.zeros(ops[0][0].shape[0]), tol=1e-9)
    phase_angles = res.x

    return np.exp(1.j * phase_angles)


def read_params(file, group='/', **mapping):
    with h5py.File(file, 'r') as h:
        for term in iter(grp := h[group]):
            if term == 'diag':
                pass
            else:
                for ops in iter(grp[term]):
                    path = grp['/'.join([term, ops, 'parameters'])]
                    op_labs = tuple(mapping.get(o, o) for o in ops.split('_'))
                    key = path.attrs['typename']
                    env = {key: namedtuple(key, path.attrs['field_names'])}
                    names = [eval(row, env) for row in path.attrs['row_names']]
                    data = path[...]
                    yield (term, op_labs), {k: v for k, v in zip(names, data)}


class Model:

    def __init__(self, symbol, angm_ops=None):

        self.symbol = symbol

        self.angm = \
            {o: tuple(angm_ops[o]) + (angm_ops[o][0] + 1.j * angm_ops[o][1],
                                      angm_ops[o][0] - 1.j * angm_ops[o][1],
                                      cartesian_op_squared(angm_ops[o])[0])
             if angm_ops is not None and o in angm_ops else
             calc_ang_mom_ops(self.symbol.qn[o]) for o in self.symbol.coupling.keys()}

    def __iter__(self):
        # todo: yield from?
        yield from (((term, labs), self.resolve_model_ops[term](labs))
                    for term, sub in self.terms.items() for labs in sub)

    def print_basis(self):
        print(self.symbol.states)

    def check_orthogonality(self):

        def proj(op1, op2):
            return np.sum(op1 * op2.conj()).real / \
                (np.linalg.norm(op1) * np.linalg.norm(op1))

        def generate_ops():
            for (term, labs), ops in iter(self):
                for key, op in ops:
                    yield op

        ortho_matrix = np.array([[proj(op1, op2) for op2 in generate_ops()]
                                 for op1 in generate_ops()])

        if not np.allclose(ortho_matrix, np.identity(len(list(generate_ops())))):
            warnings.warn("Non-orthogonality detected in model operators!")

        return


class ZeemanHamiltonian(Model):

    def __init__(self, symbol, angm_ops=None):

        self.terms = {"zee": list(map(lambda lab: (lab,), symbol.mult.keys()))}

        self.resolve_model_ops = {
            "zee": self._build_zee
        }

        super().__init__(symbol, angm_ops=angm_ops)

    def _build_zee(self, ops):

        Key = namedtuple('g', 'comp')

        return ((Key(["x", "y", "z"][comp]),
                     reduce(np.kron,
                             [self.angm[o][comp] if o == ops[0] else np.identity(m)
                              for o, m in self.symbol.mult.items()]))
                for comp in range(3))

    def resolve_zeeman_ops(self, params, verbose=False):

        g_e = 2.002319

        zee = np.zeros((3, self.symbol.multiplicity, self.symbol.multiplicity),
                        dtype='complex128')

        for (term, labs), ops in iter(self):
            if term == "zee":
                for key, op in ops:

                    if verbose:
                        print(f"Parametrising {key} of {term}{labs}")

                    zee[{'x': 0, 'y': 1, 'z': 2}[getattr(key, 'comp')]] += \
                        params[(term, labs)][key] * op

        jtot = reduce(add,
                      [reduce(np.kron,
                              [self.angm[o][:3] if o == p else np.identity(m)
                               for o, m in self.symbol.mult.items()])
                       for p in self.symbol.mult.keys()])

        spin = (zee - jtot) / (g_e - 1)
        angm = jtot - spin

        return spin, angm

    def project(self, spin, angm, verbose=False):

        g_e = 2.002319

        zee = g_e * spin + angm

        def proj(op):
            return jnp.sum(zee * op.conj()).real / jnp.linalg.norm(op)**2

        params = {(term, labs): {key: proj(op) for key, op in ops}
                  for (term, labs), ops in iter(self)}

        self.check_orthogonality()

        return params


class SpinHamiltonian(Model):
    """Set up model spin Hamiltonian to be fitted to ab initio Hamiltonian in
    angular momentum basis.
    The model might be composed of: H = V_0 + H_so + H_ex + H_cf
    (V_0: diagonal shift, H_so: spin-orbit coupling, H_ex: exchange coupling,
    H_cf: CF interaction).

    Parameters
    ----------
    symbol : obj
        Symbol object specifying the angular momentum space.
    angm_ops : dict, default = None
        Dictionary of angm operators. Keys are the angm operator labels. If
        omitted, exact operators are used.
    k_max : int, default = 6
        Maximum Stevens operator rank used in crystal field Hamiltonian.
    theta : bool, default = False
        If True, factor out operator equivalent factors theta.
    diag : bool
        If True, include constant diagonal shift term.
    iso_soc : bool
        If True, SOC interaction is described by isotropic operator.
    time_reversal_symm : ["even", "odd"], default "even"
        If "even" ("odd"), only include exchange terms which are "even" ("odd")
        under time reversal.
    ion : object, default = None
        Ion object for operator equivalent factor lookup.
    **terms: keyword arguments
        Terms to include in the model Hamiltonian specified as:
            spin-orbit coupling: soc=[("L", "S")]
            crystal field: cf=[("L",)]
            exchange: ex=[("R", "S"), ("R", "L"), ("R", "S", "L")]

    Attributes
    ----------
    symbol : obj
        Symbol object specifying the angular momentum space.
    angm : dict
        Dictionary of angm operators. Keys are the angm operator labels.
    k_max : int
        Maximum Stevens operator rank used in crystal field Hamiltonian.
    theta : bool, default = False
        If true, factor out operator equivalent factors theta.
    ion : object, default = None
        Ion object for operator equivalent factor lookup.
    term_dict : dict of dicts
        Dictionary of terms. Each entry of sub-dict is a contribution to the
        model Hamiltonian associated with a parameter.
    term_len : dict
        Dictionary of number of parameter of each term in model Hamiltonian.
    """

    def __init__(self, symbol, angm_ops=None, ion=None, k_max=6, theta=False,
                 diag=True, iso_soc=True, time_reversal_symm="even", **terms):

        self.ion = ion
        self.k_max = k_max
        self.theta = theta
        self.iso_soc = iso_soc
        self.time_reversal_symm = time_reversal_symm
        self.diag = diag

        self.terms = ({"diag": [()]} if diag else {}) | terms

        self.resolve_model_ops = {
            "diag": self._build_diag,
            "soc": self._build_soc,
            "cf": self._build_cf,
            "ex": self._build_ex,
        }

        super().__init__(symbol, angm_ops=angm_ops)

    def _build_diag(self, ops):
        if ops:
            raise ValueError("Inconsistency in building diagonal shift op.")

        Key = namedtuple('shift', '')
        return ((Key(), jnp.identity(self.symbol.multiplicity)),)

    def _build_soc(self, ops):

        if self.iso_soc:
            Key = namedtuple('lamb', '')
            return ((Key(), jnp.sum(jnp.array([
                reduce(jnp.kron,
                       [self.angm[o][c] if o in ops else jnp.identity(m)
                        for o, m in self.symbol.mult.items()])
                for c in range(3)]), axis=0)),)
        else:
            Key = namedtuple('lamb', 'component')
            return ((Key(("x", "y", "z")[c - 1]),
                    reduce(jnp.kron,
                           [self.angm[o][c] if o in ops else jnp.identity(m)
                            for o, m in self.symbol.mult.items()]))
                    for c in range(3))

    def _build_cf(self, ops):

        op = ops[0]

        if self.k_max > 12:
            warnings.warn("Exclude k > 12 terms from exchange Hamiltonian "
                          "due to numerical instability at double prec!")

        Okq = \
            calc_stev_ops(min(self.k_max, 12), (self.symbol.mult[op] - 1) / 2,
                          self.angm[op][3], self.angm[op][4], self.angm[op][2])

        if not self.theta:
            pass
        elif self.theta and op.upper() in ANGM_SYMBOLS:
            theta = self.ion.theta('l')
        elif self.theta and op.upper() in TOTJ_SYMBOLS:
            theta = self.ion.theta('j')
        else:
            raise ValueError(f"Unknown angular momentum identifier: {op}")

        Key = namedtuple('B', 'k q')
        return ((Key(k, q),
                reduce(jnp.kron,
                       [Okq[k - 1, k + q, ...] *
                        (theta[k] if self.theta else 1.0)
                        if o == op else jnp.identity(m)
                        for o, m in self.symbol.mult.items()]))
                for k in range(2, self.k_max + 1, 2) for q in range(-k, k + 1))

    def _build_ex(self, ops):

        def time_rev_symm(ranks):
            if self.time_reversal_symm == "even":
                return not sum(ranks) % 2
            elif self.time_reversal_symm == "odd":
                return sum(ranks) % 2
            else:
                return True

        Okqs = {o: calc_stev_ops(
            min(self.symbol.mult[o] - 1, 12), self.symbol.qn[o],
            self.angm[o][3], self.angm[o][4], self.angm[o][2]) for o in ops}

        kdc = (dict(zip(ops, idc))
               for idc in product(*(range(1, min(self.symbol.mult[o], 12 + 1))
                                    for o in ops)))
        for o in ops:
            if self.symbol.mult[o] - 1 > 12:
                warnings.warn("Exclude k > 12 terms from exchange Hamiltonian "
                              "due to numerical instability at double prec!")

        # generator of orders
        def qdc(kdx):
            return (dict(zip(ops, idc))
                    for idc in product(
                        *(range(-k, k + 1) for k in kdx.values())))

        idc = iter([('k', 'q'), ('n', 'm')])
        Key = namedtuple('J', (i for o in ops for i in (("alpha",) if o == 'R'
                                                        else next(idc))))

        return ((Key(*(i for o, kx, qx in zip(ops, k.values(), q.values())
                for i in ((('z', 'x', 'y')[qx],) if o == 'R' else (kx, qx)))),
                (-1) * reduce(jnp.kron,
                              [Okqs[o][k[o] - 1, k[o] + q[o], ...] /
                               (1.0 if o.upper() == 'R' else
                                Okqs[o][k[o] - 1, k[o], -1, -1])  # IC scalar
                               if o in ops else jnp.identity(m)
                               for o, m in self.symbol.mult.items()]))
                for k in kdc for q in qdc(k) if time_rev_symm(k.values()))

    def project(self, ham, verbose=False):
        """Project ab initio Hamiltonian onto model.

        Parameters
        ----------
        ham : np.array
            Ab initio Hamiltonian in the appropiate basis. (Ordering according
            to basis_mult argument of constructor.)
        verbose : bool
            Flag for printing information from least squares fit and plot
            original and fitted Hamiltonian matrices.

        Returns
        -------
        dict of dicts
            Dictionary of terms. Each term is a dictionary itself listing all
            projected model parameters. Sub-keys are Stevens operator rank
            order pairs in the same order as defined in the **terms parameters.
        """

        ham = ham * HARTREE2INVCM

        def proj(op):
            return jnp.sum(ham * op.conj()).real / jnp.linalg.norm(op)**2

        # def orthonorm(op1, op2):
        #     return (np.sum(op1 * op2.conj()) / (np.linalg.norm(op1) * np.linalg.norm(op2))).real

        params = {(term, labs): {key: proj(op) for key, op in ops}
                  for (term, labs), ops in iter(self)}

        # print(np.array([[orthonorm(op1, op2) for _, ops1 in iter(self) for _, op1 in ops1] for _, ops2 in iter(self) for _, op2 in ops2]))

        ham_fit = self.parametrise(params, verbose=False)
        err = jnp.linalg.norm(ham_fit - ham)**2

        if verbose:
            print("Absolute err (RMSD, i.e. sqrt[1/N^2 * sum of squared "
                  "residuals])\n{:10.4f}".format(
                      jnp.sqrt(err / ham.size)))
            print("Relative err (sqrt[sum of squared residuals] / "
                  "norm of ab initio Hamiltonian)\n{:10.4%}".format(
                      jnp.sqrt(err) / jnp.linalg.norm(ham)))

            print("Eigenvalues of the ab initio and model Hamiltonian "
                  "(diagonal shift substracted):")

            shift = list(params[("diag", ())].values())[0] if self.diag else 0.
            diag_shift = shift * jnp.identity(self.symbol.multiplicity)
            eig_a, _ = jnp.linalg.eigh(ham - diag_shift)
            eig_m, _ = jnp.linalg.eigh(ham_fit - diag_shift)

            for i, (a, m) in enumerate(zip(eig_a, eig_m), start=1):
                print(f"{i} {a} {m}")

            ut.plot_op([ham, ham_fit], "h_ai.png",
                       titles=["Ab initio Hamiltonian", "Model fit"])

        return params

    def parametrise(self, params, scale=None, verbose=False):

        ham = jnp.zeros((self.symbol.multiplicity, self.symbol.multiplicity),
                        dtype='complex128')

        for lab, ops in iter(self):
            for key, op in ops:
                if verbose:
                    print(f"Parametrising {key} of {lab[0]}{lab[1]}")
                if scale is None:
                    ham += params[lab][key] * op
                else:
                    ham += params[lab][key] * op * scale.get(lab[0], 1.0)

        return ham
        # return reduce(lambda x, y: x + y,
        #               (params[lab][key] * op
        #                for lab, ops in iter(self) for key, op in ops))


class FromFile:

    def __init__(self, h_file, **kwargs):

        self.h_file = h_file

        with h5py.File(self.h_file, 'r') as h:
            ops = {op: h[op][...] for op in ['hamiltonian', 'spin', 'angm']}

        super().__init__(ops, **kwargs)


class MagneticSusceptibility(Store):

    def __init__(self, ops, temperatures=None, field=None, differential=False,
                 iso=True, powder=False, chi_T=False, units='cm^3 / mol',
                 fmt='% 20.13e'):

        self.ops = ops
        self.temperatures = temperatures

        # basis options
        self.field = field
        self.differential = differential
        self.iso = iso
        self.powder = powder
        self.chi_T = chi_T

        title = "chi_T" if self.chi_T else "chi"
        description = " ".join(["Temperature-dependent"] +
                               (["differential"] if self.differential else []) +
                               (["isotropic"] if self.iso else []) +
                               ["molecular susceptibility"] +
                               (["tensor"] if not self.iso else []) +
                               (["times temperature"] if self.chi_T else []) +
                               [f"at {field} mT"])

        super().__init__(title, description, label=(), units=units, fmt=fmt)

    def evaluate(self, **ops):

        if self.differential:
            tensor_func = partial(susceptibility_tensor,
                                  hamiltonian=ops['hamiltonian'],
                                  spin=ops['spin'], angm=ops['angm'],
                                  field=self.field,
                                  differential=self.differential)
        else:
            tensor_func = make_susceptibility_tensor(
                hamiltonian=ops['hamiltonian'],
                spin=ops['spin'], angm=ops['angm'],
                field=self.field)

        if self.iso:
            def func(temp):
                return jnp.trace(tensor_func(temp)) / 3
        else:
            func = tensor_func

        # vmap does not repeat the eigen decomp
        if self.differential:
            chi_list = [func(temp) for temp in self.temperatures]
        else:  # non-bached more efficient when using the expm backend
            chi_list = [func(temp) for temp in self.temperatures]
            # chi_list = vmap(func)(jnp.array(self.temperatures))

        Key = namedtuple('chi', 'temp')
        data = {Key(temp): (temp * chi) if self.chi_T else chi
                for temp, chi in zip(self.temperatures, chi_list)}
        return [data], [()]

    def __iter__(self):
        yield from ((lab, dat) for dat, lab in zip(*self.evaluate(**self.ops)))


class MagneticSusceptibilityFromFile(FromFile, MagneticSusceptibility):
    pass


class EPRGtensor(Store):

    def __init__(self, ops, multiplets=None, eprg_values=False,
                 eprg_vectors=False, eprg_tensors=False,
                 units='au', fmt='% 20.13e'):

        self.ops = ops

        self.multiplets = multiplets

        self.eprg_values = eprg_values
        self.eprg_vectors = eprg_vectors
        self.eprg_tensors = eprg_tensors

        if self.eprg_values:
            args = ("eprg_values", "Principal values of the EPR G-tensor")
        elif self.eprg_vectors:
            args = ("eprg_vectors", "Principal axes of the EPR G-tensor")
        elif self.eprg_tensors:
            args = ("eprg_tensors", "EPR G-tensor")
        else:
            raise ValueError("Supply one of eprg_values/_vectors/_tensors!")

        super().__init__(*args, label=("doublet",), units=units, fmt=fmt)

    def evaluate(self, **ops):

        eig, vec = jnp.linalg.eigh(ops['hamiltonian'])

        if self.multiplets is None:
            labs = np.unique(np.around(eig, 8), return_inverse=True)[1]
        else:
            labs = [lab for lab, mult in enumerate(self.multiplets) for _ in range(mult)]

        spin_blks = extract_blocks(unitary_transform(ops['spin'], vec), labs, labs)
        angm_blks = extract_blocks(unitary_transform(ops['angm'], vec), labs, labs)
        eprg_list = map(eprg_tensor, spin_blks, angm_blks)

        if self.eprg_tensors:
            data = list(eprg_list)

        else:
            eprg_vals, eprg_vecs = zip(*map(jnp.linalg.eigh, eprg_list))

            if self.eprg_values:
                data = eprg_vals
            elif self.eprg_vectors:
                data = eprg_vecs

        return list(data), [(idx,) for idx, _ in enumerate(data, start=1)]

    def __iter__(self):
        yield from ((lab, dat) for dat, lab in zip(*self.evaluate(**self.ops)))


class EPRGtensorFromFile(FromFile, EPRGtensor):
    pass


class Tint(Store):

    def __init__(self, ops, field=0., states=None, units='au', fmt='% 20.13e'):

        self.ops = ops
        self.field = field
        self.states = states

        super().__init__(
            "tint",
            "Matrix elements of the magnetic dipole transition intensity",
            label=("istate",), units=units, fmt=fmt)

    def evaluate(self, **ops):

        zee = zeeman_hamiltonian(
                ops['spin'], ops['angm'], np.array([0., 0., self.field]))
        _, vec = jnp.linalg.eigh(ops['hamiltonian'] + zee)

        vec_out = vec if self.states is None else vec[:, list(self.states)]

        magm = vec_out.conj().T @ magmom(ops['spin'], ops['angm']) @ vec
        tint = np.sum(np.real(magm * magm.conj()), axis=0) / 3

        Key = namedtuple('jstate', 'index')
        data = [{Key(idx): val for idx, val in enumerate(row, start=1)} for row in tint]
        return data, [(idx,) for idx, _ in enumerate(data, start=1)]

    def __iter__(self):
        yield from ((lab, dat) for dat, lab in zip(*self.evaluate(**self.ops)))

    def __iter__(self):
        yield from ((lab, dat) for dat, lab in zip(*self.evaluate(**self.ops)))


class TintFromFile(FromFile, Tint):
    pass


def magmom(spin, angm):
    """(negative) Magnetic moment
    """
    muB = 0.5  # atomic units
    g_e = 2.002319
    return muB * (angm + g_e * spin)


def eprg_tensor(spin, angm):
    muB = 0.5  # atomic units
    magm = magmom(spin, angm) / muB
    return 2 * jnp.einsum('kij,lji->kl', magm, magm).real


def zeeman_hamiltonian(spin, angm, field):
    """Compute Zeeman Hamiltonian in atomic units.

    Parameters
    ----------
    spin : np.array
        Spin operator in the SO basis.
    angm : np.array
        Orbital angular momentum operator in the SO basis.
    field : np.array
        Magnetic field in mT.

    Returns
    -------
    np.array
        Zeeman Hamiltonian matrix.
    """

    au2mT = 2.35051756758e5 * 1e3  # mTesla / au

    # calculate zeeman operator and convert field in mT to T
    return jnp.einsum('i,imn->mn', jnp.array(field) / au2mT, magmom(spin, angm))


def Gtensor(spin, angm):
    muB = 0.5  # atomic units
    magn = magmom(spin, angm)
    return 2 / muB * jnp.einsum('kuv,lvu', magn, magn)


# @partial(jit, static_argnames=['differential', 'algorithm'])
def susceptibility_tensor(temp, hamiltonian, spin, angm, field=0.,
                          differential=True, algorithm=None):
    """Differential molar magnetic susceptipility tensor under applied magnetic
    field along z, or conventional susceptibility tensor where each column
    represents the magnetic response under applied magnetic field along x, y or
    z.

    Parameters
    ----------
    temp : float
        Temperature in Kelvin.
    hamiltonian : np.array
        Electronic Hamiltonian in atomic units.
    spin : np.array
        Spin operator in the SO basis.
    angm : np.array
        Orbital angular momentum operator in the SO basis.
    field : float
        Magnetic field in mT at which susceptibility is measured.
    differential : bool
        If True, calculate differential susceptibility.
    algorithm : {'eigh', 'expm'}
        Algorithm for the computation of the partition function.

    Returns
    -------
    3x3 np.array

    """
    a0 = 5.29177210903e-11  # Bohr radius in m
    c0 = 137.036  # a.u.
    mu0 = 4 * np.pi / c0**2  # vacuum permeability in a.u.
    au2mT = 2.35051756758e5 * 1e3  # mTesla / au

    # [hartree] / [mT mol] * [a.u.(velocity)^2] / [mT]
    algorithm = algorithm or ('expm' if differential else 'eigh')
    mol_mag = partial(molecular_magnetisation, temp, hamiltonian, spin, angm,
                      algorithm=algorithm)

    if differential:
        chi = mu0 * jacfwd(mol_mag)(jnp.array([0., 0., field]))
    else:
        # conventional susceptibility at finite field
        chi = mu0 * jnp.column_stack([mol_mag(fld) / field
                                      for fld in field * jnp.identity(3)])

    # [cm^3] / [mol] + 4*pi for conversion from SI cm3
    return (a0 * 100)**3 * au2mT**2 * chi / (4 * np.pi)


def make_susceptibility_tensor(hamiltonian, spin, angm, field=0.):
    """Differential molar magnetic susceptipility tensor under applied magnetic
    field along z, or conventional susceptibility tensor where each column
    represents the magnetic response under applied magnetic field along x, y or
    z. Maker function for partial evaluation of matrix eigen decomposition.


    Parameters
    ----------
    hamiltonian : np.array
        Electronic Hamiltonian in atomic units.
    spin : np.array
        Spin operator in the SO basis.
    angm : np.array
        Orbital angular momentum operator in the SO basis.
    field : float
        Magnetic field in mT at which susceptibility is measured.

    Returns
    -------
    3x3 np.array

    """
    a0 = 5.29177210903e-11  # Bohr radius in m
    c0 = 137.036  # a.u.
    mu0 = 4 * np.pi / c0**2  # vacuum permeability in a.u.
    au2mT = 2.35051756758e5 * 1e3  # mTesla / au

    # [hartree] / [mT mol] * [a.u.(velocity)^2] / [mT]

    mol_mag = [make_molecular_magnetisation(hamiltonian, spin, angm, fld)
               for fld in field * jnp.identity(3)]

    # conventional susceptibility at finite field
    def susceptibility_tensor(temp):
        chi = mu0 * jnp.column_stack([mol_mag[comp](temp) / field for comp in range(3)])
        # [cm^3] / [mol] + 4*pi for conversion from SI cm3
        return (a0 * 100)**3 * au2mT**2 * chi / (4 * np.pi)

    return susceptibility_tensor


def molecular_magnetisation(temp, hamiltonian, spin, angm, field, algorithm='eigh'):
    """ Molar molecular magnetisation in [hartree] / [mT mol]

    Parameters
    ----------
    temp : float
        Temperature in Kelvin.
    hamiltonian : np.array
        Electronic Hamiltonian in atomic units.
    spin : np.array
        Spin operator in the SO basis.
    angm : np.array
        Orbital angular momentum operator in the SO basis.
    field : np.array
        Magnetic field in mT at which susceptibility is measured. If None,
        returns differential susceptibility.
    algorithm : {'eigh', 'expm'}
        Algorithm for the computation of the partition function.
    """

    Na = 6.02214076e23  # 1 / mol
    kb = 3.166811563e-6  # hartree / K
    beta = 1 / (kb * temp)  # hartree
    au2mT = 2.35051756758e5 * 1e3  # mTesla / au

    h_total = hamiltonian + zeeman_hamiltonian(spin, angm, field)

    if algorithm == 'expm':
        dim = h_total.shape[0]
        # condition matrix by diagonal shift
        h_shft = h_total - stop_gradient(jnp.eye(dim) * jnp.min(h_total))
        expH = jscipy.linalg.expm(-beta * h_shft)
        Z = jnp.trace(expH).real

    elif algorithm == 'eigh':
        eig, vec = jnp.linalg.eigh(h_total)
        eig_shft = eig - stop_gradient(eig[0])
        expH = vec @ jnp.diag(jnp.exp(-beta * eig_shft)) @ vec.T.conj()
        Z = jnp.sum(jnp.exp(-beta * eig_shft))

    else:
        ValueError(f"Unknown algorithm {algorithm}!")

    dZ = -jnp.einsum('ij,mji', expH, magmom(spin, angm) / au2mT).real

    return Na * dZ / Z


def make_molecular_magnetisation(hamiltonian, spin, angm, field):
    """ Molar molecular magnetisation in [hartree] / [mT mol] maker function
    for partial evaluation of matrix eigen decomposition.

    Parameters
    ----------
    hamiltonian : np.array
        Electronic Hamiltonian in atomic units.
    spin : np.array
        Spin operator in the SO basis.
    angm : np.array
        Orbital angular momentum operator in the SO basis.
    field : np.array
        Magnetic field in mT at which susceptibility is measured. If None,
        returns differential susceptibility.
    """

    Na = 6.02214076e23  # 1 / mol
    kb = 3.166811563e-6  # hartree / K
    au2mT = 2.35051756758e5 * 1e3  # mTesla / au

    h_total = hamiltonian + zeeman_hamiltonian(spin, angm, field)
    # condition matrix by diagonal shift
    eig, vec = jnp.linalg.eigh(h_total)

    def molecular_magnetisation(temp):
        beta = 1 / (kb * temp)  # hartree
        eig_shft = eig - stop_gradient(eig[0])
        expH = vec @ jnp.diag(jnp.exp(-beta * eig_shft)) @ vec.T.conj()
        Z = jnp.sum(jnp.exp(-beta * eig_shft))
        dZ = -jnp.einsum('ij,mji', expH, magmom(spin, angm) / au2mT).real
        return Na * dZ / Z

    return molecular_magnetisation
