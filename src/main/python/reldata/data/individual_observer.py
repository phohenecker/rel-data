# -*- coding: utf-8 -*-


import abc

from reldata.data import class_membership
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
__license__ = "Simplified BSD License"
__version__ = "2017.1"
__date__ = "Nov 15, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class IndividualObserver(metaclass=abc.ABCMeta):
    """An interface that specifies various callback methods that are used by an :class:`individual.Individual` to notify
    observers about changes.
    """
    
    @abc.abstractmethod
    def class_added(self, ind, cls: class_membership.ClassMembership) -> None:
        """This method is used to notify an ``IndividualObserver`` about an added class membership statement.
        
        Args:
            ind (:class:`individual.Individual`): The respective individual.
            cls (:class:`class_membership.ClassMembership`): The added membership statement.
        """
        pass
    
    @abc.abstractmethod
    def class_removed(self, ind, cls: class_membership.ClassMembership) -> None:
        """This method is used to notify an ``IndividualObserver`` about a removed class membership statement.
        
        Args:
            ind (:class:`individual.Individual`): The respective individual.
            cls (:class:`class_membership.ClassMembership`): The removed membership statement.
        """
        pass

    @abc.abstractmethod
    def literal_added(self, ind, lit: literal_value.LiteralValue) -> None:
        """This method is used to notify an ``IndividualObserver`` about a literal value that has been specified.
        
        Args:
            ind (:class:`individual.Individual`): The respective individual.
            lit (:class:`literal_value.LiteralValue`): The specified literal value.
        """
        pass

    @abc.abstractmethod
    def literal_removed(self, ind, lit: literal_value.LiteralValue) -> None:
        """This method is used to notify an ``IndividualObserver`` about the removal of a literal value.
        
        Args:
            ind (:class:`individual.Individual`): The respective individual.
            lit (:class:`literal_value.LiteralValue`): The removed literal value.
        """
        pass