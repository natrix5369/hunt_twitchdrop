# -*- coding: utf-8 -*-
# Created by natrix5369
# telegram @natrix5369 @natrix
# vk id552503259

import shutil
import os
import logging
import chardet
import subprocess
import sys
import datetime
import psutil
import time
import multiprocessing
import twitch
import requests
from bs4 import BeautifulSoup

MONITORING_GAME = 'Hunt: Showdown' #game monitoring
twitch_dev_client = '' #twitch client ID
twitch_dev_token = '' #twitch access token

TwitchClient = twitch.TwitchClient(client_id=twitch_dev_client,
                                   oauth_token=twitch_dev_token)


def exec_program_win(arg_program: str, path_program: str = 'start_js.bat', input_stdin=None) -> dict:
    stdout = ''
    stderr = ''
    stdout_enc = dict()
    stderr_enc = dict()

    logging.debug("Processing _exec_program  %s this arg: %s" % (path_program, arg_program))
    win_com = subprocess.Popen("%s %s" % (path_program, arg_program), shell=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

    if input_stdin:
        result = win_com.communicate(input=input_stdin.encode())
    else:
        result = win_com.communicate()

    if result[0]:
        stdout_enc = chardet.detect(result[0])
    elif result[1]:
        stderr_enc = chardet.detect(result[1])
    else:
        logging.warning("Empty program output: %s" % path_program)

    if stdout_enc:
        stdout = result[0].decode(stdout_enc['encoding']).strip()
    if stderr_enc:
        stderr = result[1].decode(stderr_enc['encoding']).strip()
    logging.debug("Output program: %s" % {'stdout': stdout, 'stderr': stderr})
    return {'status_code': 0, 'output': {'stdout': stdout, 'stderr': stderr}, 'error': None}


def get_log_file():
    if len(os.listdir('logs')) > 1:
        raise Exception("Many logs in 'logs' catalog")
    elif len(os.listdir('logs')) == 0:
        raise Exception("Not found logs in 'logs' catalog")

    for i in os.listdir('logs'):
        return os.path.join(os.getcwd() + '\\logs', i)


def stream_is_online(channel):
    data_user = TwitchClient.users.translate_usernames_to_ids(channel)
    if not data_user:
        print("Bad channel: {}".format(channel))
        return False, None

    stream_data = TwitchClient.streams.get_stream_by_user(data_user[0]['id'])
    if stream_data is None:
        print("Stream offline")
        return False, None
    print("Stream is online. Game: '{}'".format(stream_data['game']))
    return True, stream_data['game']


def main(channel):
    print("Run monitoring {}".format(channel))
    proc = multiprocessing.Process(target=exec_program_win, args=(channel,))
    proc.start()
    time.sleep(5)
    log = get_log_file()
    time_start = datetime.datetime.now()
    print("START TIME: {}".format(time_start.strftime("%d/%m/%Y %H:%M")))
    try:
        while True:
            if not proc.is_alive():
                print("[Process script is not alive]")
                break

            with open(log, 'r') as log_file:
                for i in log_file.readlines():
                    if 'Script Error' in i:
                        print("Found error in twitch script. Reboot")
                        raise Exception("Found error: {}".format(i))

            time.sleep(120)
            stream_info = stream_is_online(channel)
            if not stream_info[0]:
                print("Stream is turn off")
                break
            if not stream_info[1] == MONITORING_GAME:
                print("Stream is game '{}'. Must be '{}'".format(stream_info[1], MONITORING_GAME))
                break

            child_procs = list()
            parent = psutil.Process(proc.pid)
            for child in parent.children(recursive=True):
                child_procs.append(child.pid)
            if len(child_procs) < 2:
                raise Exception("Terminate child processes")

            def_time = (datetime.datetime.now() - time_start).seconds
            print("Process time: {} sec {} min {} hour".format(def_time, int(def_time / 60), int(def_time / 3600)))

            # debug
            # print("STOP!")
            # break

    except Exception as e:
        print("Fatal error: {}".format(str(e)))
        # logging

    finally:
        if proc.is_alive():
            parent = psutil.Process(proc.pid)
            for child in parent.children(recursive=True):  # or parent.children() for recursive=False
                child.kill()
            parent.kill()
            while proc.is_alive():
                continue

    print("Exit")
    return 0


def get_channels() -> list:
    #created only for hunt showdown
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://away.vk.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
    }

    response = requests.get('https://www.huntshowdown.com/twitchdrops/streamers', headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    a_tags = soup.findAll("a", class_='streamer')
    streamers_links = list()
    for i in a_tags:
        link = i['href']
        if 'twitch.tv' in link:
            streamers_links.append(link.replace("https://twitch.tv/", ""))
    if not streamers_links:
        print("Not found streamers")
        sys.exit()

    print("Found %s streamers" % len(streamers_links))
    #print(streamers_links)
    #sys.exit()
    return streamers_links



if __name__ == '__main__':
    check_channels = get_channels()
    while True:
        try:
            print("Start BOT by Peter Emelin")
            for num, i in enumerate(check_channels, 1):
                print("\nStart stream: {} ({}/{})".format(i, num, len(check_channels)))
                status_stream = stream_is_online(i)
                if status_stream[0]:
                    if status_stream[1].strip() == MONITORING_GAME:
                        print("Found game '{}'. Open stream...".format(MONITORING_GAME))

                        if os.path.isdir('logs'):
                            shutil.rmtree('logs')

                        main(i)
        except KeyboardInterrupt:
            print("Close app...")
            break
