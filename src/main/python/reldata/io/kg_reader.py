# -*- coding: utf-8 -*-


import os
import re

from reldata import io
from reldata.data import class_membership
from reldata.data import data_context as dc
from reldata.data import individual_factory
from reldata.data import knowledge_graph
from reldata.data import literal_value
from reldata.data import triple
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
__license__ = "Simplified BSD License"
__version__ = "2017.1"
__date__ = "Nov 13, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class KgReader(object):
    """A class for reading :class:`knowledge_graph.KnowledgeGraph`s from the disk."""
    
    MEMBERSHIPS_REGEX = r"0|1|-1"
    """str: A regular expression for parsing class memberships."""
    
    TRIPLE_REGEX = r"^\s*(?P<subject>\S+)\s+(?P<predicate>\S+)\s+(?P<object>\S+)\s*$"
    """str: A regular expression for parsing triples."""

    TYPED_TRIPLE_REGEX = r"^\s*(?P<type>[\+-])\s*(?P<subject>\S+)\s+(?P<predicate>\S+)\s+(?P<object>\S+)\s*$"
    """str: A regular expression for parsing triples that are marked as positive and negative, respectively."""
    
    VOCAB_REGEX = r"^\s*(?P<index>[0-9]+)\s+(?P<name>[\S]+)\s*$"
    """str: A regular expression for parsing class/relation/literal definitions."""
    
    #  METHODS  ########################################################################################################
    
    @classmethod
    @dc.new_context
    def read(cls, input_dir: str, basename: str) -> knowledge_graph.KnowledgeGraph:
        """Loads a knowledge graph from the specified location.
        
        Args:
            input_dir (str): The directory that contains all of the files.
            basename (str): The base name, i.e., the prefix, included in all files' names.
        
        Returns:
            :class:`knowledge_graph.KnowledgeGraph`: A knowledge graph that has been populated according to the read
                information.
        
        Raises:
            ValueError: If ``input_dir`` does not refer to an existing directory or if any of the needed files is
                missing.
        """
        # //////// Sanitize Args ---------------------------------------------------------------------------------------
        
        # ensure that the inputs are strings
        input_dir = str(input_dir)
        basename = str(basename)
        
        # assemble all needed paths
        # the used postfixes have the following meanings:
        # * _vocab -> definition of a class/relation/literal
        # * _spec  -> user-defined data
        # * _inf   -> inferred data
        individual_spec = os.path.join(input_dir, basename + io.INDIVIDUALS_SPEC_EXT)
        classes_vocab = os.path.join(input_dir, basename + io.CLASSES_VOCAB_EXT)
        classes_spec = os.path.join(input_dir, basename + io.CLASSES_SPEC_EXT)
        classes_inf = os.path.join(input_dir, basename + io.CLASSES_INF_EXT)
        relations_vocab = os.path.join(input_dir, basename + io.RELATIONS_VOCAB_EXT)
        relations_spec = os.path.join(input_dir, basename + io.RELATIONS_SPEC_EXT)
        relations_inf = os.path.join(input_dir, basename + io.RELATIONS_INF_EXT)
        literals_vocab = os.path.join(input_dir, basename + io.LITERALS_VOCAB_EXT)
        literals_spec = os.path.join(input_dir, basename + io.LITERALS_SPEC_EXT)
        literals_inf = os.path.join(input_dir, basename + io.LITERALS_INF_EXT)
        
        # check whether the input directory exists
        if not os.path.isdir:
            raise ValueError("The provided <input_dir> does not exist: '{}'!".format(input_dir))
        
        # check whether all of the needed files exist:
        if not os.path.isfile(individual_spec):
            raise ValueError("Missing file: '{}'!".format(individual_spec))
        if not os.path.isfile(classes_vocab):
            raise ValueError("Missing file: '{}'!".format(classes_vocab))
        if not os.path.isfile(classes_spec):
            raise ValueError("Missing file: '{}'!".format(classes_spec))
        if not os.path.isfile(classes_inf):
            raise ValueError("Missing file: '{}'!".format(classes_inf))
        if not os.path.isfile(relations_vocab):
            raise ValueError("Missing file: '{}'!".format(relations_vocab))
        if not os.path.isfile(relations_spec):
            raise ValueError("Missing file: '{}'!".format(relations_spec))
        if not os.path.isfile(relations_inf):
            raise ValueError("Missing file: '{}'!".format(relations_inf))
        if not os.path.isfile(literals_vocab):
            raise ValueError("Missing file: '{}'!".format(literals_vocab))
        if not os.path.isfile(literals_spec):
            raise ValueError("Missing file: '{}'!".format(literals_spec))
        if not os.path.isfile(literals_inf):
            raise ValueError("Missing file: '{}'!".format(literals_inf))
    
        # //////// Read Vocabulary ---------------------------------------------------------------------------------
        
        # create new empty knowledge graph
        kg = knowledge_graph.KnowledgeGraph()
        
        # read classes
        with open(classes_vocab, "r") as f:
            for index, line in enumerate(f):
                if line == "":
                    continue
                m = re.match(cls.VOCAB_REGEX, line)
                assert int(m.group("index")) == index
                kg.classes.add(ctf.ClassTypeFactory.create_class(m.group("name")))
        
        # read relations
        with open(relations_vocab, "r") as f:
            for index, line in enumerate(f):
                if line == "":
                    continue
                m = re.match(cls.VOCAB_REGEX, line)
                assert int(m.group("index")) == index
                kg.relations.add(rtf.RelationTypeFactory.create_relation(m.group("name")))
        
        # read literals
        with open(literals_vocab, "r") as f:
            for index, line in enumerate(f):
                if line == "":
                    continue
                m = re.match(cls.VOCAB_REGEX, line)
                assert int(m.group("index")) == index
                kg.literals.add(ltf.LiteralTypeFactory.create_literal(m.group("name")))
        
        # //////// Read Individuals --------------------------------------------------------------------------------
        
        with open(individual_spec, "r") as f:
            for index, line in enumerate(f):
                if line == "":
                    continue
                m = re.match(cls.VOCAB_REGEX, line)
                assert int(m.group("index")) == index
                kg.individuals.add(individual_factory.IndividualFactory.create_individual(m.group("name")))

        # //////// Read Class Memberships --------------------------------------------------------------------------

        # read specified memberships
        with open(classes_spec, "r") as f:
            for individual_index, line in enumerate(f):  # run through all individuals
                if line == "":
                    continue
                current_ind = kg.individuals[individual_index]
                for class_index, mem in enumerate(map(int, re.findall(cls.MEMBERSHIPS_REGEX, line))):
                    if mem != 0:  # only consider specified memberships
                        current_ind.classes.add(
                                class_membership.ClassMembership(
                                        kg.classes[class_index],
                                        mem == 1,
                                        False  # not inferred
                                )
                        )
        
        # read inferred memberships
        with open(classes_inf, "r") as f:
            for individual_index, line in enumerate(f):  # run through all individuals
                if line == "":
                    continue
                current_ind = kg.individuals[individual_index]
                for class_index, mem in enumerate(map(int, re.findall(cls.MEMBERSHIPS_REGEX, line))):
                    if mem != 0:  # only consider specified memberships
                        current_ind.classes.add(
                            class_membership.ClassMembership(
                                kg.classes[class_index],
                                mem == 1,
                                True  # inferred
                            )
                        )

        # //////// Read Literals -----------------------------------------------------------------------------------
        
        # read specified literals
        with open(literals_spec, "r") as f:
            for line in f:
                if line == "":
                    continue
                
                # parse read line
                m = re.match(cls.TRIPLE_REGEX, line)
                
                # fetch respective individual, literal, and value
                current_ind = kg.individuals[int(m.group("subject"))]
                current_lit = kg.literals[int(m.group("predicate"))]
                current_value = m.group("object")
                
                # add literal to individual
                current_ind.literals.add(
                        literal_value.LiteralValue(
                                current_lit,
                                current_value,
                                False  # not inferred
                        )
                )
        
        # read inferred literals
        with open(literals_inf, "r") as f:
            for line in f:
                if line == "":
                    continue
                
                # parse read line
                m = re.match(cls.TRIPLE_REGEX, line)
        
                # fetch respective individual, literal, and value
                current_ind = kg.individuals[int(m.group("subject"))]
                current_lit = kg.literals[int(m.group("predicate"))]
                current_value = m.group("object")
        
                # add literal to individual
                current_ind.literals.add(
                        literal_value.LiteralValue(
                                current_lit,
                                current_value,
                                True  # inferred
                        )
                )
        
        # //////// Read Triples ------------------------------------------------------------------------------------
        
        # read specified triples
        with open(relations_spec, "r") as f:
            for line in f:
                if line == "":
                    continue
                
                # parse read line
                m = re.match(cls.TYPED_TRIPLE_REGEX, line)
    
                # fetch respective individual, literal, and value
                positive = m.group("type") == "+"
                sub = kg.individuals[int(m.group("subject"))]
                pred = kg.relations[int(m.group("predicate"))]
                obj = kg.individuals[int(m.group("object"))]
                
                # add triple
                kg.triples.add(triple.Triple(sub, pred, obj, positive, False))  # False -> not inferred
        
        # read inferred triples
        with open(relations_inf, "r") as f:
            for line in f:
                if line == "":
                    continue
                    
                # parse read line
                m = re.match(cls.TYPED_TRIPLE_REGEX, line)
        
                # fetch respective individual, literal, and value
                positive = m.group("type") == "+"
                sub = kg.individuals[int(m.group("subject"))]
                pred = kg.relations[int(m.group("predicate"))]
                obj = kg.individuals[int(m.group("object"))]
        
                # add triple
                kg.triples.add(triple.Triple(sub, pred, obj, positive, True))  # True -> inferred
        
        return kg
