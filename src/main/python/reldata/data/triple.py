# -*- coding: utf-8 -*-


import insanity

from reldata.data import individual
from reldata.vocab import relation_type


__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2017 Patrick Hohenecker"
        "\n\n"
        "Permission is hereby granted, free of charge, to any person obtaining a copy "
        "of this software and associated documentation files (the \"Software\"), to deal "
        "in the Software without restriction, including without limitation the rights "
        "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell "
        "copies of the Software, and to permit persons to whom the Software is "
        "furnished to do so, subject to the following conditions:"
        "\n\n"
        "The above copyright notice and this permission notice shall be included in all "
        "copies or substantial portions of the Software."
        "\n\n"
        "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR "
        "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, "
        "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE "
        "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER "
        "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, "
        "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE "
        "SOFTWARE."
)
__license__ = "MIT License"
__version__ = "2017.1"
__date__ = "Nov 12, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class Triple(object):
    """Describes a link in a knowledge graph.

    Instances of this class can be used to describe data that is present in a knowledge graph. To that end, every
    instance of ``Triple`` represents a so-called triple of the form (subject, predicate, object), which are commonly
    used to describe and store links in knowledge graphs.
    
    This class is also used the specify the absence of triples, which we sometime refer to as "negative triples". To
    that end, :attr:`positive` specifies whether an instance of ``Triple`` describes an existing triple or the fact that
    a certain triple does definitely not exist.
    
    Notice that instances of ``Triple`` are read-only by intention in order to ensure that any changes of the data in
    a ``Triple`` are properly registered by the containing knowledge graph, which would not be possible if they were
    mutable.
    """
    
    def __init__(
            self,
            subject: individual.Individual,
            predicate: relation_type.RelationType,
            obj: individual.Individual,
            positive: bool,
            inferred: bool
    ):
        """Creates a new instance of `Triple`.

        Args:
            subject (int): Specifies :attr:`subject`.
            predicate (int): Specifies :attr:`predicate`.
            obj (int): Specifies :attr:`Triple.subject`.
            positive (bool): Specifies :attr:`positive`.
            inferred (bool): Specifies :attr:`inferred`.
        """
        insanity.sanitize_type("subject", subject, individual.Individual)
        insanity.sanitize_type("predicate", predicate, relation_type.RelationType)
        insanity.sanitize_type("obj", obj, individual.Individual)
        
        self._inferred = bool(inferred)
        self._object = obj
        self._positive = bool(positive)
        self._predicate = predicate
        self._subject = subject
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other):
        return (
                isinstance(other, Triple) and
                other.subject == self._subject and
                other.predicate == self._predicate and
                other.object == self._object and
                other.positive == self._positive and
                other.inferred == self._inferred
        )
    
    def __getitem__(self, item):
        return [self._subject, self._predicate, self._object][item]
    
    def __hash__(self):
        return hash(str(self))
    
    def __iter__(self):
        return iter([self._subject, self._predicate, self._object])
    
    def __len__(self):
        return 3
    
    def __str__(self):
        return "Triple({}, {}, {}, positive = {}, inferred = {})".format(
                self._subject.index,
                self._predicate.index,
                self._object.index,
                self._positive,
                self._inferred
        )
    
    #  PROPERTIES  #####################################################################################################

    @property
    def inferred(self) -> bool:
        """bool: Indicates whether the triple has been inferred or specified."""
        return self._inferred
    
    @property
    def object(self) -> individual.Individual:
        """:class:`individual.Individual`: The individual that is the object of the triple."""
        return self._object

    @property
    def positive(self) -> bool:
        """bool: Indicates whether the triple exists."""
        return self._positive
    
    @property
    def predicate(self) -> relation_type.RelationType:
        """:class:`relation_type.RelationType`: The relation that is the predicate of the triple."""
        return self._predicate
    
    @property
    def subject(self) -> individual.Individual:
        """:class:`individual.Individual`: The individual that is the subject of the triple."""
        return self._subject
