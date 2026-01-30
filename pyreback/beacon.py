# Send UDP

import socket

import niclib


SLEEP_TIME = 60
HOSTNAME = socket.gethostname()


nics = [ nic for nic in niclib.get_public_nics() if (
                nic.ip4ip and not nic.ip4ip.startswith("127.")
                )]

for nic in nics:
    sysload = get_system_load() # --> ensure this works for Windows too

    if nic.ip4brd:
        pinglib.pingout(nic.ip4brd, nic.ip4ip, HOSTNAME, sysload)
    if nic.ip6brd:
        pinglib.pingout(nic.ip6brd, nic.ip6ip, HOSTNAME, sysload)

    time.sleep(SLEEP_TIME)

