#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import unittest

from reldata import io
from reldata.io import kg_reader
from reldata.io import kg_writer


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


class KgWriterTest(unittest.TestCase):
    
    def test_write(self):
        # load knowledge graph for testing
        # (notice, KgReader has been tested already)
        target_kg = kg_reader.KgReader.read("src/test/resources", "test-kg")
        
        # write knowledge graph
        kg_writer.KgWriter.write(target_kg, ".", "kg-writer-test-knowledge-graph")
        
        # reload written knowledge graph
        kg = kg_reader.KgReader.read(".", "kg-writer-test-knowledge-graph")
        
        # CHECK: knowledge graph was written correctly
        self.assertEqual(target_kg, kg)
        
        # remove created files again
        os.remove(os.path.join(".", "kg-writer-test-knowledge-graph" + io.CLASSES_VOCAB_EXT))
        os.remove(os.path.join(".", "kg-writer-test-knowledge-graph" + io.CLASSES_SPEC_EXT))
        os.remove(os.path.join(".", "kg-writer-test-knowledge-graph" + io.CLASSES_INF_EXT))
        os.remove(os.path.join(".", "kg-writer-test-knowledge-graph" + io.LITERALS_VOCAB_EXT))
        os.remove(os.path.join(".", "kg-writer-test-knowledge-graph" + io.LITERALS_SPEC_EXT))
        os.remove(os.path.join(".", "kg-writer-test-knowledge-graph" + io.LITERALS_INF_EXT))
        os.remove(os.path.join(".", "kg-writer-test-knowledge-graph" + io.RELATIONS_VOCAB_EXT))
        os.remove(os.path.join(".", "kg-writer-test-knowledge-graph" + io.RELATIONS_SPEC_EXT))
        os.remove(os.path.join(".", "kg-writer-test-knowledge-graph" + io.RELATIONS_INF_EXT))
        os.remove(os.path.join(".", "kg-writer-test-knowledge-graph" + io.INDIVIDUALS_SPEC_EXT))


if __name__ == "__main__":
    unittest.main()
