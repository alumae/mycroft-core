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
from datetime import datetime

from dateutil.relativedelta import relativedelta

from mycroft.util.lang.format_et import pronounce_number_et
from mycroft.util.lang.parse_common import (extract_numbers_generic,
                                            is_numeric, look_for_fractions)


numbers_nom = "null üks kaks kolm neli viis kuus seitse kaheksa üheksa kümme".split()
numbers_gen = "nulli ühe kahe kolme nelja viie kuue seitsme kaheksa üheksa kümne".split()
numbers_part = "nulli ühte kahte kolme nelja viite kuute setset kaheksat üheksat kümmet".split()

numbers_ord_nom = "nullis esimene teine kolmas neljas viies kuues seitsmes kaheksas üheksas kümnes".split()
numbers_ord_gen = "nullinda esimese teise kolmanda neljanda viienda kuuenda seitsmenda kahsanda üheksanda kümnenda".split()
numbers_ord_part = "nullindat esimest teist kolmandat neljandat viiendat kuuendat seitsmendat kaheksandat üheksandat kümnendat".split()

suffixes = "sse s st le l lt ks ni na ta ga".split()

# Converts words like "üks", "ühe", "kolmandale" (up to 10) to numbers
def convert_words_to_numbers(text):
    result = []
    for word in text.split():
        matched = False
        for numbers_list in [numbers_nom, numbers_gen, numbers_part, numbers_ord_nom, numbers_ord_gen, numbers_ord_part]:
            if word in numbers_list:
                result.append(str(numbers_list.index(word)))
                matched = True
                break
        if not matched:
            for suffix in suffixes:
                for i, number_word in enumerate(numbers_gen):
                    if word == number_word + suffix:
                        result.append(str(i))
                        matched = True
                        break
        if not matched:
            for suffix in suffixes:
                for i, number_word in enumerate(numbers_ord_gen):
                    if word == number_word + suffix:
                        result.append(str(i))
                        matched = True
                        break
        if not matched:
            result.append(word)
    return " ".join(result)



def extractnumber_et(text):
    text = convert_words_to_numbers(text)
    val = None
    for word in text.split():
        # ordinal are written like "4.""
        if word.endswith(".") and word[:-1].isdigit():
            val = int(word[:-1])
        if is_numeric(word):
            if word.isdigit():
                val = int(word)
            else:
                val = float(word)
            break
    if not val:
        return False

    return val


def extract_datetime_et(string, currentDate, default_time):
    # TODO: implement this
    return None

def normalize_et(text, remove_articles):
    """ Estonian string normalization """

    text = convert_words_to_numbers(text)

    return text


