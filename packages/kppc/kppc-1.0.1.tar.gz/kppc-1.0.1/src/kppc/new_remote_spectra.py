import numpy as np
from scipy import special
import scipy.integrate as integrate
from numpy.linalg import inv
from scipy.interpolate import interp1d, interp2d
import scipy.optimize as optimize
from . import config as conf

# Auxiliary scale factor grid
ag = np.logspace(np.log10(conf.adec), 0, conf.transfer_integrand_sampling)

# Modified from SZ_cosmo https://github.com/rcayuso/SZ_cosmo/tree/master
def az(z):
    """Scale factor at a given redshift"""
    return 1.0 / (1.0 + z)

def aeq(Omega_b, Omega_c, h, Omega_r_h2=conf.Omega_r_h2):
    """Scale factor at matter radiation equality"""
    return Omega_r_h2 / (Omega_b + Omega_c) / h**2

def k_sampling(log_kmin, log_kmax, k_res):
    return np.logspace(log_kmin, log_kmax, k_res)

def L_sampling(estim_signal_lmax):
    return np.arange(estim_signal_lmax)

# Modification to dark energy equation of state (only one model for now)
def fde(a):
    return 1.0 - a

def fde_da(a):
    return -1.0

def H0(h):
    """Hubble parameter today in Mpc**-1"""
    return 100.0 * h / (3.0 * 1.0e5)

def Omega_L(Omega_b, Omega_c, Omega_K, h, Omega_r_h2=conf.Omega_r_h2):
    """Omega_L in terms of Omega_b, Omega_c, and K imposed by consistency"""
    return 1 - Omega_K - (Omega_b + Omega_c) - Omega_r_h2/h**2


def E(a, Omega_b, Omega_c, w, wa, Omega_K, h, Omega_r_h2=conf.Omega_r_h2):
    """Reduced Hubble parameter, H/H_0"""
    exp_DE = 3.0*(1.0 + w + wa*fde(a))
    E2 = (Omega_b + Omega_c) / a**3 + Omega_K / a**2 \
        + Omega_L(Omega_b, Omega_c, Omega_K, h) / a**exp_DE \
        + Omega_r_h2/h**2  / a**4
    return np.sqrt(E2)


