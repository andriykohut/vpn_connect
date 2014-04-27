vpn_connect
===========

VPN autoconnection script with SoftToken.

#Requirements:
* vpnc
* SoftToken II with ConsoleUI running on wine
* pexpect
* python-appindicator (for vpn indicator in ubuntu)

#Installation:
Just run pyvpn.py script, try ```pyvpn.py -h``` for help.
If you want vpn indicator for ubuntu, add ```indicator-vpnc.py``` to your startup applications.

#Config:
Copy config example to your home directory:

```cp .pyvpn.example ~/.pyvpn```

Then adjust config options, if you keep some options empty, script will prompt for them.

#Thanks:

Thanks to [jonhadfield](https://github.com/jonhadfield) for vpnc indicator.
