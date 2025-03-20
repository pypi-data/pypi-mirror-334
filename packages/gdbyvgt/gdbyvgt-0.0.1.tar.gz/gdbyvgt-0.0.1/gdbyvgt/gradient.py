import numpy as np

def compute_gradient(x, y, w, b):
    """
    Compute Gradient
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
