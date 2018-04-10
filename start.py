#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twitchobserver import Observer
import subprocess
import conf


def parse_line(string):
    string = string.replace('\n', '')
    split = string.split(conf.SYMBOL_COMMAND)
    del split[0]
    message = ''.join(split)
    return message


def read_log(current_line):
    if '[CHAT]' in line and '> ' + conf.SYMBOL_COMMAND in line and conf.MINECRAFT_PSEUDO in line:
        message = parse_line(current_line)
        print("<SIGNAL>: " + str(message))
        observer.send_message(message, conf.TWITCH_CHANNEL)


if __name__ == '__main__':
    try:
        observer = Observer(conf.TWITCH_NICK, conf.TWITCH_OAUTH)
        observer.start()
        observer.join_channel(conf.TWITCH_CHANNEL)
        f = subprocess.Popen(['tail', '-F', '-n', '0', conf.LATEST_LOG], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            line = f.stdout.readline().decode('utf-8')
            read_log(line)
    except (KeyboardInterrupt, SystemExit):
        print("Python script was stop")
        exit(0)
    except:
        exit(1)
