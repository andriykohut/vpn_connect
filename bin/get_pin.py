#!/usr/bin/env python2
import sys
from argparse import ArgumentParser
from os.path import abspath, dirname, join, expanduser
from subprocess import PIPE, Popen

from gi.repository import Notify

sys.path.append(join(dirname(dirname(abspath(__file__))), 'lib'))

from config import get_config
from softtoken import SoftToken


def copy_to_clipboard(text):
    cmd = Popen(['xclip', '-selection', 'clipboard'], stdin=PIPE)
    cmd.communicate(text.encode('utf-8'))


def main():
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', help='A path to config file',
                        default="~/.pyvpn")
    args = parser.parse_args()
    Notify.init('SofToken')

    try:
        config = get_config(expanduser(args.config))
        token = SoftToken(config['tuser'], config['consoleui'], config['wine'])
        password = token.get_password(config['tpassword'])
        copy_to_clipboard(password)
        notification = Notify.Notification.new(
            "SoftToken",
            "VPN password copied to clipboard",
            "dialog-information"
        )
        notification.show()
    except Exception as e:
        notification = Notify.Notification.new(
            "SoftToken",
            str(e),
            "dialog-information"
        )
        notification.show()

if __name__ == '__main__':
    main()
