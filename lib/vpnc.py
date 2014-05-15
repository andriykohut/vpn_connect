import subprocess
import pexpect


class VPNConnect(object):

    def __init__(self, id, gateway, secret, username):
        self.id = id
        self.gateway = gateway
        self.secret = secret
        self.username = username

    def get_child(self):
        command = 'sudo vpnc --gateway %s --id %s --username %s' % (
            self.gateway, self.id, self.username
        )
        print command
        return pexpect.spawn(command)

    def handle_sudo(self, password):
        child = self.get_child()
        match = child.expect(['password for', 'Enter IPSec secret for'])
        if match == 0:
            child.sendline(password)
            child.expect('Enter IPSec secret for')
        return child

    def vpn_connect(self, sudo_password, token):
        child = self.handle_sudo(sudo_password)
        child.sendline(self.secret)
        child.expect('Enter password for %s' % self.username)
        child.sendline(token)
        child.expect('VPNC started in background')
        return True

    @staticmethod
    def get_pid():
        proc = subprocess.Popen(['pgrep', 'vpnc'], stdout=subprocess.PIPE)
        stdout = proc.communicate()[0].strip()
        if stdout:
            return int(stdout)
