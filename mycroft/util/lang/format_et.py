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

from math import floor

from mycroft.util.lang.format_common import convert_to_mixed_fraction

months = ['jaanuar', 'veebruar', 'märts', 'aprill', 'mai', 'juuni',
          'juuli', 'august', 'september', 'oktoober', 'november',
          'detsember']

NUM_STRING_ET_NOM = {
    0: 'null',
    1: 'üks',
    2: 'kaks',
    3: 'kolm',
    4: 'neli',
    5: 'viis',
    6: 'kuus',
    7: 'seitse',
    8: 'kaheksa',
    9: 'üheksa',
    10: 'kümme',
    11: 'üksteist',
    12: 'kaksteist',
    13: 'kolmteist',
    14: 'neliteist',
    15: 'viisteist',
    16: 'kuusteist',
    17: 'seitseteist',
    18: 'kaheksateist',
    19: 'üheksateist',
    20: 'kakskümmend',
    30: 'kolmkümmend',
    40: 'nelikümmend',
    50: 'viiskümmend',
    60: 'kuuskümmend',
    70: 'seitsekümmend',
    80: 'kaheksakümmend',
    90: 'üheksakümmend',
    100: 'sada'
}

NUM_STRING_ET_GEN = {
    0: 'nulli',
    1: 'ühe',
    2: 'kahe',
    3: 'kolme',
    4: 'nelja',
    5: 'viie',
    6: 'kuue',
    7: 'seitsme',
    8: 'kaheksa',
    9: 'üheksa',
    10: 'kümne',
    11: 'üheteistkümne',
    12: 'kaheteistkümne',
    13: 'kolmeteistkümne',
    14: 'neljateistkümne',
    15: 'viieteistkümne',
    16: 'kuueteistkümne',
    17: 'seitsmeteistkümne',
    18: 'kaheksateistkümne',
    19: 'üheksateistkümne',
    20: 'kahekümne',
    30: 'kolmekümne',
    40: 'neljakümne',
    50: 'viiekümne',
    60: 'kuuekümne',
    70: 'seitsmekümne',
    80: 'kaheksakümne',
    90: 'üheksakümne',
    100: 'saja'
}


NUM_POWERS_OF_TEN_NOM = [
    '', 'tuhat', 'miljon', 'miljard', 'billjon', 'biljard', 'trilljon',
    'trilljard'
]

NUM_POWERS_OF_TEN_GEN = [
    '', 'tuhande', 'miljoni', 'miljardi', 'billjoni', 'biljardi', 'trilljoni',
    'trilljardi'
]


FRACTION_STRING_ET = {
    2: 'pool',
    3: 'kolmandik',
    4: 'neljandik',
    5: 'viiendik',
    6: 'kuuendik',
    7: 'seitsmendik',
    8: 'kaheksandik',
    9: 'üheksandik',
    10: 'kümnendik',
    11: 'üheteistkümnendik',
    12: 'kaheteistkümnendik',
    13: 'kolmeteistkümnendik',
    14: 'neljateistkümnendik',
    15: 'viieteistkümnendik',
    16: 'kuueteistkümnendik',
    17: 'seitsmeteistkümnendik',
    18: 'kaheksateistkümnendik',
    19: 'üheksateistkümnendik',
    20: 'kahekümnendik'
}


def maybe_space(condition):
    if condition:
        return " "
    else:
        return ""


