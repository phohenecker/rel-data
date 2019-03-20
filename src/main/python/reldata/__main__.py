#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Executing the :mod:`reldata` package runs a tool for analysing knowledge graphs."""


import itertools
import os
import typing

import argmagic

from argmagic import decorators

from reldata import io
from reldata.io import kg_reader


__author__ = "Patrick Hohenecker"
__copyright__ = (
        "Copyright (c) 2018, Patrick Hohenecker\n"
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
__date__ = "Mar 26, 2018"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


APP_DESCRIPTION = "This tool prints summary statistics for the provided data."
"""str: The help text that is printed for this application."""

APP_NAME = "reldata"
"""str: The name of the application that is displayed in its synopsis."""


# ==================================================================================================================== #
#  CLASS  _ C O N F I G                                                                                                #
# ==================================================================================================================== #


class _Config(object):
    """This class specifies the user-defined configuration that may be passed to this application."""
    
    DEFAULT_INPUT_DIR = "."
    """str: The default value of :attr:`base_name`."""
    
    def __init__(self):
        self._base_name = None
        self._input_dir = self.DEFAULT_INPUT_DIR
        
    #  PROPERTIES  #####################################################################################################
    
    @decorators.optional
    @property
    def base_name(self) -> typing.Optional[str]:
        """str: The base name of the knowledge graph to analyze."""
        return self._base_name
    
    @base_name.setter
    def base_name(self, base_name: str) -> None:
        self._base_name = str(base_name)
    
    @property
    def input_dir(self) -> str:
        """str: The path of the directory that contains the data."""
        return self._input_dir
    
    @input_dir.setter
    def input_dir(self, input_dir: str) -> None:
        input_dir = str(input_dir)
        if not os.path.isdir(input_dir):
            raise ValueError(
                    "The provided <input_dir> does not refer to an existing directory: '{}'!".format(input_dir)
            )
        self._input_dir = input_dir


# ==================================================================================================================== #
#  CLASS  O C C U R R E N C E S                                                                                        #
# ==================================================================================================================== #


class _Occurrences(object):
    """A helper class that encapsulates counts for positive/negative specified/inferable/predictable occurrences of
    triples and classes, respectively.
    """
    
    def __init__(self):
        self.inf_neg = 0   # the number of inferable negative occurrences
        self.inf_pos = 0   # the number of inferable positive occurrences
        self.pred_neg = 0  # the number of negative prediction occurrences
        self.pred_pos = 0  # the number of positive prediction occurrences
        self.spec_neg = 0  # the number of specified negative occurrences
        self.spec_pos = 0  # the number of specified positive occurrences


# ==================================================================================================================== #
#  H E L P E R  F U N C T I O N S                                                                                      #
# ==================================================================================================================== #


def print_table(title: str, data: typing.Sequence[typing.Sequence[str]], column_labels: typing.Sequence[str]) -> None:
    """TODO"""
    num_cols = len(column_labels)
    col_lengths = [0] * num_cols
    
    # determine the space requirements of each columns
    for line in itertools.chain([column_labels], data):
        for col_idx in range(num_cols):
            col_lengths[col_idx] = max(col_lengths[col_idx], len(line[col_idx]))
    
    # determine total length of each line
    total_length = sum(col_lengths) + num_cols * 3 + 1
    
    # build pattern for printing lines
    line_pattern = "|"
    for col_len in col_lengths:
        line_pattern += " {{:{}}} |".format(col_len)
    
    # print table
    print("=" * total_length)
    print("|{{:^{}}}|".format(total_length - 2).format(title))
    print("=" * total_length)
    print(line_pattern.format(*column_labels))
    print("-" * total_length)
    for line in data:
        print(line_pattern.format(*line))
    print("=" * total_length)


# ==================================================================================================================== #
#  M A I N                                                                                                             #
# ==================================================================================================================== #


def main(args: _Config) -> None:
    
    # sanitize base_name (if provided)
    if args.base_name is not None:
        
        # assemble the needed paths
        individual_spec = os.path.join(args.input_dir, args.base_name + ".individuals")
        classes_vocab = os.path.join(args.input_dir, args.base_name + ".classes")
        classes_spec = os.path.join(args.input_dir, args.base_name + ".classes.data")
        classes_inf = os.path.join(args.input_dir, args.base_name + ".classes.data.inf")
        relations_vocab = os.path.join(args.input_dir, args.base_name + ".relations")
        relations_spec = os.path.join(args.input_dir, args.base_name + ".relations.data")
        relations_inf = os.path.join(args.input_dir, args.base_name + ".relations.data.inf")
        literals_vocab = os.path.join(args.input_dir, args.base_name + ".literals")
        literals_spec = os.path.join(args.input_dir, args.base_name + ".literals.data")
        literals_inf = os.path.join(args.input_dir, args.base_name + ".literals.data.inf")

        # check whether all of the needed files exist:
        if not os.path.isfile(individual_spec):
            print("Missing file: '{}'!".format(individual_spec))
            return
        if not os.path.isfile(classes_vocab):
            print("Missing file: '{}'!".format(classes_vocab))
        if not os.path.isfile(classes_spec):
            print("Missing file: '{}'!".format(classes_spec))
            return
        if not os.path.isfile(classes_inf):
            print("Missing file: '{}'!".format(classes_inf))
            return
        if not os.path.isfile(relations_vocab):
            print("Missing file: '{}'!".format(relations_vocab))
            return
        if not os.path.isfile(relations_spec):
            print("Missing file: '{}'!".format(relations_spec))
            return
        if not os.path.isfile(relations_inf):
            print("Missing file: '{}'!".format(relations_inf))
            return
        if not os.path.isfile(literals_vocab):
            print("Missing file: '{}'!".format(literals_vocab))
            return
        if not os.path.isfile(literals_spec):
            print("Missing file: '{}'!".format(literals_spec))
            return
        if not os.path.isfile(literals_inf):
            print("Missing file: '{}'!".format(literals_inf))
            return
    
    # load the knowledge graph(s) to analyze
    if args.base_name is None:
        
        # scan input dir for knowledge graphs
        data = ((args.input_dir, base_name) for base_name in io.find_knowledge_graphs(args.input_dir))

        if not data:
            print("No data was found in '{}'!".format(args.input_dir))
            return
    else:
        data = [(args.input_dir, args.base_name)]
    
    # create data structures for bookkeeping
    classes = {}
    relations = {}
    literals = {}
    num_individuals = 0
    
    # iterate over all of the loaded knowledge graphs
    for input_dir, base_name in data:
        
        print("processing {}/{}...".format(input_dir, base_name))
        
        kg = kg_reader.KgReader.read(input_dir, base_name)
        
        # update individual count
        num_individuals += len(kg.individuals)

        # register all classes/relations/literals of the current knowledge graph
        for c in kg.classes:
            if c.name not in classes:
                classes[c.name] = _Occurrences()
        for r in kg.relations:
            if r.name not in relations:
                relations[r.name] = _Occurrences()
        for l in kg.literals:
            if l.name not in literals:
                literals[l.name] = 0
        
        # iterate over all individuals
        for ind in kg.individuals:
            
            # register all of the individuals class memberships
            for cls_mem in ind.classes:
                if cls_mem.inferred:
                    if cls_mem.is_member:
                        classes[cls_mem.cls.name].inf_pos += 1
                    else:
                        classes[cls_mem.cls.name].inf_neg += 1
                elif cls_mem.prediction:
                    if cls_mem.is_member:
                        classes[cls_mem.cls.name].pred_pos += 1
                    else:
                        classes[cls_mem.cls.name].pred_neg += 1
                else:
                    if cls_mem.is_member:
                        classes[cls_mem.cls.name].spec_pos += 1
                    else:
                        classes[cls_mem.cls.name].spec_neg += 1
        
            # register all of the individuals literals
            for lit in ind.literals:
                literals[lit.literal.name] += 1
        
        # register all triples
        for triple in kg.triples:
        
            if triple.inferred:
                if triple.positive:
                    relations[triple.predicate.name].inf_pos += 1
                else:
                    relations[triple.predicate.name].inf_neg += 1
            elif triple.prediction:
                if triple.positive:
                    relations[triple.predicate.name].pred_pos += 1
                else:
                    relations[triple.predicate.name].pred_neg += 1
            else:
                if triple.positive:
                    relations[triple.predicate.name].spec_pos += 1
                else:
                    relations[triple.predicate.name].spec_neg += 1
    
    print("TOTAL INDIVIDUALS:", num_individuals, "\n")
    
    # print class statistics
    if classes:
        class_data = [
                (
                        name,
                        "{} / {}".format(stats.spec_pos, stats.spec_neg),
                        "{} / {}".format(stats.inf_pos, stats.inf_neg),
                        "{} / {}".format(stats.pred_pos, stats.pred_neg)
                )
                for name, stats in sorted(classes.items(), key=lambda x: x[0])
        ]
        print_table(
                "CLASSES",
                class_data,
                ["name", "spec. members (+/-)", "inf. members (+/-)", "pred. member (+/-)"]
        )
        print(
                "(TOTAL: {} / {}, {} / {} , {} / {})".format(
                        sum(stats.spec_pos for stats in classes.values()),
                        sum(stats.spec_neg for stats in classes.values()),
                        sum(stats.inf_pos for stats in classes.values()),
                        sum(stats.inf_neg for stats in classes.values()),
                        sum(stats.pred_pos for stats in classes.values()),
                        sum(stats.pred_neg for stats in classes.values())
                )
        )
        print()
        print("class_data = [")
        for name, stats in sorted(classes.items(), key=lambda x: x[0]):
            print(
                "    (\"{}\", {}, {}, {}, {}, {}, {}),".format(
                    name,
                    stats.spec_pos,
                    stats.spec_neg,
                    stats.inf_pos,
                    stats.inf_neg,
                    stats.pred_pos,
                    stats.pred_neg
                )
            )
        print("]")
    else:
        print("No classes were found!")
    print()

    # print relation statistics
    if relations:
        relation_data = [
                (
                        name,
                        "{} / {}".format(stats.spec_pos, stats.spec_neg),
                        "{} / {}".format(stats.inf_pos, stats.inf_neg),
                        "{} / {}".format(stats.pred_pos, stats.pred_neg)
                )
                for name, stats in sorted(relations.items(), key=lambda x: x[0])
        ]
        print_table(
                "RELATIONS",
                relation_data,
                ["name", "spec. triples (+/-)", "inf. triples (+/-)", "pred. member (+/-)"]
        )
        print(
                "(TOTAL: {} / {}, {} / {} , {} / {})".format(
                        sum(stats.spec_pos for stats in relations.values()),
                        sum(stats.spec_neg for stats in relations.values()),
                        sum(stats.inf_pos for stats in relations.values()),
                        sum(stats.inf_neg for stats in relations.values()),
                        sum(stats.pred_pos for stats in relations.values()),
                        sum(stats.pred_neg for stats in relations.values())
                )
        )
        print()
        print("rel_data = [")
        for name, stats in sorted(relations.items(), key=lambda x: x[0]):
            print(
                    "    (\"{}\", {}, {}, {}, {}, {}, {}),".format(
                            name,
                            stats.spec_pos,
                            stats.spec_neg,
                            stats.inf_pos,
                            stats.inf_neg,
                            stats.pred_pos,
                            stats.pred_neg
                    )
            )
        print("]")
    else:
        print("No relations were found!")
    print()

    # print literal statistics
    if literals:
        literal_data = [
                (name, stats)
                for name, stats in sorted(literals.items(), key=lambda x: x[0])
        ]
        print_table(
                "LITERALS",
                literal_data,
                ["name", "occurrences"]
        )
    else:
        print("No literals were found!")


main(argmagic.parse_args(_Config, app_name=APP_NAME, app_description=APP_DESCRIPTION))
