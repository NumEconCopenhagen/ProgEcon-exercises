import numpy as np

def expenditure_matrix():
    """Construct E[i,j] = q[i]*p[j] using broadcasting (no loop)."""

    p = np.array([1,2,5]) # prices (3,)
    q = np.array([10,20,30,40]) # quantities (4,)

    # q[:,None] has shape (4,1) and p[None,:] has shape (1,3)
    # broadcasting stretches them to (4,3)
    E = q[:,None]*p[None,:]

    print(E)
    print('shape:',E.shape)
    return E
