import numpy as np

def compute_cost(x, y, w, b): 
    """
    Computes the cost function
    """
    # m is the number of training examples
    m = x.shape[0] 
    # cost_sum is used to store the total cost
    cost_sum = 0 
    for i in range(m): 
        f_wb = w * x[i] + b   
        cost = (f_wb - y[i]) ** 2  
        cost_sum = cost_sum + cost  
    total_cost = (1 / (2 * m)) * cost_sum  

    return total_cost

def compute_cost_multi(x, y, w, b): 
    """
    Computes the cost function
    The input x is a matrix (or 2-D array) with m rows and n columns
    The input w is a vector (or 1-D array) with n elements
    """
    # m is the number of training examples
    m = x.shape[0]
    cost = 0. 
    for i in range(m): 
        f_wb = np.dot(x[i], w) + b
        cost += (f_wb - y[i]) ** 2  
    total_cost = (1 / (2 * m)) * cost
    return total_cost