from __future__ import division, absolute_import, print_function

from warnings import warn
from statsmodels.compat.collections import OrderedDict
import model

import numpy as np
import pandas as pd
from statsmodels.tsa.filters.hp_filter import hpfilter
from statsmodels.tools.data import _is_using_pandas
from statsmodels.tsa.tsatools import lagmat
import statsmodels.api as sm
import matplotlib.pyplot as plt

from IPython.display import display, Latex
# from .mlemodel import MLEModel, MLEResults, MLEResultsWrapper
from scipy.linalg import solve_discrete_lyapunov
from statsmodels.tools.tools import Bunch
from statsmodels.tools.sm_exceptions import ValueWarning, OutputWarning, SpecificationWarning
# from .tools import (
#     companion_matrix, constrain_stationary_univariate,
#     unconstrain_stationary_univariate
# )
import statsmodels.base.wrapper as wrap

_mask_map = {
    1: 'irregular',
    2: 'fixed intercept',
    3: 'deterministic constant',
    6: 'random walk',
    7: 'local level',
    8: 'fixed slope',
    11: 'deterministic trend',
    14: 'random walk with drift',
    15: 'local linear deterministic trend',
    31: 'local linear trend',
    27: 'smooth trend',
    26: 'random trend'
}



dataModel = model.Model()
calls = dataModel.returnColumn('Offered_Calls')
quarterlyHours = dataModel.returnColumn('quarterlyHour')
quarterlyHoursTimestamp =dataModel.returnColumn('Time')

dataFrame = pd.DataFrame(quarterlyHoursTimestamp, calls)
dataFrame.columns = [['quarters'], ['calls']]
#print(dataFrame)

output_mod = sm.tsa.UnobservedComponents(np.asarray(dataFrame))
print(output_mod)
plt.plot(output_mod)
plt.show()