def H(a, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Hubble parameter given a & cosmological parameters"""
    Ea = E(a, Omega_b, Omega_c, w, wa, Omega_K, h)
    return Ea * H0(h)


def dEda(a, Omega_b, Omega_c, w, wa, Omega_K, h, Omega_r_h2=conf.Omega_r_h2) :
    """
    Derivative of the reduced Hubble parameter respect to the scale factor
    """
    exp_DE = 3.0*(1.0 + w + wa*fde(a))
    d = -3.0*(Omega_b + Omega_c) / a**4 - 2.0*Omega_K / a**3 \
        + (-3.0*wa*a*np.log(a) * fde_da(a) - exp_DE) * Omega_L(Omega_b, Omega_c, Omega_K, h) / a**(exp_DE + 1) \
        - 4.0*Omega_r_h2/h**2 / a**5
    derv_E = d / (2.0 * E(a, Omega_b, Omega_c, w, wa, Omega_K, h, Omega_r_h2=Omega_r_h2))
    return derv_E


def dHdt(a, Omega_b, Omega_c, w, wa, Omega_K, h) :
    """(non-conformal) time-derivative of hubble parameter"""
    return a*H(a, Omega_b, Omega_c, w, wa, Omega_K, h)*H0(h) \
        * dEda(a, Omega_b, Omega_c, w, wa, Omega_K, h)

def sigma_nez(z, Omega_b, h):
    """Electron density as a function of redshift times the Thompson cross section"""
    mProton_SI = 1.673e-27
    G_SI = 6.674e-11
    H0 = 100 * h * 1e3  # Hubble constant in m s^-1 Mpc^-1
    MegaparsecTometer = 3.086e22
    thompson_SI = 6.6524e-29

    sigma_ne = thompson_SI * (3 * 0.88 / 8. / np.pi / MegaparsecTometer) * \
        (H0**2) * (1. / mProton_SI / G_SI) * Omega_b * (1 + z)**3

    return sigma_ne

def tau_z(z, Omega_b, h):
    """Optical depth at a given redshift"""
    chi = chifromz(z)
    chi_grid = np.linspace(0, chi, 100)
    z_grid = zfromchi(chi_grid)
    ae = az(z_grid)
    sigma_ne = sigma_nez(z_grid, Omega_b, h)

    integrand = ae * sigma_ne

    tau = integrate.simps(integrand, chi_grid)

    return tau

def tau_grid(Chi_grid, Z_grid, Omega_b, h):
    """
    Optical depth as a function of redshift
    Assumes Z_grid starts at z = 0.0!
    """
    ae = az(Z_grid)
    sigma_ne = sigma_nez(Z_grid, Omega_b, h)
    integrand = ae * sigma_ne
    tau_grid = integrate.cumtrapz(integrand, Chi_grid, initial=0.0)

    return tau_grid


def z_re(Omega_b, h, tau):
    """ redshift of recombination (?) """
    zguess = 6.0
    sol = optimize.root(root_tau2z, zguess, args=(Omega_b, h, tau))
    z_re = sol.x
    return z_re


def spherical_jn_pp(l, z):
    """
    Second derivative of spherical Bessel function.
    """
    if l == 0:
        jn = special.spherical_jn(2, z) - special.spherical_jn(1, z)/z
    else:
        jn = (special.spherical_jn(l-1,z, True)
              - (l+1)/z * special.spherical_jn(l,z, True)
              + (l+1)/(z**2) * special.spherical_jn(l,z))
    return jn


##########################################################################
################   COMOVING DISTANCES AND THEIR DERIVATIVES     ##########
##########################################################################

def Integrand_chi(a, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Integrand of the comoving distance defined below (chia, small c)"""
    int_chi = 1 / ((a**2) * H(a, Omega_b, Omega_c, w, wa, Omega_K, h))
    return int_chi


def chia(a, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Comoving distance to a (using integrate.quad)"""
    chi = integrate.quad(Integrand_chi, a, 1, args=(
        Omega_b, Omega_c, w, wa, Omega_K, h, ))[0]
    return chi


def Integrand_Chi(y, a, Omega_b, Omega_c, w, wa, Omega_K, h):
    """ Function to integrate to find chi(a) defined below (Chia, capital C) """
    g = -((a**2) * H(a, Omega_b, Omega_c, w, wa, Omega_K, h))**-1
    return g

def Chia(Omega_b, Omega_c, w, wa, Omega_K, h):
    """Comoving distance to a (using integrate.odeint)"""
    Integral = (integrate.odeint(Integrand_Chi, chia(ag[0], Omega_b, Omega_c, w, wa, Omega_K, h),
                                 ag, args=(Omega_b, Omega_c, w, wa, Omega_K, h,))).reshape(len(ag),)

    if ag[-1] == 1.0:
        Integral[-1] = 0.0

    return Integral

def chifromz(z, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Comoving distance at a redshift z"""
    chi = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(z))
    return chi


def zfromchi(chi, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Get redshift z given comoving distance chi"""
    afromchi = interp1d(
        Chia(Omega_b, Omega_c, w, wa, Omega_K, h), ag,
        kind="cubic", bounds_error=False, fill_value='extrapolate')

    aguess = afromchi(chi)

    sol = optimize.root(root_chi2a, aguess,
        args=(chi, Omega_b, Omega_c, w, wa, Omega_K, h))
    z = 1.0/sol.x - 1.0

    return z


#############################################################################
################                                          ###################
################          GROWTH FUNCTIONS                ###################
################                                          ###################
#############################################################################


def Integrand_GF(s, Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    Integrand for the growth function (as defined below)
    """
    Integrand = 1 / (s * E(s, Omega_b, Omega_c, w, wa, Omega_K, h, Omega_r_h2=0.0))**3
    return Integrand


def Integral_GF(a, Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    Integral appearing in the growth factor GF
    """
    Integral = integrate.quad(Integrand_GF, 0, a, args=(
        Omega_b, Omega_c, w, wa, Omega_K, h, ))[0]
    return Integral


def Integrand_GF_ODE(y, a, Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    Function for solving Integral_GF as an ODE (as defined below)
    """
    f = (a * E(a, Omega_b, Omega_c, w, wa, Omega_K, h, Omega_r_h2=0.0))**-3
    return f*1.0e13 # 10^13 changes scale so ODE has enough precision


def Integral_GF_ODE(Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    Integral appearing in the growth function GF solved as an ODE
    """
    Integral = integrate.odeint(Integrand_GF_ODE,
                                1.0e13*Integral_GF(ag[0], Omega_b, Omega_c,
                                            w, wa, Omega_K, h),
                                ag, args=(Omega_b, Omega_c, w, wa, Omega_K, h,))

    return Integral * 1.0e-13 # 10^13 changes scale so ODE has enough precision


def GF(Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    Growth function using ODE, D_1(ag) / ag
    Dodelson Eq. 7.5, 7.77
    """
    l = 5.0/2.0 * (Omega_b + Omega_c) * \
        E(ag, Omega_b, Omega_c, w, wa, Omega_K, h, Omega_r_h2=0.0) / ag
    GF = l * Integral_GF_ODE(Omega_b, Omega_c, w, wa,
                             Omega_K, h).reshape(len(ag),)
    return GF


def Dpsi(Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    ~ Potential "growth function" from linear theory plus approximations
    Phi = Phi_prim * T(k) * (9/10 * D_1(a)/a) per Dodelson Eq. 7.5
    Dpsi is ("9/10" * D_1(a)/a)
    Dodelson Eq. 7.5, Eq. 7.32
    """
    y = ag / aeq(Omega_b, Omega_c, h)
    fancy_9_10 = (16.0*np.sqrt(1.0 + y) + 9.0*y**3 + 2.0*y**2 - 8.0*y - 16.0) / (10.0*y**3)
    Dpsi = fancy_9_10 * GF(Omega_b, Omega_c, w, wa, Omega_K, h)
    return Dpsi


def derv_Dpsi(Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    Derivative of the growth function with respect to the scale factor
    """
    y = ag / aeq(Omega_b, Omega_c, h)
    Eag = E(ag, Omega_b, Omega_c, w, wa, Omega_K, h, Omega_r_h2=0.0)
    dEdag = dEda(ag, Omega_b, Omega_c, w, wa, Omega_K, h, Omega_r_h2=0.0)
    fancy_9_10 = (16.0*np.sqrt(1.0 + y) + 9.0*y**3 + 2.0*y**2 - 8.0*y - 16.0) / (10.0*y**3)
    P1 = ((8.0/np.sqrt(1.0 + y) + 27.0*y**2 + 4.0*y - 8.0) / (aeq(Omega_b,
      Omega_c, h)*10.0*y**3)) * GF(Omega_b, Omega_c, w, wa, Omega_K, h)
    P2 = Dpsi(Omega_b, Omega_c, w, wa, Omega_K, h) * (-4/ag + dEdag/Eag)
    P3 = fancy_9_10 * (5.0/2.0) * (Omega_b + Omega_c) / (ag**4 * Eag**2)

    derv_Dpsi = P1 + P2 + P3
    return derv_Dpsi


def Dv(Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    Velocity growth function on superhorizon scales
    Dodelson 7.15 minus 7.16, v is 5.78
    v_i ~ - Dv d_i psi
    grad*v_i ~ k^2 * Dv * psi
    """
    y = ag / aeq(Omega_b, Omega_c, h)
    Dv = 2.0 * (ag**2) * H(ag, Omega_b, Omega_c, w, wa, Omega_K, h) \
                / ((Omega_b + Omega_c)*H0(h)**2) * y / (4.0 + 3.0*y) \
            * (Dpsi(Omega_b, Omega_c, w, wa, Omega_K, h)
                + ag*derv_Dpsi(Omega_b, Omega_c, w, wa, Omega_K, h))
    return Dv


def T(k, Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    'Best fitting' transfer function From Eq. 7.70 in Dodelson
    Assumes: no baryons, nonlinear effects, phi=psi always (9/10 -> 0.86), normal (no?) DE effects
    """
    fac = np.exp(-Omega_b*(1+np.sqrt(2*h)/(Omega_b+Omega_c)))
    keq = aeq(Omega_b, Omega_c, h) * H(aeq(Omega_b, Omega_c, h),
                                       Omega_b, Omega_c, w, wa, Omega_K, h)
    x = k / keq / fac
    x[np.where(x<1.0e-10)] = 1
    T = (np.log(1 + 0.171 * x) / (0.171 * x)) * (1 + 0.284 * x
      + (1.18 * x)**2 + (0.399 * x)**3 + (0.49 * x)**4)**(-0.25)

    return T


def Ppsi(k, As, ns):
    """
    Power spectrum of primordial potential
    """
    P = (2.0/3.0)**2 * 2.0 * np.pi**2 / (k**3) \
        * As * 10**-9 * (k / conf.k0)**(ns - 1)
    return P


##########################################################################
################                                          ################
################ INTERPOLATING AND AUXILIARY FUNCTIONS    ################
################                                          ################
##########################################################################

def Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h):
    Chia_inter = interp1d(ag, Chia(Omega_b, Omega_c, w, wa, Omega_K, h),
                          kind="cubic", bounds_error=False, fill_value='extrapolate')
    return Chia_inter


def Dpsi_inter(Omega_b, Omega_c, w, wa, Omega_K, h):
    Dpsi_inter = interp1d(ag, Dpsi(Omega_b, Omega_c, w, wa, Omega_K, h),
                          kind="cubic", bounds_error=False, fill_value='extrapolate')
    return Dpsi_inter


def derv_Dpsi_inter(Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    Returns interpolating function
    of derivative of the growth function with respect to the scale factor
    """
    derv_Dpsi_inter = interp1d(ag, derv_Dpsi(Omega_b, Omega_c, w, wa, Omega_K, h),
                               kind="cubic", bounds_error=False, fill_value='extrapolate')
    return derv_Dpsi_inter


def Dv_inter(Omega_b, Omega_c, w, wa, Omega_K, h):
    """Returns interpolating funcntion of velocity growth function"""
    Dv_inter = interp1d(ag, Dv(Omega_b, Omega_c, w, wa, Omega_K, h),
                        kind="cubic", bounds_error=False, fill_value='extrapolate')
    return Dv_inter


def root_chi2a(a, chis, Omega_b, Omega_c, w, wa, Omega_K, h):
    """ Needed to use the root function of scipy's optimize module. """
    return Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(a) - chis


def root_tau2z(z, Omega_b, h, tau):
    """Needed to use the root function of scipy's optimize module below."""
    return tau_z(z, Omega_b, h) - tau


#######################################################################
################                                    ###################
################ KERNELS FOR SW, ISW AND DOPPLER    ###################
################                                    ###################
#######################################################################



def G_SW_ksz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """kSZ Integral kernel for SW effect"""
    chidec = Chia(Omega_b, Omega_c, w, wa, Omega_K, h)[0]
    chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))
    G_SW_ksz = 3 * (2 * Dpsi(Omega_b, Omega_c, w, wa, Omega_K, h)
                    [0] - 3 / 2) * special.spherical_jn(1, k * (chidec - chie))

    return G_SW_ksz


def G_SW_psz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """pSZ Integral kernel for SW effect"""
    chidec = Chia(Omega_b, Omega_c, w, wa, Omega_K, h)[0]
    chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))
    G_SW_psz = -4 * np.pi * (2 * Dpsi(Omega_b, Omega_c, w, wa, Omega_K, h)
                             [0] - 3 / 2) * special.spherical_jn(2, k * (chidec - chie))

    return G_SW_psz


def G_SW_CMB(k, l, Omega_b, Omega_c, w, wa, Omega_K, h):
    """CMB Integral kernel for SW effect"""
    chidec = Chia(Omega_b, Omega_c, w, wa, Omega_K, h)[0]
    G_SW_CMB = 4 * np.pi * ((1j)**l) * (2 * Dpsi(Omega_b, Omega_c, w,
        wa, Omega_K, h)[0] - 3 / 2) * special.spherical_jn(l, k * chidec)

    return G_SW_CMB


def G_Dopp_ksz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """kSZ Integral kernel for the Doppler effect"""
    chidec = Chia(Omega_b, Omega_c, w, wa, Omega_K, h)[0]
    chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))
    G_Dopp_ksz = k * Dv(Omega_b, Omega_c, w, wa, Omega_K, h)[0] * (special.spherical_jn(0, k * (
        chidec - chie)) - 2 * special.spherical_jn(2, k * (chidec - chie))) - k * Dv_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))

    return G_Dopp_ksz


