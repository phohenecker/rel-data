# -*- coding: utf-8 -*-


import insanity

from reldata.vocab import class_type


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


class ClassMembership(object):
    """Describes an individual's membership of a class."""
    
    def __init__(self, cls: class_type.ClassType, is_member: bool, inferred: bool):
        """Creates a new instance of ``ClassMembership`` that specifies the relation between an individual and a class.
        
        Args:
            cls (:class:`class_type.ClassType`): Specifies :attr:`class`.
            is_member (bool): Specifies :attr:`is_member`.
            inferred (bool): Specifies :attr:`inferred`.
        """
        # sanitize args
        insanity.sanitize_type("cls", cls, class_type.ClassType)
        
        # specify attributes
        self._cls = cls
        self._inferred = bool(inferred)
        self._is_member = bool(is_member)
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other) -> bool:
        return (
                isinstance(other, ClassMembership) and
                other.cls == self._cls and
                other.inferred == self._inferred and
                other.is_member == self._is_member
        )

    def __hash__(self) -> int:
        return hash(str(self))
    
    def __str__(self) -> str:
        return "ClassMembership(cls = {}, inferred = {}, is_member = {})".format(
                self._cls.index,
                self._inferred,
                self._is_member
        )

    #  PROPERTIES  #####################################################################################################

    @property
    def cls(self) -> class_type.ClassType:
        """:class:`class_type.ClassType`: The class for which the membership is specified."""
        return self._cls
    
    @property
    def inferred(self) -> bool:
        """bool: Indicates whether the class membership has been inferred or specified."""
        return self._inferred
    
    @property
    def is_member(self) -> bool:
        """bool: Indicates whether the individual is a member of the class or not."""
        return self._is_member
