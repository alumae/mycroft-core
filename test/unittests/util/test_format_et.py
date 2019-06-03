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
import datetime
import unittest

from mycroft.util.format import nice_number, nice_time, pronounce_number
from mycroft.util.lang.format_et import pronounce_ordinal_et

# fractions are not capitalized for now
NUMBERS_FIXTURE_et = {
    1.435634: '1,436',
    2: '2',
    5.0: '5',
    1234567890: '1234567890',
    12345.67890: '12345,679',
    0.027: '0,027',
    0.5: 'pool',
    1.333: '1 ja 1 kolmandik',
    2.666: '2 ja 2 kolmandikku',
    0.25: '1 neljandik',
    1.25: '1 ja 1 neljandik',
    0.75: '3 neljandikku',
    1.75: '1 ja 3 neljandikku',
    3.4: '3 ja 2 viiendikku',
    16.8333: '16 ja 5 kuuendikku',
    12.5714: '12 ja 4 seitsmendikku',
    9.625: '9 ja 5 kaheksandikku',
    6.777: '6 ja 7 üheksandikku',
    3.1: '3 ja 1 kümnendik',
    2.272: '2 ja 3 üheteistkümnendikku',
    5.583: '5 ja 7 kaheteistkümnendikku',
    8.384: '8 ja 5 kolmeteistkümnendikku',
    0.071: '1 neljateistkümnendik',
    6.466: '6 ja 7 viieteistkümnendikku',
    8.312: '8 ja 5 kuueteistkümnendikku',
    2.176: '2 ja 3 seitsmeteistkümnendikku',
    200.722: '200 ja 13 kaheksateistkümnendikku',
    7.421: '7 ja 8 üheksateistkümnendikku',
    0.05: '1 kahekümnendik'
}


class TestNiceNumberFormat(unittest.TestCase):
    def test_convert_float_to_nice_number(self):
        for number, number_str in NUMBERS_FIXTURE_et.items():
            self.assertEqual(nice_number(number, lang="et-ee"), number_str,
                             'should format {} as {} and not {}'.format(
                                 number, number_str,
                                 nice_number(number, lang="et-ee")))

    def test_specify_danominator(self):
        self.assertEqual(nice_number(5.5, lang="et-ee",
                                     denominators=[1, 2, 3]), '5 ja pool',
                         'should format 5.5 as 5 ja pool, not {}'.format(
                             nice_number(5.5, denominators=[1, 2, 3])))
        self.assertEqual(nice_number(2.333, lang="et-ee", denominators=[1, 2]),
                         '2,333',
                         'should format 2,333 as 2,333 not {}'.format(
                             nice_number(2.333, lang="et-ee",
                                         denominators=[1, 2])))

    def test_no_speech(self):
        self.assertEqual(nice_number(6.777, speech=False),
                         '6 7/9',
                         'should format 6.777 as 6 7/9 not {}'.format(
                             nice_number(6.777, lang="et-ee", speech=False)))
        self.assertEqual(nice_number(6.0, speech=False),
                         '6',
                         'should format 6.0 as 6 not {}'.format(
                             nice_number(6.0, lang="et-ee", speech=False)))


class TestPronounceOrdinal(unittest.TestCase):
    def test_convert_int_et(self):
        self.assertEqual(pronounce_ordinal_et(0),
                         "nullis")
        self.assertEqual(pronounce_ordinal_et(1),
                         "esimene")
        self.assertEqual(pronounce_ordinal_et(3),
                         "kolmas")
        self.assertEqual(pronounce_ordinal_et(5),
                         "viies")
        self.assertEqual(pronounce_ordinal_et(21),
                         "kahekümne esimene")
        self.assertEqual(pronounce_ordinal_et(2000),
                         "kahe tuhandes")
        self.assertEqual(pronounce_ordinal_et(1000),
                         "tuhandes")
        self.assertEqual(pronounce_ordinal_et(1983),
                         "tuhande üheksasaja kaheksakümne kolmas")
        self.assertEqual(pronounce_ordinal_et(2001),
                         "kahe tuhande esimene")