def G_decDopp_ksz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """kSZ Integral kernel for the Doppler effect"""
    chidec = Chia(Omega_b, Omega_c, w, wa, Omega_K, h)[0]
    chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))
    G_decDopp_ksz = k * Dv(Omega_b, Omega_c, w, wa, Omega_K, h)[0] * (special.spherical_jn(0, k * (
        chidec - chie)) - 2 * special.spherical_jn(2, k * (chidec - chie)))

    return G_decDopp_ksz




def G_localDopp_ksz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """kSZ Integral kernel for the local Doppler effect"""
    chidec = Chia(Omega_b, Omega_c, w, wa, Omega_K, h)[0]
    chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))
    G_localDopp_ksz = -k * \
        Dv_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))

    return G_localDopp_ksz


def G_Dopp_psz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """pSZ Integral kernel for the Doppler effect"""
    chidec = Chia(Omega_b, Omega_c, w, wa, Omega_K, h)[0]
    chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))
    G_Dopp_psz = (4 * np.pi / 5) * k * Dv(Omega_b, Omega_c, w, wa, Omega_K, h)[0] * (
        3 * special.spherical_jn(3, k * (chidec - chie)) - 2 * special.spherical_jn(1, k * (chidec - chie)))

    return G_Dopp_psz


