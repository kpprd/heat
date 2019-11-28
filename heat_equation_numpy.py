import matplotlib.pyplot
from numpy import *
import sys

# Oystein Kapperud, 2015

def heat_numpy(t0, t1, dt, nu, timer=False, dim=None, verbose=False, start_u=None, f=None):
    """
    A function that simulates the dissipation of heat using numpy arrays.
    
    Arguments: 
    t0 (start time, float)
    t1 (end time, float)
    dt (time step value, float)
    nu (thermal diffusivity, float)
    timer (turns on timer if True, boolean, optional)
    dim (the dimensions of the arrays, list, optional)
    verbose (turns on verbose mode if True, boolean, optional)
    start_u (the temperature map at the start of the simulation, numpy array/list (in the latter case it will be converted to a numpy array), optional)
    f (heat source, numpy array/list (in the latter case it will be converted to a numpy array), optional)
    
    Returns:
    u (Updated heat map after simulation, numpy array)
    """
    if verbose:
        print 'Verbose mode activated!'
    if dim is None:
        if start_u is not None and f is not None: # if both u and f are passed
            u=array(start_u)
            f=array(f)
            if u.shape != f.shape:
                print 'Error! u and f must have the same dimensions!'
                sys.exit(1)
        else:
            if start_u is None and f is None:   # if neither dimensions, u or f is specified, u and f is set by default to a 100 x 50 rectangle with all values set to zero and one, respectively
                u=zeros((100,50))
                f=ones((u.shape))
            elif start_u is None:
                u=zeros(f.shape) # if only f is given, u is set to an array of the same dimensions as f with all values set to zero
            elif f is None:
                f=ones(start_u.shape) # if only u is given, f is set to an array of the same dimensions as u with all values set to one
                u=start_u
    else: # if dimensions are specified, u and f are set to rectangles with dimensions dim[0] x dim[1] with all values set to zero and one, respectively.
        u=zeros((dim[0], dim[1]))
        f=ones((dim[0], dim[1]))
    t=t0
    #print t0, t1, dt, nu, u, f, timer
    print "u:",u
    print "f:",f
    if timer:
        from timeit import default_timer as time
        start_time=time()  # starts the timer, which times the loop if prompted by the user.
    while t<t1: # loops over the time values (not to be confused with the timer!) and updates u by vectorization.
        u[1:-1, 1:-1] = u[1:-1, 1:-1] + dt*(nu*u[0:-2,1:-1] + nu*u[1:-1, 0:-2] - 4*nu*u[1:-1,1:-1] + nu*u[1:-1,2:] + nu*u[2:,1:-1] + f[1:-1,1:-1])
        if verbose:
            print "Now processing time step", t
        t=t+dt
    if timer:
        end_time=time()  # stops the timer
        print 'loop executed in {t:.3f} seconds'.format(t=end_time-start_time)
    return u

if __name__ == "__main__":
    """"
    Example of usage.
    """
    t0=0.0
    t1=1000.0
    dt=0.1
    nu=1
    verbose=True
    u=heat_numpy(t0, t1, dt, nu, verbose=verbose)
    matplotlib.pyplot.imshow(u, cmap= matplotlib.pyplot.get_cmap("gray"), interpolation="nearest")
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.show()
