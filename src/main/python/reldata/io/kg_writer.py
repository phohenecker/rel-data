# -*- coding: utf-8 -*-


import os
import typing

import insanity

from collections import abc

from reldata import io
from reldata.data import individual
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
__license__ = "BSD-2-Clause"
__version__ = "2017.1"
__date__ = "Nov 12, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


class KgWriter(object):
    """A class for writing :class:`knowledge_graph.KnowledgeGraph`s to disk."""
    
    VOCAB_PATTERN = "{index} {name}\n"
    """str: A pattern for writing class/relation/literal definitions."""
    
    TRIPLES_PATTERN = "{subject} {predicate} {object}\n"
    """str: A pattern for writing triples."""

    TYPED_TRIPLES_PATTERN = "{type} {subject} {predicate} {object}\n"
    """str: A pattern for writing triples that are marked as positive and negative, respectively."""
    
    #  METHODS  ########################################################################################################
    
    @classmethod
    def _create_membership_vectors(
            cls,
            kg: knowledge_graph.KnowledgeGraph,
            ind: individual.Individual
    ) -> typing.Tuple[str, str, str]:
        num_classes = len(kg.classes)
        spec = ["0"] * num_classes
        inf = ["0"] * num_classes
        pred = ["0"] * num_classes
        
        for c in ind.classes:
            value = "1" if c.is_member else "-1"
            if c.inferred:
                inf[c.cls.index] = value
            elif c.prediction:
                pred[c.cls.index] = value
            else:
                spec[c.cls.index] = value
        
        return " ".join(spec) + "\n", " ".join(inf) + "\n", " ".join(pred) + "\n"

    @classmethod
    def write(
            cls,
            kg: knowledge_graph.KnowledgeGraph,
            target_dir: str,
            base_name: str,
            index: int = None
    ) -> None:
        """Writes the provided knowledge graph to the specified path.
        
        Args:
            kg (:class:`knowledge_graph.KnowledgeGraph`): The knowledge graph to write to disk.
            target_dir (str): The path of the directory to place all the files in.
            base_name (str): The base name to use, i.e., the prefix, included in all files' names.
            index (int, optional): If this is provided, then ``input_dir`` and ``basename`` are assumed to specify a
                sequence of knowledge graphs, and ``index`` specifies the element of this sequence to be written to
                disk.
        
        Raises:
            ValueError: If ``target_dir`` does not refer to an existing directory.
        """
        # sanitize args
        insanity.sanitize_type("kg", kg, knowledge_graph.KnowledgeGraph)
        target_dir = str(target_dir)
        base_name = str(base_name)
        if not os.path.isdir(target_dir):
            raise ValueError("The directory <target_dir> does not exist: '{}'!".format(target_dir))
        if index is not None:
            insanity.sanitize_type("index", index, int)
            insanity.sanitize_range("index", index, minimum=0)

        # //////// Write Vocabulary ------------------------------------------------------------------------------------
        
        # write classes
        with open(os.path.join(target_dir, base_name + io.CLASSES_VOCAB_EXT), "w") as f:
            for c in kg.classes:
                f.write(cls.VOCAB_PATTERN.format(index=c.index, name=c.name))

        # write literals
        with open(os.path.join(target_dir, base_name + io.LITERALS_VOCAB_EXT), "w") as f:
            for l in kg.literals:
                f.write(cls.VOCAB_PATTERN.format(index=l.index, name=l.name))
        
        # write relations
        with open(os.path.join(target_dir, base_name + io.RELATIONS_VOCAB_EXT), "w") as f:
            for r in kg.relations:
                f.write(cls.VOCAB_PATTERN.format(index=r.index, name=r.name))

        # //////// Write Individuals -----------------------------------------------------------------------------------
        
        with open(os.path.join(target_dir, base_name + io.INDIVIDUALS_SPEC_EXT), "w") as f:
            for i in kg.individuals:
                f.write(cls.VOCAB_PATTERN.format(index=i.index, name=i.name))

        # //////// Write Class Memberships -----------------------------------------------------------------------------

        classes_spec = os.path.join(target_dir, base_name + io.CLASSES_SPEC_EXT)
        classes_inf = os.path.join(target_dir, base_name + io.CLASSES_INF_EXT)
        classes_pred = os.path.join(target_dir, base_name + io.CLASSES_PRED_EXT)
        if index is not None:
            classes_spec += "." + str(index)
            classes_inf += "." + str(index)
            classes_pred += "." + str(index)
        with open(classes_spec, "w") as f_spec:
            with open(classes_inf, "w") as f_inf:
                with open(classes_pred, "w") as f_pred:
                    for i in kg.individuals:
                        spec, inf, pred = cls._create_membership_vectors(kg, i)
                        f_spec.write(spec)
                        f_inf.write(inf)
                        f_pred.write(pred)
        
        # //////// Write Literals --------------------------------------------------------------------------------------

        literals_spec = os.path.join(target_dir, base_name + io.LITERALS_SPEC_EXT)
        literals_inf = os.path.join(target_dir, base_name + io.LITERALS_INF_EXT)
        literals_pred = os.path.join(target_dir, base_name + io.LITERALS_PRED_EXT)
        if index is not None:
            literals_spec += "." + str(index)
            literals_inf += "." + str(index)
            literals_pred += "." + str(index)
        with open(literals_spec, "w") as f_spec:
            with open(literals_inf, "w") as f_inf:
                with open(literals_pred, "w") as f_pred:
                    for i in kg.individuals:
                        for l in i.literals:
                            line = cls.TRIPLES_PATTERN.format(
                                    subject=i.index,
                                    predicate=l.literal.index,
                                    object=l.value
                            )
                            if l.inferred:
                                f_inf.write(line)
                            elif l.prediction:
                                f_pred.write(line)
                            else:
                                f_spec.write(line)

        # //////// Write Relations -------------------------------------------------------------------------------------

        relations_spec = os.path.join(target_dir, base_name + io.RELATIONS_SPEC_EXT)
        relations_inf = os.path.join(target_dir, base_name + io.RELATIONS_INF_EXT)
        relations_pred = os.path.join(target_dir, base_name + io.RELATIONS_PRED_EXT)
        if index is not None:
            relations_spec += "." + str(index)
            relations_inf += "." + str(index)
            relations_pred += "." + str(index)
        with open(relations_spec, "w") as f_spec:
            with open(relations_inf, "w") as f_inf:
                with open(relations_pred, "w") as f_pred:
                    for t in kg.triples:
                        line = cls.TYPED_TRIPLES_PATTERN.format(
                                type=("+" if t.positive else "-"),
                                subject=t.subject.index,
                                predicate=t.predicate.index,
                                object=t.object.index
                        )
                        if t.inferred:
                            f_inf.write(line)
                        elif t.prediction:
                            f_pred.write(line)
                        else:
                            f_spec.write(line)
    
    @classmethod
    def write_sequence(
            cls,
            seq: typing.Sequence[knowledge_graph.KnowledgeGraph],
            target_dir: str,
            base_name: str
    ) -> None:
        """Writes the provided knowledge graph to the specified path.

        Args:
            seq (sequence[:class:`knowledge_graph.KnowledgeGraph`]): The knowledge graph sequence to write to disk.
            target_dir (str): The path of the directory to place all the files in.
            base_name (str): The base name to use, i.e., the prefix, included in all files' names.

        Raises:
            ValueError: If ``target_dir`` does not refer to an existing directory.
        """
        # sanitize args
        insanity.sanitize_type("seq", seq, abc.Sequence)
        insanity.sanitize_iterable("seq", seq, elements_type=knowledge_graph.KnowledgeGraph, min_length=1)
        target_dir = str(target_dir)
        if not os.path.isdir(target_dir):
            raise ValueError("The provided <target_dir> does not exist: '{}'!".format(target_dir))
        base_name = str(base_name)
        
        # write the sequence to disk
        for idx, kg in enumerate(seq):
            cls.write(kg, target_dir, base_name, index=idx)
