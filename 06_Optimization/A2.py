from A1 import utility_ces

def x2_from_x1(x1,I,p1,p2):
    """Return x2 given x1 and the budget line."""
    return (I - p1*x1)/p2

def value_of_choice_ces(x1,alpha,beta,I,p1,p2):
    """Utility of choosing x1 and spending the rest of income on x2."""
    
    x2 = x2_from_x1(x1, I, p1, p2)
    return utility_ces(x1, x2, alpha, beta)
