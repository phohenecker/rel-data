#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

import reldata

from reldata.data import class_membership
from reldata.data import data_context as dc
from reldata.data import individual
from reldata.data import individual_factory
from reldata.data import knowledge_graph
from reldata.data import literal_value
from reldata.data import triple
from reldata.util import observable_set
from reldata.util import ordered_set
from reldata.vocab import class_type
from reldata.vocab import class_type_factory as ctf
from reldata.vocab import literal_type
from reldata.vocab import literal_type_factory as ltf
from reldata.vocab import relation_type
from reldata.vocab import relation_type_factory as rtf


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
__date__ = "Nov 13, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class KnowledgeGraphTest(unittest.TestCase):
    
    def setUp(self):
        # prepare factories
        reldata.reset()
        individual_factory.IndividualFactory.check_names = False
        
        # create test classes
        self.cls_0 = ctf.ClassTypeFactory.create_class("class-0")
        self.cls_1 = ctf.ClassTypeFactory.create_class("class-1")
        
        self.rel_0 = rtf.RelationTypeFactory.create_relation("relation-0")
        
        # create test literals
        self.lit_0 = ltf.LiteralTypeFactory.create_literal("literal-0")
    
    def test_adding_individuals(self):
        # create test individual
        ind = individual_factory.IndividualFactory.create_individual("individual-0")
        ind.classes.add(class_membership.ClassMembership(self.cls_0, True, False))
        ind.classes.add(class_membership.ClassMembership(self.cls_1, False, True))
        ind.literals.add(literal_value.LiteralValue(self.lit_0, 666, False))
        
        # create test knowledge graph
        kg = knowledge_graph.KnowledgeGraph()
        kg.individuals.add(ind)
        
        # CHECK: the individual was stored
        target_individuals = ordered_set.OrderedSet(individual.Individual, lambda x: x.index, data=[ind])
        self.assertEqual(target_individuals, kg.individuals)
        
        # CHECK: the individual's classes were registered
        target_classes = ordered_set.OrderedSet(class_type.ClassType, lambda x: x.index, data=[self.cls_0, self.cls_1])
        self.assertEqual(target_classes, kg.classes)
        
        # CHECK: the individual's literals were registered
        target_literals = ordered_set.OrderedSet(literal_type.LiteralType, lambda x: x.index, data=[self.lit_0])
        self.assertEqual(target_literals, kg.literals)
    
    def test_adding_triples(self):
        # create test individuals
        ind_0 = individual_factory.IndividualFactory.create_individual("individual-0")
        ind_0.classes.add(class_membership.ClassMembership(self.cls_0, True, False))
        ind_0.literals.add(literal_value.LiteralValue(self.lit_0, 666, True))

        # create test individuals
        ind_1 = individual_factory.IndividualFactory.create_individual("individual-1")
        ind_1.classes.add(class_membership.ClassMembership(self.cls_1, False, True))
        
        # create test triple
        tri = triple.Triple(ind_0, self.rel_0, ind_1, True, False)

        # create test knowledge graph
        kg = knowledge_graph.KnowledgeGraph()
        kg.triples.add(tri)

        # CHECK: the triple was stored
        target_triples = observable_set.ObservableSet(triple.Triple, data=[tri])
        self.assertEqual(target_triples, kg.triples)
        
        # CHECK: the relation was registered
        target_relations = ordered_set.OrderedSet(relation_type.RelationType, lambda x: x.index, data=[self.rel_0])
        self.assertEqual(target_relations, kg.relations)
        
        # CHECK: the individuals in the triple were registered
        target_individuals = ordered_set.OrderedSet(individual.Individual, lambda x: x.index, data=[ind_0, ind_1])
        self.assertEqual(target_individuals, kg.individuals)

        # CHECK: the individuals' classes were registered
        target_classes = ordered_set.OrderedSet(class_type.ClassType, lambda x: x.index, data=[self.cls_0, self.cls_1])
        self.assertEqual(target_classes, kg.classes)

        # CHECK: the individuals' literals were registered
        target_literals = ordered_set.OrderedSet(literal_type.LiteralType, lambda x: x.index, data=[self.lit_0])
        self.assertEqual(target_literals, kg.literals)
    
    @dc.new_context
    def test_modifying_individuals(self):
        # create test data
        kg = knowledge_graph.KnowledgeGraph()
        cls = ctf.ClassTypeFactory.create_class("class-0")
        lit = ltf.LiteralTypeFactory.create_literal("literal-0")
        ind = individual_factory.IndividualFactory.create_individual("individual-0")
        
        # add individual to knowledge graph
        kg.individuals.add(ind)
        
        # CHECK: new classes are registered if an individual is changed
        ind.classes.add(class_membership.ClassMembership(cls, True, False))
        self.assertTrue(cls in kg.classes)
        
        # CHECK: new literals are registered if an individual is changed
        ind.literals.add(literal_value.LiteralValue(lit, 666, False))
        self.assertTrue(lit in kg.literals)


if __name__ == "__main__":
    unittest.main()
