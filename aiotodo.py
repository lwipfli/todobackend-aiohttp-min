import logging
from aiohttp import web
import aiohttp_cors

import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy_utils

import os

ENGINE = None
CONNECTION = None

TODOS = {
    0: {'title': 'build an API', 'order': 1, 'completed': False},
    1: {'title': '?????', 'order': 2, 'completed': False},
    2: {'title': 'profit!', 'order': 3, 'completed': False}
}

TAGS = {
    0: {'title': 'THE TAG'},
}

MAP = {
    0:{'todo_id': 9, 'tag_id': 10}
}


METADATA = sqlalchemy.MetaData()

TODOS_TABLE = sqlalchemy.Table('TODOS', METADATA,
                               sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                               sqlalchemy.Column('title', sqlalchemy.String),
                               sqlalchemy.Column('order', sqlalchemy.Integer),
                               sqlalchemy.Column('completed', sqlalchemy.Boolean),
                               sqlalchemy.Column('url', sqlalchemy.String))

TAGS_TABLE = sqlalchemy.Table('TAGS', METADATA,
                              sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                              sqlalchemy.Column('title', sqlalchemy.String),
                              sqlalchemy.Column('url', sqlalchemy.String))

MAP_TABLE = sqlalchemy.Table('MAP', METADATA, sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                             sqlalchemy.Column('todo_id', sqlalchemy.Integer),
                             sqlalchemy.Column('tag_id', sqlalchemy.Integer))

## Database functions ***

def remove_tag_from_database(id):
    try:
        CONNECTION.execute(TAGS_TABLE.delete().where(TAGS_TABLE.c.id == id))
    except Exception as e:
        print('ERROR: Could not remove tag with id ',id,' from database')
        print(e)

def remove_all_tags_from_database():
    try:
        CONNECTION.execute(TAGS_TABLE.delete())
    except Exception as e:
        print('ERROR: Could not remove all tags from database')
        print(e)


def insert_tag_into_database(id,title,url):
    try:
        CONNECTION.execute(TAGS_TABLE.insert().values(id=id, title=title, url=url))
    except Exception as e:
        print('ERROR: Could not create tag with id: ',id,' title: ',title, ' url:', url )
        print(e)


def update_tag_in_database(id,title=None,url=None):
    try:
        if title:
            CONNECTION.execute(TAGS_TABLE.update().where(TAGS_TABLE.c.id == id).values(title=title))
        if url:
            CONNECTION.execute(TAGS_TABLE.update().where(TAGS_TABLE.c.id == id).values(url=url))
    except Exception as e:
        print('ERROR: Could not update tag with id: ',id)
        print(e)

def select_tag_from_database(id):
    try:
        result = CONNECTION.execute(TAGS_TABLE.select().where(TAGS_TABLE.c.id == id))
        return result
    except Exception as e:
        print('ERROR: Could not get tag with id:',id)
        print(e)

def select_all_tags_from_database():
    try:
        result = CONNECTION.execute(TAGS_TABLE.select())
        return result
    except Exception as e:
        print('ERROR: Could not get all tags from database')
        print(e)

def tag_exists_in_database(id):
    try:
        result = CONNECTION.execute(TAGS_TABLE.select().where(TAGS_TABLE.c.id == id))
        for row in result:
            return True
        return False

    except Exception as e:
        print('ERROR: Could not check if tag with id:',id,' exists in database')
        print(e)

def tag_count():
    try:
        count = 0
        result = CONNECTION.execute(TAGS_TABLE.select())
        for row in result:
            count=count+1
        return count
    except Exception as e:
        print('Could not get the count of entries in table database')
        print(e)

def remove_todo_from_database(id):
    try:
        CONNECTION.execute(TODOS_TABLE.delete().where(TODOS_TABLE.c.id == id))
    except Exception as e:
        print('ERROR: Could not remove todo with id ',id,' from database')
        print(e)

def remove_all_todos_from_database():
    try:
        CONNECTION.execute(TODOS_TABLE.delete())
    except Exception as e:
        print('ERROR: Could not remove all todos from database')
        print(e)


async def insert_todo_into_database(id,title,order,completed,url):
    try:
        CONNECTION.execute(TODOS_TABLE.insert().values(id=id, title=title,order=order,completed=completed,url=url))
    except Exception as e:
        print('ERROR: Could not create todo with id: ',id,' title: ',title,' order: ', order,' completed:', completed, ' url:', url )
        print(e)

