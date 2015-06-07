import rpy2.robjects as r

# evaluate some r code
r.r['pi']

# our data file
filename = 'data/Ex11-3.txt'

# R function to read data
read = r.r['read.csv']

# read data into R object and grab column names
data = read(filename, head=True, sep = ",")
var_names = data.colnames

# get a particular column
data.rx('num_delay')

# R function to do the modeling, glm is poisson in this case
# could be least squares, robust, nest logit, whatever
model_func = r.r['glm']

def build_formula(dependent_var, independent_vars):
    '''Build string describing what we are modeling...this will be built each
    time in exhaust'''
    # Add together strings of vars, if appended a 1, include as string
    ind_vars = ' + '.join(map(str,independent_vars))
    # All together now!
    formula = '{0} ~ {1}'.format(dependent_var,ind_vars)
    return formula

test_form = build_formula('num_delay', var_names[5:9])

model_res = model_func(formula = test_form, data = data)


