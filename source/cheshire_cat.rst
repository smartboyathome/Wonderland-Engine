Cheshire Cat
============

Cheshire Cat is the name of the REST API that was built to allow access to the
underlying scoring engine. It talks to to the scoring engine through
:doc:`Doorknob <doorknob>`
and Redis, and is generally a frontend to Doorknob
in general. All the views are pluggable, loaded dynamically from the blueprints
folder, so routes can be added, removed, and renamed easily, without having to
modify any other code. Each route has a number of properties, such as whether
users need to be logged in to access it, what user role(s) are allowed to
access it, and what parameters are allowed to be passed to it. Unless otherwise
stated, all routes require a user to log in to be able to access them.

Default routes
--------------

.. http:get:: /

   The name and version of the engine.

   **Example request**:

   .. sourcecode:: http

      GET /
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json
      {
         'id': 'Wonderland Scoring Engine',
         'version': 0.1
      }