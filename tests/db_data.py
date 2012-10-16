from copy import deepcopy
from hashlib import md5
from datetime import timedelta, datetime

def generate_db_data():
    db_data = {
        'teams': [
            {
                'id': '1',
                'name': 'University of Washington, Seattle'
            },
            {
                'id': '2',
                'name': 'Western Washington University'
            },
            {
                'id': '6',
                'name': 'University of Washington, Bothell'
            }
        ],
        'machines': [
            {
                'id': 'MongoDB',
                'general_ip': '127.0.0.1'
            },
            {
                'id': 'Redis',
                'general_ip': '127.0.0.2'
            },
            {
                'id': 'Apache',
                'general_ip': '127.0.0.3'
            }
        ],
        'team_configs': [
            {
                'team_id': '1',
                'machine_id': 'MongoDB',
                'username': 'team1',
                'password': 'team1mongo',
                'port': '27017'
            },
            {
                'team_id': '1',
                'machine_id': 'Redis',
                'username': 'team1',
                'password': 'team1redis',
                'port': 6379
            },
            {
                'team_id': '1',
                'machine_id': 'Apache',
                'username': 'team1',
                'password': 'team1apache',
                'port': 80
            },
            {
                'team_id': '2',
                'machine_id': 'MongoDB',
                'username': 'team2',
                'password': 'team2mongo',
                'port': 27017
            },
            {
                'team_id': '2',
                'machine_id': 'Redis',
                'username': 'team2',
                'password': 'team2redis',
                'port': 6379
            }
        ],
        'team_scores': [
            {
                'team_id': '1',
                'score': 0,
                'timestamp': datetime.now()
            },
            {
                'team_id': '2',
                'score': 5,
                'timestamp': datetime.now() - timedelta(hours=5)
            },
            {
                'team_id': '6',
                'score': 0,
                'timestamp': datetime.now()
            }
        ],
        'check_scripts': [
            {
                'id': 'ServiceChecks',
                'path': '/example/path/ServiceChecks.py'
            },
            {
                'id': 'InjectChecks',
                'path': '/example/path/InjectChecks.py'
            },
            {
                'id': 'Attacker1Checks',
                'path': '/example/path/Attacker1Checks.py'
            }
        ],
        'check_classes': [
            {
                'id': 'SampleServiceCheck',
                'check_type': 'service',
                'module_id': 'ServiceChecks'
            },
            {
                'id': 'SampleInjectCheck',
                'check_type': 'inject',
                'module_id': 'InjectChecks'
            },
            {
                'id': 'SampleAttackerCheck',
                'check_type': 'attacker',
                'module_id': 'Attacker1Checks'
            }
        ],
        'active_checks': [
            {
                'id': 'MongoDBUp',
                'description': 'Checks whether MongoDB is up.',
                'machine': 'MongoDB',
                'type': 'service',
                'class_name': 'SampleServiceCheck'
            },
            {
                'id': 'EmailUp',
                'description': 'Checks whether email is up.',
                'machine': 'MongoDB',
                'type': 'service',
                'class_name': 'SampleServiceCheck'
            },
            {
                'id': 'DeadThingUp',
                'description': 'Checks whether a failing service is up.',
                'machine': 'MongoDB',
                'type': 'service',
                'class_name': 'SampleServiceCheck'
            },
            {
                'id': 'RemovedFiles',
                'description': 'Checks whether each team removed certain files.',
                'machine': 'Apache',
                'type': 'inject',
                'class_name': 'SampleInjectCheck',
                'inject_number': '42',
                'time_to_check': datetime.now() + timedelta(seconds=3)
            },
            {
                'id': 'AdjustedSpamFilter',
                'description': 'Checks whether each team adjusted the spam filter to catch more spam.',
                'machine': 'MongoDB',
                'type': 'inject',
                'class_name': 'SampleInjectCheck',
                'inject_number': '14',
                'time_to_check': datetime.now() + timedelta(hours=1, minutes=30)
            },
            {
                'id': 'UnspecifiedInject',
                'description': 'Checks whether an unspecified inject was completed.',
                'machine': 'Redis',
                'type': 'inject',
                'class_name': 'SampleInjectCheck',
                'inject_number': '-1',
                'time_to_check': datetime.now() + timedelta(hours=36)
            },
            {
                'id': 'MySecurityHole',
                'description': 'Checks whether my security hole is still there.',
                'machine': 'Redis',
                'type': 'attacker',
                'team_id': '1',
                'class_name': 'SampleAttackerCheck'
            },
            {
                'id': 'MySecurityHole',
                'description': 'Checks whether my security hole is still there.',
                'machine': 'Redis',
                'type': 'attacker',
                'team_id': '2',
                'class_name': 'SampleAttackerCheck'
            },
            {
                'id': 'MongoDBExploit',
                'description': 'Checks whether the exploit in MongoDB has been patched.',
                'machine': 'MongoDB',
                'type': 'attacker',
                'team_id': '6',
                'class_name': 'SampleAttackerCheck'
            },
            {
                'id': 'BrokenExploit',
                'description': 'This exploit is broken and does not work.',
                'machine': 'Redis',
                'type': 'attacker',
                'team_id': '2',
                'class_name': 'SampleAttackerCheck'
            }
        ],
        'completed_checks': [
            {
                'id': 'MongoDBUp',
                'description': 'Checks whether MongoDB is up.',
                'type': 'service',
                'timestamp': datetime.now() - timedelta(hours=5),
                'team_id': '1',
                'score': 0
            },
            {
                'id': 'MongoDBUp',
                'description': 'Checks whether MongoDB is up.',
                'type': 'service',
                'timestamp': datetime.now() - timedelta(hours=3),
                'team_id': '1',
                'score': 0
            },
            {
                'id': 'MongoDBUp',
                'description': 'Checks whether MongoDB is up.',
                'type': 'service',
                'timestamp': datetime.now() - timedelta(hours=5),
                'team_id': '6',
                'score': 5
            },
            {
                'id': 'RemovedFiles',
                'description': 'Checks whether each team removed certain files.',
                'type': 'inject',
                'inject_number': 5,
                'time_to_check': datetime.now() - timedelta(hours=5, minutes=5),
                'timestamp': datetime.now() - timedelta(hours=5),
                'team_id': '1',
                'score': 0
            },
            {
                'id': 'RemovedFiles',
                'description': 'Checks whether each team removed certain files.',
                'type': 'inject',
                'inject_number': 5,
                'time_to_check': datetime.now() - timedelta(hours=5, minutes=5),
                'timestamp': datetime.now() - timedelta(hours=5),
                'team_id': '2',
                'score': 0
            },
            {
                'id': 'BoardPresentation',
                'description': 'The teams present to a board on what they did.',
                'comments': 'This team did great! They definitely deserve full points!',
                'type': 'manual',
                'inject_number': '107',
                'timestamp': datetime.now() - timedelta(hours=4),
                'team_id': '6',
                'score': 10
            },
            {
                'id': 'BoardPresentation',
                'description': 'The teams present to a board on what they did.',
                'comments': "This team didn't put any effort into their presentation, so we failed them.",
                'type': 'manual',
                'inject_number': '107',
                'timestamp': datetime.now() - timedelta(hours=3, minutes=55),
                'team_id': '1',
                'score': 0
            },
            {
                'id': 'USBPolicy',
                'description': 'The teams had to write up a policy on how usb devices could be used.',
                'comments': "This paper wasn't any good. We couldn't understand what they were saying.",
                'type': 'manual',
                'inject_number': '114',
                'timestamp': datetime.now() - timedelta(hours=3, minutes=50),
                'team_id': '1',
                'score': 0
            },
            {
                'id': 'MySecurityHole',
                'description': 'Checks whether my security hole is still there.',
                'machine': 'Redis',
                'type': 'attacker',
                'timestamp': datetime.now() - timedelta(hours=2, minutes=22),
                'team_id': '1',
                'score': -5
            },
            {
                'id': 'MySecurityHole',
                'description': 'Checks whether my security hole is still there.',
                'machine': 'Redis',
                'type': 'attacker',
                'timestamp': datetime.now() - timedelta(hours=1, minutes=52),
                'team_id': '1',
                'score': -5
            },
            {
                'id': 'MySecurityHole',
                'description': 'Checks whether my security hole is still there.',
                'machine': 'Redis',
                'type': 'attacker',
                'timestamp': datetime.now() - timedelta(hours=1, minutes=22),
                'team_id': '1',
                'score': -5
            }
        ],
        'users': [
            {
                'id': 'team1',
                'password': md5('uw seattle').hexdigest(),
                'email': 'team1@example.com',
                'role': 'team',
                'team': '1'
            },
            {
                'id': 'admin',
                'password': md5('admin').hexdigest(),
                'email': 'admin@example.com',
                'role':'administrator'
            },
            {
                'id': 'white_team',
                'password': md5('white_team').hexdigest(),
                'email': 'white_team@example.com',
                'role': 'organizer'
            },
            {
                'id': 'evil_red_team',
                'password': md5('evil_red_team').hexdigest(),
                'email': 'evil_red_team@example.com',
                'role': 'attacker'
            }
        ],
        'session': [
            {
                'start_time': datetime.now() - timedelta(hours=5),
                'end_time': datetime.now() + timedelta(minutes=15),
                'state': 'stopped'
            }
        ]
    }
    db_data['archived_sessions'] = [deepcopy(db_data)]
    db_data['archived_sessions'][0]['id'] = 'first_session'
    for user in db_data['archived_sessions'][0]['users']:
        del user['password']
    return db_data