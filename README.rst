============================
pip requirements For Aliens
============================

It's not for human.

Write these sections in ``setup.cfg``::

    [piplock:common]
    reqs = sqlalchemy

    [piplock:dev]
    reqs =
        testfixtures
        factory-boy

    [piplock:prod]
    reqs = psycopg2

Install packages::

  piplock install (--dev/--prod)

Generating requirements.txt to your project root::

  piplock lock (--dev/--prod)
