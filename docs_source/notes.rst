:orphan:

Notes on Sphinx
===============
This is info I could only find after much StackExchange digging... It could
be a result of me just not knowing things though. If you install Sphinx, it
gets associated with the Python version that you installed it with. This means
that if you installed it with python3.8 and then write code in python3.9,
Sphinx will be unable (as far as I know...) to make documentation for the new
code. Plus, it's difficult for me to ensure I'm using the most recent version
of Sphinx.

Quickstart
----------
Setup the project by running :code:`<python> -m sphinx.cmd.quickstart`. This
is equivalent to the terminal command :code:`sphinx-quickstart` that you'll find
online, but you can control the Python version associated with Sphinx this way.
Currently this makes 2 directories named "build" and "source". I change "build"
to "docs" because Github only allows a few options for where to build from.
Then I change "source" to "docs_source" so it's clear this is the source code
for the docs.

Building docs
-------------
When you're ready to build docs you'd usually run :code:`make html` from
Terminal. In code form, :code:`make html` =
:code:`<python> -m sphinx.cmd.build -b html <path to conf.py>
<path to where to put the html files>`. You can also add a :code:`-E` flag
to tell Sphinx to overwrite the old docs and rebuild them all each time. I
prefer this, since sometimes changes to the header of one file aren't
registered in other files.

Suppose PyUVS is in the repos directory in your home folder. The command
will look like:
:code:`~/repos/PyUVS/venv/bin/python -m sphinx.cmd.build -b html
~/repos/PyUVS/docs_source ~/repos/pyRT_DISORT/docs -E`