def update_todo_in_database(id,title=None,order=None,completed=None,url=None):
    try:
        if title:
            CONNECTION.execute(TODOS_TABLE.update().where(TODOS_TABLE.c.id == id).values(title=title))
        if order:
            CONNECTION.execute(TODOS_TABLE.update().where(TODOS_TABLE.c.id == id).values(order=order))
        if completed:
            CONNECTION.execute(TODOS_TABLE.update().where(TODOS_TABLE.c.id == id).values(completed=completed))
        if url:
            CONNECTION.execute(TODOS_TABLE.update().where(TODOS_TABLE.c.id == id).values(url=url))
    except Exception as e:
        print('ERROR: Could not update todo with id: ',id)
        print(e)

def select_todo_from_database(id):
    try:
        result = CONNECTION.execute(TODOS_TABLE.select().where(TODOS_TABLE.c.id == id))
        return result
    except Exception as e:
        print('ERROR: Could not get todo with id:',id)
        print(e)

def select_all_todos_from_database():
    try:
        result = CONNECTION.execute(TODOS_TABLE.select())
        return result
    except Exception as e:
        print('ERROR: Could not get all todos from database')
        print(e)

def todo_exists_in_database(id):
    try:
        result = CONNECTION.execute(TODOS_TABLE.select().where(TODOS_TABLE.c.id == id))
        for row in result:
            return True
        return False

    except Exception as e:
        print('ERROR: Could not check if todo with id:',id,' exists in database')
        print(e)

def todo_count():
    try:
        count = 0
        result = CONNECTION.execute(TODOS_TABLE.select())
        for row in result:
            count=count+1
        return count
    except Exception as e:
        print('Could not get the count of entries in table database')
        print(e)


def map_count():
    try:
        count = 0
        result = CONNECTION.execute(MAP_TABLE.select())
        for row in result:
            count=count+1
        return count
    except Exception as e:
        print('Could not get the count of entries in table database')
        print(e)


def select_map_entries_from_database(todo_id):
    try:
        result = CONNECTION.execute(MAP_TABLE.select().where(MAP_TABLE.c.todo_id == todo_id))
        return result
    except Exception as e:
        print('ERROR: Could not get map entries with todo_id:',id)
        print(e)

def select_map_entries_from_database(tag_id):
    try:
        result = CONNECTION.execute(MAP_TABLE.select().where(MAP_TABLE.c.tag_id == tag_id))
        return result
    except Exception as e:
        print('ERROR: Could not get map entries with tag_id:',id)
        print(e)

def select_map_entries_from_database(todo_id, tag_id):
    try:
        result = CONNECTION.execute(MAP_TABLE.select().where(MAP_TABLE.c.tag_id == tag_id and MAP_TABLE.c.todo_id == todo_id))
        return result
    except Exception as e:
        print('ERROR: Could not get map entries with tag_id:',tag_id,' and todo_id: ',todo_id)
        print(e)

def remove_map_entries_from_database(todo_id):
    try:
        CONNECTION.execute(MAP_TABLE.delete().where(MAP_TABLE.c.todo_id == todo_id))
    except Exception as e:
        print('ERROR: Could not remove map entries with todo_id: ',todo_id,' from database')
        print(e)

def remove_map_entries_from_database(todo_id):
    try:
        CONNECTION.execute(MAP_TABLE.delete().where(MAP_TABLE.c.todo_id == todo_id))
    except Exception as e:
        print('ERROR: Could not remove map entries with tag_id: ',todo_id,' from database')
        print(e)

def remove_map_entries_from_database(todo_id, tag_id):
    try:
        CONNECTION.execute(MAP_TABLE.delete().where(MAP_TABLE.c.todo_id == todo_id and MAP_TABLE.c.tag_id == tag_id))
    except Exception as e:
        print('ERROR: Could not remove map entries with tag_id: ',tag_id,' and todo_id:', todo_id,' from database')
        print(e)

def remove_all_map_entries_from_database():
    try:
        CONNECTION.execute(MAP_TABLE.delete())
    except Exception as e:
        print('ERROR: Could not remove all map entries from database')
        print(e)

def insert_map_entry_into_database(todo_id,tag_id):
    try:
        CONNECTION.execute(MAP_TABLE.insert().values(todo_id=id, tag_id=tag_id))
    except Exception as e:
        print('ERROR: Could not create map entry with tag_id: ',tag_id,' and todo_id: ',todo_id)
        print(e)