class TestPronounceNumber(unittest.TestCase):
    def test_convert_int_et(self):
        self.assertEqual(pronounce_number(1, lang="et-ee"), "üks")
        self.assertEqual(pronounce_number(10, lang="et-ee"), "kümme")
        self.assertEqual(pronounce_number(15, lang="et-ee"), "viisteist")
        self.assertEqual(pronounce_number(20, lang="et-ee"), "kakskümmend")
        self.assertEqual(pronounce_number(
            27, lang="et-ee"), "kakskümmend seitse")
        self.assertEqual(pronounce_number(30, lang="et-ee"), "kolmkümmend")
        self.assertEqual(pronounce_number(
            33, lang="et-ee"), "kolmkümmend kolm")
        self.assertEqual(pronounce_number(
            71, lang="et-ee"), "seitsekümmend üks")
        self.assertEqual(pronounce_number(80, lang="et-ee"), "kaheksakümmend")
        self.assertEqual(pronounce_number(
            74, lang="et-ee"), "seitsekümmend neli")
        self.assertEqual(pronounce_number(
            79, lang="et-ee"), "seitsekümmend üheksa")
        self.assertEqual(pronounce_number(
            91, lang="et-ee"), "üheksakümmend üks")
        self.assertEqual(pronounce_number(300, lang="et-ee"), "kolmsada")
        self.assertEqual(pronounce_number(310, lang="et-ee"), "kolmsada kümme")
        self.assertEqual(pronounce_number(205310, lang="et-ee"),
                         "kakssada viis tuhat kolmsada kümme")
        self.assertEqual(pronounce_number(1000000, lang="et-ee"), "üks miljon")
        self.assertEqual(pronounce_number(
            2000000, lang="et-ee"), "kaks miljonit")
        self.assertEqual(pronounce_number(
            2000001, lang="et-ee"), "kaks miljonit üks")
        self.assertEqual(pronounce_number(23100000, lang="et-ee"),
                         "kakskümmend kolm miljonit ükssada tuhat")

    def test_convert_negative_int_et(self):
        self.assertEqual(pronounce_number(-1, lang="et-ee"),
                         "miinus üks")
        self.assertEqual(pronounce_number(-10, lang="et-ee"),
                         "miinus kümme")

    def test_convert_decimals_et(self):
        self.assertEqual(pronounce_number(1.234, lang="et-ee"),
                         "üks koma kaks kolm")
        self.assertEqual(pronounce_number(21.234, lang="et-ee"),
                         "kakskümmend üks koma kaks kolm")
        self.assertEqual(pronounce_number(21.234, lang="et-ee", places=1),
                         "kakskümmend üks koma kaks")
        self.assertEqual(pronounce_number(21.234, lang="et-ee", places=0),
                         "kakskümmend üks")
        self.assertEqual(pronounce_number(-1.234, lang="et-ee"),
                         "miinus üks koma kaks kolm")


class TestNiceDateFormat_et(unittest.TestCase):
    def test_convert_times_et(self):
        dt = datetime.datetime(2017, 1, 31, 13, 22, 3)

        self.assertEqual(nice_time(dt, lang="et-ee"),
                         "üks kakskümmend kaks")
        self.assertEqual(nice_time(dt, lang="et-ee", use_ampm=True),
                         "üks kakskümmend kaks pärast lõunat")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False),
                         "01:22")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_ampm=True),
                         "01:22 PM")
        self.assertEqual(nice_time(dt, lang="et-ee",
                                   speech=False, use_24hour=True),
                         "13:22")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "13:22")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=True),
                         "kolmteist kakskümmend kaks")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=False),
                         "kolmteist kakskümmend kaks")

        dt = datetime.datetime(2017, 1, 31, 13, 0, 3)
        self.assertEqual(nice_time(dt, lang="et-ee"), "üks")
        self.assertEqual(nice_time(dt, lang="et-ee", use_ampm=True),
                         "üks pärast lõunat")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False),
                         "01:00")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_ampm=True),
                         "01:00 PM")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True),
                         "13:00")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "13:00")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=True),
                         "kolmteist")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=False),
                         "kolmteist")

        dt = datetime.datetime(2017, 1, 31, 13, 2, 3)
        self.assertEqual(nice_time(dt, lang="et-ee"), "üks null kaks")
        self.assertEqual(nice_time(dt, lang="et-ee", use_ampm=True),
                         "üks null kaks pärast lõunat")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False),
                         "01:02")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_ampm=True),
                         "01:02 PM")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True),
                         "13:02")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "13:02")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=True),
                         "kolmteist null kaks")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=False),
                         "kolmteist null kaks")

        dt = datetime.datetime(2017, 1, 31, 0, 2, 3)
        self.assertEqual(nice_time(dt, lang="et-ee"), "kaksteist null kaks")
        self.assertEqual(nice_time(dt, lang="et-ee", use_ampm=True),
                         "kaksteist null kaks öösel")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False),
                         "12:02")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_ampm=True),
                         "12:02 AM")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True),
                         "00:02")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "00:02")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=True),
                         "null null kaks")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=False),
                         "null null kaks")

        dt = datetime.datetime(2017, 1, 31, 12, 15, 9)
        self.assertEqual(nice_time(dt, lang="et-ee"), "kaksteist viisteist")
        self.assertEqual(nice_time(dt, lang="et-ee", use_ampm=True),
                         "kaksteist viisteist pärast lõunat")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False),
                         "12:15")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_ampm=True),
                         "12:15 PM")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True),
                         "12:15")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "12:15")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=True),
                         "kaksteist viisteist")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=False),
                         "kaksteist viisteist")

        dt = datetime.datetime(2017, 1, 31, 19, 40, 49)
        self.assertEqual(nice_time(dt, lang="et-ee"), "seitse nelikümmend")
        self.assertEqual(nice_time(dt, lang="et-ee", use_ampm=True),
                         "seitse nelikümmend õhtul")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False),
                         "07:40")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_ampm=True),
                         "07:40 PM")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True),
                         "19:40")
        self.assertEqual(nice_time(dt, lang="et-ee", speech=False,
                                   use_24hour=True, use_ampm=True),
                         "19:40")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=True),
                         "üheksateist nelikümmend")
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True,
                                   use_ampm=False),
                         "üheksateist nelikümmend")

        dt = datetime.datetime(2017, 1, 31, 1, 15, 00)
        self.assertEqual(nice_time(dt, lang="et-ee", use_24hour=True),
                         "üks viisteist")

        dt = datetime.datetime(2017, 1, 31, 5, 30, 00)
        self.assertEqual(nice_time(dt, lang="et-ee", use_ampm=True),
                         "viis kolmkümmend hommikul")


if __name__ == "__main__":
    unittest.main()
