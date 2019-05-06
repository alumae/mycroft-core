# Cache handler - reads all the .dialog files (The default
# mycroft responses) and does a tts inference.
# It then saves the .wav files to mark1 device

import base64
import glob
import os
import re
import shutil
import hashlib
import json
from urllib import parse
from requests_futures.sessions import FuturesSession
from mycroft.util.log import LOG


REGEX_SPL_CHARS = re.compile('[@#$%^*()<>/\|}{~:]')
MIMIC2_URL = 'https://mimic-api.mycroft.ai/synthesize?text='

# Check for more default dialogs
res_path = '/opt/venvs/mycroft-core/lib/python3.4/' \
           'site-packages/mycroft/res/text/en-us/'
wifi_setup_path = '/usr/local/mycroft/mycroft-wifi-setup/dialog/en-us/'
cache_dialog_path = [res_path, wifi_setup_path]
# Path where cache is stored and not cleared on reboot/TTS change
cache_audio_dir = '/opt/mycroft/preloaded_cache'
cache_text_file = cache_audio_dir + '/cache_text.txt'


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
    for file in glob.glob(cache_path + "*.dialog"):
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
    if not os.path.isdir(cache_audio_dir + '/Mimic2'):
        # create if the directory of pre-loaded cache does not exist
        cache_audio_files = cache_audio_dir + '/Mimic2'
        os.mkdir(cache_audio_files)
        session = FuturesSession()
        with open(cache_text_file, 'r') as fp:
            all_dialogs = fp.readlines()
            for each_dialog in all_dialogs:
                each_dialog = each_dialog.strip()
                key = str(hashlib.md5(
                    each_dialog.encode('utf-8', 'ignore')).hexdigest())
                wav_file = cache_audio_files + '/' + key + '.wav'
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


def move_cache():
    source = cache_audio_dir + '/Mimic2'
    if os.path.exists(source):
        # tmp directory where tts cache is stored
        dest = '/tmp/mycroft/cache/tts/Mimic2'
        if not os.path.exists(dest):
            os.makedirs(dest)
        files = os.listdir(source)
        for f in files:
            shutil.copy2(source + '/' + f, dest)
        # todo : get this path from config
        LOG.info("Moved all pre-loaded cache to /tmp/mycroft/cache/tts/Mimic2")
    else:
        LOG.info("No Source directory for pre-loaded cache")


# Start here
def main():
    generate_cache_text()
    download_audio()
    move_cache()
