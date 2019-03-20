# -*- coding: utf-8 -*-

"""This module contains classes that define functions for reading and writing knowledge graphs, respectively."""


import os
import re
import typing

from reldata.io.kg_reader import KgReader
from reldata.io.kg_writer import KgWriter


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


# ==================================================================================================================== #
#  C O N S T A N T S                                                                                                   #
# ==================================================================================================================== #


#  FILE EXTENSIONS  ####################################################################################################

CLASSES_INF_EXT = ".classes.data.inf"
"""str: The file extension that is used for storing inferred class memberships."""

CLASSES_PRED_EXT = ".classes.data.pred"
"""str: The file extension that is used for storing class predictions, i.e., those that are neither facts nor inferable.
"""

CLASSES_SPEC_EXT = ".classes.data"
"""str: The file extension that is used for storing specified class memberships."""

CLASSES_VOCAB_EXT = ".classes"
"""str: The file extension that is used for storing class definitions."""

INDIVIDUALS_SPEC_EXT = ".individuals"
"""str: The file extension that is used for storing individual specifications."""

LITERALS_INF_EXT = ".literals.data.inf"
"""str: The file extension that is used for storing inferred literal values."""

LITERALS_PRED_EXT = ".literals.data.pred"
"""str: The file extension that is used for storing literal predictions, i.e., those that are neither facts nor
inferable."""

LITERALS_SPEC_EXT = ".literals.data"
"""str: The file extension that is used for storing specified literal values."""

LITERALS_VOCAB_EXT = ".literals"
"""str: The file extension that is used for storing literal definitions."""

RELATIONS_INF_EXT = ".relations.data.inf"
"""str: The file extension that is used for storing inferred triples."""

RELATIONS_PRED_EXT = ".relations.data.pred"
"""str: The file extension that is used for storing triple predictions, i.e., those that are neither facts nor
inferable."""

RELATIONS_SPEC_EXT = ".relations.data"
"""str: The file extension that is used for storing specified triples."""

RELATIONS_VOCAB_EXT = ".relations"
"""str: The file extension that is used for storing relation definitions."""


#  OTHER CONSTANTS  ####################################################################################################

ALL_EXT = [
        CLASSES_VOCAB_EXT,
        INDIVIDUALS_SPEC_EXT,
        LITERALS_VOCAB_EXT,
        RELATIONS_VOCAB_EXT,
        CLASSES_INF_EXT,  # <<<<<<<<<<<<<<<<<< from here on, files have additional extensions (e.g., ".0") for sequences
        CLASSES_PRED_EXT,
        CLASSES_SPEC_EXT,
        LITERALS_INF_EXT,
        LITERALS_PRED_EXT,
        LITERALS_SPEC_EXT,
        RELATIONS_INF_EXT,
        RELATIONS_PRED_EXT,
        RELATIONS_SPEC_EXT
]
"""list[str]: A list of all file extensions that are used to store the different parts of a knowledge graph."""

INDIVIDUALS_REGEX = "^(?P<base_name>.+){}$".format(INDIVIDUALS_SPEC_EXT.replace(".", "\\."))
"""str: A regex that matches any files that specify the individuals of a knowledge graph."""

KG_FILE_REGEX = "^(?P<base_name>.+)\\.({})$".format("|".join([e[1:] for e in ALL_EXT]))
"""str: A regex that matches any filename that belongs to one of the files of a knowledge graph."""


# ==================================================================================================================== #
#  F U N C T I O N S                                                                                                   #
# ==================================================================================================================== #


def find_knowledge_graphs(input_dir: str) -> typing.List[str]:
    """Scans the provided directory for stored knowledge graphs.
    
    Args:
        input_dir (str): The path of the directory that is being searched.
    
    Returns:
        list[str]: A list that contains the base names of all knowledge graphs that were found in ``input_dir``.
    
    Raises:
        ValueError: If the specified directory does not exist.
    """
    # sanitize args
    input_dir = str(input_dir)
    if not os.path.isdir(input_dir):
        raise ValueError("The specified <input_dir> does not exist: '{}'!".format(input_dir))
    
    # gather the base names of all files that have one of the required file extensions
    candidates = set()
    for file in os.listdir(input_dir):  # run through all files in the input dir
        # check if the file has one of the considered file extensions
        m = re.match(KG_FILE_REGEX, file)
        if m is not None:
            candidates.add(m.group("base_name"))
    
    # check for which of the found base names all of the required files exist
    all_kgs = []
    for base_name in candidates:
        try:
            for ext in ALL_EXT:  # run through the file extensions of all needed files
                # if current extensions is not found -> skip candidate
                if not os.path.isfile(os.path.join(input_dir, base_name + ext)):
                    raise StopIteration
            
            # add candidate to the list of discovered knowledge graphs
            all_kgs.append(base_name)
        except StopIteration:
            pass  # nothing to do
    
    return sorted(all_kgs)


def find_knowledge_graph_sequences(input_dir: str) -> typing.List[str]:
    """Scans the provided directory for stored knowledge-graph sequences.

    Args:
        input_dir (str): The path of the directory that is being searched.

    Returns:
        list[str]: A list that contains the base names of all knowledge graphs that were found in ``input_dir``.

    Raises:
        ValueError: If the specified directory does not exist.
    """
    # sanitize args
    input_dir = str(input_dir)
    if not os.path.isdir(input_dir):
        raise ValueError("The specified <input_dir> does not exist: '{}'!".format(input_dir))
    
    # gather the base names of all files that have one of the required file extensions
    candidates = set()
    for file in os.listdir(input_dir):  # run through all files in the input dir
        # check if the file has one of the considered file extensions
        m = re.match(INDIVIDUALS_REGEX, file)
        if m is not None:
            candidates.add(m.group("base_name"))
    
    # check for which of the found base names all of the required files exist
    all_seq = []
    for base_name in candidates:
        try:
            # run through the file extensions of all needed files
            for ext in ALL_EXT[:4]:
                # if current extensions is not found -> skip candidate
                if not os.path.isfile(os.path.join(input_dir, base_name + ext)):
                    raise StopIteration
            for ext in ALL_EXT[4:]:
                # if current extensions is not found -> skip candidate
                if not os.path.isfile(os.path.join(input_dir, base_name + ext + ".0")):
                    raise StopIteration
            
            # add candidate to the list of discovered knowledge graphs
            all_seq.append(base_name)
        except StopIteration:
            pass  # nothing to do
    
    return sorted(all_seq)
