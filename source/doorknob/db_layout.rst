Database structure::

    teams: [ # Index on id
        {
            "id": str,
            "name": str
        }
    ]

    team_configs: [ # Index on team_id, then machine_id
        {
            "team_id": str,
            "machine_id": str,
            "username": str,
            "password": str,
            "port": int
        }
    ]

    team_scores: [
        {
            "team_id": str,
            "score": int,
            "timestamp": datetime # timestamp of last check used
        }
    ]

    completed_checks: [ # Index on id, then team_id, then timestamp
        {
            "id": str,
            "description": str,
            "type": str, # Type may be Service, Inject, Manual, or Attacker.
            "timestamp": datetime,
            "team_id": str,
            "score": int,
            # More fields may be present depending on type
        }
    ]

    active_checks: [ # Index on id
        {
            "id": str,
            "description": str,
            "type": str, # Type may be Service, Inject, or Attacker. Manual
                         # checks are completed immediately and team dependent,
                         # so they can't be stored here.
            "class_name": str,
            # More fields may be present depending on type
        }
    ]

    check_scripts: [ # Index on module_name
        {
            "id": str,
            "path": str
        }
    ]

    check_classes: [ # Index on class_name
        {
            "id": str,
            "check_type": str,
            "module_id": str
        }
    ]

    machines: [ # Index on id
        {
            "id": str,
            "general_ip": str # This requires that at least one character in
                              # the IP address be replaced with {team}. This
                              # is to be replaced by the team's ID.
        }
    ]

    users: [ # Index on id
        {
            "id": str,
            "password" str, # This will be a hash, probably using bcrypt
            "email": str,
            "role": str
            # More fields may be present depending on role
        }
    ]

    session: [ # This should only have one element
        {
            "start_time": datetime,
            "end_time": datetime,
            "state": str # Could be "started", or "stopped"
        }
    ]

    archived_sessions: [ # Index on session.started_at and then session.ended_at
        {
            # These will all mirror the above sections
            "teams": [
                ...
            ],
            "completed_checks": [
                ...
            ],
            "active_checks": [
                ...
            ],
            "check_scripts": [
                ...
            ],
            "check_classes": [
                ...
            ],
            "machines": [
                ...
            ],
            "users": [
                ...
            ],
            "session": {
                "started_at": datetime,
                "ended_at": datetime,
                "total_time": timedelta
            },
            "id": str
        }
    ]

That was the database structure.