import numpy as np
import time
from unit_sphere_a_designs.tools import symmetric_factorization, pairs_mat, random_start
from numpy.typing import NDArray
from typing import Optional, Tuple, List
#import matplotlib.pyplot as plt




def local_move(S : NDArray[np.float64], curr_obj: float, keep: List[bool] ) -> float:
    
    """
    Updates a given solution by replacing a desin points. Considers replacing each of the k design point in the solution with a point that gives the best improvement in the objective value. 
    Chooses the best replacement among these k choices. The function modifies the given matrix S.

    Args:
        S (NDArray[np.float64]): The current solution.
        curr_obj (int): The objective value of the current solution.

    Returns:
        float: The new objective value after making the local move. If not improving move was found, curr_obj is returned.
    """

    eigen_time = 0

    X = S @ S.T
    
    # index of vector we will replace
    replace_idx = -1
    replace_vec = None

    best_obj = curr_obj

    for i in range(S.shape[1]):
        if keep[i]: continue

        x_i = S[:, i].reshape(-1, 1)

        X_i = X - x_i @ x_i.T
        

        # eigenvalue decombposition
        t = time.perf_counter()
        P, D = symmetric_factorization(X_i)
        eigen_time += time.perf_counter() - t


        D = 1 / D 

        
        obj_vals = (D * D) / (1 + D)


        tr_inv = D.sum()
        max_val = obj_vals.max()
        new_vec = P[:, obj_vals.argmax()]

    
        if tr_inv - max_val < best_obj - 10**(-4):
            replace_idx, replace_vec  = i, new_vec
            best_obj = tr_inv - max_val
            # uncomment below break to take first improvement
            #break 

    if replace_vec is not None:
        S[:, replace_idx] = replace_vec
    
    #all_time = time.perf_counter() - all_time
    #print(f'non binary time was {all_time=} {all_time - eigen_time} {eigen_time=}')
    return best_obj#, eigen_time


# def local_move_pairs(S : NDArray[np.float64], pairs: list[tuple[int, int]], curr_obj: float):

#     d = S.shape[0]
#     eigen_time = 0

#     S_mat = pairs_mat(S, pairs)

#     X = S_mat @ S_mat.T

#     replace_idx = -1
#     replace_vec = None

#     best_obj = curr_obj

#     for i in range(S.shape[1]):

#         x_i = S_mat[:, i].reshape(-1, 1)

#         X_i = X - x_i @ x_i.T

#         #pXi = pairs_mat(X_i, pairs)

#         inv = np.linalg.inv(X_i)
#         tr_inv = inv.diagonal().sum()

#         t = time.perf_counter()
#         #start = S[:, i].copy()
#         start = np.random.randn(d)
#         start /= np.linalg.norm(start)
#         max_val = ls_pairs(d, start, tr_inv - curr_obj, inv)
#         new_vec = start
#         #new_vec, max_val = pairs_opt(d, inv, start)
#         eigen_time += time.perf_counter() - t

        
#         if tr_inv - max_val < best_obj - 10**(-4):
#             replace_idx, replace_vec  = i, new_vec
#             best_obj = tr_inv - max_val

#             #if i > 4 and pairs is not None: break
#             if pairs is not None: break
    
#     if replace_vec is not None:
#         S[:, replace_idx] = replace_vec
    
#     return best_obj, eigen_time
        

# pairs = None
def local_search(d: int, k: int, S: Optional[NDArray[np.float64]] = None, fixed_points: Optional[List[int]] = [], iter_limit: Optional[int] = 1e18) ->  NDArray[np.float64]:

    """
    Runs the local search algortihm given a starting solution S.

    Args:
        d (int): Dimension of the design points.
        k (int) : Number of points in the design.
        S (Optional[NDArray[np.float64]], optional): Matrix where the columns are the design points. Defaults to a random starting matrix if not supplied.
        iter_limit (Optional[int], optional): A limit on the number of local moves the algortihm can make. Defaults to 10^18.
        fixed_points (Optional[List[int]], optional): A (0-indexed) list of indices for design points that should not be replaced in the local search.
        
    Returns:
        S (numpy.ndarray): Returns the final solution.
    """
    if S is None:
        S = random_start(d, k)

    # set up fixed design points for quick access
    keep = (S.shape[1]) * [False]

    for idx in fixed_points:
        keep[idx] = True

    # make a copy of input matrix so matirx supplied by user won't be modified
    S, S_input = S.copy(), S

    #vals = []
    #eigen_time = 0
    #d, k = S.shape
    #S_mat = S if pairs is None else pairs_mat(S, pairs)
    S_mat = S
    curr_obj = np.trace( np.linalg.inv( S_mat @ S_mat.T ) )

    
    #np.linalg.inv(S @ S.T).diagonal().sum()
    #print(f'{d=} {curr_obj=}')

    iters = 0
    delta = 0
    while iters < iter_limit:
        #print(f'Iteration {iters}: {float(curr_obj):.5f}')
        #vals.append(curr_obj)

        new_obj = local_move(S, curr_obj, keep) # if pairs is None else local_move_pairs(S, pairs, curr_obj)
        #, bt
        #eigen_time += bt

        #print(f'{new_obj=}')
        delta = curr_obj - new_obj
        if np.isclose( delta, 0):
            break
            
        curr_obj = new_obj
        iters += 1
    
    #return new_obj, vals, eigen_time, iters
    return S