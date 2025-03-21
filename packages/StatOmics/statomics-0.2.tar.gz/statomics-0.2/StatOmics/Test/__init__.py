# /Test/__init__.py

from ..r_interface import source_r_script, get_r_function

# Load R script(s) for this module
source_r_script(["Test/test1.R", "Test/test2.R"])

def call(func_name, *args):
    """
    Calls an R function dynamically by name with provided arguments.
    Example: call_r_function("count_chars", "hello")
    """
    r_func = get_r_function(func_name)
    return r_func(*args)

