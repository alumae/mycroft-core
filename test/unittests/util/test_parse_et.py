# -*- coding: utf-8 -*-
#
# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import unittest
from datetime import datetime, time

from mycroft.util.parse import extract_datetime
from mycroft.util.parse import extract_number
from mycroft.util.parse import extract_numbers
from mycroft.util.parse import normalize


class TestNormalize(unittest.TestCase):

    def test_extract_number(self):
        self.assertEqual(extract_number("see on test number 12",
                         lang="et-ee"), 12)
        self.assertEqual(extract_number("see on 7. test",
                         lang="et-ee"), 7)

        self.assertEqual(extract_number("see on esimene test",
                         lang="et-ee"), 1)
        self.assertEqual(extract_number("see test on seitsmes",
                         lang="et-ee"), 7)
        self.assertEqual(extract_number("palun kolmandale korrusele",
                         lang="et-ee"), 3)


if __name__ == "__main__":
    unittest.main()
