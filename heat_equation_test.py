import py.test
from heat_equation_numpy import heat_numpy
from numpy import *
import matplotlib.pyplot
import py.test

# Oystein Kapperud, 2015

def make_u_f(n,m, nu):
    """
    Initialize the f and analytic_u arrays to be used in the test.
    """
    f = zeros((m,n))
    analytic_u = zeros((m,n))
    for i in range(len(f)):
        for j in range(len(f[i])):
            f[i][j] = nu*((2*pi/(n-1))**2 + (2*pi/(m-1))**2)*sin(2*pi/(m-1)*i)*sin(2*pi/(n-1)*j)
            analytic_u[i][j] = sin(2*pi/(m-1)*i)*sin(2*pi/(n-1)*j)
    return analytic_u, f
    
    
    
def test_heat_equation():
    """
    Tests that the numpy solution is similar to the analytic solution (within the error margin specified in the assignment text)
    and that the error decreases as the size of the rectangle increases.
    """
    t0=0
    t1=1000
    dt=0.1
    nu=1
    n = 50
    m = 100
    analytic_u1, f1 = make_u_f(n,m, nu)
    start_u1= zeros((m,n))
    u1 = heat_numpy(t0, t1, dt, nu, start_u=start_u1, f=f1)
    # Tests whether the largest difference between two corresponding cells in the numpy and analytic solutions is smaller than 0.0012
    err1=(abs(u1-analytic_u1)).max()
    print err1
    assert err1<0.0012
    
    
    # Do the same with rectangles twice the size of those in the previous run
    n = 100
    m = 200 
    analytic_u2, f2 = make_u_f(n,m, nu)
    start_u2= zeros((m,n))
    t1=t1*2
    u2 = heat_numpy(t0, t1, dt, nu, start_u=start_u2, f=f2)
    err2 =(abs(u2-analytic_u2)).max()
    print err2
    # Tests whether the error is smaller with larger rectangles
    assert err2<err1
    
if __name__ == "__main__":
    """
    To run the tests, run this script like an ordinary python script from the command line.
    """
    py.test.cmdline.main(["-v", 'heat_equation_test.py'])

    
