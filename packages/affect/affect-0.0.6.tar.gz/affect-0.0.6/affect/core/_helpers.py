from affect.core._decorators import as_result

safe_print = as_result()(print)
