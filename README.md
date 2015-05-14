### Requirements

Flask
Flask-SQLAlchemy
Flask-Misaka
Flask-Migrate

Just run `web.py runserver`. This runs the server on localhost, port 5000. To interface with the database 
you can use the web.py app as a module, as per 
these [instructions](https://pythonhosted.org/Flask-SQLAlchemy/quickstart.html).

When you make changes to the database model you can save them as [Alembic](https://alembic.readthedocs.org/en/latest/)
revisions with `web.py db migrate -m "* Some message"`. This creates migrations under `migrations/versions` which then
can be applied to the database with `web.py db upgrade`.