import click
from flask.cli import with_appcontext
from gevent.pywsgi import WSGIServer

from app import create_app, db
from app.models import BannedUser, StaffMember, User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "BannedUser": BannedUser,
        "StaffMember": StaffMember,
        "User": User,
    }


@click.command()
@with_appcontext
def create_dummy_user():
    user = User(username="admin")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()


app.cli.add_command(create_dummy_user, name="create_dummy_user")

if __name__ == "__main__":
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
