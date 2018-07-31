# -*- coding: utf-8 -*-


import unittest

from concurrent import futures

from reldata.data import class_membership
from reldata.data import data_context as dc
from reldata.data import individual_factory
from reldata.data import knowledge_graph
from reldata.data import literal_value
from reldata.data import triple
from reldata.io import kg_reader
from reldata.vocab import class_type_factory as ctf
from reldata.vocab import literal_type_factory as ltf
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


class KgReaderTest(unittest.TestCase):
    
    def test_read(self):
        # //////// Knowledge Graph -------------------------------------------------------------------------------------
        
        # this knowledge graph describes what is specified in the files src/test/resources/test-kg.*
        
        with dc.DataContext():
            target_kg = knowledge_graph.KnowledgeGraph()
    
            target_kg.classes.add_all(
                    [
                            ctf.ClassTypeFactory.create_class("class-0"),
                            ctf.ClassTypeFactory.create_class("class-1"),
                            ctf.ClassTypeFactory.create_class("class-2")
                    ]
            )
            target_kg.relations.add_all(
                    [
                            rtf.RelationTypeFactory.create_relation("relation-0"),
                            rtf.RelationTypeFactory.create_relation("relation-1")
                    ]
            )
            target_kg.literals.add_all(
                    [
                            ltf.LiteralTypeFactory.create_literal("literal-0"),
                            ltf.LiteralTypeFactory.create_literal("literal-1")
                    ]
            )
            
            ind_0 = individual_factory.IndividualFactory.create_individual("individual-0")
            ind_0.classes.add(class_membership.ClassMembership(target_kg.classes[0], True))
            ind_0.classes.add(class_membership.ClassMembership(target_kg.classes[1], True, prediction=True))
            ind_0.classes.add(class_membership.ClassMembership(target_kg.classes[2], False, inferred=True))
            ind_0.literals.add(literal_value.LiteralValue(target_kg.literals[1], "0-lit-1", prediction=True))
            ind_1 = individual_factory.IndividualFactory.create_individual("individual-1")
            ind_1.classes.add(class_membership.ClassMembership(target_kg.classes[1], False))
            ind_1.classes.add(class_membership.ClassMembership(target_kg.classes[0], True, inferred=True))
            ind_1.literals.add(literal_value.LiteralValue(target_kg.literals[1], "1-lit-1", inferred=True))
            ind_2 = individual_factory.IndividualFactory.create_individual("individual-2")
            ind_2.classes.add(class_membership.ClassMembership(target_kg.classes[2], True,))
            ind_2.classes.add(class_membership.ClassMembership(target_kg.classes[0], False, inferred=True))
            ind_2.literals.add(literal_value.LiteralValue(target_kg.literals[0], "2-lit-0"))
            ind_3 = individual_factory.IndividualFactory.create_individual("individual-3")
            ind_3.classes.add(class_membership.ClassMembership(target_kg.classes[0], False))
            ind_3.classes.add(class_membership.ClassMembership(target_kg.classes[1], False, prediction=True))
            ind_3.classes.add(class_membership.ClassMembership(target_kg.classes[2], True, inferred=True))
            ind_3.literals.add(literal_value.LiteralValue(target_kg.literals[0], "3-lit-0"))
            ind_3.literals.add(literal_value.LiteralValue(target_kg.literals[1], "3-lit-1"))
    
            target_kg.triples.add(triple.Triple(ind_0, target_kg.relations[1], ind_2, True))
            target_kg.triples.add(triple.Triple(ind_3, target_kg.relations[0], ind_1, False))
            target_kg.triples.add(triple.Triple(ind_3, target_kg.relations[0], ind_0, False, inferred=True))
            target_kg.triples.add(triple.Triple(ind_2, target_kg.relations[1], ind_1, True, inferred=True))
            target_kg.triples.add(triple.Triple(ind_0, target_kg.relations[0], ind_1, False, prediction=True))
            target_kg.triples.add(triple.Triple(ind_1, target_kg.relations[0], ind_0, True, prediction=True))

        # //////// Tests -----------------------------------------------------------------------------------------------
        
        # load knowledge graph
        kg = kg_reader.KgReader.read("src/test/resources", "test-kg")
        
        # CHECK: vocabulary, individuals and triples of loaded graph are correct
        self.assertEqual(target_kg, kg)
        
        # iterate over all individuals in the loaded graph
        for ind in kg.individuals:
            target_ind = target_kg.individuals[ind.index]
            
            # CHECK: class memberships and literals were loaded correctly
            self.assertEqual(target_ind.classes, ind.classes)
            self.assertEqual(target_ind.literals, ind.literals)
    
    def test_read_all(self):
        # the data that will be loaded
        input_dir = "src/test/resources"
        base_name = "test-kg"
        
        # the resources dir contains one knowledge graph, which should be discovered and loaded
        target_kgs = [kg_reader.KgReader.read(input_dir, base_name)]
        
        # load all knowledge graphs from resources dir
        all_kgs = kg_reader.KgReader.read_all(input_dir)
        
        # CHECK: the knowledge graphs were loaded correctly
        self.assertEqual(target_kgs, all_kgs)
        
        # load all knowledge graphs with a thread pool
        pool = futures.ThreadPoolExecutor(max_workers=1)
        all_kgs = kg_reader.KgReader.read_all(input_dir, executor=pool)
        pool.shutdown()
        
        # CHECK: the knowledge graphs were loaded correctly (with the thread pool)
        self.assertEqual(target_kgs, all_kgs)

        # load all knowledge graphs with a process pool
        pool = futures.ProcessPoolExecutor(max_workers=1)
        all_kgs = kg_reader.KgReader.read_all(input_dir, executor=pool)
        pool.shutdown()

        # CHECK: the knowledge graphs were loaded correctly (with the process pool)
        self.assertEqual(target_kgs, all_kgs)
        

if __name__ == "__main__":
    unittest.main()
