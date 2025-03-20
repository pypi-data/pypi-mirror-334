import numpy as np
from numpy.typing import NDArray


def pairs_mat(S, pairs):
    newMat = np.zeros((len(pairs), S.shape[1]))

    for col in range(newMat.shape[1]):
        for i, p in enumerate(pairs):
            newMat[i, col] = S[p[0], col] * S[p[1], col]

    return np.vstack([S, newMat])


def get_pairs_idx_map(d, plus_one = 1):
    idx_map = {}
    
    idx = d
    for i in range(plus_one, d + plus_one):
        for j in range(i + 1, d + plus_one):
            idx_map[i, j] = idx 
            idx += 1
    return idx_map


def random_start(d: int, k: int) ->  NDArray[np.float64]:
    """
    Create a uniformly at random d x k matrix with unit norm columns.s

    Args:
        d (int): Dimension of the design points
        k (int) : Number of points in the design
        
    Returns:
       NDArray[np.float64]: The random matrix
    """
    S = np.random.normal(size=(d, k))
    S /= np.linalg.norm(S, axis=0, keepdims=True)
    return S

def symmetric_factorization(A: NDArray[np.float64]):
    """
    Factorizes a symmetric matrix A into PDP^T where:
    - P is an orthogonal matrix (P @ P.T = I),
    - D is a diagonal matrix (containing the eigenvalues of A).
    
    Args:
        A (numpy.ndarray): Symmetric matrix to factorize.
        
    Returns:
        P (numpy.ndarray): Orthogonal matrix (eigenvectors of A).
        D (numpy.ndarray): array of (eigenvalues of A).
    """
    # Ensure the matrix is symmetric
    # if not np.allclose(A, A.T):
    #     raise ValueError("Input matrix A must be symmetric.")
    
    # Perform eigenvalue decomposition
    eigenvalues, eigenvectors = np.linalg.eigh(A)
    
    # Create the diagonal matrix D
    #D = np.diag(eigenvalues)
    
    # P is the matrix of eigenvectors
    P = eigenvectors
    
    return P, eigenvalues









