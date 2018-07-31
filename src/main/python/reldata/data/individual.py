# -*- coding: utf-8 -*-


import abc
import typing

from reldata.data import class_membership
from reldata.data import individual_observer
from reldata.data import literal_value


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
__date__ = "Nov 12, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class Individual(metaclass=abc.ABCMeta):
    """Instances of this class represent individuals in a knowledge graph.
    
    Every individual is uniquely identified through its index on the one hand and a unique name on the other hand. While
    using unique name is the usual way to identify individuals, the additional index exist mostly for implementation
    purposes.
    """
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Individual) and other.index == self.index
    
    def __hash__(self) -> int:
        return self.index
    
    def __str__(self) -> str:
        return "Individual(index = {}, name = '{}', classes = [{}], literals = [{}])".format(
            self.index,
            self.name,
            ", ".join([("+" if m.is_member else "-") + str(m.cls.index) for m in self.classes]),
            ", ".join(["({}, {})".format(l.literal.index, l.value) for l in self.literals])
        )
    
    #  PROPERTIES  #####################################################################################################
    
    @property
    @abc.abstractmethod
    def classes(self) -> typing.MutableSet[class_membership.ClassMembership]:
        """set[:class:`class_membership.ClassMembership`]: All known class memberships of an individual.
        
        Notice that these include both positive and negative propositions, i.e., claims of memberships as well as
        non-memberships.
        """
        pass
    
    @property
    @abc.abstractmethod
    def literals(self) -> typing.MutableSet[literal_value.LiteralValue]:
        """set[:class:`literal_value.LiteralValue`]: All known literal assignments of an individual."""
        pass
    
    @property
    @abc.abstractmethod
    def index(self) -> int:
        """int: The unique index of an ``Individual``."""
        pass
    
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """str: The unique name of an ``Individual``."""
        pass
    
    #  METHODS  ########################################################################################################

    @abc.abstractmethod
    def add_observer(self, obs: individual_observer.IndividualObserver) -> None:
        """Adds an observer to an ``Individual`` if it is not observing already."""
        pass
    
    @abc.abstractmethod
    def remove_observer(self, obs: individual_observer.IndividualObserver) -> None:
        """Removes an observer of an ``Individual`` if it is indeed observing."""
        pass
