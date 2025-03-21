# Proprocessing/__init__.py

from ..r_interface import source_r_script, get_r_function

# Load R script(s) for this module
source_r_script(["Analysis/mannWhitneyU_test.R", "Analysis/normality_check_byShapi.R", "Analysis/permutation_basedpvalues.R", "Analysis/ttest&BH.R", "Analysis/variance_check_byLeve.R", "Analysis/welcht_test.R"])

def call(func_name, *args):
    """
    Calls an R function dynamically by name with provided arguments.
    """
    r_func = get_r_function(func_name)
    return r_func(*args)

