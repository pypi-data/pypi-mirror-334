
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import lstsq


def IncPoly(N, af, ab, W, p_max, p_min, B, n):
    """
    Calculate da/dN using the Incremental Quadratic Regression Method.
    
    Parameters:
    N : numpy array
        Cycle numbers corresponding to crack lengths
    af, ab : numpy arrays
        Forward and backward crack length measurements
    W, p_max, p_min, B : float
        Specimen width, max/min load, and thickness
    n : int
        Number of neighboring points for regression
    
    Returns:
    dadN : numpy array
        Incremental crack growth rate values
    dK : numpy array
        Stress intensity factor range values
    """
    dadN = []
    dK = []
    
    for i in range(n, len(N) - n):
        N_range = N[i - n:i + n + 1]
        a_range = (af[i - n:i + n + 1] + ab[i - n:i + n + 1]) / 2  # Average crack length

        C1 = 0.5 * (N[i - n] + N[i + n])
        C2 = 0.5 * (N[i + n] - N[i - n])
        
        X = np.vstack([
            np.ones(len(N_range)), 
            (N_range - C1) / C2, 
            ((N_range - C1) / C2) ** 2
        ]).T
        

        b, _, _, _ = lstsq(X, a_range)
        b0, b1, b2 = b
        

        da_dN = (b1 / C2) + (2 * b2 * (N[i] - C1) / (C2 ** 2))
        dadN.append(da_dN)

        alpha = a_range[n] / W
        dP = p_max - p_min
        dK_value = ((((dP / (B * np.sqrt(W))) * ((2 + alpha)))) /
                    ((1 - alpha) ** (3 / 2))) * (0.886 + 4.64 * alpha - 
                    13.32 * alpha ** 2 + 14.72 * alpha ** 3 - 5.6 * alpha ** 4)
        dK.append(dK_value)


        if 0.25 <= alpha <= 0.4 and da_dN * N[i] > 0.04 * W:
            print(f"Error: da exceeds limit at N={N[i]}")
            return None, None
        elif 0.4 < alpha <= 0.6 and da_dN * N[i] > 0.02 * W:
            print(f"Error: da exceeds limit at N={N[i]}")
            return None, None
        elif alpha > 0.6 and da_dN * N[i] > 0.01 * W:
            print(f"Error: da exceeds limit at N={N[i]}")
            return None, None

    return np.array(dadN), np.array(dK)

























# import numpy as np
# import matplotlib.pyplot as plt

# def Secant(N, af, ab, W, p_max, p_min, B):
#     dP = p_max - p_min  # Load range

#     # Compute average crack length
#     a_ave = (af + ab) / 2  

#     # Compute da/dN using the secant method correctly
#     da = np.diff(a_ave)  # Change in average crack size
#     dN = np.diff(N)  # Change in cycles
#     dadN = da / dN  # Crack growth rate

#     # Ensure da/dN is increasing
#     if np.any(np.diff(dadN) < 0):
#         print("Warning: da/dN is not strictly increasing!")

#     # Compute alpha and dK
#     alpha = a_ave[:-1] / W  # Exclude last value to match da/dN length
#     dK = ((((dP / (B * np.sqrt(W))) * ((2 + alpha)))) /
#           ((1 - alpha) ** (3 / 2))) * (0.886 + 4.64 * alpha - 
#           13.32 * alpha ** 2 + 14.72 * alpha ** 3 - 5.6 * alpha ** 4)

#     return dadN, dK, a_ave

# # Generate 100 data points
# N = np.linspace(500000, 600000, 10)  # 100 cycle values
# a_values = 2 + 0.0000000001 * (N - 500000)**3  # Cubic growth for crack size

# af = a_values  # Front crack length
# ab = a_values  # Back crack length (same as af)

# W = 50  # mm (Width)
# p_max = 4000  # N (Maximum load)
# p_min = 400  # N (Minimum load)
# B = 5  # mm (Thickness)

# # Compute da/dN and dK
# dadN, dK, a_ave = Secant(N, af, ab, W, p_max, p_min, B)

# # Plot results
# plt.figure()
# plt.plot(dK,dadN, color = "red")




# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.linalg import lstsq

# def incremental_dadn(N, a, n=2):
#     """
#     Calculate da/dN using the Incremental Quadratic Regression Method.
    
#     Parameters:
#     N : numpy array
#         Cycle numbers corresponding to crack lengths
#     a : numpy array
#         Crack length measurements
#     n : int
#         Number of neighboring points to use for regression
    
#     Returns:
#     dadN : numpy array
#         Incremental crack growth rate values
#     N_mid : numpy array
#         Midpoint cycle values for plotting da/dN
#     """
#     dadN = []
#     N_mid = []
    
#     for i in range(n, len(N) - n):
#         N_range = N[i - n:i + n + 1]  # select the range of neighboring points
#         a_range = a[i - n:i + n + 1]  # select the corresponding crack lengths for a_range

        
#         # Normalize N values
#         C1 = 0.5 * (N[i - n] + N[i + n])
#         C2 = 0.5 * (N[i + n] - N[i - n])
        
#         X = np.vstack([
#             np.ones(len(N_range)), 
#             (N_range - C1) / C2, 
#             ((N_range - C1) / C2) ** 2
#         ]).T
        
#         # Solve for b0, b1, b2 using least squares
#         b, _, _, _ = lstsq(X, a_range)
#         b0, b1, b2 = b
        
#         # Compute crack growth rate at N[i]
#         da_dN = (b1 / C2) + (2 * b2 * (N[i] - C1) / (C2 ** 2))
#         dadN.append(da_dN)
#         N_mid.append(N[i])
    
#     return np.array(dadN), np.array(N_mid)

# # Example data (replace with experimental data)

# #a_values = np.array([2.0, 2.2, 2.6, 3.1, 3.7, 4.4, 5.2, 6.1, 7.1, 8.2])  # Crack lengths in mm
# a = a_values

# # Compute da/dN using quadratic regression method
# dadN, N_mid = incremental_dadn(N, a, n=5)

# # Plot results
# plt.plot(dK,dadN, color = "blue")