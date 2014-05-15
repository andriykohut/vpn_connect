from ConfigParser import ConfigParser


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
