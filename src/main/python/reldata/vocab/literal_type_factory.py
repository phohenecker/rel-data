# -*- coding: utf-8 -*-


from reldata.data import data_context as dc
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


# ==================================================================================================================== #
#  CLASS  L I T E R A L  T Y P E  F A C T O R Y                                                                        #
# ==================================================================================================================== #


class LiteralTypeFactory(object):
    """A factory for creating instances of :class:`literal_type.LiteralType`.
    
    Notice that the ``LiteralTypeFactory`` is sensitive with respect to the current data context as specified in
    :class:`dc.DataContext`.
    """

    _LAST_INDEX = "LiteralTypeFactory.last_index"
    """str: The key that is used for storing the last index that was assigned to a LiteralType in the context."""
    
    #  METHODS  ########################################################################################################

    @classmethod
    def _prepare_context(cls):
        if dc.DataContext.get_context()[cls._LAST_INDEX] is None:
            cls.reset()
    
    @classmethod
    def create_literal(cls, name: str) -> literal_type.LiteralType:
        """Constructs an instance of :class:`literal_type.LiteralType` with the provided name.

        Args:
            name (str): The name to assign to the created :class:`literal_type.LiteralType`. If the provided ``name``
                is not a ``str``, then it is converted into such.

        Returns:
            :class:`literal_type.LiteralType`: The constructed instance.
        """
        # prepare context if necessary
        cls._prepare_context()

        # fetch current context
        ctx = dc.DataContext.get_context()

        ctx[cls._LAST_INDEX] += 1
        return _LiteralType(ctx[cls._LAST_INDEX], str(name))

    @classmethod
    def reset(cls) -> None:
        """Resets the factory to its initial state."""
        dc.DataContext.get_context()[cls._LAST_INDEX] = -1


# ==================================================================================================================== #
#  CLASS  _  L I T E R A L  T Y P E                                                                                    #
# ==================================================================================================================== #


class _LiteralType(literal_type.LiteralType):
    """A private implementation of :class:`literal_type.LiteralType`."""
    
    def __init__(self, index: int, name: str):
        self._index = index
        self._name = name
    
    #  PROPERTIES  #####################################################################################################
    
    @property
    def index(self) -> int:
        return self._index
    
    @property
    def name(self) -> str:
        return self._name
