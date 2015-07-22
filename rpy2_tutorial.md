# R and Python, A Tale of Friendship
R is a wonder statistical programming language.  Python is a great general purpose language with a module for just about everything (try `import antigravity`).  In fact, Python even has a module, `rpy2`, to join the two.  This guide will show you how to enjoy the best of both worlds.

First, we have to load up `rpy2`.  If it's not available as a [package](https://www.archlinux.org/packages/community/x86_64/python-rpy2/) through your operating system, then you can install it with `pip install rpy2` (learn more about Python's package manager, `pip`, [here](https://docs.python.org/3/installing/)).  Now we can `import py2.robjects as r` in our Python script.  `r.r['foo']` then gives Python access to the R object, `foo`.  It might seem like an odd construction, but now `r` exposes all the power of R to Python!

```python
# Connect R to Python
import rpy2.robjects as r

# Take a peek at our favorite number in R
print(r.r['pi'])
```

This interface exposes all R objects, not just constants.  For instance, Python can use the R trigonometric function, `sin`, by calling `r.r['sin']`.  If we save this to some Python variable, `rpy2` does the right thing and makes it a Python function.  We can pass it arguments exactly as we normally do, letting `rpy2` handle simple conversions.


```python
import rpy2.robjects as r

# Grab the R function
rsin = r.r['sin']

# Make some interesting data
data = [0, 3.14/2, r.r['pi'], 3.14]

# Reap what you have sown
out = [rsin(d) for d in data]
print(out)
# [<FloatVector - Python:0x7f5a4704d108 / R:0x7f5a6a096e78>
# [0.000000], <FloatVector - Python:0x7f5a4704d188 / R:0x7f5a6a096de8>
# [1.000000], <FloatVector - Python:0x7f5a4704d208 / R:0x7f5a6a096d88>
# [0.000000], <FloatVector - Python:0x7f5a4704d1c8 / R:0x7f5a6a096cf8>
# [0.001593]]
```

Just as you can import R objects into Python space, `rpy2` can similarly translate Python objects into the R world.  For example, `r.FloatVector([0,1,2,3,4])` converts a short Python `list` into, shockingly, an R `FloatVector`.  You can create whole `DataFrame` objects from Python, allowing you to manipulate in Python, statistically analyze in R, and push the results back to Python.  Right tool for the right job.

```python
import rpy2.robjects as r
import random

# Generate a simple data set
num_data = 20
coeff = 1.5
offset = 4
offset_var = 1
ind_data = list(range(num_data))
dep_data = [coeff*i + random.randint(offset-offset_var,offset+offset_var) for i in ind_data]

# Convert data to R, god of statistics
pdata = dict()
pdata['X'] = r.FloatVector(ind_data)
pdata['Y'] = r.FloatVector(dep_data)
data = r.DataFrame(pdata)

# Grab R regression function
pylm = r.r['lm']

# Make a formula for the regression
formula = 'Y ~ X + 1'

# Run the regression
m = pylm(formula = formula, data = data)

# Take a look at results
summary = r.r['summary'](m)
print(summary)
```

