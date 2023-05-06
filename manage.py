from flask_script import Manager

from server import app, db, migrate

manager = Manager(app)


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
