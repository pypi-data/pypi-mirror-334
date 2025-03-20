from kppc import *
import numpy as np
from classy import Class
from math import pi


A_s = 2.2
n_s = 0.965
Omega_m = 0.31
Omega_b = 0.049
Omega_c=Omega_m-Omega_b
Omega_r_h2 = 4.15 * 10**-5
h = 0.68
tau = 0.06
w = -1.0
wa = 0.0
Omega_K = 0.0

log_kmax = -2
log_kmin = -5
k_res = 1000


k_pivot = 0.05 # 1/Mpc
k = np.logspace(log_kmin, log_kmax, k_res)
# Premordial scalar perturbation power spectrum
Pk_pri = 2*np.pi**2*A_s*(k/k_pivot)**(n_s-1)*1e-9/k**3 # (Mpc)^3


lmax = 3000
ls = np.arange(0, lmax)
Chi = 3000

l1min = 1000
l1max = 3000
l1 = np.arange(0, l1max+1)

l2min = 0
l2max = 60


pSZ_PS = pSZ_ps(A_s, n_s, Omega_b, Omega_c, h, tau, w, wa, Omega_K)

# print(pSZ_PS.CLdd_eff_oneChi(2000, Chi))
# print(pSZ_PS.CLqq_oneChi(np.arange(0, 100, 1), Chi, k=k, Pk_pri=Pk_pri))
# print(pSZ_PS.CLee_psz1_oneChi(lmax, l1min, l1max, l2min, l2max, Chi, k=k, Pk_pri=Pk_pri))
# print(pSZ_PS.CLEE_psz1(lmax, l1min, l1max, l2min, l2max, k=k, Pk_pri=Pk_pri))
print(pSZ_PS.CLEE_psz0(100, k=k, Pk_pri=Pk_pri))