## Database functions end***

def get_all_todos(request):

    todos = []
    for key, todo in TODOS.items():
        tags = []
        for map_id,entry in MAP.items():
            if entry['todo_id']==key:
                tags.append({'id':entry['tag_id'],**TAGS[entry['tag_id']]})
        todos.append({'id' : key, **TODOS[key] ,'tags':tags})

    return web.json_response(todos)


def remove_all_todos(request):
    TODOS.clear()
    MAP.clear()
    return web.Response(status=204)


def get_one_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    tags = []
    for map_id, entry in MAP.items():
        if entry['todo_id'] == id:
            tags.append({'id': entry['tag_id'], **TAGS[entry['tag_id']]})

    return web.json_response({'id': id, **TODOS[id],'tags':tags})


async def create_todo(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    data['completed'] = bool(data.get('completed', False))
    new_id = max(TODOS.keys(), default=0) + 1
    data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=str(new_id))))

    TODOS[new_id] = data

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )


async def update_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    data = await request.json()
    TODOS[id].update(data)

    return web.json_response(TODOS[id])


def remove_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'})

    for map_id, entry in MAP.items():
        if entry['todo_id'] == id:
            del MAP[map_id]

    del TODOS[id]

    return web.Response(status=204)


###### My code ######

def remove_all_tags(request):
    TAGS.clear()
    MAP.clear()
    return web.Response(status=204)


def get_all_tags(request):
    tags = []
    for key, tag in TAGS.items():
        todos = []
        for map_id, entry in MAP.items():
            if entry['tag_id'] == key:
                todos.append({'id' : entry['todo_id'],**TODOS[entry['todo_id']]})
        tags.append({'id' : key, **TAGS[key] ,'todos': todos})

    return web.json_response(tags)

async def create_tag(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})

    title = data['title']

    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    new_id = max(TAGS.keys(), default=0) + 1

    data['url'] = str(request.url.join(request.app.router['one_tag'].url_for(id=str(new_id))))

    TAGS[new_id] = data

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )


def remove_tag(request):
    id = int(request.match_info['id'])

    if id not in TAGS:
        return web.json_response({'error': 'Tag not found'})

    for map_id, entry in MAP.items():
        if entry['tag_id'] == id:
            del MAP[map_id]

    del TAGS[id]

    return web.Response(status=204)


def get_one_tag(request):
    id = int(request.match_info['id'])

    if id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)
    todos = []
    for map_id, entry in MAP.items():
        if entry['tag_id'] == id:
            todos.append({'id': entry['todo_id'], **TODOS[entry['todo_id']]})

    return web.json_response({'id': id, **TAGS[id],'todos':todos})

async def update_tag(request):
    id = int(request.match_info['id'])

    if id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)

    data = await request.json()
    TAGS[id].update(data)

    return web.json_response(TAGS[id])


def get_todos_of_tag(request):
    id = int(request.match_info['id'])

    if id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)

    todos = []

    for key, entry in MAP.items():
        if entry['tag_id'] == id:
            if entry['todo_id'] not in TODOS:
                return web.json_response({'error': 'Todo not found'}, status=404)
            todos.append({'id': entry['todo_id'], **TODOS[entry['todo_id']]})
    return web.json_response(todos)

def remove_tag_from_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    tag_id = int(request.match_info['tag_id'])

    if tag_id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)

    delete=[]
    for key, entry in MAP.items():
        if entry['tag_id'] == tag_id and entry['todo_id'] == id:
            delete.append(key)

    for element in delete:
        del MAP[element]
    return web.Response(status=204)

def remove_tags_from_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    delete = []
    for key, entry in MAP.items():
        if entry['todo_id'] == id:
            delete.append(key)

    for element in delete:
        del MAP[element]
    return web.Response(status=204)



def get_tags_from_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    tags = []

    for key, entry in MAP.items():
        if entry['todo_id'] == id:
            if entry['tag_id'] not in TAGS:
                return web.json_response({'error': 'Todo not found'}, status=404)
            tags.append({'id': entry['tag_id'], **TAGS[entry['tag_id']]})
    return web.json_response(tags)

