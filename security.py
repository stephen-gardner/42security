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


if __name__ == "__main__":
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
