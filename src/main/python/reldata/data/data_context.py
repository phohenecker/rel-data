# -*- coding: utf-8 -*-


import functools
import threading
import typing

from reldata.util import sync


__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2017, Patrick Hohenecker\n"
        "All rights reserved.\n"
        "\n"
        "Redistribution and use in source and binary forms, with or without\n"
        "modification, are permitted provided that the following conditions are met:\n"
        "\n"
        "1. Redistributions of source code must retain the above copyright notice, this\n"
        "   list of conditions and the following disclaimer.\n"
        "2. Redistributions in binary form must reproduce the above copyright notice,\n"
        "   this list of conditions and the following disclaimer in the documentation\n"
        "   and/or other materials provided with the distribution.\n"
        "\n"
        "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\" AND\n"
        "ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n"
        "WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n"
        "DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR\n"
        "ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n"
        "(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n"
        "LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND\n"
        "ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n"
        "(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n"
        "SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
)
__license__ = "Simplified BSD License"
__version__ = "2017.1"
__date__ = "Nov 14, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


def new_context(func: typing.Callable) -> typing.Callable:
    """A function decorator that ensures that the annotated function is always executed in a fresh :class:`DataContext`.
    """
    @functools.wraps(func)
    def func_with_context(*args, **kwargs):
        with DataContext():
            return func(*args, *kwargs)
    return func_with_context
    

class DataContext(object):
    """An instance of ``DataContext`` is used to store the current state of the creation of a knowledge graph.
    
    Many parts of a knowledge graph are subject to certain uniqueness constraints, e.g., the names of individuals.
    Therefore, objects for representing such data have to be created by means of factories, which enforce the respective
    constraints, in the ``reldata`` package.
    However, in order to allow for working with multiple graphs at the same time, all of the factories make use of
    *data contexts*. A data context, which is represented by an instance of ``DataContext``, could simply be considered
    as a current state in the creation of a knowledge graph, and may be used to store according data, which is what all
    of the factories in ``reldata`` do.
    
    At any time, there is exactly one active ``DataContext``, which is accessible via the class method
    :meth:``DataContext.get_context``. If you want to make use of a different than the default context, then you can
    create a new instance of ``DataContext``, and wrap the code that is supposed to run in this fresh context with a
    ``with`` block:
    
        from reldata.data import data_context as dc
        
        with dc.DataContext():
            # this part is executed in a fresh context
            ...
    
    If you have an entire function that is supposed to always run in a new context, then you can also use the function
    decorator :func:`new_context`, which simply puts the annotated function in a ``with`` block as described above:
    
        @dc.new_context
        def some_func():
            # this parts is executed in a fresh context
            ...
    
    Finally, notice that you can always reset a ``DataContext`` by means of the provided :meth:`clear` method. For the
    currently active context, this is invoked as ``DataContext.get_context().clear()``.
    """
    
    _current_context = dict()
    """dict[int, DataContext]: The currently active contexts for all threads identifiers."""
    
    #  CONSTRUCTOR  ####################################################################################################
        
    def __init__(self):
        """Creates a new empty ``DataContext``."""
        self._data = dict()                      # stores the data in the context
        self._last_context = None                # stores previous context if the current one is used in a with block
        self._thread_id = self._get_thread_id()  # the ID of the thread that context lives in
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __enter__(self):
        # store active context
        if self._thread_id in DataContext._current_context:
            self._last_context = DataContext._current_context[self._thread_id]
        # make self the active context
        DataContext._current_context[self._thread_id] = self
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # reinstate previously active context
        if self._last_context is not None:
            DataContext._current_context[self._thread_id] = self._last_context
        else:
            del DataContext._current_context[self._thread_id]
        
        self._last_context = None
    
    def __getitem__(self, item):
        if item in self._data:
            return self._data[item]
        else:
            return None
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    #  METHODS  ########################################################################################################
    
    @staticmethod
    def _get_thread_id() -> int:
        """Retrieves a unique identifier for the thread that the object that invokes this method lives in.
        
        Returns:
            int: The ID.
        """
        # NOTICE:
        # we do not use threading.get_ident() to identify a thread, as Python recycles these identifiers
        return id(threading.current_thread())

    def clear(self):
        """Resets a ``DataContext`` to its initial state.

        Notice that this clears **all data** that have been stored in a context.
        """
        self._data.clear()
    
    @classmethod
    @sync.synchronized
    def get_context(cls):
        """Retrieves the currently active context for the Thread that invoked this method.
        
        Returns:
            DataContext: The context.
        """
        # create context for current thread if there is none yet
        thread_id = cls._get_thread_id()
        if thread_id not in cls._current_context:
            cls._current_context[thread_id] = DataContext()
        
        # return the requested DataContext
        return cls._current_context[thread_id]
