import argparse
from heat_equation_numpy import heat_numpy as numpy
from heat_equation import heat as python
from heat_equation_weave import heat_weave as weave
import matplotlib.pyplot
from numpy import *
import cPickle as pickle
import sys
import os.path

# Oystein Kapperud, 2015

"""
Run python heat_equation_ui.py -h from the command line to see a list of possible input variables. 
"""

parser = argparse.ArgumentParser(description='A simulation of the dissipation of heat in a (2D) material with a given thermal diffusivity.')
# add arguments:
parser.add_argument('-t0', type=float, help='The start time, e.g. -t0 0.0 (default = 0.0)', default=0.0)
parser.add_argument('-t1', type=float, help= 'The end time in seconds, e.g. -t1 1000.0 (default= 1000.0)', default=1000.0)
parser.add_argument('-dt', type=float, help= 'The time step, e.g. -dt 0.05 (default= 0.1)', default=0.1)
parser.add_argument('-nu', type=float, help= 'Thermal diffusivity, e.g. - nu 2.0 (default= 1.0)', default=1.0)
parser.add_argument('-dim', type=int, nargs=2, help= 'The dimensions of the rectangle, e.g. -dim 100 50 (default: 100 x 50)', default=None)
parser.add_argument('-f', type=str, help= 'Heat source. Can be given as a nested list or numpy array enclosed in quotation marks, e.g. -f "ones((100,50))"', default=None)
parser.add_argument('-start_u', type=str, help= 'Temperature array at the start of the simulation. Can be given as a nested list or numpy array enclosed in quotation marks, e.g. -start_u "zeros((100,50))"', default=None)
parser.add_argument('-show', type=str, help= 'Choose whether or not to show the heat plot at the end time, e.g. -show no (default: yes)', default='yes')
parser.add_argument('-plot_file', type=str, help= 'An optional file name for storing of the resulting heat plot, e.g. -plot_file plot.png (default= None)', default=None)
parser.add_argument('-i', '--implementation', type=str, help= 'Select which implementation you want to use, e.g. -implementation numpy, options: numpy, weave, python (default= weave)', default='weave')
parser.add_argument('-timer', action="store_true", help=  'Turn on the timer')
parser.add_argument('-input_file', type=str, help= 'An optional file name for retrieving of stored initial temperature map, e.g. -input_file heat.txt (default=None)', default=None)
parser.add_argument('-output_file', type=str, help= 'An optional file name for storing of temperature map at end time, e.g. -output_file heat.txt (default=None)', default=None)
parser.add_argument('-v', '--verbose', action="store_true", help="Activate verbose mode")


allargs = vars(parser.parse_args()) # This creates a dictionary with all the arguments as keys and the input/default values as values.
if allargs['f'] is not None:
    try:
        allargs['f']=eval(allargs['f']) # Converts from string to list
    except:
        print "Error! Invalid input for f!"
        sys.exit(1)
    if type(allargs['f'])!=ndarray and type(allargs['f']!= list):
        print "Error! f must be a list or a numpy array!"
        sys.exit(1)
    
if allargs['start_u'] is not None:
    try:
        allargs['start_u']=eval(allargs['start_u']) # Converts from string to list
    except:
        print "Error! Invalid input for start_u!"
        sys.exit(1)
    if type(allargs['start_u'])!=ndarray and type(allargs['start_u']!= list):
        print "Error! start_u must be a list or a numpy array!"
        sys.exit(1)
    

if allargs['dt']>0.25:
    print "Error! Please choose a dt value smaller than or equal to 0.25"
    sys.exit(1)

if allargs['nu']>2.5:
    print "Error! Please choose a nu value smaller than or equal to 2.5"
    sys.exit(1)

if allargs['dim'] is not None:
    if allargs['dim'][0] < 3 or allargs['dim'][1] < 3:
        print "Error! X and Y must both be larger than 2 for dimensions X x Y."
        sys.exit(1)
        
if allargs['t0']>=allargs['t1']:
    print "Error! t1 must be larger than t0!"
    sys.exit(1)

# Not all the arguments should be passed to the function. I therefore copy allargs to a dictionary function_args and delete from the latter the superfluous keys.
function_args = allargs.copy()
del function_args['plot_file'], function_args['implementation'], function_args['input_file'], function_args['output_file'], function_args['show']

# Imports start_u array using pickle if prompted
    
if allargs['input_file'] is not None:
    if os.path.isfile(allargs['input_file']):
        try:
            if allargs['verbose']:
                print 'Fetching file from', allargs['input_file']
            file=open(allargs['input_file'], 'r')
            function_args['start_u']=pickle.load(file)
            file.close()
        except:
            print 'Error! Invalid input file!'
            sys.exit(1)
    else:
        print "Error! Input file does not exist!"
        sys.exit(1)
        

u = eval(allargs['implementation'])(**function_args) # eval(allargs['implementation']) converts the string (e.g. 'numpy') in the dictionary to the corresponding function name. (**function_args) sends the contents of the function_args dictionary to that function as keyword arguments (e.g. {'dt': 0.1} will be interpreted as dt=0.1)
u = array(u) # converts u to numpy array (in case the pure python solution is chosen)
# saves the resulting u using pickle if prompted
if allargs['output_file'] is not None:
    try:
        if allargs['verbose']:
            print "Saving to file", allargs['output_file']
        file=open(allargs['output_file'], 'w')
        pickle.dump(u, file)
        file.close()
    except:
        print 'Error! Invalid output file name!'

matplotlib.pyplot.imshow(u, cmap= matplotlib.pyplot.get_cmap("gray"), interpolation="nearest")
matplotlib.pyplot.colorbar()

# saves an image plot of u if prompted
if allargs['plot_file'] is not None:
    try:
        matplotlib.pyplot.savefig(allargs['plot_file'], dpi=100)
    except:
        print 'Error! Invalid plot file name!'
        
        
# shows the plot of u. Default is to show the plot, but this can be turned off by passing -show no
if allargs['show']=='yes':
    if allargs['verbose']:
        print "Plotting..."
    matplotlib.pyplot.show()
