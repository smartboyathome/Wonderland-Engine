.. Wonderland Engine documentation master file, created by
   sphinx-quickstart on Fri Oct 19 10:46:17 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Wonderland Engine |version| Documentation
=========================================

Overview
--------

The Wonderland Cyber Defense Scoring Engine aims to be a highly flexible
scoring engine for use in Cybersecurity competitions. Inspired by the Pacific
Rim Collegiate Cyber Defense Competition, Wonderland aims to allow greater
modularity for administrators, while also allowing automation of some currently
unautomated procedures. Using MongoDB, Redis, Flask, and Sphinx, it will score
any type of cyber defense competition, big or small, using different
types of pluggable checks. It was designed and programmed from the ground up by
Alexander Abbott during the summer and fall of 2012, and is available under the
GNU Affero Public License.

.. toctree::
   :hidden:

   introduction/index
   doorknob/index
   cheshire_cat/index
   white_rabbit/index

:doc:`Introduction <introduction/index>`
   Introduction to the Wonderland Engine, including the high-level design.

Getting Started
   How to set up and run the Wonderland Engine

:doc:`Doorknob <doorknob/index>`
   The Database Wrapper

:doc:`Cheshire Cat <cheshire_cat/index>`
   The REST API

:doc:`White Rabbit <white_rabbit/index>`
   The Scoring Daemon

Dinah
   The name of the future Web GUI for this engine.

Source
------

To download and test the newest version of the Wonderland Engine, please visit
`the github repository <https://github.com/smartboyathome/Wonderland-Engine/>`_
and make sure to report any issues you come across.

TODO
----

If there are any items that need to be done, they will be listed below. If it
blank, then that means there is nothing that needs to be done!

.. todolist::