Default Routes
==============

The routes listed on this page are those that do not exist in any plugin. They
are provided as sane defaults for the paths they are at in order to provide
some functionality that otherwise wouldn't exist. These are not likely to
change anytime soon, though more may be added in the future.

.. _cheshire-default-routes-index:

Index
-----

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
         'version': 0.9
      }