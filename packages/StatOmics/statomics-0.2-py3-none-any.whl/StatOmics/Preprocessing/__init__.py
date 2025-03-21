# Proprocessing/__init__.py

from ..r_interface import source_r_script, get_r_function

# Load R script(s) for this module
source_r_script(["Preprocessing/Filter_fun_by_Pct.R", "Preprocessing/Imputation_byNormal.R", "Preprocessing/log2Transf.R", "Preprocessing/Normalization_bySingleRef.R"])

def call(func_name, *args):
    """
    Calls an R function dynamically by name with provided arguments.
    """
    r_func = get_r_function(func_name)
    return r_func(*args)

