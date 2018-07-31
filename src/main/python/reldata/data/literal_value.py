# -*- coding: utf-8 -*-


import typing

import insanity

from reldata.vocab import literal_type


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


class LiteralValue(object):
    """Describes an assignment of a literal value to an individual."""

    def __init__(self, literal: literal_type.LiteralType, value, inferred: bool=False, prediction: bool=False):
        """Creates a new instance of ``LiteralValue`` that specifies a type of literal together with an according value .

        Args:
            literal (:class:`literal_type.LiteralType`): Specifies :attr:`literal`.
            value: Specifies :attr:`value`.
            inferred (bool, optional): Specifies :attr:`inferred`.
            prediction (bool, optional): Specifies :attr:`prediction`.
        """
        # sanitize args
        insanity.sanitize_type("literal", literal, literal_type.LiteralType)
        if inferred and prediction:
            raise ValueError("A literal cannot be an inference and a prediction at the same time!")
    
        # specify attributes
        self._literal = literal
        self._inferred = bool(inferred)
        self._prediction = bool(prediction)
        self._value = value
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other) -> bool:
        return (
                isinstance(other, LiteralValue) and
                other.literal == self._literal and
                other.inferred == self._inferred and
                other.value == self._value and
                other.prediction == self._prediction
        )
    
    def __hash__(self) -> int:
        return hash(str(self))
    
    def __str__(self) -> str:
        return "LiteralValue(literal = {}, value = {}, inferred = {}, prediction = {})".format(
                self._literal.index,
                self._value,
                self._inferred,
                self._prediction
        )

    #  PROPERTIES  #####################################################################################################
    
    @property
    def literal(self) -> literal_type.LiteralType:
        """:class:`literal_type.LiteralType`: The literal for which the value is specified."""
        return self._literal

    @property
    def inferred(self) -> bool:
        """bool: Indicates whether the value has been inferred or specified."""
        return self._inferred
    
    @property
    def prediction(self) -> bool:
        """bool: Indicates whether the literal is a prediction target, i.e., it is neither a fact nor inferable."""
        return self._prediction

    @property
    def value(self) -> typing.Any:
        """The actual value that the individual has for the literal."""
        return self._value