def G_Dopp_CMB(k, l, Omega_b, Omega_c, w, wa, Omega_K, h):
    """CMB Integral kernel for the Doppler effect"""
    chidec = Chia(Omega_b, Omega_c, w, wa, Omega_K, h)[0]
    G_Dopp_CMB = (4 * np.pi / (2.0 * l + 1.0)) * (1j**l) * k * Dv(Omega_b, Omega_c, w, wa, Omega_K, h)[
        0] * (l * special.spherical_jn(l - 1, k * chidec) - (l + 1) * special.spherical_jn(l + 1, k * chidec))

    return G_Dopp_CMB


def G_ISW_ksz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Integral kernel for the ksz ISW effect"""
    a = np.logspace(np.log10(conf.adec), np.log10(az(ze)), conf.transfer_integrand_sampling)
    Chia = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(a)
    Chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))
    Deltachi = Chia - Chie
    Deltachi[-1] = 0
    s2 = k[..., np.newaxis] * Deltachi

    integrand = special.spherical_jn(1, s2) * derv_Dpsi_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(a)
    g_isw_ksz = 6.0*integrate.simps(integrand, a)

    return g_isw_ksz


def G_ISW_psz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Integral kernel for the psz ISW effect"""
    a = np.logspace(np.log10(conf.adec), np.log10(az(ze)), 1000)
    Chia = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(a)
    Chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))
    Deltachi = Chia - Chie
    Deltachi[-1] = 0

    s2 = k[..., np.newaxis] * Deltachi
    integrand = special.spherical_jn(
        2, s2) * derv_Dpsi_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(a)
    g_isw_psz = -8 * np.pi * integrate.simps(integrand, a)

    return g_isw_psz