def nice_number_et(number, speech, denominators):
    """ Estonian helper for nice_number
    This function formats a float to human understandable functions. Like
    4.5 becomes "4 ja pool" for speech and "4 1/2" for text
    Args:
        number (int or float): the float to format
        speech (bool): format for speech (True) or display (False)
        denominators (iter of ints): denominators to use, default [1 .. 20]
    Returns:
        (str): The formatted string.
    """
    result = convert_to_mixed_fraction(number, denominators)
    if not result:
        # Give up, just represent as a 3 decimal number
        return str(round(number, 3)).replace(".", ",")
    whole, num, den = result
    if not speech:
        if num == 0:
            # TODO: Number grouping?  E.g. "1,000,000"
            return str(whole)
        else:
            return '{} {}/{}'.format(whole, num, den)
    if num == 0:
        return str(whole)
    den_str = FRACTION_STRING_ET[den]
    if whole == 0:
        if num == 1:
            if den == 2:
                return_string = '{}'.format(den_str)
            else:
                return_string = '{} {}'.format(num, den_str)
        else:
            return_string = '{} {}ku'.format(num, den_str)
    else:
        if num == 1:
            if den == 2:
                return_string = '{} ja {}'.format(whole, den_str)
            else:
                return_string = '{} ja {} {}'.format(whole, num, den_str)
        else:
            return_string = '{} ja {} {}ku'.format(whole, num, den_str)

    return return_string


def pronounce_number_et(num, places=2):
    """
    Convert a number to its spoken equivalent
    For example, '5.2' would return 'viis koma kaks'
    Args:
        num(float or int): the number to pronounce (set limit below)
        places(int): maximum decimal places to speak
    Returns:
        (str): The pronounced number

    """
    return pronounce_number_et_impl(num, places, ordinal=False)


def pronounce_number_et_impl(num, places=2, ordinal=False):
    if ordinal:
        num_string = NUM_STRING_ET_GEN
        num_powers_of_ten = NUM_POWERS_OF_TEN_GEN
    else:
        num_string = NUM_STRING_ET_NOM
        num_powers_of_ten = NUM_POWERS_OF_TEN_NOM

    def pronounce_triplet_et(num):
        result = ""
        num = floor(num)
        if num > 99:
            hundreds = floor(num / 100)
            if hundreds > 0:
                result += num_string[
                    hundreds] + num_string[100]
                num -= hundreds * 100
                if num > 0:
                    result += " "
        if num == 0:
            result += ''  # do nothing
        elif num == 1:
            result += 'üks'  
        elif num <= 20:
            result += num_string[num]
        elif num > 20:
            ones = num % 10
            tens = num - ones
            if tens > 0:
                result += num_string[tens]
                if ones > 0:
                    result += " "
            if ones > 0:
                result += num_string[ones]
        return result

    def pronounce_fractional_et(num, places):
        # fixed number of places even with trailing zeros
        result = ""
        place = 10
        while places > 0:
            # doesn't work with 1.0001 and places = 2: int(
            # num*place) % 10 > 0 and places > 0:
            result += " " + num_string[int(num * place) % 10]
            place *= 10
            places -= 1
        return result

    def pronounce_whole_number_et(num, scale_level=0):
        if num == 0:
            return ''

        num = floor(num)
        result = ''
        last_triplet = num % 1000

        if last_triplet == 1:
            if scale_level == 0:
                if result != '':
                    result += '' + num_string[1]
                else:
                    result += num_string[1]
            elif scale_level == 1:
                result += num_powers_of_ten[1]
            else:
                result += "üks " + num_powers_of_ten[scale_level]
        elif last_triplet > 1:
            result += pronounce_triplet_et(last_triplet)
            if scale_level == 1:
                result += ' ' + num_powers_of_ten[1]
            if scale_level >= 2:
                result += " " + num_powers_of_ten[scale_level]
            if scale_level >= 2:
                if scale_level % 2 == 0:
                    # result += "it"  # miljonit
                    pass
                result += "it"  # miljardit, miljonit

        num = floor(num / 1000)
        scale_level += 1
        next_scale_result = pronounce_whole_number_et(num, scale_level)
        return next_scale_result + maybe_space(next_scale_result != "" and result != "") + result

    result = ""

    if abs(num) >= 1000000000000000000000000:  # cannot do more than this
        return str(num)
    elif num == 0:
        return str(num_string[0]) + ("s" if ordinal else "")
    elif num < 0:
        return "miinus " + pronounce_number_et(abs(num), places)
    else:
        if num == int(num):
            result = pronounce_whole_number_et(num) + ("s" if ordinal else "")
            if ordinal:
                result = result.replace("ühes", "esimene")
                result = result.replace("kahes", "teine")
                result = result.replace("kolmes", "kolmas")
            return result
        else:
            whole_number_part = floor(num)
            fractional_part = num - whole_number_part
            result += pronounce_whole_number_et(whole_number_part)
            if places > 0:
                result += " koma"
                result += pronounce_fractional_et(fractional_part, places)
            return result


