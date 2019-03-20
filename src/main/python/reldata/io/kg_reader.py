# -*- coding: utf-8 -*-


import os
import re
import typing

import insanity

from concurrent import futures

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
__license__ = "BSD-2-Clause"
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
    def read(cls, input_dir: str, basename: str, index: int = None) -> knowledge_graph.KnowledgeGraph:
        """Loads a knowledge graph from the specified location.
        
        Args:
            input_dir (str): The directory that contains all of the files.
            basename (str): The base name, i.e., the prefix, included in all files' names.
            index (int, optional): If this is provided, then ``input_dir`` and ``basename`` are assumed to specify a
                sequence of knowledge graphs, and ``index`` specifies the element of this sequence to retrieve.
        
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
        if index is not None:
            insanity.sanitize_type("index", index, int)
            insanity.sanitize_range("index", index, minimum=0)
        
        # assemble all needed paths
        # the used postfixes have the following meanings:
        # * _vocab -> definition of a class/relation/literal
        # * _spec  -> user-defined data
        # * _inf   -> inferred data
        individual_spec = os.path.join(input_dir, basename + io.INDIVIDUALS_SPEC_EXT)
        classes_vocab = os.path.join(input_dir, basename + io.CLASSES_VOCAB_EXT)
        classes_spec = os.path.join(input_dir, basename + io.CLASSES_SPEC_EXT)
        classes_inf = os.path.join(input_dir, basename + io.CLASSES_INF_EXT)
        classes_pred = os.path.join(input_dir, basename + io.CLASSES_PRED_EXT)
        relations_vocab = os.path.join(input_dir, basename + io.RELATIONS_VOCAB_EXT)
        relations_spec = os.path.join(input_dir, basename + io.RELATIONS_SPEC_EXT)
        relations_inf = os.path.join(input_dir, basename + io.RELATIONS_INF_EXT)
        relations_pred = os.path.join(input_dir, basename + io.RELATIONS_PRED_EXT)
        literals_vocab = os.path.join(input_dir, basename + io.LITERALS_VOCAB_EXT)
        literals_spec = os.path.join(input_dir, basename + io.LITERALS_SPEC_EXT)
        literals_inf = os.path.join(input_dir, basename + io.LITERALS_INF_EXT)
        literals_pred = os.path.join(input_dir, basename + io.LITERALS_PRED_EXT)
        if index is not None:
            classes_spec += "." + str(index)
            classes_inf += "." + str(index)
            classes_pred += "." + str(index)
            relations_spec += "." + str(index)
            relations_inf += "." + str(index)
            relations_pred += "." + str(index)
            literals_spec += "." + str(index)
            literals_inf += "." + str(index)
            literals_pred += "." + str(index)
        
        # check whether the input directory exists
        if not os.path.isdir(input_dir):
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
        if not os.path.isfile(classes_pred):
            raise ValueError("Missing file: '{}'!".format(classes_pred))
        if not os.path.isfile(relations_vocab):
            raise ValueError("Missing file: '{}'!".format(relations_vocab))
        if not os.path.isfile(relations_spec):
            raise ValueError("Missing file: '{}'!".format(relations_spec))
        if not os.path.isfile(relations_inf):
            raise ValueError("Missing file: '{}'!".format(relations_inf))
        if not os.path.isfile(relations_pred):
            raise ValueError("Missing file: '{}'!".format(relations_pred))
        if not os.path.isfile(literals_vocab):
            raise ValueError("Missing file: '{}'!".format(literals_vocab))
        if not os.path.isfile(literals_spec):
            raise ValueError("Missing file: '{}'!".format(literals_spec))
        if not os.path.isfile(literals_inf):
            raise ValueError("Missing file: '{}'!".format(literals_inf))
        if not os.path.isfile(literals_pred):
            raise ValueError("Missing file: '{}'!".format(literals_pred))
    
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
                                        mem == 1
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
                                inferred=True
                            )
                        )
        
        # read memberships that are prediction targets
        with open(classes_pred, "r") as f:
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
                                        prediction=True
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
                                current_value
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
                                inferred=True
                        )
                )
        
        # read literals that are prediction targets
        with open(literals_pred, "r") as f:
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
                                prediction=True
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
                kg.triples.add(triple.Triple(sub, pred, obj, positive))
        
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
                kg.triples.add(triple.Triple(sub, pred, obj, positive, inferred=True))
        
        # read triples that are prediction targets
        with open(relations_pred, "r") as f:
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
                kg.triples.add(triple.Triple(sub, pred, obj, positive, prediction=True))
        
        return kg
    
    @classmethod
    def read_all(cls, input_dir: str, executor: futures.Executor = None) -> typing.List[knowledge_graph.KnowledgeGraph]:
        """Loads all knowledge graphs that are discovered in the specified directory.
        
        Args:
            input_dir (str): The path of the directory that is being searched.
            executor (futures.Executor, optional): An optional executor for loading multiple knowledge graphs
                concurrently.
    
        Returns:
            list[:class:`knowledge_graph.KnowledgeGraph`]: All knowledge graphs that were found in ``input_dir``.
        
        Raises:
            ValueError: If the specified directory does not exist.
        """
        # sanitize args
        input_dir = str(input_dir)
        if not os.path.isdir(input_dir):
            raise ValueError("The specified <input_dir> does not exist: '{}'!".format(input_dir))
        insanity.sanitize_type("executor", executor, futures.Executor, none_allowed=True)
        
        # find all knowledge graphs in the input directory
        all_kgs = io.find_knowledge_graphs(input_dir)
        
        # load all knowledge graphs that were found
        if executor is None:
            return [cls.read(input_dir, kg) for kg in all_kgs]
        else:
            all_kgs = [os.path.join(input_dir, kg) for kg in all_kgs]
            return list(executor.map(cls._read_from_one, all_kgs))
    
    @classmethod
    def read_all_sequences(
            cls,
            input_dir: str,
            executor: futures.Executor = None
    ) -> typing.List[typing.List[knowledge_graph.KnowledgeGraph]]:
        """Loads all knowledge-graph sequences that are discovered in the specified directory.

        Args:
            input_dir (str): The path of the directory that is being searched.
            executor (futures.Executor, optional): An optional executor for loading multiple knowledge-graph sequences
                concurrently.

        Returns:
            list[list[:class:`knowledge_graph.KnowledgeGraph`]]: All knowledge-graph sequences that were found in
                ``input_dir``.

        Raises:
            ValueError: If the specified directory does not exist.
        """
        # sanitize args
        input_dir = str(input_dir)
        if not os.path.isdir(input_dir):
            raise ValueError("The specified <input_dir> does not exist: '{}'!".format(input_dir))
        insanity.sanitize_type("executor", executor, futures.Executor, none_allowed=True)
    
        # find all knowledge-graph sequences in the input directory
        all_seq = io.find_knowledge_graph_sequences(input_dir)
    
        # load all knowledge graphs that were found
        if executor is None:
            return [cls.read_sequence(input_dir, seq) for seq in all_seq]
        else:
            all_seq = [os.path.join(input_dir, seq) for seq in all_seq]
            return list(executor.map(cls._read_seq_from_one, all_seq))
    
    @classmethod
    def read_sequence(cls, input_dir: str, basename: str) -> typing.List[knowledge_graph.KnowledgeGraph]:
        """Loads a sequence of knowledge graph from the specified location.

        Args:
            input_dir (str): The directory that contains all of the files.
            basename (str): The base name, i.e., the prefix, included in all files' names.

        Returns:
            list[:class:`knowledge_graph.KnowledgeGraph`]: A knowledge graph seqeunce that has been populated according
                to the read information.

        Raises:
            ValueError: If ``input_dir`` does not refer to an existing directory or if any of the needed files is
                missing.
        """
        # sanitize args
        input_dir = str(input_dir)
        basename = str(basename)
        if not os.path.isdir(input_dir):
            raise ValueError("The provided <input_dir> does not exist: '{}'!".format(input_dir))
        
        # determine the length of the sequence to load
        seq_len = 0
        while os.path.isfile(os.path.join(input_dir, basename + io.CLASSES_SPEC_EXT + "." + str(seq_len))):
            seq_len += 1
        
        return [cls.read(input_dir, basename, index=idx) for idx in range(seq_len)]

    @classmethod
    def _read_from_one(cls, path: str) -> knowledge_graph.KnowledgeGraph:
        """Splits the provided path into the directory and the base name of a knowledge graph, and then invokes
        :meth:`read`.
        
        Args:
            path (str): The path the contains both the input directory and the base name of a knowledge graph.
        
        Returns:
            :class:`knowledge_graph.KnowledgeGraph`: The knowledge graph that was loaded from ``path``.
        """
        split_index = path.rfind(os.path.sep)
        input_dir = path[:split_index]
        base_name = path[split_index + 1:]
        return cls.read(input_dir, base_name)

    @classmethod
    def _read_seq_from_one(cls, path: str) -> typing.List[knowledge_graph.KnowledgeGraph]:
        """Splits the provided path into the directory and the base name of a knowledge-graph sequence, and then invokes
        :meth:`read_sequence`.

        Args:
            path (str): The path the contains both the input directory and the base name of a knowledge-graph sequence.

        Returns:
            list[:class:`knowledge_graph.KnowledgeGraph`]: The knowledge-graph sequence that was loaded from ``path``.
        """
        split_index = path.rfind(os.path.sep)
        input_dir = path[:split_index]
        base_name = path[split_index + 1:]
        return cls.read_sequence(input_dir, base_name)
