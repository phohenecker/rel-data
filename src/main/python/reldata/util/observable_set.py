# -*- coding: utf-8 -*-


import collections
import typing

import insanity

from reldata.util import set_observer


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
__date__ = "Nov 12, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


T = typing.TypeVar("T")


class ObservableSet(collections.MutableSet, typing.Generic[T]):
    """An implementation of ``collections.MutableSet`` that enforces its elements to be of a specified type, and that
    allows for adding observers to be notified about any changes of the contained data.
    """

    def __init__(self, element_type: typing.Type[T], data: typing.Iterable[T]=None):
        """Creates a new instance of ``ObservableSet``.
        
        Args:
            element_type (type): The required type of the elements of the newly created set.
            data (Iterable): Initial elements to add to the new set.
        """
        # sanitize args
        insanity.sanitize_type("element_type", element_type, type)
        insanity.sanitize_type("data", data, collections.Iterable, none_allowed=True)
        
        # define attributes
        self._data = set()
        self._observers = []
        self._element_type = element_type

        # add provided data
        if data is not None:
            self.add_all(data)
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __contains__(self, item):
        return item in self._data
    
    def __iter__(self) -> typing.Iterator[T]:
        # As it turned out, the order in which the data is iterated may vary over multiple executions of the same Python
        # script if we simply return iter(self._data) in this method. Interestingly, this is the case even if we read
        # a pickled knowledge graph and iterate through it's triples. However, to ensure a consistent order of
        # iteration, we first order the triples (by their string representations).
        ordered_data = list(self._data)
        ordered_data.sort(key=lambda x: str(x))
        return iter(ordered_data)
    
    def __len__(self) -> int:
        return len(self._data)
    
    #  METHODS  ########################################################################################################
    
    def add_observer(self, obs: set_observer.SetObserver) -> None:
        """Adds an observer to an ``ObservableSet``.
        
        Notice that the provided observer is only added if it not observing already.
        
        Args:
            obs (:class:`set_observer.SetObserver`): The observer to add.
        """
        if obs not in self._observers:
            self._observers.append(obs)
    
    def add(self, elem) -> None:
        # sanitize args
        insanity.sanitize_type("elem", elem, self._element_type)
        
        # add element to list
        if elem not in self:
            self._data.add(elem)
            
            # notify observers
            for obs in self._observers:
                obs.element_added(elem)
    
    def add_all(self, elements: typing.Iterable[T]) -> None:
        """Adds all elements in the provided ``Iterable`` to an ``ObservableSet``.
        
        Args:
            elements (Iterable): The elements to add.
        """
        insanity.sanitize_type("elements", elements, collections.Iterable)
        for e in elements:
            self.add(e)
    
    def discard(self, elem) -> None:
        # remove element if present
        if elem in self:
            self._data.discard(elem)

            # notify observers
            for o in self._observers:
                o.element_removed(elem)
    
    def remove_observer(self, obs: set_observer.SetObserver) -> None:
        """Removes an observer of an ``ObservableSet``.
        
        Args:
            obs (:class:`set_observer.SetObserver`): The observer to remove.
        """
        if obs in self._observers:
            self._observers.remove(obs)
