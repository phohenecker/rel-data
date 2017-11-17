# -*- coding: utf-8 -*-


import typing

import insanity

from reldata.data import base_individual
from reldata.data import data_context as dc
from reldata.data import individual


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


# a type var for instances of type Individual or any subclass
T = typing.TypeVar("T", bound=individual.Individual)


# ==================================================================================================================== #
#  CLASS  I N D I V I D U A L  F A C T O R Y                                                                           #
# ==================================================================================================================== #


class IndividualFactory(object):
    """A factory for creating instances of :class:`individual.Individual`.
    
    This factory enforces the uniqueness of an individual's :attr:`individual.Individual.index` and
    :attr:`individual.Individual.name`. It is important to notice, though, that these uniqueness guarantees always
    stand with respect to the currently active :class:`dc.DataContext`. This means that two individuals that were
    created in different contexts may indeed have the same ``index`` or ``name``
    
    Notice further that this class can, and in fact **should**, also be used to create instances of classes the extend
    :attr:`individual.Individual` (cf. :meth:`create_individual`).
    
    Notice:
        Enforcing the uniqueness of :attr:`individual.Individual.name`s may be turned off by setting the attribute
        :attr:`check_names` to ``False``. However, this should be done for testing only!
    """
    
    _LAST_INDEX = "IndividualFactory.last_index"
    """str: The key that is used for storing the last index that was assigned to an individual in the context."""
    
    _USED_NAMES = "IndividualFactory.used_names"
    """str: The key that is used for storing individual names that have been used already in the context."""

    check_names = True
    """bool: Indicates whether to check uniqueness of :class:`individual.Individual` names."""
    
    #  METHODS  ########################################################################################################
    
    @classmethod
    def _prepare_context(cls):
        if dc.DataContext.get_context()[cls._LAST_INDEX] is None:
            cls.reset()

    @classmethod
    def create_individual(
            cls,
            name: str,
            target_type: typing.Type[T]=None,
            args: typing.Iterable=None,
            kwargs: typing.Dict[str, typing.Any]=None
    ) -> T:
        """Constructs an instance of :class:`individual.Individual` with the provided name.
        
        The newly created instance is assigned a unique :attr:`individual.Individual.index`, and it is checked whether
        the provided name has been used already. Notice again that the ``IndividualFactory`` is sensitive to the
        currently active context.
        
        To create an instance of a subclass of :class:`individual.Individual`, one may provide the according type via
        the arg ``target_type``. The ``__init__`` of this class is supposed to accept ``index`` and ``name`` as the
        first two positional args. If the constructor should require additional args, then these may be specified via
        ``args`` and ``kwargs``. This means that an instance of ``target_type`` is created as follows:
        
            new_instance = target_type(index, name, *args, **kwargs)

        Args:
            name (str): The name to assign to the created :class:`individual.Individual`. If the provided ``name``
                is not a ``str``, then it is converted into such.
            target_type (type, optional): The type of the instance to create, which has to be a subclass of
                :class:`individual.Individual`.
            args (iterable, optional): The positional args to pass to the constructor of ``target_type``.
            kwargs (dict, optional): The keyword args to pass to the constructor of ``target_type``.

        Returns:
            :class:`individual.Individual`: The newly constructed instance.
        
        Raises:
            ValueError: If :attr:`check_names` is ``True`` and the provided ``name`` has been used before, or if
                a provided ``target_type`` is not a subclass of :class:`individual.Individual`.
        """
        # sanitize target type
        insanity.sanitize_type("target_type", target_type, type, none_allowed=True)
        if target_type is not None and not issubclass(target_type, individual.Individual):
            raise ValueError(
                    "The provided <target_type> is not a subclass of reldata.individual.Individual: {}!".format(
                            target_type
                    )
            )
        
        # ensure that the name is a string
        name = str(name)
        
        # prepare context if necessary
        cls._prepare_context()
        
        # fetch current context
        ctx = dc.DataContext.get_context()
        
        # sanitize name if configured to do so
        if cls.check_names:
            if name in ctx[cls._USED_NAMES]:
                raise ValueError("An individual with name '{}' exists already!".format(name))
            ctx[cls._USED_NAMES].add(name)
        
        # create individual
        ctx[cls._LAST_INDEX] += 1
        if target_type is None:
            return _Individual(ctx[cls._LAST_INDEX], name)
        else:
            args = [] if args is None else args
            kwargs = {} if kwargs is None else kwargs
            return target_type(ctx[cls._LAST_INDEX], name, *args, **kwargs)
    
    @classmethod
    def reset(cls) -> None:
        """Resets the ``IndividualFactory`` to its initial state."""
        ctx = dc.DataContext.get_context()
        ctx[cls._LAST_INDEX] = -1
        ctx[cls._USED_NAMES] = set()


# ==================================================================================================================== #
#  CLASS  _  I N D I V I D U A L                                                                                       #
# ==================================================================================================================== #


class _Individual(base_individual.BaseIndividual):
    """A private implementation of :class:`individual.Individual`."""

    def __init__(self, index: int, name: str):
        super().__init__()
        self._index = index
        self._name = name
