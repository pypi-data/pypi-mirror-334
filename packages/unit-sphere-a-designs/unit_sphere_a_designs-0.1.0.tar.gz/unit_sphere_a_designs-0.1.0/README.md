# Unit Sphere A Designs

A package for computing A Designs over the unit sphere.

## Installation

You can install the package using pip:

```bash
pip install .
```

## Usage

Here is an example of how to use the package:

```python
from unit_sphere_a_designs.local import local_search
import numpy as np

# Example Runs
d = 40
k = 2 * d + 1

# Run local search with a random staring solution
S_LS = local_search(d, k)
alg_val = np.trace(np.linalg.inv(S_LS @ S_LS.T))
print(f'Finished with a value of {float(alg_val):.5f}')


# Run local search with a fixed starting solution. Fix the first and third vectors so they are not replaced by the algortihm.
S_random = np.random.normal(size=(d, k))
S_random /= np.linalg.norm(S_random, axis=0, keepdims=True)
rand_val = np.trace(np.linalg.inv(S_random @ S_random.T))

print(f'Random solution has a value of {float(rand_val):.5f}')

S_LS_random_start = local_search(d, k, S = S_random, fixed_points = [0, 1, 2])
alg_val_rand_start = np.trace(np.linalg.inv(S_LS_random_start @ S_LS_random_start.T))

print(f'Finished with a value of {float(alg_val_rand_start):.5f}')


```

## Running Tests

You can run the tests using pytest:

```bash
pytest tests/
```
