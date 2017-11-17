#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

from reldata import data_context as dc
from reldata import individual_factory
from reldata.data import base_individual


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


class IndividualFactoryTest(unittest.TestCase):
    
    def test_create_individual(self):
        factory = individual_factory.IndividualFactory
        
        # CHECK: factory assigns indices as expected
        factory.reset()
        ind_0 = factory.create_individual("ind-0")
        ind_1 = factory.create_individual("ind-1")
        self.assertEqual(0, ind_0.index)
        self.assertEqual(1, ind_1.index)
        
        # CHECK: enforcing unique names works as expected
        factory.check_names = False
        factory.create_individual("SAME-NAME")
        factory.create_individual("SAME-NAME")  # -> no error
        factory.check_names = True
        factory.create_individual("SAME-NAME")
        with self.assertRaises(ValueError):
            factory.create_individual("SAME-NAME")
        
        # CHECK: the factory uses contexts correctly
        factory.reset()
        ind_0 = factory.create_individual("ind-0")
        with dc.DataContext():
            ind_1 = factory.create_individual("ind-1")
            with dc.DataContext():
                ind_2 = factory.create_individual("ind-2")
            ind_3 = factory.create_individual("ind-3")
        ind_4 = factory.create_individual("ind-4")
        self.assertEqual(0, ind_0.index)
        self.assertEqual(0, ind_1.index)
        self.assertEqual(0, ind_2.index)
        self.assertEqual(1, ind_3.index)
        self.assertEqual(1, ind_4.index)
        
        # CHECK: the factory correctly creates sub-types of Individual
        factory.reset()
        my_ind = factory.create_individual(
                "my-ind",
                target_type=MyIndividual,
                args=[False],
                kwargs={"school": "Oxford"}
        )
        self.assertIsInstance(my_ind, MyIndividual)
        self.assertEqual(0, my_ind.index)
        self.assertEqual("my-ind", my_ind.name)
        self.assertEqual(False, my_ind.female)
        self.assertEqual("Oxford", my_ind.school)
        
        # CHECK: the target type has to be a type, otherwise a TypeError is raised
        factory.reset()
        with self.assertRaises(TypeError):
            factory.create_individual("ind", target_type=0)
        
        # CHECK: providing an illegal target type causes a ValueError
        factory.reset()
        with self.assertRaises(ValueError):
            factory.create_individual("ind", target_type=int)


class MyIndividual(base_individual.BaseIndividual):
    
    def __init__(self, index, name, female: bool, school: str=None):
        super().__init__()
        self._index = index
        self._name = name
        self._female = female
        self._school = school
    
    @property
    def female(self):
        return self._female
    
    @property
    def school(self):
        return self._school


if __name__ == "__main__":
    unittest.main()
