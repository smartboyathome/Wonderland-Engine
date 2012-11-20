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

.. toctree::
   :hidden:

   default_routes

Routes Overview
---------------

:doc:`Default Routes <default_routes>`

* :ref:`Index <cheshire-default-routes-index>`

Teams

* Get all teams

* Create team

* Get specific team

* Modify team

* Remove team

Current Team

* Get current team

Team Configuration

* Get all configs for team

* Create team config for machine

* Get team config for machine

* Modify team config for machine

* Remove team config for machine

Current Team Configuration

* Get all configs for current team

* Create config for current team's machine

* Get specific config for current team's machine

* Modify config for current team's machine

* Remove config for current team's machine

Team Checks

* Get all completed checks for specific team

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