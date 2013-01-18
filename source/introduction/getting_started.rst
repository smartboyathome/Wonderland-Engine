.. highlight:: console

Getting Started
===============

Purpose
-------

This document exists to help users of the Wonderland Engine through the initial
stages of setting it up and running it. It will guide users through the
installation of dependencies for Wonderland, as well as Wonderland itself. In
addition, it will discuss how to modify the configuration for Wonderland and
how to install checks into White Rabbit. If you find any part of this
documentation confusing, feel free to post about it on the user mailing list.

Please note that, while Wonderland may work on other operating systems, it has
only been tested on Linux. As such, whenever this documentation says
"distribution", it is referring to Linux distributions in general. If you use
this on another operating system, please let us know on the mailing list and
provide us with any additions or changes to these steps that you had to make
(if any) in order to get it to install and run.

Prerequisites
-------------

Before you install the Wonderland Engine, a few dependencies must be installed
and their versions must be checked to ensure compatibility.

#. Make sure that you are using Python version 2, and not version 3. You can do
   this by running the following command::

      user@host:~$ python --version

   Some distributions install Python 2 to the `python2` command. If this is the
   case, substitute any `python` commands in this document with `python2`. You
   can check this by using the following command::

      user@host:~$ python2 --version

   If the second command fails and the first returns that you are using Python
   version 3, please consult the documentation for your distribution in order
   to install Python version 2 on your system, then rerun these commands to
   ensure it installed correctly. In addition to the main Python 2 files, you
   should install the development header files. These are required for some
   libraries that will be installed alongside the Wonderland Engine itself.

#. After you have made sure you have Python version 2 installed, you need to
   ensure that setuptools is installed. While not required for the installation
   of the Wonderland Engine, it is highly recommended since it will install all
   python libraries for you. If you choose not to install or are unable to, an
   extra step will be provided below to install it. However, it is usually
   installed by default on most distributions. To check if it's installed, run
   the following command::

      user@host:~$ python2 -c 'import setuptools'

   If this command returns with no errors, then setuptools is installed. If you
   get an import error, then consult your distribution's documentation for
   instructions on how to install setuptools.

#. As of this time, MongoDB is the only database supported by Doorknob, so if
   you don't want to implement your own wrapper, you need to install MongoDB
   onto your system. MongoDB is very rarely installed by default on most
   distributions, but another app may have installed it as a dependency. To
   check if MongoDB is already installed, run the following command::

      user@host:~$ mongod --version

   If the terminal returns command not found, then it is not installed. MongoDB
   has a good list of installation instructions in their own documentation for
   many different distributions. You can find this
   `here <http://docs.mongodb.org/manual/tutorial/>`_. Otherwise, consult your
   distribution's documentation for how to install MongoDB.

   After you have MongoDB installed, rerun the above command and note the
   version number that you are using. Doorknob's wrapper is optimized for
   MongoDB 2.0 or above. While MongoDB 1.8 may work, we do not recommend it
   since it is legacy and has not been tested against at this time.

#. Redis is the only implementation of Publish-Subscribe  that is supported at
   this time by Wonderland. Plans are being made to abstract it out to allow
   for other implementations by abstracting this into Doorknob, but as of yet
   that is not done. Therefore, you will have to install Redis in order to use
   Cheshire Cat  or White Rabbit.

   To check if Redis is installed on your system, run the following command::

      user@host:~$ redis-server --version

   If the terminal returns command not found, then it is not installed. Consult
   your distribution's documentation for how to install Redis.

#. Currently, the Wonderland Engine uses Git as its source code repository. Due
   to this, you will need to have git installed in order to download the code
   in the following installation steps. To check if git is installed, run the
   following command::

      user@host:~$ git --version

   If the terminal returns command not found, then Git is not installed.
   Consult your distribution's documentation for how to install it.

Installation
------------

Now that the dependencies for the Wonderland Engine are installed, you can
download and install the Wonderland Engine itself.

#. First, you'll need to download the code from the Github repository. To do
   this, you need to run the following command::

      user@host:~$ git clone git://github.com/smartboyathome/Wonderland-Engine.git

   This will clone the most recent version of the source code from the Github
   repository into a new folder named `Wonderland-Engine`, which is created
   inside the current directory. You can move this folder anywhere on the
   filesystem at this point without breaking it, as all the information is
   contained within the `Wonderland-Engine` directory.

#. Then, change into the newly created source directory::

      user@host:~$ cd Wonderland-Engine

