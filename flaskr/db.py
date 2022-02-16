import sqlite3

import click
from flask import current_app, g # g is unique per request.
#current_app points to the Flask handling each reqest
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(#establishes connection to file pointed at by databse
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # tells connection to return rows that behave like dicts
        #allows accessing cloumns by name

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()#returns db connection used to execute cmds from file.

    with current_app.open_resource('schema.sql') as f:#opens file relative to flaskr pkg
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')#defines command line cmd
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    db = init_db()
    click.echo('Initialized the databse.')

#Take an application and register
def init_app(app):
    app.teardown_appcontext(close_db)#tells Flask to call clean up func
    app.cli.add_command(init_db_command)#adds new cmd that can be called with flask cmd
