# Created by Sean L. on Mar 15
# 
# emb2emb client
# embed.py
# 
# PromptCraft, 2025. All rights reserved.

from typing import Callable
import functools
import time
from utils.output import ClientConsole
from models.memglobalstore_model import global_manager

class PerformanceMetrics:
    """Utility class for collecting and reporting performance metrics.
    
    Provides decorators for monitoring function execution times and logging
    performance data through the ClientConsole system.

    Example:
        >>> @PerformanceMetrics.runtime_monitor
        ... def sample_function(delay=1):
        ...     time.sleep(delay)
        ...     return "Done"
        ...
        >>> sample_function()
        Finished executing sample_function in 1.005 seconds
        'Done'
    """

    @staticmethod
    def runtime_monitor(input_function: Callable) -> Callable:
        """Decorator that measures and logs function execution time.
        
        Tracks runtime using high-resolution perf_counter and reports results
        through ClientConsole. Preserves original function metadata via functools.

        Parameters:
            input_function (Callable): Target function to be monitored

        Returns:
            Callable: Wrapped function with timing instrumentation

        Example:
            >>> @runtime_monitor
            ... def data_processor(items):
            ...     # Processing logic
            ...     return len(items)
            ...
            >>> data_processor(range(1000))
            Finished executing data_processor in 0.045 seconds
            1000
        """
        @functools.wraps(input_function)
        def runtime_wrapper(*args, **kwargs):
            start_value = time.perf_counter()
            return_value = input_function(*args, **kwargs)
            end_value = time.perf_counter()
            runtime_value = (end_value - start_value) * 1000
            if global_manager.get('verbose'):
                ClientConsole.log(
                    f"Finished executing {input_function.__name__} "
                    f"in {runtime_value:.3f} ms"
                )
                ...
            return return_value
        return runtime_wrapper