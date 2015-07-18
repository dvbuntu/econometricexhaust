import argparse
import rpy2.robjects as r
import numpy as np
import itertools

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help="data file")
parser.add_argument('-v', '--verbose', help="turn on verbose mode", action="store_true", default=False)
parser.add_argument('-t', '--thresh', help="probability threshold for variable significance", type=float, default=0.05)
parser.add_argument('-m', '--model', help="R model type (lm, poisson, etc)", default='lm')
parser.add_argument('--no_label', help="Flag for data without labels", action="store_true", default=False)
parser.add_argument('-d', '--dependent_var', help="Dependent variable name or column")
parser.add_argument('-i', '--independent_var', help="Independent variable name and/or column numbers.  Ranges acceptable (2,3-5,num_foo,8-12)")
parser.add_argument('--no_constant', help="Turn off constanst variable", action="store_true", default = False)
parser.add_argument('-s', '--field_separator', help="Character for separating fields", default=',')
# this is non-trivial, see stack overflow for changing R record separator
# parser.add_argument('-r', '--record_separator', help="Character for separating records", default='\n
args = parser.parse_args()

# our data file
if args.filename:
    filename = args.filename
else:
    filename = 'data/Ex11-3.txt'

# R function to read data
read = r.r['read.csv']

# read data into R object and grab column names
if args.no_label:
    data = read(filename, sep = ",")
    var_names = ['x{0}'.format(i) for i in range(data.ncol)]
else:
    data = read(filename, head=True, sep = ",")
    var_names = data.colnames

# extract useful information from model
rsumm = r.r['summary']

# R function to do the modeling, glm is poisson in this case
# could be least squares, robust, nest logit, whatever
if args.model == 'lm':
    model_func = r.r['lm']
elif args.model == 'poisson':
    model_func = r.r['glm']
else:
    raise NotImplementedError("{0} is not an R model I know".format(args.model))

def build_formula(dependent_var, independent_vars):
    '''Build string describing what we are modeling...this will be built each
    time in exhaust'''
    # Copy in the variables
    my_ind_vars = list(independent_vars[:])
    # Check for intercept variable, R makes you add things to remove it..
    if '1' not in my_ind_vars and 1 not in my_ind_vars:
        my_ind_vars += ['0']
    # Add together strings of vars, if appended a 1, include as string
    ind_vars = ' + '.join(map(str,my_ind_vars))
    # All together now!
    formula = '{0} ~ {1}'.format(dependent_var,ind_vars)
    return formula

# grab the coefficients and their significances
def get_pvals(summ):
    '''Get the probabilities of the coefficients being random.'''
    coeff_idx = summ.names.index('coefficients')
    my_coeff = summ[coeff_idx]
    coeff_arr = np.array(my_coeff)
    p_col = my_coeff.colnames.index('Pr(>|t|)')
    pvals = coeff_arr[:,p_col]
    return pvals

def get_aic(summ):
    '''Get the Akaike Information Criterion value from the model summary'''
    aic_idx = summ.names.index('aic')
    aic = summ[aic_idx][0]
    return aic

# stupid exhauster, don't pay attention to anything but pvals, keep only significant sets
def check_model(dep_var, ivars, data, model = model_func):
    '''Model dep_var using the ivars and model_func.  Return the probabilities of the variable coefficients being random and some score (like AIC)'''
    form = build_formula(dep_var, ivars)
    m = model(formula = form, data = data)
    summary = rsumm(m)
    return get_pvals(summary), get_aic(summary), summary

thresh = args.thresh

# assume first column is dependent variable
dep_var = args.dependent_var
dep_var_idx = var_names.index(dep_var)

# pull out the independent variables of interest
def parse_ind_vars(var_str, var_names):
    digits = set('0123456789')
    my_vars = []
    elements = (x.split('-') for x in var_str.split(','))
    for e in elements:
        if set(e[0]) in digits:
            my_vars.extend([var_names[i] for i in range(e[0],e[-1] + 1)])
        else:
            my_vars.append(e)
    return my_vars

ind_vars = parse_ind_vars(args.independent_vars, var_names)
if not no_constant:
    ind_vars.append('1')

debug = args.verbose

good_models = []
for num_vars in range(1,len(ind_vars)):
    for ivars in itertools.combinations(ind_vars,num_vars):
        if debug:
            print(ivars)
        var_probs, score, summ = check_model(dep_var, ivars, data)
        # if all vars are significant, add to pile of good models
        if True not in map(lambda x: x > thresh, var_probs): 
            good_models.append((ivars,var_probs,score,summ)) 

# sort decent models by AIC
sorted_models = sorted(good_models, key=lambda x: x[2], reverse = True)
