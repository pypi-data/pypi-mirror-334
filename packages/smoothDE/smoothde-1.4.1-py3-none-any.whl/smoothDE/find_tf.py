"""Rhys M. Adams"""
# ignore after this line
from scipy.special import lambertw
from scipy.optimize import minimize
import numpy as np

def fx_app(eff_t,R, V):
    """Fast but approximate solution to action with only diagonal 
    smoothing penalty terms

    Args:
        neg_t (float): -t
        R (numpy array): empirical density

    Returns:
        _type_: _description_
    """
    if any(eff_t > 200):
        return R
    logV = np.log(V)

    logx = np.exp(eff_t) * R + eff_t + logV

    usethis = logx > 50
    out = np.zeros(len(R))
    out[~usethis] = np.real(lambertw(np.exp( logx[~usethis])))

    logx = logx[usethis]
    loglogx = np.log(logx)
    out[usethis] = logx - loglogx + loglogx / logx + (loglogx - 2) * loglogx / (2*logx**2)

    phi = out - R * np.exp(eff_t)
    return phi

def obj(t, R, n_samples, L1_deviation, mu, logD, V):
    """Objective function for |phi_f - mu|

    Args:
        neg_t (float): t parameter to fit
        R (numpy array): empirical density
        L1_deviation (float): desired distance
        mu (numpy array): defaults to empirical density
        t_shift (numpy array): if diagonals are not identical, this
        term rescales them to 1 and then finds an exact solution

    Returns:
        _type_: _description_
    """
    t = float(t)
    phi = fx_app(t - logD, R, V * n_samples)
    Q = np.exp(-phi) * V
    Q /= Q.sum()

    deviation = Q*n_samples - mu
    residual = L1_deviation - np.sum(np.abs(deviation))
    out = residual
    return out**2

def find_tf(R, L1_deviation, D, n_samples, mu=None, neg_t0=0, V=1):
    """find upper bound of t sampling points

    Args:
        R (numpy array): empirical density
        L1_deviation (float): phi density should be this far away from emprical density
        l_scale (array): Diagonal of smoothing penalty
        mu (numpy array, optional): what phi should deviate from. Assumed to be R if not set.
        Defaults to None.
        neg_t0 (float, optional): Starting guess of what t_f (highest t) should be. 
        Defaults to 0.

    Returns:
        float: highest t value 
    """
    if mu is None:
        mu = R
    logD = np.log(D)
    lstar = minimize(lambda x:obj(x, R, n_samples, L1_deviation, mu, logD, V),
        x0=neg_t0, method='nelder-mead')['x']
    return float(lstar)
