# -*- coding: utf-8 -*-

"""This package provides classes for specifying the actual data, both factual and inferred, in a knowledge graph."""


from reldata.data.base_individual import BaseIndividual
from reldata.data.class_membership import ClassMembership
from reldata.data.data_context import DataContext
from reldata.data.data_context import new_context
from reldata.data.individual import Individual
from reldata.data.individual_factory import IndividualFactory
from reldata.data.knowledge_graph import KnowledgeGraph
from reldata.data.literal_value import LiteralValue
from reldata.data.triple import Triple


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
__date__ = "Nov 15, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"