def G_ISW_CMB(k, l, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Integral kernel for the CMB ISW effect"""
    a = np.logspace(np.log10(conf.adec), np.log10(1.0), 1000)
    Chia = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(a)
    Deltachi = Chia
    Deltachi[-1] = 0
    s2 = k[..., np.newaxis] * Deltachi

    integrand = special.spherical_jn(
        l, s2) * derv_Dpsi_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(a)
    g_isw_CMB = 8 * np.pi * \
        (1j**l) * integrate.simps(integrand, a)

    return g_isw_CMB


def G_ksz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Sum of kSZ integral kernels"""

    # Lower sampling for slow ISW term
    ks_isw = np.logspace(conf.k_min, conf.k_max, conf.k_res//10)
    Gs_isw = G_ISW_ksz( ks_isw, ze, Omega_b, Omega_c, w, wa, Omega_K, h )
    G_int_ISW = interp1d(
        ks_isw, Gs_isw, kind="cubic", bounds_error=False, fill_value='extrapolate')

    return G_int_ISW(k) \
        + G_SW_ksz( k, ze, Omega_b, Omega_c, w, wa, Omega_K, h ) \
        + G_Dopp_ksz( k, ze, Omega_b, Omega_c, w, wa, Omega_K, h )


def G_ksz_localDopp(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """kSZ integral kernel including only local peculiar velocity"""
    G_s = G_localDopp_ksz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h)
    return G_s


def G_psz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Sum of psz integral kernels"""
    G = G_SW_psz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h )\
        + G_Dopp_psz( k, ze, Omega_b, Omega_c, w, wa, Omega_K, h )\
        + G_ISW_psz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h)

    return G


def G_CMB(k, l, Omega_b, Omega_c, w, wa, Omega_K, h):
    """Sum of CMB integral kernels"""
    G = G_SW_CMB(k, l, Omega_b, Omega_c, w, wa, Omega_K, h )\
        + G_Dopp_CMB( k, l, Omega_b, Omega_c, w, wa, Omega_K, h )\
        + G_ISW_CMB(k, l, Omega_b, Omega_c, w, wa, Omega_K, h)

    return G

def Transfer_ksz_redshift(k, L, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    KSZ transfer function at a given redshift `ze`
    """
    transfer_ksz = np.zeros((len(k), len(L)), dtype=np.complex64)
    Ker = G_ksz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h)
    Tk = T(k, Omega_b, Omega_c, w, wa, Omega_K, h)
    Chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))

    for l_id, l in enumerate(L):
        if l == 0:
            transfer_ksz[:, l_id] = 0.0 + 1j * 0.0
        else:
            c = (4 * np.pi * (1j)**l) / (2 * l + 1)
            transfer_ksz[:, l_id] = c * (l * special.spherical_jn(l - 1, k * Chie) - (
                l + 1) * special.spherical_jn(l + 1, k * Chie)) * Tk * Ker

    return transfer_ksz


