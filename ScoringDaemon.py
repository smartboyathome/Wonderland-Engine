'''
    Copyright (c) 2012 Alexander Abbott

    This file is part of the Cheshire Cyber Defense Scoring Engine (henceforth
    referred to as Cheshire).

    Cheshire is free software: you can redistribute it and/or modify it under
    the terms of the GNU Affero General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.

    Cheshire is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
    more details.

    You should have received a copy of the GNU Affero General Public License
    along with Cheshire.  If not, see <http://www.gnu.org/licenses/>.
'''

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