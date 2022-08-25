import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from cmath import log
from typing import Union
from fastapi import Body, FastAPI
from pydantic import BaseModel

#user : Union[User, None] = None


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

'''
login = "tembubu"
password = "12345"
name = "Tembulat"
surname = "Sokmyshev"
interests = "Valorant"
register_request = ''' '''
insert into lucas_egor_agvan.users(login, password, name, surname, interests)
values ('{}', '{}', '{}', '{}', '{}');
''' '''.format(login, password, name, surname, interests)
cursor.execute(register_request)
'''
'''
name = "Project Assistant1"
info = "Create app to search projects"
manager_id = 2
project_request = ''' '''
insert into lucas_egor_agvan.projects(name, info, manager_id)
values ('{}', '{}', '{}');
''' '''.format(name, info, manager_id)
cursor.execute(project_request)'''

#users = {}
#projects = {}


@app.post("/auth/register")
async def register_user(user: User):
    register_request = '''
    insert into lucas_egor_agvan.users(login, password, name, surname, interests)
    values ('{}', '{}', '{}', '{}', '{}');
    '''.format(user.login, user.password, user.name, user.surname, user.interests)
    cursor.execute(register_request)
    #users[user.login] = user
    # return "Register Successful!\r\n"


@app.post("/project/create")
async def createProject(project: Project):
    project_request = '''
    insert into lucas_egor_agvan.projects(name, info, manager_id)
    values ('{}', '{}', {});
    '''.format(project.name, project.info, project.manager_id)
    cursor.execute(project_request)
    #projects[project.name.lower()] = project
    # return "Project was created successfully!"


@app.get("/auth/login/{login}")
async def login(login: str, password: Union[str, None] = None):
    '''user = users.get(login)
    print(users)
    if user is None:
        return "Login failed!\r\n"
    else:
        if password is None:
            return "Password is None"
        if user.password == password:
            return "Login Successful!\r\n"
        else:
            return "Password failed! " + user.password + " " + password'''
    find_request = '''
    select exists (
        SELECT 1 FROM lucas_egor_agvan.users
        WHERE lucas_egor_agvan.users.login = '{}' and lucas_egor_agvan.users.password = '{}'
        LIMIT 1);
    '''.format(login, password)
    cursor.execute(find_request)
    success_login = cursor.fetchall()
    if success_login[0][0]:
        print('Login successful')
    else:
        print('Login failed')


'''
@app.get("/auth/login/{login}")
async def login(login: str, password: Union[str, None] = None):
    user = users.get(login)
    print(users)
    if user is None:
        return "Login failed!\r\n"
    else:
        if password is None:
            return "Password is None"
        if user.password == password:
            return "Login Successful!\r\n"
        else:
            return "Password failed! " + user.password + " " + password


@app.post("/project/create")
async def createProject(project: Project):
    projects[project.name.lower()] = project
    return "Project was created successfully!"


@app.get("/project/projects")
async def getProjects():
    return projects


@app.get("/project/{id}")
async def getProject(id: str):
    project = projects.get(id.lower())
    if project is None:
        return "No such project"
    return project


@app.get("/project/search/{notFullId}")
async def getProjectSearch(notFullId: str):
    currProjects = []
    for pr in projects:
        if notFullId.lower() in pr.lower():
            currProjects.append(projects[pr])
    if len(currProjects) == 0:
        return "No such projects"
    return currProjects


@app.post("/project/update/{id}")
async def updateProject(id: Union[str, None] = None, project: Union[Project, None] = None):
    if id is None:
        return "id is None"
    id = id.lower()
    if project is None:
        return "projet is None"
    projects[id].name = project.name.lower()
    projects[id].info = project.info.lower()
    return "Updated successfully!"


@app.post("/project/update/{id}")
async def updateProject(id: Union[str, None] = None, project: Union[Project, None] = None):
    if id is None:
        return "id is None"
    id = id.lower()
    if project is None:
        return "projet is None"
    projects[id].name = project.name.lower()
    projects[id].info = project.info.lower()
    return "Updated successfully!"


@app.delete("/project/delete/{id}")
async def deleteProject(id: Union[str, None] = None):
    return projects.pop(id.lower(), "Nothing deleted")


# class Image(BaseModel):
#     url: str
#     name: str


# class Item(BaseModel):
#     name: str
#     description: Union[str, None] = None
#     price: float
#     tax: Union[float, None] = None


# @app.get("/items/")
# async def read_item(item_id: Union[int, None] = None, item : Union[Item, None] = None):
#     return items


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     item = {"item_id": item_id, **item.dict()}
#     items[item_id] = item
#     # results = {"item_id": item_id, "item": item}
#     return item


#     @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int,
#     item: Item = Body(
#         examples={
#             "normal": {
#                 "summary": "A normal example",
#                 "description": "A **normal** item works correctly.",
#                 "value": {
#                     "name": "Foo",
#                     "description": "A very nice Item",
#                     "price": 35.4,
#                     "tax": 3.2,
#                 },
#             },
#             "converted": {
#                 "summary": "An example with converted data",
#                 "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
#                 "value": {
#                     "name": "Bar",
#                     "price": "35.4",
#                 },
#             },
#             "invalid": {
#                 "summary": "Invalid data is rejected with an error",
#                 "value": {
#                     "name": "Baz",
#                     "price": "thirty five point four",
#                 },
#             },
#         },
#     ),
# ):
#     item = {**item.dict()}
#     items[item_id] = item
#     # results = {"item_id": item_id, "item": item}
#     return item
'''
