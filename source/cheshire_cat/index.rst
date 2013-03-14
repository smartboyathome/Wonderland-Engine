Cheshire Cat
============

Cheshire Cat is the name of the REST API that was built to allow access to the
underlying scoring engine. It talks to to the scoring engine through
:doc:`Doorknob </doorknob/index>`
and Redis, and is generally a frontend to Doorknob. All the views are
implemented as plugins, and are loaded dynamically from the blueprints folder
upon startup, so routes can be added, removed, and renamed easily, without
having to modify any other code. Each route has a number of properties, such as
whether users need to be logged in to access it, what user role(s) are allowed
to access it, and what parameters are allowed to be passed to it. Unless
otherwise stated, all routes require a user to log in to be able to access
them.

*Please note*: Until this documentation is complete, you can find how routes
are to be used by looking in Cheshire Cat's tests.

.. toctree::
   :hidden:

   routes/default
   routes/teams
   routes/current_team
   routes/team_configs
   routes/current_team_configs
   routes/team_checks

Routes Overview
---------------

:doc:`Defaults <routes/default>`

* :ref:`Index <cheshire-default-routes-index>`

:doc:`Teams <routes/teams>`

* :ref:`Get all teams <cheshire-team-routes-all>`

* :ref:`Create team <cheshire-team-routes-create>`

* :ref:`Get specific team <cheshire-team-routes-specific>`

* :ref:`Modify team <cheshire-team-routes-modify>`

* :ref:`Remove team <cheshire-team-routes-delete>`

:doc:`Current Team <routes/current_team>`

* :ref:`Get current team <cheshire-current_team-routes-get>`

:doc:`Team Configuration <routes/team_configs>`

* :ref:`Get all configs for team <cheshire-team_configs-routes-all>`

* :ref:`Create team config for machine <cheshire-team_configs-routes-create>`

* :ref:`Get team config for machine <cheshire-team_configs-routes-specific>`

* :ref:`Modify team config for machine <cheshire-team_configs-routes-modify>`

* :ref:`Remove team config for machine <cheshire-team_configs-routes-delete>`

:doc:`Current Team Configuration <routes/current_team_configs>`

* :ref:`Get all configs for current team <cheshire-current_team_configs-routes-all>`

* :ref:`Create config for current team's machine <cheshire-current_team_configs-routes-create>`

* :ref:`Get specific config for current team's machine <cheshire-current_team_configs-routes-specific>`

* :ref:`Modify config for current team's machine <cheshire-current_team_configs-routes-modify>`

* :ref:`Remove config for current team's machine <cheshire-current_team_configs-routes-delete>`

:doc:`Team Checks <routes/team_checks>`

* :ref:`Get all completed checks for all teams <cheshire-team_checks-routes-all>`

* :ref:`Get all completed checks for specific team <cheshire-team_checks-routes-specific>`

Team Service Checks

* Get all completed service checks for specific team

* Get specific completed service check for specific team

Team Inject Checks

* Get all completed inject checks for specific team

* Get specific completed inject check for specific team

Team Attacker Checks

* Get all completed attacker checks for specific team

* Create attacker check for specific team

* Get specific completed attacker check for specific team

* Modify specific attacker check for specific team

* Remove specific attacker check for specific team

Team Manual Checks

* Get all completed manual checks for specific team

* Create manual check for specific team

* Get specific completed manual check for specific team

* Modify specific manual check for specific team

* Remove specific manual check for specific team