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

.. _cheshire-current_team_configs-routes-all:

Get All Configs for Current Team
--------------------------------

.. http:get:: /current_team/configs

   Gets all machine configs for the team that the currently logged in user
   belongs to.

   **Example request**:

   .. sourcecode:: http

      GET /current_team/configs HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript
      Cookie: userid=team1

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

   **Allowed Roles**: Team

   **URL Parameters**:
      *There are no URL parameters for this interface.*

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
      *No optional JSON parameters are allowed for this interface.*

   **Forbidden JSON Parameters**:
      *No JSON parameters are forbidden for this interface.*

   **Exceptions**:
      * *IllegalParameter*: You submitted parameters with your GET request.
        Parameters are not allowed on this interface.

.. _cheshire-current_team_configs-routes-create:

Create Config for Current Team
------------------------------

.. http:post:: /current_team/configs

   Creates a new machine config for the team which the currently logged in user
   belongs to use in the current scoring session.

   **Example request**:

   .. sourcecode:: http

      POST /current_team/configs HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript
      Cookie: userid=team1
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
      Location: http://example.com/current_team/configs/MongoDB

   **Requires Authentication**: Yes

   **Allowed Roles**: Team

   **URL Parameters**:
      *There are no URL parameters for this interface.*

   **Required JSON Parameters**:
      * *machine_id*: The ID of the machine you are creating a config for.

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

.. _cheshire-current_team_configs-routes-specific:

Get Specific Config for Current Team
------------------------------------

.. http:get:: /current_team/configs/(machine_id)

   Gets a specific machine's config for the team that the currently logged in
   user belongs to.

   **Example request**:

   .. sourcecode:: http

      GET /current_team/configs/MongoDB HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript
      Cookie: userid=team1

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

   **Allowed Roles**: Team

   **URL Parameters**:
      * *machine_id*: The ID of the machine you are requesting the config for.

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
      *No optional parameters are allowed for this interface.*

   **Forbidden JSON Parameters**:
      *No JSON parameters are forbidden for this interface.*

   **Exceptions**:
      * *IllegalParameter*: You submitted JSON parameters with your GET request.
        Parameters are not allowed on this interface.

.. _cheshire-current_team_configs-routes-modify:

Modify Specific Config for Current Team
---------------------------------------

.. http:patch:: /current_team/configs/(machine_id)

   Modifies a specific machine's config for the team that the currently logged in
   user belongs to.

   **Example request**:

   .. sourcecode:: http

      PATCH /current_team/configs/MongoDB HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript
      Cookie: userid=team1
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

   **Allowed Roles**: Team

   **URL Parameters**:
      * *machine_id*: The ID of the machine you are requesting to modify the
        config for.

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

.. _cheshire-current_team_configs-routes-delete:

Delete Specific Config for Team
-------------------------------

.. http:delete:: /current_team/configs/(machine_id)

   Deletes a specific machine's config for the team that the currently logged in
   user belongs to.

   **Example request**:

   .. sourcecode:: http

      DELETE /current_team/configs/MongoDB HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript
      Cookie: userid=team1

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 204 No Content

   **Requires Authentication**: Yes

   **Allowed Roles**: Team

   **URL Parameters**:
      * *machine_id*: The ID for the machine you are requesting to delete the
        config for.

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
     *No optional parameters are allowed for this interface.*

   **Forbidden JSON Parameters**:
      *No JSON parameters are forbidden for this interface.*

   **Exceptions**:
      * *IllegalParameter*: You submitted parameters with your DELETE request.
        Parameters are not allowed on this interface.