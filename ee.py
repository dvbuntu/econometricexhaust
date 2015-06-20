import rpy2.robjects as r
import numpy as np
import itertools

# evaluate some r code
r.r['pi']

# our data file
filename = 'data/Ex11-3.txt'

# R function to read data
read = r.r['read.csv']

# read data into R object and grab column names
data = read(filename, head=True, sep = ",")
var_names = data.colnames

# extract useful information from model
rsumm = r.r['summary']

# get a particular column
data.rx('num_delay')

# R function to do the modeling, glm is poisson in this case
# could be least squares, robust, nest logit, whatever
model_func = r.r['glm']

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

test_form = build_formula('num_delay', var_names[5:9])

# do the model
model_res = model_func(formula = test_form, data = data)
summ_res = rsumm(model_res)

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

model_pvals = get_pvals(summ_res)
# note that an intercept is the first one, will have to check which var is where
# have to handle the intercept special and explicitly turn it off

# test with intercept
test_int = build_formula('num_delay', list(var_names[5:9]) + ['1'])
model_int = model_func(formula = test_int, data = data)
summ_int = rsumm(model_int)
int_pvals = get_pvals(summ_int)

# stupid exhauster, don't pay attention to anything but pvals, keep only significant sets
def check_model(dep_var, ivars, data, model = model_func):
    '''Model dep_var using the ivars and model_func.  Return the probabilities of the variable coefficients being random and some score (like AIC)'''
    form = build_formula(dep_var, ivars)
    m = model(formula = form, data = data)
    summary = rsumm(m)
    return get_pvals(summary), get_aic(summary)

# typical academic threshold for significance
thresh = 0.05
dep_var = var_names[1]
ind_vars = list(var_names[5:9]) + ['1']

debug = True

good_models = []
for num_vars in range(1,len(ind_vars)):
    for ivars in itertools.combinations(ind_vars,num_vars):
        if debug:
            print(ivars)
        var_probs, score = check_model(dep_var, ivars, data)
        # if all vars are significant, add to pile of good models
        if True not in map(lambda x: x > thresh, var_probs): 
            good_models.append((ivars,var_probs,score)) 

