# fracmechpy: Fracture Mechanics

## Overview
fracmechpy is a Python package that calculates the fatigue crack growth rate (da/dN) and the stress intensity factor range (ΔK) for Compact Tension (CT) specimens with the Secant method based on ASTM E647.

## Features
- Computes fatigue crack growth rate (da/dN)
- Computes stress intensity factor range (ΔK)
- Implements ASTM E647 standard
- Includes error handling for ASTM E647 validity limits
- **Newly added**: Incremental Polynomial Regression (IncPoly) method for crack growth rate calculation.

## Installation
### Installing from PyPI (Future Deployment)
If fracmechpy is available on PyPI, you can install it using:
```bash
pip install fracmechpy
```

### Installing from Source
To install the package manually:
1. Clone the repository:
   ```bash
   git clone https://github.com/dhaselib/fracmechpy.git
   ```
2. Navigate to the directory:
   ```bash
   cd fracmechpy
   ```
3. Install using pip:
   ```bash
   pip install .
   ```

Ensure you have NumPy installed using:
```bash
pip install numpy
```

## Functions

### `Secant(N, af, ab, W, p_max, p_min, B)`
This function calculates the fatigue crack growth rate (da/dN) and the stress intensity factor range (ΔK) for a CT specimen.

#### Parameters:
- `N` (numpy array): Number of cycles
- `af` (numpy array): Crack length at the front face of the specimen
- `ab` (numpy array): Crack length at the back face of the specimen
- `W` (float): Width of the specimen
- `p_max` (float): Maximum applied load
- `p_min` (float): Minimum applied load
- `B` (float): Thickness of the specimen

#### Returns:
- `dadN` (numpy array): Fatigue crack growth rate (da/dN)
- `dK` (numpy array): Stress intensity factor range (ΔK)

### `IncPoly(N, af, ab, W, p_max, p_min, B, n)`
This function calculates the crack growth rate (da/dN) using the Incremental Polynomial Regression method for a CT specimen.

#### Parameters:
- `N` (numpy array): Number of cycles
- `af` (numpy array): Crack length at the front face of the specimen
- `ab` (numpy array): Crack length at the back face of the specimen
- `W` (float): Width of the specimen
- `p_max` (float): Maximum applied load
- `p_min` (float): Minimum applied load
- `B` (float): Thickness of the specimen
- `n` (int): Number of neighboring points for regression

#### Returns:
- `dadN` (numpy array): Incremental crack growth rate (da/dN)
- `dK` (numpy array): Stress intensity factor range (ΔK)

#### Limitations on Choosing the Value of `n`
- **Dataset Size**: Ensure that `n` is smaller than the length of the dataset. If `n` exceeds the available data points, the method may fail to run, leading to errors or empty results.
  
- **Accuracy vs. Data Availability**: A larger `n` improves regression accuracy but may result in fewer available data points, especially in smaller datasets. Conversely, smaller `n` might yield less stable results but can handle more data points.

- **Edge Effects**: For data points near the beginning or end of the dataset, the number of available neighbors may be limited. If `n` is too large, it may not be possible to compute regression near the edges.

- **Performance Considerations**: Large values of `n` can increase memory usage and slow down performance, especially for larger datasets. Start with smaller values of `n` and increase it as needed.


## Example Usage
```python
import numpy as np
from fracmechpy import Secant, IncPoly

# Sample input data
N = np.array([70000, 90000, 100000, 110000,120000,130000])
af = np.array([1.90, 3.09, 3.78, 4.45, 6.19, 6.84])
ab = np.array([0.89, 2.07, 2.81, 3.53, 5.09, 6.21])
W = 50  # Width in (mm)
p_max = 4000  # Maximum load in (N)
p_min = 400  # Minimum load in (N)
B = 5  # Thickness in (mm)
n = 1  # Number of neighboring points for regression

# Compute crack growth rate and stress intensity factor range using Secant method
dadN_secant, dK_secant = Secant(N, af, ab, W, p_max, p_min, B)
print("Secant Method - da/dN:", dadN_secant)
print("Secant Method - dK:", dK_secant)

# Compute crack growth rate and stress intensity factor range using IncPoly method
dadN_incpoly, dK_incpoly = IncPoly(N, af, ab, W, p_max, p_min, B, n)
print("IncPoly Method - da/dN:", dadN_incpoly)
print("IncPoly Method - dK:", dK_incpoly)

```

## Error Handling
The function enforces ASTM E647 validity limits for crack growth increments (da). If the increment exceeds the standard-defined limits based on α = aᵥₑ/W , the function prints an error message and returns `None`.

## License
This package is distributed under the MIT License.

## Contact
For questions or contributions, please reach out to the author at dhaselib@gmail.com.
```

### Key Updates:
1. **New Section for `IncPoly`**: Added a description of the `IncPoly` method in the functions section.
2. **Updated Example Usage**: Added an example that demonstrates the usage of both `Secant` and `IncPoly` functions.
3. **Feature Addition**: Mentioned the addition of the `IncPoly` method in the Features section.
4. **Limitations of `n`**: Provided detailed information about the limitations on choosing the value of `n`, including dataset size, accuracy vs. data availability, edge effects, and performance considerations.

This should now fully reflect the functionality of the `IncPoly` method and the limitations for the `n` parameter.
