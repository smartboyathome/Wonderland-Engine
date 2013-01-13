Team Routes
===========

These routes relate to retrieving and manipulating a team's configuration for
their machines. These can hold any relevant data pertaining to the machines
that you would like teams to be able to edit. This data is meant to be used by
checks in order to facilitate checking whether a service is up, such as
authentication information for getting access to that service. There is no
checking done on these fields in order to tell whether they are needed or not
by the checks, for that I suggest reading the documentation on the checks
themselves.

.. _cheshire-team_configs-routes-all:

Get All Configs for a Team
--------------------------

.. http:get:: /teams/(team_id)/configs

   Gets all machine configs for a specific team.

   **Example request**:

   .. sourcecode:: http

      GET /teams/1/configs HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json
      [
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
         }
      ]

   **Requires Authentication**: Yes

   **Allowed Roles**: Administrator, Organizer

   **URL Parameters**:
      * *team_id*: The ID of the team which you want to get the machine config
        for.

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
      *No optional JSON parameters are allowed for this interface.*

   **Forbidden JSON Parameters**:
      *No JSON parameters are forbidden for this interface.*

   **Exceptions**:
      * *IllegalParameter*: You submitted parameters with your GET request.
        Parameters are not allowed on this interface.

.. _cheshire-team_configs-routes-create:

Create Config for a Team
------------------------

.. http:post:: /teams/(team_id)/configs

   Creates a new machine config for the team to use in the current scoring
   session.

   **Example request**:

   .. sourcecode:: http

      POST /teams/1/configs HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript
      Content-Type: application/json
      {
         "machine_id": "MongoDB",
         "username": "team1",
         "password": "team1mongo",
         "port": "27017"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 201 Created
      Location: http://example.com/teams/3/configs/MongoDB

   **Requires Authentication**: Yes

   **Allowed Roles**: Administrator

   **URL Parameters**:
      * *team_id*: The ID of the team which you want to get the machine config
        for.

   **Required JSON Parameters**:
      * *machine_id*: This is the name of the machine the config is being
        created for.

   **Optional JSON Parameters**:
     *This allows any parameters to be entered except for those that are*
     *forbidden below.*

   **Forbidden JSON Parameters**:
      * *team_id*

   **Exceptions**:
     * *Exists*: A config for a machine with the specified ID already exists.
       You should modify the config instead of trying to recreate it.
     * *IllegalParameter*: Either a parameter submitted in the request is not
       allowed on this interface, or a parameter is missing from the request.
       See the reason in the exception for more information.

.. _cheshire-team_configs-routes-specific:

Get Specific Config for a Team
------------------------------

.. http:get:: /teams/(team_id)/configs/(machine_id)

   Gets a specific machine's config for a specific team.

   **Example request**:

   .. sourcecode:: http

      GET /teams/1/configs/MongoDB HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json
      {
         "username": "team1",
         "password": "team1mongo",
         "port": "27017"
      }

   **Requires Authentication**: Yes

   **Allowed Roles**: Administrator, Organizer

   **URL Parameters**:
      * *team_id*: The ID of the team you are requesting the config for.
      * *machine_id*: The ID of the machine you are requesting the config for.

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
      *No optional parameters are allowed for this interface.*

   **Forbidden JSON Parameters**:
      *No JSON parameters are forbidden for this interface.*

   **Exceptions**:
      * *IllegalParameter*: You submitted parameters with your GET request.
        Parameters are not allowed on this interface.

.. _cheshire-team_configs-routes-modify:

Modify Specific Config for Team
-------------------------------

.. http:patch:: /teams/(team_id)/configs/(machine_id)

   Modifies a specific machine's config for a specific team.

   **Example request**:

   .. sourcecode:: http

      PATCH /teams/1/configs/MongoDB HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript
      Content-Type: application/json
      {
         "username": "team1a",
         "password": "team1amongo",
         "port": "27018"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 204 No Content

   **Requires Authentication**: Yes

   **Allowed Roles**: Administrator

   **URL Parameters**:
      * *team_id*: The ID of the team you are requesting the config for.
      * *machine_id*: The ID of the machine you are requesting the config for.

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
      *This allows any parameters to be entered except for those that are*
      *forbidden below.*

   **Forbidden JSON Parameters**:
      * *team_id*
      * *machine_id*

   **Exceptions**:
     * *IllegalParameter*: Either a parameter submitted in the request is not
       allowed on this interface, or a parameter is missing from the request.
       See the reason in the exception for more information.

.. _cheshire-team_configs-routes-delete:

Delete Specific Config for Team
-------------------------------

.. http:delete:: /teams/(team_id)/configs/(machine_id)

   Deletes a specific machine's config for a specific team.

   **Example request**:

   .. sourcecode:: http

      DELETE /teams/1/configs/MongoDB HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 204 No Content

   **Requires Authentication**: Yes

   **Allowed Roles**: Administrator

   **URL Parameters**:
      * *team_id*: The ID of the team you are requesting the config for.
      * *machine_id*: The ID of the machine you are requesting the config for.

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
     *No optional parameters are allowed for this interface.*

   **Forbidden JSON Parameters**:
      *No JSON parameters are forbidden for this interface.*

   **Exceptions**:
      * *IllegalParameter*: You submitted parameters with your DELETE request.
        Parameters are not allowed on this interface.