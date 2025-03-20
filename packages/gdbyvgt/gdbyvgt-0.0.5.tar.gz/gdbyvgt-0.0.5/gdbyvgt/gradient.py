import numpy as np

def compute_gradient(x, y, w, b):
    """
    Compute Gradient
    The input x is a vector (or 1-D array) with m elements
    """
    m = x.shape[0]    
    dj_dw = 0
    dj_db = 0
    for i in range(m):  
        f_wb = w * x[i] + b 
        dj_dw_i = (f_wb - y[i]) * x[i] 
        dj_db_i = f_wb - y[i] 
        dj_dw += dj_dw_i 
        dj_db += dj_db_i
    dj_dw /= m 
    dj_db /= m 
    return dj_dw, dj_db

def gradient_descent(x, y, w_init, b_init, alpha, num_iters):
    """
    Implement Gradient Descent
    """
    w = w_init
    b = b_init
    for i in range(num_iters):
        dj_dw, dj_db = compute_gradient(x, y, w, b)
        w -= alpha * dj_dw
        b -= alpha * dj_db
    return w, b

def compute_gradient_multi(x, y, w, b):
    """
    Compute Gradient for multiple variables
    The input x is a matrix (or 2-D array) with m rows and n columns
    The input w is a vector (or 1-D array) with n elements
    """
    # m is the number of training examples, n is the number of features
    m = x.shape[0]
    n = x.shape[1]
    # dj_dw is a vector (or 1-D array) with n elements, dj_dw has the type of float64
    dj_dw = np.zeros((n,))
    dj_db = 0.
    for i in range(m):
        err = np.dot(x[i], w) - y[i]
        # calculate the gradient for each feature
        for j in range(n):
            dj_dw[j] += err * x[i, j]
        dj_db += err
    dj_dw /= m
    dj_db /= m
    return dj_dw, dj_db

def gradient_descent_multi(x, y, w_init, b_init, alpha, num_iters):
    """
    Implement Gradient Descent for multiple variables
    The input x is a matrix (or 2-D array) with m rows and n columns
    The input w_init is a vector (or 1-D array) with n elements
    """
    w = w_init.astype(np.float64)
    b = float(b_init)
    for i in range(num_iters):
        dj_dw, dj_db = compute_gradient_multi(x, y, w, b)
        dj_dw = dj_dw.astype(np.float64)
        dj_db = float(dj_db)
        w -= alpha * dj_dw
        b -= alpha * dj_db
    return w, b
