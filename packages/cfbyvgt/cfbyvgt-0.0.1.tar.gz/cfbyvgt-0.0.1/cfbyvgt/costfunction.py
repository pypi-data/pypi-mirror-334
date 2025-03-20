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