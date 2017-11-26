#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import threading
import unittest

from reldata.data import data_context as dc
from reldata.data import individual_factory
from reldata.data import knowledge_graph


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
__date__ = "Nov 14, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class DataContextTest(unittest.TestCase):
    
    def test_clear(self):
        ctx = dc.DataContext.get_context()
        ctx["data-context-test.test-item"] = 666
        ctx.clear()
        
        # CHECK: the previously added item has been removed from the context
        self.assertIsNone(ctx["data-context-test.test-item"])
    
    def test_enter_exit(self):
        dc.DataContext.get_context()["data-context-test.outer-item"] = 101
        
        with dc.DataContext() as ctx:
            ctx["data-context-test.inner-item"] = 666
            
            # CHECK: the outer context is not available any longer
            self.assertIsNone(ctx["data-context-test.outer-item"])
            self.assertIsNone(dc.DataContext.get_context()["data-context-test.outer-item"])
            
            # CHECK: the inner context is new default context
            self.assertEqual(
                    666,
                    dc.DataContext.get_context()["data-context-test.inner-item"]
            )
        
        # CHECK: the outer context is reinstated
        self.assertEqual(
                101,
                dc.DataContext.get_context()["data-context-test.outer-item"]
        )
        
        # CHECK: the inner context is not available any longer
        self.assertIsNone(dc.DataContext.get_context()["data-context-test.inner-item"])
    
    def test_get_set_item(self):
        ctx = dc.DataContext.get_context()
        ctx["data-context-test.int-test-item"] = 666
        ctx["data-context-test.str-test-item"] = "666"
        
        # CHECK: all of the specified values are stored properly
        self.assertEqual(666, ctx["data-context-test.int-test-item"])
        self.assertEqual("666", ctx["data-context-test.str-test-item"])
    
    def test_new_context(self):
        # define a test function that has its own context
        @dc.new_context
        def func_with_own_context():
            return individual_factory.IndividualFactory.create_individual("individual-0")
        
        with dc.DataContext():
            # change current context
            individual_factory.IndividualFactory.create_individual("individual-0")
            individual_factory.IndividualFactory.create_individual("individual-1")
            # -> next ID is 2
            
            # CHECK: the function does indeed use a new context when it is invoked
            ind = func_with_own_context()
            self.assertEqual(0, ind.index)
            self.assertEqual("individual-0", ind.name)
    
    def test_threading_support(self):
        # create a target knowledge graph
        with dc.DataContext():
            target_kg = knowledge_graph.KnowledgeGraph()
            for i in range(100):
                target_kg.individuals.add(
                        individual_factory.IndividualFactory.create_individual("individual-{}".format(i))
                )
            
        # stores three KGs to be created in 3 threads
        kgs = [None, None, None]
        
        # this is the KG-creation method that is executed by the threads
        def create_kg(kg_list: list, index: int):
            local_kg = knowledge_graph.KnowledgeGraph()
            for x in range(100):
                local_kg.individuals.add(
                        individual_factory.IndividualFactory.create_individual("individual-{}".format(x))
                )
            kg_list[index] = local_kg

        # create the same KG simultaneously in 3 threads
        t_1 = threading.Thread(target=create_kg, args=(kgs, 0))
        t_2 = threading.Thread(target=create_kg, args=(kgs, 1))
        t_3 = threading.Thread(target=create_kg, args=(kgs, 2))
        t_1.start()
        t_2.start()
        t_3.start()
        t_1.join()
        t_2.join()
        t_3.join()
        
        # CHECK: all created KGs are equal to the expected target
        self.assertEqual(target_kg, kgs[0])
        self.assertEqual(target_kg, kgs[1])
        self.assertEqual(target_kg, kgs[2])


if __name__ == "__main__":
    unittest.main()
