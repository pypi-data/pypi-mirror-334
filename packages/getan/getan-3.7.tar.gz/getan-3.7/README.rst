Usage
=====

Call ``getan`` or ``getan.py`` in a terminal to start
with an empty list of tasks (in the default datebase)
that you want to track time for.

Use the Insert-Key to add a new task to track or import a list of task via SQL.
(A *task* is called *project* within getan.)
You will have to give a project "key" and a project "description".

Now select one of the projects with the arrow keys from your keyboard
and press enter to start the clock. See ``INTRODUCTION`` for more keyboard
commands.

The time log entries will be saved in an sqlite database,
by default getan will create ``~/.getan/time.db``.
The ``scripts/`` will help to generate reports from them.

Tree mode
---------
Getan supports a hierarchy of projects. A top level project key
has only one character, once you starting using a second character
as project key, it will be the next level down in the hierarchy.
Example::

    a    Top level project
    aa   1st second level project
    ab   2nd second level project
    aba  Third level Project

Use the switch_project_order key which is ``f2`` by default
to cycle to the hierarchical view.


Customization
-------------

Use ``~/.getan/getanrc`` or the system-wide ``/etc/getanrc``
to customize keys and colors. See ``getan/config.py`` for
the recognized options. Example::

    [keybindings]
    # changes the insert function to be activated by the `)` key
    insert: )

    [theme]
    header: light green, dark green
    body: light green, black



Installation
============

Getan requires `urwid <http://urwid.org/>`_ in a version >= 1.0. Urwid is
a console user interface library written in Python. For console output e.g.
zeiterfassung.py Getan also requires `Jinja2 <http://jinja.pocoo.org/>_`.

Install urwid
-------------

On Debian GNU/Linux >= Wheezy just run as root:::

    $ apt-get install python3-urwid

On other systems urwid may be installed via pip or directly put into the sources
of getan.

Using pip
^^^^^^^^^

To install urwid via pip run as root::

    $ pip install urwid

Or if you prefer using a virtualenv::

    $ virtualenv getan-env
    $ source getan-env/bin/activate
    (getan-env)$ pip install -U pip  # to get the latest pip
    (getan-env)$ pip install urwid

Using urwid sources
^^^^^^^^^^^^^^^^^^^

Urwid can be put as source to the getan directory when getan is run directly
from the sources. Urwid source can be downloaded from `pypi
<https://pypi.python.org/pypi/urwid/>`_.

For urwid 1.1.2 the direct download link from pypi is
`<https://pypi.python.org/packages/source/u/urwid/urwid-1.1.2.tar.gz>`_
(sha256sum is
f56568b4f8459b3265c65d9e275ef72df6cb16ad0c291f0feb027cc911ea0f26).::

    $ cd getan-source
    $ v=urwid-1.1.2
    $ curl -O https://pypi.python.org/packages/source/u/urwid/$v.tar.gz
    $ sha256sum $v.tar.gz
    $ tar -xzvf $v.tar.gz
    $ ln -s $v/urwid urwid

Install Jinja2
--------------

On Debian GNU/Linux just run as root:::

    $ apt-get install python3-jinja2

On other systems jinja2 may be installed via pip or directly put into the
sources of getan.

Using pip
^^^^^^^^^

To install jinja2 via pip run as root::

    $ pip install jinja2

Or if you prefer using a virtualenv::

    $ source getan-env/bin/activate
    (getan-env)$ pip install jinja2

Install getan
-------------

A installation of getan is not required. It can also be run directly from the
sources. To install getan system wide the following command must be run as root
user::

    $ python3 setup.py install

You may need to install setuptools first, on Debian GNU/Linux just run as root:::

    $ apt-get install python3-setuptools


Starting getan
==============

Getan can be directly run from sources or after a system wide installation from
the bin dir (e.g. /usr/bin).

Running from Sources
--------------------

To run getan from the sources run::

    $ ./getan.py

or::

    $ ./getan.py /path/to/mytime.db

to choose a different sqlite3 database then the default time.db


Running from installation
-------------------------

After installing getan it can be run with::

    $ getan

or::

    $ getan /path/to/mytime.db


Writing Templates
=================

External templates must be stored in ~/.getan/templates/ to be able to call
them.

Getan uses the Jinja2 templating language. You can find more information
at `Jinja2 <http://jinja.pocoo.org/>`_.

If a year or a week is specified, only the entries in this period will be
loaded.

Variables
---------

current_week
    The current week.
current_year
    The current year.

user
    What You indicated with -u.
week
    What You indicated with -w.
iso_week
    What You indicated with -w, in iso notation.
unix_week
    What You indicated with -w, in unix notation.
year
    What you indicated with -y.

get_total_duration()
    Total duration of all entries.

database
    Path of the database.

entries
    List of all entries.

    get_comment()
        Description of the entry.
    get_workpackage()
        Work package of the entry.
    desc
        Work package and Description of the entry.

    startisoday
        Year, month and day in ISO format.
    start
        Start time as datetime.
    end
        End time as datetime.
    get_duration()
        Duration of the entry.

projects
    List of all projects.

    get_total_duration()
        Total duration of all entries in the project.
    desc
        Description of the project.
    key
        Key of the project.

    entries
        All entries in this project (See entries).


If -w is specified, only this week will be loaded from the database.

year()
    All entries in this year.
month()
    All entries in this month.
week()
    All entries in this week.
day()
    All entries in this day.


Filters
-------
human_time(delta)
    return "%d:%02d" % (h, m)

date_format(datetime)
    strftime("%d.%m.%Y")

decimal_hours(delta) -> float
    Return hours as decimal with max 1 place after locale's decimal_point.

duration(events)
    Sum of the durations of the given entries.

sum_duration(projects)
    Sum of the durations of the given projects.


Example
-------

Example::

    {{ user }}, (KW {{ week }}, {{ year }})
    {% for i in user -%}
    =
    {%- endfor -%}

    {% for proj in projects %}
    # {{ proj.desc }}
    {% for entry in proj.entries|sort(attribute='start') -%}
    {{ entry.get_comment() }}
    {% endfor -%}
    # total time: {{ proj.get_total_duration()|human_time }}h
    {% endfor %}
    # total: {{ total_time|decimal_hours }}h


CREDITS
=======
Getan is Free Software licensed under the terms of GNU GPL v>=3.
For details see LICENSE coming with the source of 'getan'.


Main development
----------------
| 2018-     Magnus Schieder <magnus.schieder@intevation.de> (current maintainer)
| 2014-     Bernhard E. Reiter <bernhard@intevation.de>
| 2011-2014 Björn Ricks <bjoern.ricks@intevation.de>
| 2010      Ingo Weinzierl <ingo.weinzierl@intevation.de>
| 2009-2014 Thomas Arendsen Hein <thomas@intevation.de>
| 2008-2010 Sascha L. Teichmann <sascha.teichmann@intevation.de>

Contributions
-------------
| Frank Koormann
| Stephan Holl
| Tom Gottfried

Thanks
------
To all users that gave feedback, especially at Intevation.


.. vim: set ts=4 sw=4 tw=80 filetype=rst :
