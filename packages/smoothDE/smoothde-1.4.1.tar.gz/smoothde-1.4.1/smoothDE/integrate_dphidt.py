"""Rhys M. Adams 24.11.08"""
# ignore after this line
from sksparse.cholmod import cholesky, CholmodNotPositiveDefiniteError
from scipy.sparse import diags
from scipy.integrate import ode
from scipy.sparse.linalg import lsqr
import numpy as np
from smoothDE.optimize_phi import optimize_phi

FAILED_INTEGRATION = 0
SUCCESSFUL_INTEGRATION = 1
SUCCESSFUL_INTEGRATION_RECORDED = 2
NEWTONS_METHOD = 3

def make_factor(A):
    """cholesky factor of sparse matrix A

    Args:
        A (sparse matrix): some sparse matrix

    Returns:
        _type_: factored version of A
    """
    return cholesky(A)

def sparse_det(factor):
    """get determinant of factored matrix

    Args:
        factor (_type_): Cholesky factor of matrix

    Returns:
        float: log determinant
    """
    return factor.logdet()

def sparse_solve(factor, Q, R):
    """Solve sparse set of equations A x = Q-R

    Args:
        factor (_type_): factored matrix of A
        Q (numpy array): Current predicted density
        pR (numpy array): empirical density

    Returns:
        numpy array: solution, x
    """
    return factor( Q - R )

def dphidt(t, phi, R, nodes, Delta, n_samples, records, no_delta_penalty):
    """calculate dphi/dt

    Args:
        t (float): t, function of smoothing penalty
        phi (numpy array): current phi estimate
        R (numpy array): empirical density
        nodes (numpy array): weight of each point
        Delta (sparse array): smoothing penalty matrix
        n_samples (int): number of samples
        records (dict): record results
        no_delta_penalty (numpy array): don't apply smoothing penalty to
        this part of phi

    Returns:
        numpy array: dphi/dt
    """
    if no_delta_penalty is None:
        Q = np.exp(-phi)
        working_phi = phi
    else:
        working_phi = phi + no_delta_penalty
        Q = np.exp(-working_phi)
    Q = Q * nodes
    Z = (Q * nodes).sum()
    Q /= Z
    nQ = n_samples * Q / nodes
    A = Delta + diags(np.exp(t) * nQ, 0)
    max_D = Delta.max()
    try:
        factor = make_factor(A / max_D)
        solution, ld = sparse_solve(factor, nQ/max_D, R / nodes /max_D), sparse_det(factor)

    except CholmodNotPositiveDefiniteError:
        solution = lsqr(A, np.exp(t) * (nQ - R / nodes))[0]
        ld = np.nan
        #ld = np.linalg.slogdet(A)[1]

    out = solution * np.exp(t) / nodes
    if records['record']!=SUCCESSFUL_INTEGRATION_RECORDED:
        records['scan'][t] = (np.exp(-phi)/Z, ld - np.log(max_D), phi + np.log(Z),
            int(records['record']), out)
        records['record'] = SUCCESSFUL_INTEGRATION_RECORDED

    return out #/ max_D

def integrate_dphidt(phi1, ts, R, nodes, Delta, n_samples, no_delta_penalty):
    """calculate all the phi solutions for ts

    Args:
        phi1 (numpy array): starting phi guess
        ts (numpy array): sampling points
        R (numpy array ): empirical density
        nodes (numpy array): weight of each points
        Delta (sparse matrix): smoothing penalty matrix
        n_samples (int): number of empirical points
        no_delta_penalty (numpy array): don't apply smoothing
        penalty to this portion of phi

    Returns:
        dict: record of scan
    """
    records = {'record':SUCCESSFUL_INTEGRATION,'scan':{}}
    backend = 'vode'
    tol = 1e-7
    solver = ode(dphidt).set_integrator(backend,  atol=tol, rtol=tol, first_step=0.001)
    x = phi1 #/ rescale
    t_i = ts[0]
    solver.set_initial_value(x, t_i)
    solver.set_f_params(R, nodes, Delta, n_samples, records, no_delta_penalty)
    solver._integrator.iwork[2] = -1
    for t_n in ts[1:]:
        #print(t_n, end='\r')
        if records['record'] == SUCCESSFUL_INTEGRATION_RECORDED:
            records['record'] = SUCCESSFUL_INTEGRATION

        while (solver.t < t_n) and (records['record']!=FAILED_INTEGRATION):
            x = solver.integrate(t_n)
            if not solver.get_return_code() == 2:
                records['record'] = FAILED_INTEGRATION

        if records['record'] == FAILED_INTEGRATION:
            print("integrator failed, switching to Newton's method")
            beta = np.exp(-t_n) * n_samples
            phi = optimize_phi(np.zeros(len(x)), beta, nodes, R, Delta, n_samples, no_delta_penalty,
                tol=1e-8, n_iter=100)
            records['record'] = NEWTONS_METHOD
            solver.set_initial_value(phi, t_n)

    if not solver.get_return_code() == 2:
        records['record'] = FAILED_INTEGRATION

    dphidt(t_n, x, R, nodes, Delta, n_samples, records, no_delta_penalty)
    return records['scan']
