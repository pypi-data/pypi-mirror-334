"""Rhys M. Adams 24.11.10"""
# ignore after this line
import numpy as np

def robust_dot(a,b, sumB):
    """dot product that works if a is an integer

    Args:
        a (int or numpy array): left dot product term
        b (float or numpy array): right dot product term
        sumB (_type_): sum of b

    Returns:
        float: dot product
    """
    if isinstance(a,int):
        return a * sumB
    return a.dot(b)

def OJ(coefficients, X, moments, poly_fun, dxs, dx2s, max_exp=50):
    """Objective and Jacobian to fit max entropy

    Args:
        coefficients (numpy array): terms to fit
        X (numpy array): grid of points
        moments (numpy array): moments of X
        poly_fun (function): polynomial function
        dxs (list): derivatives of polynomial function
        dx2s (list of lists): 2nd order derivatives of polynomial function
        max_exp (float, optional): rescale expontial terms to this value
        so no overflow values. Defaults to 50.

    Returns:
        float: objective
        numpy array: Jacobian
    """
    exponent = -poly_fun(X, coefficients)
    max_exponent = exponent.max()
    quasiQ = np.exp(exponent-max_exponent+max_exp)
    l0 = np.sum(quasiQ)
    obj = moments.dot(coefficients) + l0 / np.exp(- max_exponent+max_exp)
    J = moments - np.array([robust_dot(np.prod(X**dx, axis=1), quasiQ, l0) / np.exp(- max_exponent+max_exp)
                               for dx in dxs])
    return obj, J

def H(coefficients, X, moments, poly_fun, dxs, dx2s, max_exp=50):
    """Hessian of objective function

    Args:
        coefficients (numpy array): params to fit
        X (numpy array): grid of points
        moments (numpy array): moments of X
        poly_fun (function): polynomial function
        dxs (list): derivatives of polynomial function
        dx2s (list of lists): 2nd order derivatives of polynomial function
        max_exp (float, optional): rescale expontial terms to this value
        so no overflow values. Defaults to 50.

    Returns:
        numpy array: Hessian
    """
    exponent = -poly_fun(X, coefficients)
    max_exponent = exponent.max()
    quasiQ = np.exp(exponent-max_exponent+max_exp)
    l0 = np.sum(quasiQ)
    out = np.array([[robust_dot(np.prod(X**dx2iijj, axis=1),quasiQ, l0) / np.exp(- max_exponent+max_exp)
          for dx2iijj in dx2ii] for dx2ii in dx2s])
    return out
