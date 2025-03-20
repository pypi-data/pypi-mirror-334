import numpy as np
import jax.numpy as jnp
from classy import Class
from .glquad import GLQuad
from .wignerd import *
from .new_remote_spectra import *
from scipy.interpolate import interp1d, interp2d
import ipdb

class test_operation:
    def __init__(self, *args):
        self.a = args[0]
        self.b = args[1]

    def operation(self, c):
        return (self.a + self.b)*c


class pSZ_ps():
    def __init__(self, A_s, n_s, Omega_b, Omega_c, h, tau, w, wa, Omega_K):
        """
        Cosmological parameters container

        Attributes:
        Omega_b (float): Baryon density parameter
        Omega_c (float): Cold dark matter density parameter
        h (float): Dimensionless Hubble parameter (H0/100 km/s/Mpc)
        """
        self.A_s = A_s
        self.n_s = n_s
        self.Omega_b = Omega_b
        self.Omega_c = Omega_c
        self.h = h
        self.tau = tau
        self.w = w
        self.wa = wa
        self.Omega_K = Omega_K
        self.common_settings = {
            'h':self.h,
            'omega_b':self.Omega_b*self.h**2,
            'omega_cdm':self.Omega_c*self.h**2,
            'A_s': self.A_s*1e-9,
            'n_s': self.n_s,
            'tau_reio':self.tau,
            'output':'mPk',
            'P_k_max_1/Mpc':12,
            'gauge':'newtonian'
        }

        self.M = Class()
        self.M.set(self.common_settings)
        self.M.set({'z_pk':1000})
        self.M.compute()


    def CLEE_psz0(self, lmax, k=None, Pk_pri=None, Chi_low=1, Chi_re=9000, Chi_grid_num=100):
        L = np.arange(0, lmax+1, 1)
        T_list = [Transfer_E(k, L, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h, self.tau, Chi_low=Chi_low, Chi_re=Chi_re, Chi_grid_num=Chi_grid_num)]

        return CL_bins(T_list, T_list, L, k=k, Pk_pri=Pk_pri)[0]


    def CLdd_eff_oneChi(self, L, Chi):
        """
        CLdd_eff(Chi)
        """
        if not isinstance(L, np.ndarray):
            L = np.array([L])
        CL = np.zeros(len(L), dtype=np.complex64)

        Z = zfromchi(Chi, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        a = az(Z)
        sigma_ne = sigma_nez(Z, self.Omega_b, self.h)
        # ipdb.set_trace()
        CL = a**2*sigma_ne**2*self.M.get_pk_all((L+1/2)/np.array(Chi), Z)
        return CL[0]


    def CLqq_oneChi(self, L, Chi, k=None, Pk_pri=None):
        """
        CLqq(Chi)
        """
        if not isinstance(L, np.ndarray):
            L = np.array([L])
        CL = np.zeros(len(L), dtype=np.complex64)

        Z = zfromchi(Chi, self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)
        Integrand = np.zeros((len(k), len(L)), dtype=np.complex64)
        T = Transfer_psz_redshift(k, L, Z[0], self.Omega_b, self.Omega_c, self.w, self.wa, self.Omega_K, self.h)

        k_broad = np.broadcast_to(k, (len(L), len(k))).transpose()
        Pk_pri_broad = np.broadcast_to(Pk_pri, (len(L), len(k))).transpose()

        Integrand = (k_broad**2)/(2*np.pi)**3*Pk_pri_broad*np.conj(T)*T

        CL = np.real(integrate.simps(Integrand, k, axis=0))

        return CL


    def CLee_psz1_oneChi(self, lmax, l1min, l1max, l2min, l2max, Chi, k=None, Pk_pri=None):
        """
        CLee_psz_1(Chi)
        Attributes:
        k:
        Pk_pri: primordial scalar perturbation power spectrum
        """
        l = jnp.arange(0, lmax+1)
        glq = GLQuad(int((3*lmax+1)/2))

        # l1 = jnp.arange(0, l1max+1)
        l1 = np.arange(0, l1max+1)
        l2 = np.arange(0, l2max+1)

        # ipdb.set_trace()
        Cl1 = self.CLdd_eff_oneChi(l1, Chi)
        Cl2 = self.CLqq_oneChi(l2, Chi, k=k, Pk_pri=Pk_pri)

        f1 = Cl1
        f2 = Cl2
        # ipdb.set_trace()
        zeta_00 = glq.cf_from_cl(0, 0, f1, lmin=l1min, lmax=l1max, prefactor=True)
        zeta_m2m2 = glq.cf_from_cl(-2, -2, f2, lmin=l2min, lmax=l2max, prefactor=True)
        zeta_p2m2 = glq.cf_from_cl(2, -2, f2, lmin=l2min, lmax=l2max, prefactor=True)

        A = glq.cl_from_cf(2, 2, zeta_00 * zeta_m2m2, lmax=lmax)
        B = glq.cl_from_cf(-2, 2, zeta_00 * zeta_p2m2, lmax=lmax)

        return 6/100*np.pi*(A + B)


    def CLbb_psz1_oneChi(self, lmax, l1min, l1max, l2min, l2max, Chi, k=None, Pk_pri=None):
        """
        CLbb_psz_1(Chi)
        """
        l = jnp.arange(0, lmax+1)
        glq = GLQuad(int((3*lmax+1)/2))

        # l1 = jnp.arange(0, l1max+1)
        l1 = np.arange(0, l1max+1)
        l2 = np.arange(0, l2max+1)

        # ipdb.set_trace()
        Cl1 = self.CLdd_eff_oneChi(l1, Chi)
        Cl2 = self.CLqq_oneChi(l2, Chi, k=k, Pk_pri=Pk_pri)

        f1 = Cl1
        f2 = Cl2
        # ipdb.set_trace()
        zeta_00 = glq.cf_from_cl(0, 0, f1, lmin=l1min, lmax=l1max, prefactor=True)
        zeta_m2m2 = glq.cf_from_cl(-2, -2, f2, lmin=l2min, lmax=l2max, prefactor=True)
        zeta_p2m2 = glq.cf_from_cl(2, -2, f2, lmin=l2min, lmax=l2max, prefactor=True)

        A = glq.cl_from_cf(2, 2, zeta_00 * zeta_m2m2, lmax=lmax)
        B = glq.cl_from_cf(-2, 2, zeta_00 * zeta_p2m2, lmax=lmax)

        return 6/100*np.pi*(A - B)

    def CLEE_psz1(self, lmax, l1min, l1max, l2min, l2max, k=None, Pk_pri=None, Chi_low=1000, Chi_re=9000, Chi_grid_num=100):

        Chi_grid = np.linspace(Chi_low, Chi_re, Chi_grid_num)
        Cl = np.zeros((lmax+1, len(Chi_grid)))

        Integrand = np.zeros((lmax+1, len(Chi_grid)), dtype=np.complex64)

        print("calculating CLEE_pSZ1")
        for i in np.arange(len(Chi_grid)):
            Cl[:, i] = self.CLee_psz1_oneChi(lmax, l1min, l1max, l2min, l2max, Chi_grid[i], k=k, Pk_pri=Pk_pri)
            Integrand[:, i] = 1/Chi_grid[i]**2*Cl[:, i]

        Cl = integrate.simps(Integrand, Chi_grid, axis=-1).real
        return Cl

    def CLBB_psz1(self, lmax, l1min, l1max, l2min, l2max, k=None, Pk_pri=None, Chi_low=1000, Chi_re=9000, Chi_grid_num=100):

        Chi_grid = np.linspace(Chi_low, Chi_re, Chi_grid_num)
        Cl = np.zeros((lmax+1, len(Chi_grid)))

        Integrand = np.zeros((lmax+1, len(Chi_grid)), dtype=np.complex64)

        print("calculating CLBB_pSZ1")
        for i in np.arange(len(Chi_grid)):
            print(i)
            Cl[:, i] = self.CLbb_psz1_oneChi(lmax, l1min, l1max, l2min, l2max, Chi_grid[i], k=k, Pk_pri=Pk_pri)
            Integrand[:, i] = 1/Chi_grid[i]**2*Cl[:, i]

        Cl = integrate.simps(Integrand, Chi_grid, axis=-1).real
        return Cl