async def associate_tag_to_todo(request):
    data = await request.json()

    id = int(request.match_info['todo_id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    if 'id' not in data:
        return web.json_response({'error': '"id" is a required field'})
    tag_id = data['id']

    for key,entry in MAP.items():
        if entry['todo_id']==id and entry['tag_id']==tag_id:
            return web.json_response({'error': 'Tag already associated with todo'})

    new_id = max(MAP.keys(), default=0) + 1
    entry = {'todo_id':id,'tag_id':tag_id}
    MAP[new_id]=entry


########################

# http://todo.thing.zone/documentation#!/tags/deleteTags
# https://docs.aiohttp.org/en/latest/web_quickstart.html
# http://demos.aiohttp.org/en/latest/tutorial.html
# https://ilias.unibe.ch/ilias.php?ref_id=1841334&cmd=frameset&cmdClass=ilrepositorygui&cmdNode=113&baseClass=ilRepositoryGUI
# https://ilias.unibe.ch/ilias.php?ref_id=1919292&target=1919292&cmd=showOverview&cmdClass=ilobjexercisegui&cmdNode=e1:qp&baseClass=ilexercisehandlergui
# http://localhost:8080
# http://todospecs.thing.zone/

########################

app = web.Application()

########################

dir_path = os.path.dirname(os.path.realpath(__file__))
print('Current path for database: ', dir_path)
ENGINE = sqlalchemy.create_engine('sqlite:///'+dir_path+'\\app_database.db')
CONNECTION = ENGINE.connect()


if not sqlalchemy_utils.database_exists(ENGINE.url):
    print('No database found. Creating new one.')

    sqlalchemy_utils.create_database(ENGINE.url)
    try:
        METADATA.create_all(ENGINE)
    except Exception as e:
        print('Error during table creation.')
        print(e)

#### Test of database #####
insert_tag_into_database(0,"Test_Tag", "Test_Url")
print('Inserted test value')


result=select_all_tags_from_database()
print('Printing table entries:')
for row in result:
    print('id: ',row['id'],' title: ',row['title'],' url: ',row['url'])

update_tag_in_database(0,"Klaus Heinrich tag")

result=select_all_tags_from_database()
print('Printing table entries after removal:')
for row in result:
    print('id: ',row['id'],' title:', row['title'],' url: ',row['url'])

print('Is tag with id 0 there? Answer: ',tag_exists_in_database(0))
print('Is tag with id 1 there? Answer: ',tag_exists_in_database(1))

########################

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods="*",
    )
})

cors.add(app.router.add_get('/todos/', get_all_todos, name='all_todos'))
cors.add(app.router.add_delete('/todos/', remove_all_todos, name='remove_todos'))
cors.add(app.router.add_post('/todos/', create_todo, name='create_todo'))
cors.add(app.router.add_get('/todos/{id:\d+}', get_one_todo, name='one_todo'))
cors.add(app.router.add_patch('/todos/{id:\d+}', update_todo, name='update_todo'))
cors.add(app.router.add_delete('/todos/{id:\d+}', remove_todo, name='remove_todo'))

###### My code ########

cors.add(app.router.add_delete('/todos/{id:\d+}/tags/', remove_tags_from_todo, name='remove_tags_from_todo'))
cors.add(app.router.add_get('/todos/{id:\d+}/tags/', get_tags_from_todo, name='get_tags_from_todo'))
cors.add(app.router.add_post('/todos/{todo_id:\d+}/tags/', associate_tag_to_todo, name='associate_tag_to_todo'))
cors.add(app.router.add_delete('/todos/{id:\d+}/tags/{tag_id:\d+}', remove_tag_from_todo, name='remove_tag_from_todo'))

cors.add(app.router.add_get('/tags/', get_all_tags, name='all_tags'))
cors.add(app.router.add_delete('/tags/', remove_all_tags, name='remove_tags'))
cors.add(app.router.add_post('/tags/', create_tag, name='create_tag'))
cors.add(app.router.add_delete('/tags/{id:\d+}', remove_tag, name='remove_tag'))
cors.add(app.router.add_get('/tags/{id:\d+}', get_one_tag, name='one_tag'))
cors.add(app.router.add_patch('/tags/{id:\d+}', update_tag, name='update_tag'))
cors.add(app.router.add_get('/tags/{id:\d+}/todos/', get_todos_of_tag, name='todos_of_tag'))

########################
logging.basicConfig(level=logging.DEBUG)
web.run_app(app, port=8080)
