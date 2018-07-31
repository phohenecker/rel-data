#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import threading
import time
import unittest

from reldata.util import sync


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
__date__ = "Nov 26, 2017"
__maintainer__ = "Patrick Hohenecker"
__email__ = "mail@paho.at"
__status__ = "Development"


# ==================================================================================================================== #
#  CLASS  S Y N C  T E S T                                                                                             #
# ==================================================================================================================== #

class SyncTest(unittest.TestCase):
    
    @staticmethod
    def add_to_store(store: "Store", store_index: int, num_iters: int, synced: bool):
        for _ in range(num_iters):
            if synced:
                store.synced_add_to(store_index)
            else:
                store.add_to(store_index)
    
    def test_synchronized(self):
        num_iters = 10
        
        # CHECK: the non-synchronized version does not work
        store = Store()
        t_1 = threading.Thread(target=self.add_to_store, args=(store, 1, num_iters, False))
        t_2 = threading.Thread(target=self.add_to_store, args=(store, 2, num_iters, False))
        t_3 = threading.Thread(target=self.add_to_store, args=(store, 3, num_iters, False))
        t_1.start()
        t_2.start()
        t_3.start()
        t_1.join()
        t_2.join()
        t_3.join()
        self.assertNotEqual("1" * num_iters, store.store_1)
        self.assertNotEqual("2" * num_iters, store.store_2)
        self.assertNotEqual("3" * num_iters, store.store_3)

        # CHECK: the synchronized version works
        store = Store()
        t_1 = threading.Thread(target=self.add_to_store, args=(store, 1, num_iters, True))
        t_2 = threading.Thread(target=self.add_to_store, args=(store, 2, num_iters, True))
        t_3 = threading.Thread(target=self.add_to_store, args=(store, 3, num_iters, True))
        t_1.start()
        t_2.start()
        t_3.start()
        t_1.join()
        t_2.join()
        t_3.join()
        self.assertEqual("1" * num_iters, store.store_1)
        self.assertEqual("2" * num_iters, store.store_2)
        self.assertEqual("3" * num_iters, store.store_3)
    

# ==================================================================================================================== #
#  CLASS  S T O R E                                                                                                    #
# ==================================================================================================================== #


class Store(object):
    
    def __init__(self):
        self._buffer = None
        self._store_1 = ""
        self._store_2 = ""
        self._store_3 = ""
    
    #  PROPERTIES  #####################################################################################################
    
    @property
    def store_1(self) -> str:
        return self._store_1
    
    @property
    def store_2(self) -> str:
        return self._store_2

    @property
    def store_3(self) -> str:
        return self._store_3
    
    #  METHODS  ########################################################################################################
    
    def _add_to(self, index: int) -> None:
        if index == 1:
            self._buffer = "1"
        elif index == 2:
            self._buffer = "2"
        else:
            self._buffer = "3"
    
        time.sleep(0.01)
    
        if index == 1:
            self._store_1 += self._buffer
        elif index == 2:
            self._store_2 += self._buffer
        else:
            self._store_3 += self._buffer
    
    def add_to(self, index: int) -> None:
        self._add_to(index)

    @sync.synchronized
    def synced_add_to(self, index: int) -> None:
        self._add_to(index)


if __name__ == "__main__":
    unittest.main()
