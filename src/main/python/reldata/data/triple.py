# -*- coding: utf-8 -*-


import insanity

from reldata.data import individual
from reldata.vocab import relation_type


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
            inferred: bool=False,
            prediction: bool=False
    ):
        """Creates a new instance of `Triple`.

        Args:
            subject (int): Specifies :attr:`subject`.
            predicate (int): Specifies :attr:`predicate`.
            obj (int): Specifies :attr:`Triple.subject`.
            positive (bool): Specifies :attr:`positive`.
            inferred (bool, optional): Specifies :attr:`inferred`.
            prediction (bool, optional): Specifies :attr:`prediction`.
        """
        insanity.sanitize_type("subject", subject, individual.Individual)
        insanity.sanitize_type("predicate", predicate, relation_type.RelationType)
        insanity.sanitize_type("obj", obj, individual.Individual)
        if inferred and prediction:
            raise ValueError("A triple cannot be an inference and a prediction at the same time!")
        
        self._inferred = bool(inferred)
        self._object = obj
        self._positive = bool(positive)
        self._predicate = predicate
        self._prediction = bool(prediction)
        self._subject = subject
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __eq__(self, other):
        return (
                isinstance(other, Triple) and
                other.subject == self._subject and
                other.predicate == self._predicate and
                other.object == self._object and
                other.positive == self._positive and
                other.inferred == self._inferred and
                other.prediction == self._prediction
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
        return "Triple({}, {}, {}, positive = {}, inferred = {}, prediction = {})".format(
                self._subject.index,
                self._predicate.index,
                self._object.index,
                self._positive,
                self._inferred,
                self._prediction
        )
    
    #  PROPERTIES  #####################################################################################################

    @property
    def inferred(self) -> bool:
        """bool: Indicates whether the triple has been inferred rather than specified as fact."""
        return self._inferred
    
    @property
    def is_fact(self) -> bool:
        """bool: Indicates whether the triple is a fact, i.e., neither an inference nor a prediction target."""
        return not self._inferred and not self._prediction
    
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
    def prediction(self) -> bool:
        """bool: Indicates whether the triple is a prediction target, i.e., it is neither a fact nor inferable."""
        return self._prediction
    
    @property
    def subject(self) -> individual.Individual:
        """:class:`individual.Individual`: The individual that is the subject of the triple."""
        return self._subject
