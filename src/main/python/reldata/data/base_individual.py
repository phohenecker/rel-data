# -*- coding: utf-8 -*-


import typing

import insanity

from reldata.data import class_membership
from reldata.data import individual
from reldata.data import individual_observer
from reldata.data import literal_value
from reldata.util import observable_set
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
__date__ = "Nov 15, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class BaseIndividual(individual.Individual, set_observer.SetObserver):
    """This is a basic implementation of :class:`individual.Individual`.
    
    Notice that ``BaseIndividual`` does not provide any way to specify :attr:`individual.Individual.index` or
    :attr:`individual.Individual.name`, though, as these have to be checked with respect to uniqueness. Therefore,
    instances of any (sub-)class of :class:`individual.Individual` should be created by a factory that defines a
    private implementation of :class:`individual.Individual`, which may make use of this base implementation.
    """

    def __init__(self):
        # define attributes
        self._classes = observable_set.ObservableSet(class_membership.ClassMembership)
        self._index = None
        self._literals = observable_set.ObservableSet(literal_value.LiteralValue)
        self._name = None
        self._observers = []
        
        # make BaseIndividual an observer of the class/literal set
        self._classes.add_observer(self)
        self._literals.add_observer(self)
    
    #  PROPERTIES  #####################################################################################################

    @property
    def index(self) -> int:
        return self._index

    @property
    def classes(self) -> typing.MutableSet[class_membership.ClassMembership]:
        return self._classes

    @property
    def name(self) -> str:
        return self._name

    @property
    def literals(self) -> typing.MutableSet[literal_value.LiteralValue]:
        return self._literals

    #  METHODS  ########################################################################################################
    
    def add_observer(self, obs: individual_observer.IndividualObserver) -> None:
        insanity.sanitize_type("obs", obs, individual_observer.IndividualObserver)
        if obs not in self._observers:
            self._observers.append(obs)
    
    def element_added(self, elem):
        if isinstance(elem, class_membership.ClassMembership):
            for obs in self._observers:
                obs.class_added(self, elem)
        elif isinstance(elem, literal_value.LiteralValue):
            for obs in self._observers:
                obs.literal_added(self, elem)

    def element_removed(self, elem):
        if isinstance(elem, class_membership.ClassMembership):
            for obs in self._observers:
                obs.class_removed(self, elem)
        elif isinstance(elem, literal_value.LiteralValue):
            for obs in self._observers:
                obs.literal_removed(self, elem)
    
    def remove_observer(self, obs: individual_observer.IndividualObserver) -> None:
        if obs in self._observers:
            self._observers.remove(obs)
