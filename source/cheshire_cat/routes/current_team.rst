Current Team Routes
===================

This interface deals with getting information on the team that the currently
logged in user belongs to.

.. _cheshire-current_team-routes-get:

Get Current Team
----------------

.. http:get:: /current_team
   

   **Example request**:

   .. sourcecode:: http

      GET /current_team HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json
      {
         'name': 'Team A'
      }

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