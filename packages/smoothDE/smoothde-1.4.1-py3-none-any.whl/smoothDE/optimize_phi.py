"""Rhys M. Adams 24.11.09"""
# ignore after this line
import numpy as np
from sksparse.cholmod import cholesky, CholmodNotPositiveDefiniteError
from scipy.sparse import diags
from scipy.sparse.linalg import lsqr

def OJ(phi, beta, nodes, R, Delta, n_samples, phi0):
    """Objective and Jacobian

    Args:
        phi (numpy array): params to fit
        beta (float): function of smoothing penalty
        nodes (numpy array): weight of each grid point
        R (numpy array): empirical density
        Delta (sparse array): smoothing penalty matrix
        n_samples (int): number of samples
        phi0 (numpy array): don't apply smoothing penalty to this part of phi

    Yields:
        float: objective
        numpy array: Jacobian
    """
    phi = np.clip(phi, a_min=None, a_max=100)
    if phi0 is None:
        Q = np.exp(-phi)
    else:
        Q = np.exp(-phi - phi0)
    Q = Q*nodes
    Z = Q.sum()
    Q /= Z
    nQ = n_samples * Q / nodes
    del Q
    phi = phi + np.log(Z)
    myf = R.dot(phi)
    Delta_phi = Delta.dot(phi)
    d_penalty = 0.5 * (phi * nodes).T.dot(Delta_phi)
    out1 = myf + d_penalty * beta
    yield out1
    try:
        factor = cholesky(Delta * beta + diags(nQ, 0))
        out2 = factor(Delta_phi  * beta / nodes + R / nodes - nQ)
    except CholmodNotPositiveDefiniteError:
        #print('could not invert, using scipy sparse library')
        out2 = lsqr(Delta * beta + diags(nQ, 0), Delta_phi  * beta / nodes + R / nodes - nQ)[0]
    yield out2

def optimize_phi(phi0,
        beta, nodes,
        R, Delta,
        n_samples,
        no_delta_penalty,
        tol=1e-8, n_iter=100, step_size=1.0, step_size_tol=1e-12):
    """Get Newton's method solution for phi

    Args:
        phi0 (numpy array): initial guess
        beta (float): function of smoothing penalty
        nodes (numpy array): weight of each point
        R (numpy array): empirical density
        Delta (sparse array): smoothing penalty matrix
        n_samples (int): number of samples
        no_delta_penalty (numpy array): don't apply 
        smoothing penalty to this part of phi
        tol (float, optional): new objective needs to be
        this much lower than the old objective to keep
        optimizing. Defaults to 1e-8.
        n_iter (int, optional): number of iterations to try.
        Defaults to 100.
        step_size (float, optional): starting coefficient for
        iterative step. Defaults to 1.0.
        step_size_tol (float, optional): if step_size is
        smaller than this, stop optimizing. Defaults to 1e-12.

    Returns:
        numpy array: solution for phi
    """
    phi = phi0
    keep_optimize = True
    for ii in range(n_iter):
        if (not keep_optimize) or (step_size<step_size_tol):
            break
        keep_optimize = False
        myf = OJ(phi, beta, nodes, R, Delta, n_samples, no_delta_penalty)
        old_O, dx = next(myf), next(myf)
        while step_size > step_size_tol:
            step_size = np.min([1, step_size * 1.5])
            phi_1 = phi - dx * step_size
            myf = OJ(phi_1, beta, nodes, R, Delta, n_samples, no_delta_penalty)
            if next(myf) < (old_O - tol):
                phi = phi_1
                phi -= phi.min()

                keep_optimize = True
                break
            step_size /= 8
    return phi
