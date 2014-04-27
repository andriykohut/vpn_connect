import sys
import pexpect


class InvalidPin(Exception):
    pass


class SoftToken(object):

    def __init__(self, user, consoleui, wine='wine64'):
        self.command = "%s %s %s" % (wine, consoleui, user)

    def get_child(self, debug=False):
        if debug:
            child = pexpect.spawn(self.command, logfile=sys.stdout)
        else:
            child = pexpect.spawn(self.command)
        return child

    def get_password(self, password):
        child = self.get_child()
        child.expect('Enter Pin:')
        child.sendline(password)
        match = child.expect(['Your password is: [0-9A-Z]+', 'Invalid PIN.'])
        if match == 0:
            matched = child.match.group().strip()
            return matched[-8:]
        raise InvalidPin
