Introduction
============

Purpose
-------

Through this page, I hope to guide you, the reader, through all the stages of
the design and development of the Wonderland Engine. By doing this, I hope to
help you better understand the engine at a higher level, as well as some the
background behind the engine. Hopefully, you will find this useful in
determining whether the Wonderland Engine is right for your group or not, and
that it will serve future developers and administrators in understanding some
basic concepts behind the engine.

Background
----------

Before any code was actually written, and before I had any idea that I would be
writing a scoring engine, I had started participating in the first teams that
my university, the University of Washington Bothell Campus, had sent to the
Pacific Rim Collegiate Cyber Defense Competition. While competing during the
2012 Competition, my team had done a pretty reasonable move and blocked any
incoming requests from outside our network from reaching the database, domain,
and intranet systems. For most systems, this is a very reasonable layout, but
unfortunately the database wasn't written to accomodate this.

The database that was in use up until that competition was hard coded to use
the public IPs of each system it was checking the uptime on. All these systems
were ones that it was not showing uptime for, even though technically, they
were up. As I learned later while designing this scoring engine, the paths were
hard coded, and in fact it took a significant amount of effort on the
competition organizer's part to set it up for new competitions such as the
smaller ones that my team started to participate in during the summer and fall
of 2012.

This is why I decided that, for my Cooperative Education project that was
required for me to graduate university, I would create a new engine to replace
the old one. I worked closely with the people who set up the PRCCDC event every
year as well as the aforementioned smaller competitons to design it how they
needed it. Throughout the lifecycle of this project, I have learned many new
skills in both python and project management that I hope to use in future jobs.
I hope to continue working on this in the future.

Design
------

The Wonderland Engine was created with modularity as the most crucial element
of its design. Before even starting on any code, I took a month to create a
50-page design document which described its architecture and each path that the
would have, including what was the input for that path and its output. This has
been incorporated into this documentation, although some elements of the
original design were changed along the span of developing the project.

One of the first design decisions I made was that the engine would utilize the
web using a REST-based architecture. My reasoning for this was that it would
need to be accessed across a large variety of systems, including Linux,
Windows, and eventually even Mac. It would be a pain for the system
administrator to have to set up a client on each workstation in order to allow
teams access to the scoring engine, so the next best setup was using a web
browser.

Another was that this would be utilizing a multilayer master-worker model in
order to run the checks that score the competition. This would be done from the
server itself, and wouldn't require any software to be installed on the client.
The only requirement would be that the server running the scoring engine would
have both a public IP on the competition environment, as well as a private IP
for each team's network. By utilizing this private IP, the engine would be able
to access the various team machines while allowing teams to maintain good
security practices.

Very early on, the scoring server was separated out into two different modules.
These were the scoring daemon and the REST server that gave access to the data
that the scoring server generated. Unfortunately, python servers are started
with several processes, which forced me to consider options for communication
outside of traditional pipes. I considered using sockets, but decided that
wouldn't allow for the flexibility that I needed. Eventually, I ended up using
Redis's pubsub feature. By utilizing this, the REST interface did not care
about what daemon, if any, it communicated with, and the daemon didn't care
about what clients it was getting its commands from.