#. Now that you are in the source directory, you can compile and install the
   Wonderland Engine by executing the following command::

      user@host:~/Wonderland-Engine$ sudo python setup.py --single-version-externally-managed install

   This command will install all the python libraries that this depends on
   before installing Wonderland itself. You can find the Wonderland Engine in
   `/usr/lib/python2.7/site-packages/wonderland-engine/` and configuration in
   `/etc/wonderland-engine/settings.cfg`. You should change the default
   configuration (described in the next section) before running either Cheshire
   Cat or White Rabbit for the first time.

Configuration
-------------

As stated above, the default configuration for the Wonderland Engine is located
in `/etc/wonderland-engine/settings.cfg`. It contains all the settings for
connecting to MongoDB and Redis, as well as some settings for Cheshire Cat and
White Rabbit. Each of these sections will be explained below.

A configspec file is also located in `/etc/wonderland-engine/configspec.cfg`
but you should not ever need to modify this. It is there for checking to make
sure that you formatted your settings.cfg correctly so that all parts of the
Wonderland Engine can make use of it.

With that out of the way, here is the default configuration file::

   [CORE]
   DEBUG = False
   SECRET_KEY = 'eL7nqsY9x0P7WhsOfnMi'
   HTTPS_ONLY = True

       [[SERVER]]
       HOST = 'localhost'
       PORT = 5000
       PASSWORD_HASH = 'bcrypt'
       DEBUG_OUTPUT = True

       [[DAEMON]]
       CHECK_DELAY = 60 #seconds

       [[DATABASE]]
       HOST = 'localhost'
       PORT = 27017
       DB_NAME = 'cheshire_engine'

       [[REDIS]]
       HOST = 'localhost'
       PORT = 6379
       PASSWORD = ''
       DAEMON_CHANNEL = 'scoring-daemon'

What does each section mean? What about each property? We'll step through them
one by one below:

* **CORE**: This is the main section for the whole config for the Wonderland
  Engine. Anything not within core will not be available as a setting within
  any module in the Wonderland Engine.

  * **DEBUG**: Whether to enter debug mode or not. This should be set to false
    for a production environment, since using it may lead to security holes.
  * **SECRET_KEY**: This is the secret key for use by Cheshire Cat's HMAC
    signing of cookies. This should be changed before running Cheshire Cat in a
    production environment.
  * **HTTPS_ONLY**: Whether cookies should be used only with an HTTPS
    connection. This should be set to true in a production environment to
    lessen the likelihood of someone stealing a user's session ID.
  * **SERVER**: This section contains all the settings that Cheshire Cat needs
    prior to being able to run.

    * **HOST**: The host that you are running Cheshire Cat on. In a production
      environment, this would be either the IP of the machine running Cheshire
      Cat, or the domain name.
    * **PORT**: The port that you are running Cheshire Cat on. In a production
      environment, this would be the port that you set your webserver to run
      on, typically port 80.
    * **PASSWORD_HASH**: The password hashing algorithm to use. By default,
      md5 and bcrypt are supported. md5 should only be used for testing
      purposes, and should not be used in a competition environment.
    * **DEBUG_OUTPUT**: Separate from DEBUG above, DEBUG_OUTPUT specifies
      whether you want Cheshire Cat to intercept and output exceptions that it
      throws. This should be set to false in a production environment.

  * **DAEMON**: This section contains the settings that White Rabbit needs
    prior to being able to run.

    * **CHECK_DELAY**: The minimum amount of time (in seconds) between each run
      of a single check. For example, if a MongoDB service check was run, it
      will not run again for at least 60 seconds by default. A higher number
      may be better for a production environment.

  * **DATABASE**: These are the settings for the database (i.e., MongoDB), so
    that Doorknob can connect to it.

    * **HOST**: The host that you are running the database Doorknob is
      connecting to on. This may be a URL or an IP.
    * **PORT**: The port that you are running the database Doorknob is
      connecting to on. This must be an integer less than 65536.
    * **DB_NAME**: The name of the database that Doorknob will use.

  * **REDIS**: These are the settings for connecting to the Redis (and soon
    other) PubSub client.

    * **HOST**: The host that you are running Redis on. This may be a URL or an
      IP.
    * **PORT**: The port that you are running Redis on. This must be an integer
      less than 65536.
    * **PASSWORD**: The password to be able to connect to Redis. If none is
      set, assign it to the empty string (this is the default).
    * **DAEMON_CHANNEL**: The channel on which the scoring daemon is listening.
      This is important, since you don't want to use a channel that is in use
      by other apps.