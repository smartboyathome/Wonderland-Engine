from copy import deepcopy
from hashlib import md5
from datetime import timedelta, datetime

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
            'score': 0,
            'timestamp': datetime.now() - timedelta(hours=5)
        },
        {
            'team_id': '6',
            'score': 5,
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
            'id': 'MongoDBCheck',
            'check_type': 'service',
            'module_id': 'ServiceChecks'
        },
        {
            'id': 'RemovedFilesCheck',
            'check_type': 'inject',
            'module_id': 'InjectChecks'
        },
        {
            'id': 'SecurityHole1Check',
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
            'class_name': 'MySQLServiceCheck'
        },
        {
            'id': 'RemovedFiles',
            'description': 'Checks whether each team removed certain files.',
            'machine': 'Apache',
            'type': 'inject',
            'class_name': 'RemovedFilesCheck',
            'inject_number': '42',
            'time_to_check': datetime.now() + timedelta(hours=1)
        },
        {
            'id': 'MySecurityHole',
            'description': 'Checks whether my security hole is still there.',
            'machine': 'Redis',
            'type': 'attacker',
            'team_id': '1',
            'class_name': 'SecurityHole1Check'
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