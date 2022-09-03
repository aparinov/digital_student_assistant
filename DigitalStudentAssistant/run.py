from app import app, db
from app.models import User, Project

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Project': Project}

if __name__ == '__main__':
    app.run(port=9999,debug = False)