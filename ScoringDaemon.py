import random
from configobj import ConfigObj
import os, threading, redis, time

def monitor(channel, host, port, password):
    _redis = redis.Redis(host, port, password=password)
    pubsub = _redis.pubsub()
    pubsub.subscribe(channel)
    for message in pubsub.listen():
        print "server recieving message:", message['data']
        pass # We'll do something with each message

def message(channel, host, port, password):
    _redis = redis.Redis(host, port, password=password)
    for i in range(0, 13):
        msg = "changed team {}".format(random.randint(1,14))
        print "client sending message:", msg
        _redis.publish(channel, msg)
        time.sleep(2)


def setup_daemons(_config_file=os.path.join(os.getcwd(), 'settings.cfg')):
    config = ConfigObj(_config_file)['CORE']
    args = [
        config['REDIS']['PREFIX']+config['REDIS']['DAEMON_CHANNEL'],
        config['REDIS']['HOST'],
        int(config['REDIS']['PORT']),
        config['REDIS']['PASSWORD']
    ]
    monitor_thread = threading.Thread(target=monitor, args=args)
    monitor_thread.setDaemon(True)
    message_thread = threading.Thread(target=message, args=args)
    return monitor_thread, message_thread

if __name__ == '__main__':
    monitor_thread, message_thread = setup_daemons()
    monitor_thread.start()
    message_thread.start()