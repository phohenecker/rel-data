# -*- coding: utf-8 -*-


import typing

from reldata.data import class_membership
from reldata.data import individual
from reldata.data import individual_observer
from reldata.data import literal_value
from reldata.data import triple
from reldata.util import observable_set
from reldata.util import ordered_set
from reldata.util import set_observer
from reldata.vocab import class_type
from reldata.vocab import literal_type
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
__license__ = "Simplified BSD License"
__version__ = "2017.1"
__date__ = "Nov 12, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class KnowledgeGraph(set_observer.SetObserver, individual_observer.IndividualObserver):
    """An instance of this class represents a knowledge graph including its vocabulary as well as all of its data."""

    def __init__(self):
        """Creates a new empty ``KnowledgeGraph``."""
        self._classes = ordered_set.OrderedSet(class_type.ClassType, lambda c: c.index)
        self._classes.add_observer(self)
        self._relations = ordered_set.OrderedSet(relation_type.RelationType, lambda r: r.index)
        self._relations.add_observer(self)
        self._literals = ordered_set.OrderedSet(literal_type.LiteralType, lambda l: l.index)
        self._literals.add_observer(self)
        
        self._individuals = ordered_set.OrderedSet(individual.Individual, lambda i: i.index)
        self._individuals.add_observer(self)
        self._triples = observable_set.ObservableSet(triple.Triple)
        self._triples.add_observer(self)
    
    #  MAGIC FUNCTIONS  ################################################################################################
    
    def __contains__(
            self,
            item: typing.Union[
                    class_type.ClassType,
                    relation_type.RelationType,
                    literal_type.LiteralType,
                    individual.Individual,
                    triple.Triple
            ]
    ) -> bool:
        if isinstance(item, class_type.ClassType):
            return item in self._classes
        elif isinstance(item, relation_type.RelationType):
            return item in self._relations
        elif isinstance(item, literal_type.LiteralType):
            return item in self._literals
        elif isinstance(item, individual.Individual):
            return item in self._individuals
        elif isinstance(item, triple.Triple):
            return item in self._triples
        else:
            raise TypeError("A KnowledgeGraph cannot contain objects of type {}!".format(type(item)))
    
    def __eq__(self, other) -> bool:
        return (
                isinstance(other, KnowledgeGraph) and
                other.classes == self._classes and
                other.relations == self._relations and
                other.literals == self._literals and
                other.individuals == self._individuals and
                other.triples == self._triples
        )
    
    #  PROPERTIES  #####################################################################################################
    
    @property
    def classes(self) -> ordered_set.OrderedSet[class_type.ClassType]:
        """:class:`ordered_set.OrderedSet`: The classes that appear in the ``KnowledgeGraph``."""
        return self._classes
    
    @property
    def individuals(self) -> ordered_set.OrderedSet[individual.Individual]:
        """:class:`ordered_set.OrderedSet`: The individuals that appear in the ``KnowledgeGraph``."""
        return self._individuals

    @property
    def literals(self) -> ordered_set.OrderedSet[literal_type.LiteralType]:
        """:class:`ordered_set.OrderedSet`: The literals that appear in the ``KnowledgeGraph``."""
        return self._literals

    @property
    def relations(self) -> ordered_set.OrderedSet[relation_type.RelationType]:
        """:class:`ordered_set.OrderedSet`: The relations that appear in the ``KnowledgeGraph``."""
        return self._relations
    
    @property
    def triples(self) -> observable_set.ObservableSet[triple.Triple]:
        """:class:`observable_set.ObservableSet`: The triples that appear in the ``KnowledgeGraph``."""
        return self._triples
    
    #  METHODS  ########################################################################################################
    
    def _register_individual(self, i: individual.Individual) -> None:
        """Registers an individual that was added to the ``KnowledgeGraph``.
        
        If the new triple contains class types or literal types that are not part the ``KnowledgeGraph`` yet, then they
        are added automatically.
        
        Args:
            i (:class:`individual.Individual`): The individual to add.
        """
        # store individual
        self._individuals.add(i)
        i.add_observer(self)
        
        # add any missing classes
        for cls in map(lambda cls_mem: cls_mem.cls, i.classes):
            self._classes.add(cls)
        
        # add any missing labels
        for lit in map(lambda lit_value: lit_value.literal, i.literals):
            self._literals.add(lit)
    
    def _register_triple(self, t: triple.Triple) -> None:
        """Registers a triple that was added to the ``KnowledgeGraph``.

        If the new triple contains a relation type, literal types, or individuals that are not part the
        ``KnowledgeGraph`` yet, then they are added automatically.

        Args:
            t (:class:`triple.Triple`): The triple that was added.
        """
        # add relation if missing
        self._relations.add(t.predicate)
        
        # add any missing individuals
        self._register_individual(t.subject)
        self._register_individual(t.object)
    
    def class_added(self, ind, cls: class_membership.ClassMembership) -> None:
        self._classes.add(cls.cls)
    
    def class_removed(self, ind, cls: class_membership.ClassMembership) -> None:
        pass  # nothing

    def element_added(self, elem) -> None:
        if isinstance(elem, individual.Individual):
            self._register_individual(elem)
        elif isinstance(elem, triple.Triple):
            self._register_triple(elem)

    def element_removed(self, elem: typing.Union[individual.Individual, triple.Triple]) -> None:
        pass  # nothing to do

    def literal_added(self, ind, lit: literal_value.LiteralValue) -> None:
        self._literals.add(lit.literal)
    
    def literal_removed(self, ind, lit: literal_value.LiteralValue) -> None:
        pass  # nothing to do
