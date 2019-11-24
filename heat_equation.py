import matplotlib.pyplot
from numpy import ndarray
from copy import deepcopy, copy
import sys
#import matplotlib.image
#import matplotlib.cm as cm

def heat(t0, t1, dt, nu, timer=False, dim=None, verbose=False, start_u=None, f=None):
    """
    A function that simulates the dissipation of heat using pure python.
    
    Arguments: 
    t0 (start time, float)
    t1 (end time, float)
    dt (time step value, float)
    nu (thermal diffusivity, float)
    timer (turns on timer if True, boolean, optional)
    dim (the dimensions of the arrays, list, optional)
    verbose (turns on verbose mode if True, boolean, optional)
    start_u (the temperature map at the start of the simulation, list/numpy array (in the latter case it will be converted to a list), optional)
    f (heat source, list/numpy array (in the latter case it will be converted to a list), optional)
    
    Returns:
    u_new (Updated heat map after simulation, list)
    """
    if verbose:
        print "verbose mode activated!"
    if dim is None:
        if start_u is not None and f is not None: # if both u and f are passed
            if type(start_u) == ndarray:
                u=start_u.tolist() # converts input u to python list if the user tries to pass a numpy array (as will happen e.g. if the user use the input_file argument in ui.py)
            else:
                u = start_u
            if type(f) == ndarray:
                f=f.tolist()
            if len(f) != len(u) or len(f[0]) != len(u[0]):
                print 'Error! u and f must have the same dimensions!'
                sys.exit(1)
        else:
            if start_u is None and f is None:   # if neither dimensions, u or f is specified, u and f is set by default to a 100 x 50 rectangle with all values set to zero and one, respectively
                u = [[0 for x in range(50)] for x in range(100)]
                f = [[1 for x in range(50)] for x in range(100)]
            elif start_u is None: # if only f is given, u is set to an array of the same dimensions as f with all values set to zero
                if type(f)==ndarray:
                    f=f.tolist()
                u=[[0 for x in range(len(f[0]))] for x in range(len(f))] 
            elif f is None: # if only u is given, f is set to an array of the same dimensions as u with all values set to one
                if type(start_u)==ndarray:
                    u=start_u.tolist()
                else:
                    u=start_u
                f=[[1 for x in range(len(u[0]))] for x in range(len(u))] 
    else: # if dimensions are specified, u and f are set to rectangles with dimensions dim[0] x dim[1] with all values set to zero and one, respectively.
        u = [[0 for x in range(dim[1])] for x in range(dim[0])]
        f = [[1 for x in range(dim[1])] for x in range(dim[0])]
    t=t0
    if timer: # start timer if promted by the user
        from timeit import default_timer as time
        start_time = time()
    u_new = deepcopy(u)
    while t<t1: # a triple loop over time values, row indexes and collumn indexes  
        for i in range(1, len(u)-1):
            for j in range(1, len(u[i])-1):
                u_new[i][j] = u[i][j] + dt*(nu*u[i-1][j] + nu*u[i][j-1] - 4*nu*u[i][j] + nu*u[i][j+1] + nu*u[i+1][j] + f[i][j])
        if verbose:
            print "Now processing time step", t
        u=deepcopy(u_new)
        t=t+dt
    if timer:
        end_time = time() # end timer
        print 'loop executed in {t:.3f} seconds'.format(t=end_time-start_time)
    return u_new
        
        
if __name__ == "__main__":
    """
    Example of usage.
    """
    t0=0.0
    t1=1000
    dt=0.1
    nu=1
    u = heat(t0, t1, dt, nu)
    matplotlib.pyplot.imshow(u, cmap= matplotlib.pyplot.get_cmap("gray"), interpolation="nearest")
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.show()

        
        