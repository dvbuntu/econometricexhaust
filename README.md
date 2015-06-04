Econometric-Exhauster
---

## Overview

Building econometric models can be really tedious.  Once you setup the basic model in whatever your favorite language is, you muddle through various combinations and transformations of variables, hoping that they form a significant and logical set.  Depending on the model, this can take hours to days to weeks to forever.  And, a human being might not hit all the causes, missing some key variable or combination in the process.  The whole workflow is error-prone.

The econometric-exhauster, EE, is an automated program for finding good (leave "best" up to the human) sets of variables and transformations given a prescribed model.  Primarily, it does this by trying all the variables and transformations that it can.  When there are too many combinations to try, it will only do some and try to mix-and-match variables intelligently using something like a genetic algorithm to evolve a good set.

EE takes in your dataset, and a model specification.  Most of the grunt work of preparing models is in `python` while the actual statistical modeling is done in `R`.  It outputs a sorted list of the top N sets of variables, according to the overall score and significance of the variables.  Using this, a researcher can select the most logically appropriate one or tweak the model further with more complicated combinations.

## Notes

* Use `Rpy` to interface `python` and `R`
* Ditch `python` entirely and do pure `R`?
* Parallelism a must, connect to a sage cloud?
    * Just use sage to begin with?
* Pull up some old grad school problems as examples (SEM I & II from Mannering)