def pronounce_ordinal_et(num):
    return pronounce_number_et_impl(num, places=2, ordinal=True)


def nice_time_et(dt, speech=True, use_24hour=False, use_ampm=False):
    """
    Format a time to a comfortable human format

    For example, generate 'viis kolmkümmend' for speech or '5:30' for
    text display.

    Args:
        dt (datetime): date to format (assumes already in local timezone)
        speech (bool): format for speech (default/True) or display (False)=Fal
        use_24hour (bool): output in 24-hour/military or 12-hour format
        use_ampm (bool): include the am/pm for 12-hour format
    Returns:
        (str): The formatted time string
    """
    if use_24hour:
        # e.g. "03:01" or "14:22"
        string = dt.strftime("%H:%M")
    else:
        if use_ampm:
            # e.g. "3:01 AM" or "2:22 PM"
            string = dt.strftime("%I:%M %p")
        else:
            # e.g. "3:01" or "2:22"
            string = dt.strftime("%I:%M")

    if not speech:
        return string

    # Generate a speakable version of the time
    speak = ""
    if use_24hour:
        if dt.hour == 1:
            speak += "üks"  # 01:00 is "et" not "en"
        else:
            speak += pronounce_number_et(dt.hour)
        if not dt.minute == 0:
            if dt.minute < 10:
                speak += ' null'
            speak += " " + pronounce_number_et(dt.minute)

        return speak  # ampm is ignored when use_24hour is true
    else:
        if dt.hour == 0 and dt.minute == 0:
            return "kesköö"
        if dt.hour == 12 and dt.minute == 0:
            return "keskpäev"
        # TODO: "half past 3", "a quarter of 4" and other idiomatic times

        if dt.hour == 0:
            speak += pronounce_number_et(12)
        elif dt.hour <= 13:
            if dt.hour == 1 or dt.hour == 13:  # 01:00 and 13:00 is "et"
                speak += 'üks'
            else:
                speak += pronounce_number_et(dt.hour)
        else:
            speak += pronounce_number_et(dt.hour - 12)

        if not dt.minute == 0:
            if dt.minute < 10:
                speak += ' null'
            speak += " " + pronounce_number_et(dt.minute)

        if use_ampm:
            if dt.hour > 11:
                if dt.hour < 18:
                    # 12:01 - 17:59 nachmittags/afternoon
                    speak += " pärast lõunat"
                elif dt.hour < 22:
                    # 18:00 - 21:59 abends/evening
                    speak += " õhtul"
                else:
                    # 22:00 - 23:59 nachts/at night
                    speak += " öösel"
            elif dt.hour < 3:
                # 00:01 - 02:59 nachts/at night
                speak += " öösel"
            else:
                # 03:00 - 11:59 morgens/in the morning
                speak += " hommikul"

        return speak


def nice_response_et(text):
    # check for months and call nice_ordinal_et declension of ordinals
    # replace "^" with "hoch" (to the power of)
    words = text.split()

    for idx, word in enumerate(words):
        if word.lower() in months:
            text = nice_ordinal_et(text)

        if word == '^':
            wordNext = words[idx + 1] if idx + 1 < len(words) else ""
            if wordNext.isnumeric():
                words[idx] = "astmes"
                text = " ".join(words)
    return text


def nice_ordinal_et(text):
    normalized_text = text
    words = text.split()

    for idx, word in enumerate(words):
        wordNext = words[idx + 1] if idx + 1 < len(words) else ""
        wordPrev = words[idx - 1] if idx > 0 else ""
        if word[-1:] == ".":
            if word[:-1].isdecimal():
                if wordNext.lower() in months:
                    word = pronounce_ordinal_et(int(word[:-1]))
                    words[idx] = word
            normalized_text = " ".join(words)
    return normalized_text
