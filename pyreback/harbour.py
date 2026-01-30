# Listen to pings and save them

LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 42324
RECORD_ALL = True
CHANNELS = []

listener = pinglib.listen(LISTEN_IP, LISTEN_PORT)

while ping := listener.receive():
    # If no channels specified, or CHANNELS and ping.channels have a common item
    if RECORD_ALL or not CHANNELS or set(CHANNELS) & set(ping.channels):
        clerk.register_ping(ping.mac, ping.host, ping.ip, ping.data)