def Transfer_ksz_localDopp_redshift(k, L, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """
    KSZ transfer function for a given redshift using only local doppler
    """
    transfer_ksz = np.zeros((len(k), len(L)), dtype=np.complex64)
    Ker = G_ksz_localDopp(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h)
    Tk = T(k, Omega_b, Omega_c, w, wa, Omega_K, h)
    Chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))

    for l_id, l in enumerate(L):
        if l == 0:
            transfer_ksz[:, l_id] = 0.0 + 1j * 0.0
        else:
            c = (4 * np.pi * (1j)**l) / (2 * l + 1)
            transfer_ksz[:, l_id] = c * (l * special.spherical_jn(l - 1, k * Chie) - (
                l + 1) * special.spherical_jn(l + 1, k * Chie)) * Tk * Ker

    return transfer_ksz


def Transfer_psz_redshift(k, L, ze, Omega_b, Omega_c, w, wa, Omega_K, h):
    """PSZ transfer function for a given redshift"""
    if ze == 0.0:
        transfer_psz = np.zeros((len(k), len(L)), dtype=np.complex64)
        Ker = G_psz(k, 0.0, Omega_b, Omega_c, w, wa, Omega_K, h)
        Tk = T(k, Omega_b, Omega_c, w, wa, Omega_K, h)

        for l_id, l in enumerate(L):
            if l == 2:
                c = -(5 * (1j)**l) * np.sqrt(3.0 / 8.0) * \
                    np.sqrt(special.factorial(l + 2) /
                            special.factorial(l - 2))
                transfer_psz[:, l_id] = c * (1. / 15.) * Tk * Ker
            else:
                transfer_psz[:, l_id] = 0.0 + 1j * 0.0

    else:
        transfer_psz = np.zeros((len(k), len(L)), dtype=np.complex64)
        Ker = G_psz(k, ze, Omega_b, Omega_c, w, wa, Omega_K, h)
        Tk = T(k, Omega_b, Omega_c, w, wa, Omega_K, h)
        Chie = Chia_inter(Omega_b, Omega_c, w, wa, Omega_K, h)(az(ze))

        for l_id, l in enumerate(L):
            if l < 2:
                transfer_psz[:, l_id] = 0.0 + 1j * 0.0
            else:
                c = -(5 * (1j)**l) * np.sqrt(3.0 / 8.0) * \
                    np.sqrt(special.factorial(l + 2) /
                            special.factorial(l - 2))
                transfer_psz[
                    :, l] = c * (special.spherical_jn(l, k * Chie) / ((k * Chie)**2)) * Tk * Ker

        return transfer_psz

    def Transfer_CMB(k, L, Omega_b, Omega_c, w, wa, Omega_K, h):
        """CMB transfer function for large scales at z = 0"""
        transfer_CMB = np.zeros((len(k), len(L)), dtype=np.complex64)
        Tk = T(k, Omega_b, Omega_c, w, wa, Omega_K, h)

        for l_id, l in enumerate(L):
            if l < 1:
                transfer_CMB[:, l_id] = 0.0 + 1j * 0.0
            else:
                Ker = G_CMB(k, l, Omega_b, Omega_c, w, wa, Omega_K, h)
                transfer_CMB[:, l_id] = Tk * Ker

        return transfer_CMB


