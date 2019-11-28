from numpy import *
from scipy import weave
import matplotlib.pyplot
import sys

# Oystein Kapperud, 2015

def heat_weave(t0, t1, dt, nu, timer=False, dim=None, verbose=False, start_u=None, f=None):
    """
    A function that simulates the dissipation of heat using weave.
    
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
    if dim is None: # if dimemsions are not specified
        if start_u is not None and f is not None: # if both u and f are passed
            u=array(start_u)
            o=u.copy() # o for "old". This array will be used to store the result from the previous time step inside the weave loop
            f=array(f)
            if u.shape != f.shape:
                print 'Error! u and f must have the same dimensions!'
                sys.exit(1)
        else:
            if start_u is None and f is None:   # if neither dimensions, u or f is specified, u and f is set by default to a 100 x 50 rectangle with all values set to zero and one, respectively
                u=zeros((100,50))
                o=zeros((100,50))
                f=ones((u.shape))
            elif start_u is None:
                u=zeros(f.shape) # if only f is given, u is set to an array of the same dimensions as f with all values set to zero
                o=zeros(f.shape)
            elif f is None:
                f=ones(start_u.shape) # if only u is given, f is set to an array of the same dimensions as u with all values set to one
                u=start_u
                o=u.copy()
    else: # if dimensions are specified, u and f are set to rectangles with dimensions dim[0] x dim[1] with all values set to zero and one, respectively.
        u=zeros((dim[0], dim[1]))
        o=zeros((dim[0], dim[1]))
        f=ones((dim[0], dim[1]))
    if verbose: # convert from boolean to 0/1, which can be read in C
        v=1
    else:
        v=0
        
    """
    Below is the string containing the c code that will be read using weave. Note that u, o and f can be referenced in weave by using U2, O2 and F2 
    (where 2 indicates the number of dimensions) and that the dimensions can be referenced using Nu, No and Nf, respectively (e.g. in the default case Nu[0]=100 and Nu[1]=50)
    """
    expr = r"""
float t=t0;
int i, j;
for(t=t0;t<t1;t+=dt){
    if(v==1){ // prints if verbose mode is activated
        printf("Now processing time step %.1f\n", t);
        }
    for (i=1; i<Nu[0]-1; i++){ // update new array (U2)
        for (j=1; j<Nu[1]-1; j++){
            U2(i,j) = O2(i,j) + dt*(nu*O2(i-1,j) + nu*O2(i,j-1) - 4*nu*O2(i,j) + nu*O2(i,j+1) + nu*O2(i+1,j) + F2(i,j)); 
        }
    }
    for (i=1; i<Nu[0]-1; i++){ // save updated array (U2) as the old array (O2) for next time step
        for (j=1; j<Nu[1]-1; j++){
            O2(i,j)=U2(i,j);
        }
    }
}
""" 
    if timer:
        from timeit import default_timer as time
        start_time=time() # starts timer if prompted
    weave.inline(expr, ['u','f', 'o', 't1','t0','dt', 'nu', 'v']) # executes loop using weave. The first argument is the c code string, and the second argument is a list of variables to be imported from the python script. u will after execution be updated in accordance with the code in "expr".
    if timer:
        end_time=time() # ends timer.
        print 'loop executed in {t:.3f} seconds'.format(t=end_time-start_time)
    return u
if __name__ == "__main__":
    """
    Example of usage.
    """
    t0=0.0
    t1=1000.0
    dt=0.1
    nu=1.0
    u = heat_weave(t0, t1, dt, nu)
    matplotlib.pyplot.imshow(u, cmap= matplotlib.pyplot.get_cmap("gray"), interpolation="nearest")
    matplotlib.pyplot.colorbar()
    matplotlib.pyplot.show()
    


#U2(1:-1, 1:-1) = U2(1:-1, 1:-1) + dt*(nu*U2(0:-2,1:-1) + nu*U2(1:-1, 0:-2) - 4*nu*U2(1:-1,1:-1) + nu*U2(1:-1,2:) + nu*U2(2:,1:-1) + F2(1:-1,1:-1));

#printf("%d\\n",i);
