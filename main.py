import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from cmath import log
from typing import Union
from fastapi import Body, FastAPI
from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str
    name: str
    surname: str
    interests: str


class Project(BaseModel):
    #userLogin: str
    info: str
    name: str
    manager_id: int


app = FastAPI()
connection = psycopg2.connect(user="dsa1",
                              password="HSEPAassword2022",
                              host="77.37.164.38",
                              port="5432",
                              database="dsa1")
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = connection.cursor()


@app.post("/auth/register")
async def register_user(user: User):
    register_request = '''
    insert into lucas_egor_agvan.users(login, password, name, surname, interests)
    values ('{}', '{}', '{}', '{}', '{}');
    '''.format(user.login, user.password, user.name, user.surname, user.interests)
    cursor.execute(register_request)
    return 'User added'


@app.post("/project/create")
async def createProject(project: Project):
    project_request = '''
    insert into lucas_egor_agvan.projects(name, info, manager_id)
    values ('{}', '{}', {});
    '''.format(project.name, project.info, project.manager_id)
    cursor.execute(project_request)
    return 'Project added'


@app.get("/auth/login/{login}")
async def login(login: str, password: Union[str, None] = None):
    find_request = '''
    select exists (
        SELECT 1 FROM lucas_egor_agvan.users
        WHERE lucas_egor_agvan.users.login = '{}' and lucas_egor_agvan.users.password = '{}'
        LIMIT 1);
    '''.format(login, password)
    cursor.execute(find_request)
    success_login = cursor.fetchall()
    if success_login[0][0]:
        return 'Login successful'
    else:
        return 'Login failed'


@app.get("/project/projects")
async def getProjects():
    project_request = '''
    select * from lucas_egor_agvan.projects;
    '''
    cursor.execute(project_request)
    return str(cursor.fetchall())


@app.get("/project/{id}")
async def getProject(id: str):
    project_request = '''
    select * from lucas_egor_agvan.projects where projects.project_id = '{}';
    '''.format(id)
    cursor.execute(project_request)
    return str(cursor.fetchall())


@app.delete("/project/delete/{id}")
async def deleteProject(id: Union[str, None] = None):
    delete_request = '''
    delete from lucas_egor_agvan.projects where projects.project_id = '{}';
    '''.format(id)
    cursor.execute(delete_request)
    return 'Deleted'


@app.get("/project/search/{notFullName}")
async def getProjectSearch(notFullName: str):
    find_request = '''
    select * from lucas_egor_agvan.projects where position('{}' in projects.name)>0;
    '''.format(notFullName)
    cursor.execute(find_request)
    return str(cursor.fetchall())


@app.post("/project/update/{id}")
async def updateProject(id: Union[str, None] = None, project: Union[Project, None] = None):
    if id is None:
        return "id is None"
    id = id.lower()
    if project is None:
        return "No data to update"
    update_request = '''
    update lucas_egor_agvan.projects
    set name = '{}',
        info = '{}',
        manager_id = {}
    where project_id = {};
    '''.format(project.name, project.info, project.manager_id, id)
    cursor.execute(update_request)
    return "Updated successfully!"
