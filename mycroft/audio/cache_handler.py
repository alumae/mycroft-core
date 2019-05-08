# Copyright 2019 Mycroft AI Inc.
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

"""
Cache handler - reads all the .dialog files (The default
mycroft responses) and does a tts inference.
It then saves the .wav files to mark1 device

"""

import base64
import glob
import os
import re
import shutil
import hashlib
import json
import mycroft.util as util
from urllib import parse
from requests_futures.sessions import FuturesSession
from mycroft.configuration import Configuration
from mycroft.util.log import LOG


REGEX_SPL_CHARS = re.compile(r'[@#$%^*()<>/\|}{~:]')
MIMIC2_URL = 'https://mimic-api.mycroft.ai/synthesize?text='
TTS = 'Mimic2'

# Check for more default dialogs
res_path = os.path.abspath(os.path.join(os.path.abspath(__file__), '..',
                                        '..', 'res', 'text', 'en-us'))
wifi_setup_path = '/usr/local/mycroft/mycroft-wifi-setup/dialog/en-us'
cache_dialog_path = [res_path, wifi_setup_path]
# Path where cache is stored and not cleared on reboot/TTS change
cache_audio_dir = Configuration.get().get("preloaded_cache").get(TTS)
cache_text_file = os.path.join(cache_audio_dir, 'cache_text.txt')


def generate_cache_text():
    try:
        if not os.path.exists(cache_audio_dir):
            os.mkdir(cache_audio_dir)
        f = open(cache_text_file, 'w')
        for each_path in cache_dialog_path:
            if os.path.exists(each_path):
                write_cache_text(each_path, f)
        f.close()
        LOG.info("Completed generating cache")
    except:
        LOG.info("Could not open text file to write cache")


def write_cache_text(cache_path, f):
    for file in glob.glob(cache_path + "/*.dialog"):
        try:
            with open(file, 'r') as fp:
                all_dialogs = fp.readlines()
                for each_dialog in all_dialogs:
                    # split the sentences
                    each_dialog = re.split(
                        r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\;|\?)\s',
                        each_dialog.strip())
                    for each in each_dialog:
                        if (REGEX_SPL_CHARS.search(each) is None):
                            # Do not consider sentences with special
                            # characters other than any punctuation
                            # ex : <<< LOADING <<<
                            # should not be considered
                            f.write(each.strip() + '\n')
                            # f.write(each)
        except:
            # LOG.info("Dialog Skipped")
            pass


def download_audio():
    cache_audio_files = os.path.join(cache_audio_dir, TTS)
    if not os.path.isdir(cache_audio_files):
        # create if the directory of pre-loaded cache does not exist
        os.mkdir(cache_audio_files)
        session = FuturesSession()
        with open(cache_text_file, 'r') as fp:
            all_dialogs = fp.readlines()
            for each_dialog in all_dialogs:
                each_dialog = each_dialog.strip()
                key = str(hashlib.md5(
                    each_dialog.encode('utf-8', 'ignore')).hexdigest())
                wav_file = os.path.join(cache_audio_files, key + '.wav')
                each_dialog = parse.quote(each_dialog)

                mimic2_url = MIMIC2_URL + each_dialog + '&visimes=True'
                req = session.get(mimic2_url)
                results = req.result().json()
                audio = base64.b64decode(results['audio_base64'])
                vis = results['visimes']
                if audio:
                    try:
                        with open(wav_file, 'wb') as audiofile:
                            audiofile.write(audio)
                    except Exception:
                        # For now skip that .wav file and continue
                        # todo: Add proper log statements
                        pass
                if vis:
                    pho_file = os.path.join(cache_audio_files, key + ".pho")
                    try:
                        with open(pho_file, "w") as cachefile:
                            cachefile.write(json.dumps(vis))  # Mimic2
                            # cachefile.write(str(vis))  # Mimic
                    except Exception:
                        # For now skip that .pho file and continue
                        # todo: Add proper log statements
                        pass
        LOG.info("Completed downloading cache for mimic2")
    else:
        LOG.info("Pre-loaded cache already exists")


def copy_cache():
    source = os.path.join(cache_audio_dir, TTS)
    if os.path.exists(source):
        # get tmp directory where tts cache is stored
        dest = util.get_cache_directory('tts/' + 'Mimic2')
        files = os.listdir(source)
        for f in files:
            shutil.copy2(os.path.join(source, f), dest)
        # todo : get this path from config
        LOG.info("Moved all pre-loaded cache to {}".format(dest))
    else:
        LOG.info("No Source directory for pre-loaded cache")


# Start here
def main():
    generate_cache_text()
    download_audio()
    copy_cache()