def Transfer_E(k, L, Omega_b, Omega_c, w, wa, Omega_K, h, tau, Chi_low=None, Chi_re=None, Chi_grid_num=None):
    """E transfer function for large scales at z = 0"""
    transfer_E = np.zeros((len(k), len(L)), dtype=np.complex64)
    Tk = T(k, Omega_b, Omega_c, w, wa, Omega_K, h)
    Chi_grid = np.linspace(Chi_low, Chi_re, Chi_grid_num)
    Z_grid = zfromchi(Chi_grid, Omega_b, Omega_c, w, wa, Omega_K, h)
    a_grid = az(Z_grid)
    sigma_ne = sigma_nez(Z_grid, Omega_b, h)
    etau = np.exp(-tau_grid(Chi_grid, Z_grid, Omega_b, h))

    Integrand = np.zeros((len(k), len(L), len(Chi_grid)), dtype=np.complex64)
    for i in np.arange(len(Chi_grid)):
        Integrand[:, :, i] = (-np.sqrt(6.0) / 10.0) * Transfer_psz_redshift(k, L, Z_grid[
            i], Omega_b, Omega_c, w, wa, Omega_K, h) * a_grid[i] * sigma_ne[i] * etau[i]

    transfer_E = integrate.simps(Integrand, Chi_grid, axis=-1)

    return transfer_E


def CL_bins(T_list1, T_list2, L, k=None, Pk_pri=None):
    """
        Compute correlation C_l's using transfer function pairs in T_list1 and T_list2
        assumes T[l_idx, k], not T[k,l].
    """
    CL = np.zeros((len(T_list1),len(L)))

    for i in np.arange(len(T_list1)):
        for l in L:
            T1 = T_list1[i]
            T2 = T_list2[i]

            I = (k**2)/(2*np.pi)**3 *Pk_pri* np.conj(T1[:,l]) * T2[:,l]

            CL[i,l] = np.real(integrate.simps(I, k))
    return CL
