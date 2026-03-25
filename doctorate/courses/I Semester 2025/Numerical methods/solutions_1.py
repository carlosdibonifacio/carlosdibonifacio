import numpy as np
import scipy as opt
import matplotlib.pyplot as plt
import scipy.linalg as linalg

# Exercise 1 - The SIR model.

#1.a Implement the SIR model using the explicit Euler method.
def ds(t,S,I,r):
    return - r * S * I

def di(t,S,I,r,a):
    return r * S * I - a * I

def dr(t,I,a):
    return a * I

def euler_explicit(ds, di, dr, t, dt, params_SIR, initial):
    
    S = np.zeros(len(t))
    I = np.zeros(len(t))
    R = np.zeros(len(t))

    S[0], I[0], R[0] = initial

    for i in range(1,len(t)):
        S[i] = S[i-1] + dt * ds(t[i-1], S[i-1], I[i-1],params_SIR[0])
        I[i] = I[i-1] + dt * di(t[i-1], S[i-1], I[i-1], params_SIR[0], params_SIR[1])
        R[i] = R[i-1] + dt * dr(t[i-1], I[i-1], params_SIR[1])
    return S,I,R


params_SIR = (0.00218, 0.44)
initial = (1000, 1, 0)

t = np.linspace(0, 14, 50)
dt = t[1] - t[0]

S,I,R = euler_explicit(ds, di,dr , t, dt, params_SIR, initial)

plt.plot(t, S, label='Susceptible')
plt.plot(t, I, label='Infected')
plt.plot(t, R, label='Recovered')
plt.title('SIR Model using Explicit Euler Method')
plt.legend()
plt.show()

#1.b Now checkt that for each t the population is constant, i.e. S(t)+I(t)+R(t)=S(0)+I(0)+R(0).




########################################################################################
# Finite differences methods
########################################################################################

# Exercise 1.a - computing the matrix A 

def compute_matrix_A(a,b,N):
    A_1 = np.zeros((N-1,N-1))
    # Main diagonal, upper diagonal and lower diagonal
    np.fill_diagonal(A_1,2)
    np.fill_diagonal(A_1[:,1:],-1)        
    np.fill_diagonal(A_1[1:,:],-1)  
    # Scalar      
    Δ = ((b-a)/N)**2
    return  Δ * A_1

# Exercise 1.b - approximating the PDE

"""
We have to solve the linear system AU = B for some initial and terminal values
We have the function to obtain A, 
"""

def f(x):
    return (2 * np.pi)**2 * np.sin(2 * np.pi * x)


def grid(a,b,N):
    x = np.zeros(N)
    for i in range(0,N):
        x[i] = a + i * ( (b-a/N) )
    return x 

def approximate(compute_matrix_A,f, N, a,b):
    """
    A is the matrix
    U is the vector with the approximated functions u(x)
    B is the approximated function f(x)
    """ 

    x = grid(a,b,N-1)
    B = f(x)
    A = compute_matrix_A(a,b,N)

    # first solver lu_factor
    """
    
    """
    lu, piv = linalg.lu_factor(A)
    U_1 = linalg.lu_solve((lu, piv), B)

    #second solver
    U_2 = linalg.lu_factor(A, B)
    """
    
    """
    # third solver using Cholesky decomposition
    L = np.linalg.cholesky(A)
    y = np.linalg.solve(L, B)
    U_3 = np.linalg.solve(L.T, y)

    # last and the easier one
    U_4 = np.linalg.solve(A,B)

    return U_1, U_2, U_3, U_4, x


N = 50
a=0
b=1

U_1, U_2, U_3, U_4, x = approximate(compute_matrix_A, f, N, a,b)

plt.plot(x,U_1)
plt.plot(x,U_2)
plt.show()