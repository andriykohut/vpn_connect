#!/usr/bin/env python2
import sys
import os
from os.path import dirname, abspath
libpath = os.path.join(dirname(dirname(abspath(__file__))), 'lib')
sys.path.append(libpath)
from optparse import OptionParser
from ConfigParser import ConfigParser
import getpass

from softtoken import SoftToken
from vpnc import VPNConnect

HUMAN_READABLE_NAMES = {
    'tuser': 'SoftToken username',
    'vuser': 'VPN username',
    'gateway': 'VPN gateway name',
    'secret': 'VPN cluster secret',
    'consoleui': 'path to ConsoleUI.exe',
    'tpassword': 'SoftToken password',
    'id': 'VPN cluster id',
    'wine': 'wine executable',
}

def get_opts():
    parser = OptionParser()
    parser.add_option('--config',
                      help='Specify config file path, default "%default"',
                      default='~/.pyvpn')
    parser.add_option('--tuser', help='SoftToken username')
    parser.add_option('--tpassword', help='SoftToken password')
    parser.add_option('--wine', help='Select wine version',
                      choices=('wine', 'wine64'))
    parser.add_option('--consoleui', help='A path to SoftToken consoleui')
    parser.add_option('--gateway', help='Gateway hostname')
    parser.add_option('--id', help='VPN cluster id')
    parser.add_option('--vuser', help='VPN user name')
    parser.add_option('--secret', help='VPN cluster secret')
    parser.add_option('--status', help='Display VPN status.',
                      action='store_true')
    return parser.parse_args()[0].__dict__


def get_config(path):
    parser = ConfigParser()
    parser.read(path)
    config = {}
    config['tuser'] = parser.get('softtoken', 'user')
    config['tpassword'] = parser.get('softtoken', 'password')
    config['wine'] = parser.get('softtoken', 'wine')
    config['consoleui'] = parser.get('softtoken', 'consoleui')
    config['gateway'] = parser.get('vpnc', 'gateway')
    config['id'] = parser.get('vpnc', 'id')
    config['vuser'] = parser.get('vpnc', 'username')
    config['secret'] = parser.get('vpnc', 'secret')
    return config


if __name__ == '__main__':
    opts = get_opts()
    if opts['status']:
        pid = VPNConnect.get_pid()
        if pid:
            print 'vpnc running with PID %s' % pid
        else:
            print 'vpnc is not running'
        sys.exit(0)
    config = get_config(os.path.expanduser((opts['config'])))
    for key, value in opts.items():
        if value:
            config[key] = value
    for unhuman, human in HUMAN_READABLE_NAMES.items():
        if not config[unhuman]:
            if ('password' in unhuman) or ('secret' in unhuman):
                config[unhuman] = getpass.getpass('Please enter %s: ' % human)
            else:
                config[unhuman] = raw_input('Please enter %s: ' % human)
    token = SoftToken(config['tuser'], config['consoleui'], config['wine'])
    vpnpassword = token.get_password(config['tpassword'])
    vpnc = VPNConnect(config['id'], config['gateway'],
                      config['secret'], config['vuser'])
    sudo_pass = getpass.getpass('Enter password for %s: ' % getpass.getuser())
    vpnc.vpn_connect(sudo_pass, vpnpassword)