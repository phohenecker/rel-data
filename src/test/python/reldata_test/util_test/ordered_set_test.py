#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest

from reldata.util import ordered_set


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
__date__ = "Nov 13, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class OrderedSetTest(unittest.TestCase):
    
    def test_add(self):
        test_set = ordered_set.OrderedSet(str, lambda x: int(x))
        
        # CHECK: ensure that added values are ordered
        test_set.add("2")
        self.assertEqual(["2"], list(test_set))
        test_set.add("0")
        self.assertEqual(["0", "2"], list(test_set))
        test_set.add("1")
        self.assertEqual(["0", "1", "2"], list(test_set))
        test_set.add("10")
        self.assertEqual(["0", "1", "2", "10"], list(test_set))
        
        # CHECK: adding element multiple times does not change set
        test_set.add("10")
        self.assertEqual(["0", "1", "2", "10"], list(test_set))
        self.assertEqual(4, len(test_set))
        
        # CHECK: length is updated correctly after adding elements
        self.assertEqual(4, len(test_set))
    
        # CHECK: adding illegal types causes error
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            test_set.add(999)
    
    def test_add_all(self):
        test_set = ordered_set.OrderedSet(str, lambda x: int(x))
        
        # CHECK: ensure that added values are ordered
        test_set.add_all(["5", "3", "7", "1"])
        self.assertEqual(["1", "3", "5", "7"], list(test_set))
        
        # CHECK: length is updated correctly after adding elements
        self.assertEqual(4, len(test_set))
        
        # CHECK: passing a non-iterable causes error
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            test_set.add_all(999)
        
        # CHECK: providing an iterable with illegally typed elements causes error
        with self.assertRaises(TypeError):
            test_set.add_all([999, "1000"])
    
    def test_contains(self):
        test_set = ordered_set.OrderedSet(str, lambda x: int(x))
        test_set.add_all(["1", "3", "5", "7"])
        
        self.assertTrue("3" in test_set)
        self.assertFalse("4" in test_set)
    
    def test_equal(self):
        test_set_1 = ordered_set.OrderedSet(str, lambda x: int(x))
        test_set_1.add_all(["1", "2", "3"])
        test_set_2 = ordered_set.OrderedSet(str, lambda x: int(x))
        test_set_2.add_all(["1", "2", "3"])
        test_set_3 = ordered_set.OrderedSet(str, lambda x: int(x))
        test_set_3.add_all(["2", "3"])
        test_set_4 = ordered_set.OrderedSet(int, lambda x: x)
        test_set_4.add_all([1, 2, 3])
        
        # CHECK: equality works for equal sets
        self.assertEqual(test_set_1, test_set_2)
        
        # CHECK: equality works for different sets
        self.assertNotEqual(test_set_1, test_set_3)
    
    def test_get_item(self):
        test_set = ordered_set.OrderedSet(str, lambda x: int(x))
        test_set.add_all(["1", "3", "5", "7"])
        
        # CHECK: indexing existing elements yields correct value
        self.assertEqual("3", test_set[3])
        self.assertEqual("7", test_set[7])

        # CHECK: indexing non-existing elements causes KeyError
        with self.assertRaises(KeyError):
            # noinspection PyStatementEffect
            test_set[999]

        # CHECK: indexing with illegal type causes KeyError
        with self.assertRaises(KeyError):
            # noinspection PyStatementEffect,PyTypeChecker
            test_set["3"]

    # noinspection PyTypeChecker
    def test_init(self):
        # CHECK: create an empty set does not cause any errors
        ordered_set.OrderedSet(str, lambda x: int(x))
        
        # CHECK: create set with initial data provided
        test_set = ordered_set.OrderedSet(str, lambda x: int(x), data=["3", "1"])
        self.assertEqual(["1", "3"], list(test_set))
        
        # CHECK: providing illegally typed args causes TypeError
        with self.assertRaises(TypeError):
            ordered_set.OrderedSet("str", lambda x: int(x))
        with self.assertRaises(TypeError):
            ordered_set.OrderedSet(str, "a function")
        with self.assertRaises(TypeError):
            ordered_set.OrderedSet(str, lambda x: int(x), data=666)
        with self.assertRaises(TypeError):
            ordered_set.OrderedSet(str, lambda x: int(x), data=[1, 3, 5])
    
    def test_remove(self):
        test_set = ordered_set.OrderedSet(str, lambda x: int(x))
        test_set.add_all(["1", "3", "5", "7"])

        # CHECK: ensure that values are removed properly by value
        test_set.remove("3")
        self.assertEqual(["1", "5", "7"], list(test_set))
        test_set.remove("1")
        self.assertEqual(["5", "7"], list(test_set))
        
        # CHECK: ensure that values are removed properly by idnex
        test_set.remove(7)
        self.assertEqual(["5"], list(test_set))

        # CHECK: length is updated correctly after removing elements
        self.assertEqual(1, len(test_set))
        
        # CHECK: removing non-existing elements causes ValueError
        with self.assertRaises(KeyError):
            test_set.remove("999")
        
        # CHECK: providing illegally typed element causes TypeError
        with self.assertRaises(KeyError):
            # noinspection PyTypeChecker
            test_set.remove(["1", "2"])


if __name__ == "__main__":
    unittest.main()
