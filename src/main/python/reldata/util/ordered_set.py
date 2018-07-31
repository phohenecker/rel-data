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
__license__ = "BSD-2-Clause"
__version__ = "2017.1"
__date__ = "Nov 13, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


T = typing.TypeVar("T")


class OrderedSet(collections.MutableSet, typing.Generic[T]):
    """This class implements an ordered set that stores instances of a particular type ordered by their indices.
    
    Notice that instances of this class are suitable for storing instances that are numbered consecutively from 0, but
    may be wasteful with respect to memory consumption otherwise.
    """

    def __init__(
            self,
            element_type: typing.Type[T],
            index_func: typing.Callable[[T], int],
            data: typing.Iterable[T]=None
    ):
        """Creates a new empty ``OrderedSet``.
        
        Args:
            element_type (type): The type of the elements that will be added to the newly created set.
            index_func (function): A function that maps instances of type ``element_type`` to (unique) integer indices.
            data (Iterable, optional): An optional iterable that specifies data to add the newly created set.
        """
        # sanitize args
        insanity.sanitize_type("element_type", element_type, type)
        if not callable(index_func):
            raise TypeError("The parameter <index_func> has to be callable!")
        insanity.sanitize_type("data", data, collections.Iterable, none_allowed=True)
        
        # define attributes
        self._data = []                    # a list that stores the data orderly
        self._element_type = element_type  # the type of elements of the set
        self._index_func = index_func      # a function that maps elements to indices
        self._len = 0                      # the length of self._data
        self._num_elements = 0             # the actual number of elements in self._data (without Nones)
        self._observers = []               # a list of all registered observers of an OrderedSet
    
        # add provided data
        if data is not None:
            self.add_all(data)
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __contains__(self, item: typing.Union[T, int]) -> bool:
        if not isinstance(item, self._element_type) and not isinstance(item, int):
            return False
        
        # fetch index if provided item is not such
        if isinstance(item, self._element_type):
            item = self._index_func(item)
        
        return item < self._len and self._data[item] is not None
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, OrderedSet) or len(other) != len(self):
            return False
        
        for element in self:
            if element not in other:
                return False
        
        return True
    
    def __getitem__(self, item: int) -> T:
        if not isinstance(item, int) or item < 0:
            raise KeyError("Unknown key: {}!".format(item))
        
        # return requested item if it exists
        if item < len(self._data) and self._data[item] is not None:
            return self._data[item]
        
        # the item is missing -> raise error
        raise KeyError("Unknown key: {}!".format(item))
    
    def __iter__(self) -> typing.Iterator[T]:
        for element in self._data:
            if element is not None:
                yield element
    
    def __len__(self) -> int:
        return self._num_elements
    
    #  METHODS  ########################################################################################################
    
    def add(self, element: T) -> None:
        # sanitize args
        insanity.sanitize_type("element", element, self._element_type)
        
        # get index of new element
        index = self._index_func(element)
        
        # check if element is contained already -> nothing to do
        if index < self._len and self._data[index] is not None:
            return
        
        # extend list of data if necessary
        if index >= self._len:
            new_entries = index - self._len + 1
            self._len = index + 1
            self._data.extend([None] * new_entries)
        
        # store provided element
        self._data[index] = element
        self._num_elements += 1
        
        # notify all observers about the new element
        for obs in self._observers:
            obs.element_added(element)
    
    def add_all(self, elements: typing.Iterable[T]) -> None:
        """Adds all elements in the provided ``Iterable`` to an ``OrderedSet``.
        
        Args:
            elements (Iterable): The elements to add.
        """
        insanity.sanitize_type("elements", elements, collections.Iterable)
        for e in elements:
            self.add(e)
    
    def add_observer(self, obs: set_observer.SetObserver) -> None:
        """Adds an observer to an ``OrderedSet``.
        
        Notice that the provided observer is only added if it not observing already.
        
        Args:
            obs (:class:`set_observer.SetObserver`): The observer to add.
        """
        if obs not in self._observers:
            self._observers.append(obs)
    
    def discard(self, value: typing.Union[T, int]) -> None:
        # if value is not contained in the set -> nothing to do
        if value not in self:
            return
        
        # fetch index of element to remove
        element = self._index_func(value) if isinstance(value, self._element_type) else value

        # remove element from data list
        if element == self._len - 1:
            del self._data[element]
            self._len -= 1
        else:
            self._data[element] = None
        self._num_elements -= 1
    
        # notify all observers about the removed element
        for obs in self._observers:
            obs.element_removed(element)
    
    def remove_observer(self, obs: set_observer.SetObserver) -> None:
        """Removes an observer of an ``OrderedSet``.
        
        Args:
            obs (:class:`set_observer.SetObserver`): The observer to remove.
        """
        if obs in self._observers:
            self._observers.remove(obs)
