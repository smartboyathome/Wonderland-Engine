Team Routes
===========

These routes relate to retrieving and manipulating a team's information, which,
by default, includes the name of the team and their ID (used for the IPs of
machines). They do not deal with team configuration or team checks, however.

.. _cheshire-team-routes-all:

Get All Teams
-------------

.. http:get:: /teams

   Gets information for all teams that have been created in the current scoring
   session.

   **Example request**:

   .. sourcecode:: http

      GET /teams HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json
      [
         {
             'id': '1',
             'name': 'Team A'
         },
         {
             'id': '2',
             'name': 'Team B'
         }
      ]

   **URL Parameters**:
      *There are no URL parameters for this interface.*

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
      *No optional JSON parameters are allowed for this interface.*

   **Exceptions**:
      * *IllegalParameter*: You submitted parameters with your GET request.
        Parameters are not allowed on this interface.

.. _cheshire-team-routes-create:

Create Team
-----------

.. http:post:: /teams

   Creates a new team for use in the current scoring session.

   **Example request**:

   .. sourcecode:: http

      POST /teams HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript
      Content-Type: application/json
      {
         'name': 'Team C',
         'id': '3'
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 201 Created
      Location: http://example.com/teams/3

   **URL Parameters**:
      *There are no URL parameters for this interface.*

   **Required JSON Parameters**:
      * *name*: This is the name of the team.
      * *id*: This is the ID of the team, which is what is placed in the
        relevant position in each machine's ID.

   **Optional JSON Parameters**:
     *No optional parameters are allowed for this interface.*

   **Exceptions**:
     * *Exists*: A team with the specified ID already exists. You must specify
       a different ID for the team.
     * *IllegalParameter*: Either a parameter submitted in the request is not
       allowed on this interface, or a parameter is missing from the request.
       See the reason in the exception for more information.

.. _cheshire-team-routes-specific:

Get Specific Team
-----------------

.. http:get:: /teams/(team_id)

   Gets information on a specific team with the ID ``team_id``.

   **Example request**:

   .. sourcecode:: http

      GET /teams/1 HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json
      {
         'id': '1',
         'name': 'Team A'
      }

   **URL Parameters**:
      * *team_id*: The ID for the team you are requesting information for.

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
     *No optional parameters are allowed for this interface.*

   **Exceptions**:
      * *IllegalParameter*: You submitted parameters with your GET request.
        Parameters are not allowed on this interface.

.. _cheshire-team-routes-modify:

Modify Team
-----------

.. http:patch:: /teams/(team_id)

   Modifies the information for a team specified by ``team_id``.

   **Example request**:

   .. sourcecode:: http

      PATCH /teams/1 HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript
      Content-Type: application/json
      {
         'name': 'A'
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 204 No Content

   **URL Parameters**:
      * *team_id*: The ID for the team you are requesting information for.

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
     * *name*: The name of the team.

   **Exceptions**:
     * *IllegalParameter*: Either a parameter submitted in the request is not
       allowed on this interface, or a parameter is missing from the request.
       See the reason in the exception for more information.

.. _cheshire-team-routes-delete:

Delete Team
-----------

.. http:delete:: /teams/(team_id)

   Deletes a team specified by ``team_id``.

   **Example request**:

   .. sourcecode:: http

      DELETE /teams/1 HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript
      Content-Type: application/json
      {
         'name': 'A'
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 204 No Content

   **URL Parameters**:
      * *team_id*: The ID for the team you are requesting information for.

   **Required JSON Parameters**:
      *No JSON parameters are required for this interface.*

   **Optional JSON Parameters**:
     *No optional parameters are allowed for this interface.*

   **Exceptions**:
      * *IllegalParameter*: You submitted parameters with your DELETE request.
        Parameters are not allowed on this interface.