import asyncio
import logging
from aiohttp import web
import aiohttp_cors

import sqlalchemy
import databases

import sqlalchemy_utils

import os

#Synchronous
ENGINE = None
CONNECTION = None

#Asynchronous
DIR_PATH = ''
DATABASE = None

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

async def remove_tag_from_database(id):
    try:
        query = TAGS_TABLE.delete().where(TAGS_TABLE.c.id == id)
        await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not remove tag with id ',id,' from database')
        print(e)

async def remove_all_tags_from_database():
    try:
        query = TAGS_TABLE.delete()
        await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not remove all tags from database')
        print(e)


async def insert_tag_into_database(id,title,url):
    try:
        query = TAGS_TABLE.insert().values(id=id, title=title, url=url)
        await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not create tag with id: ',id,' title: ',title, ' url:', url )
        print(e)


async def update_tag_in_database(id,title=None,url=None):
    try:
        if title:
            query = TAGS_TABLE.update().where(TAGS_TABLE.c.id == id).values(title=title)
            await DATABASE.execute(query=query)
        if url:
            query = TAGS_TABLE.update().where(TAGS_TABLE.c.id == id).values(url=url)
            await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not update tag with id: ',id)
        print(e)

async def select_tag_from_database(id):
    try:
        query = TAGS_TABLE.select().where(TAGS_TABLE.c.id == id)
        result = await DATABASE.fetch_one(query=query)
        return result
    except Exception as e:
        print('ERROR: Could not get tag with id:',id)
        print(e)

async def select_all_tags_from_database():
    try:
        query = TAGS_TABLE.select()
        result = await DATABASE.fetch_all(query=query)
        return result
    except Exception as e:
        print('ERROR: Could not get all tags from database')
        print(e)

async def tag_exists_in_database(id):
    try:
        query = TAGS_TABLE.select().where(TAGS_TABLE.c.id == id)
        result = await DATABASE.fetch_all(query=query)
        for row in result:
            return True
        return False

    except Exception as e:
        print('ERROR: Could not check if tag with id:',id,' exists in database')
        print(e)

async def tag_count():
    try:
        count = 0
        query = TAGS_TABLE.select()
        result = await DATABASE.fetch_all(query=query)
        for row in result:
            count = max(row[0],count)
        return count
    except Exception as e:
        print('Could not get the count of entries in table database')
        print(e)

async def remove_todo_from_database(id):
    try:
        query = TODOS_TABLE.delete().where(TODOS_TABLE.c.id == id)
        await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not remove todo with id ',id,' from database')
        print(e)

async def remove_all_todos_from_database():
    try:
        query = TODOS_TABLE.delete()
        await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not remove all todos from database')
        print(e)


async def insert_todo_into_database(id,title,order,completed,url):
    try:
       query = TODOS_TABLE.insert().values(id=id, title=title,order=order,completed=completed,url=url)
       await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not create todo with id: ',id,' title: ',title,' order: ', order,' completed:', completed, ' url:', url )
        print(e)

async def update_todo_in_database(id,title=None,order=None,completed=None,url=None):
    try:
        if title:
            query = TODOS_TABLE.update().where(TODOS_TABLE.c.id == id).values(title=title)
            await DATABASE.execute(query=query)
        if order:
            query = TODOS_TABLE.update().where(TODOS_TABLE.c.id == id).values(order=order)
            await DATABASE.execute(query=query)
        if completed:
            query = TODOS_TABLE.update().where(TODOS_TABLE.c.id == id).values(completed=completed)
            await DATABASE.execute(query=query)
        if url:
            query = TODOS_TABLE.update().where(TODOS_TABLE.c.id == id).values(url=url)
            await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not update todo with id: ',id,' title: ',title,' order:',order,' completed:',completed,' url:',url)
        print(e)

async def select_todo_from_database(id):
    try:
        query = TODOS_TABLE.select().where(TODOS_TABLE.c.id == id)
        result = await DATABASE.fetch_one(query=query)
        return result
    except Exception as e:
        print('ERROR: Could not get todo with id:',id)
        print(e)

async def select_all_todos_from_database():
    try:
        query = TODOS_TABLE.select()
        result = await DATABASE.fetch_all(query=query)
        return result
    except Exception as e:
        print('ERROR: Could not get all todos from database')
        print(e)

async def todo_exists_in_database(id):
    try:
        query = TODOS_TABLE.select().where(TODOS_TABLE.c.id == id)
        result = await DATABASE.fetch_all(query=query)
        for row in result:
            return True
        return False

    except Exception as e:
        print('ERROR: Could not check if todo with id:',id,' exists in database')
        print(e)

async def todo_count():
    try:
        count = 0
        query = TODOS_TABLE.select()
        result = await DATABASE.fetch_all(query=query)
        for row in result:
            count = max(row[0],count)
        return count
    except Exception as e:
        print('Could not get the count of entries in table database')
        print(e)


async def map_count():
    try:
        count = 0
        query = MAP_TABLE.select()
        result = await DATABASE.fetch_all(query=query)
        for row in result:
            count=count+1
        return count
    except Exception as e:
        print('Could not get the count of entries in table database')
        print(e)


async def select_map_entries_from_database_todo(todo_id):
    try:
        query = MAP_TABLE.select().where(MAP_TABLE.c.todo_id == todo_id)
        result = await DATABASE.fetch_all(query=query)
        return result
    except Exception as e:
        print('ERROR: Could not get map entries with todo_id:',id)
        print(e)

async def select_all_map_entries_from_database():
    try:
        query = MAP_TABLE.select()
        result = await DATABASE.fetch_all(query=query)
        return result
    except Exception as e:
        print('ERROR: Could not get all map entries')
        print(e)

async def select_map_entries_from_database_tag(tag_id):
    try:
        query = MAP_TABLE.select().where(MAP_TABLE.c.tag_id == tag_id)
        result = await DATABASE.fetch_all(query=query)
        return result
    except Exception as e:
        print('ERROR: Could not get map entries with tag_id:',id)
        print(e)

async def select_map_entries_from_database(todo_id, tag_id):
    try:
        query = MAP_TABLE.select().where(MAP_TABLE.c.todo_id == todo_id ).where( MAP_TABLE.c.tag_id == tag_id)
        result = await DATABASE.fetch_all(query=query)
        return result
    except Exception as e:
        print('ERROR: Could not get map entries with tag_id:',tag_id,' and todo_id: ',todo_id)
        print(e)

async def remove_todo_map_entries_from_database(todo_id):
    try:
        query = MAP_TABLE.delete().where(MAP_TABLE.c.todo_id == todo_id)
        await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not remove map entries with todo_id: ',todo_id,' from database')
        print(e)

async def remove_tag_map_entries_from_database(tag_id):
    try:
        query = MAP_TABLE.delete().where(MAP_TABLE.c.tag_id == tag_id)
        await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not remove map entries with tag_id: ',tag_id,' from database')
        print(e)

async def remove_map_entries_from_database(todo_id, tag_id):
    try:
        query = MAP_TABLE.delete().where(MAP_TABLE.c.todo_id == todo_id).where(MAP_TABLE.c.tag_id == tag_id)  # MAP_TABLE.delete().where(MAP_TABLE.c.todo_id == todo_id and MAP_TABLE.c.tag_id == tag_id)
        await DATABASE.execute(query=query)

    except Exception as e:
        print('ERROR: Could not remove map entries with tag_id: ',tag_id,' and todo_id:', todo_id,' from database')
        print(e)

async def remove_all_map_entries_from_database():
    try:
        query = MAP_TABLE.delete()
        await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not remove all map entries from database')
        print(e)

async def insert_map_entry_into_database(todo_id,tag_id):
    try:
        query = MAP_TABLE.insert().values(todo_id=todo_id, tag_id=tag_id)
        await DATABASE.execute(query=query)
    except Exception as e:
        print('ERROR: Could not create map entry with tag_id: ',tag_id,' and todo_id: ',todo_id)
        print(e)

## Database functions end***

async def get_all_todos(request):
    await DATABASE.connect()
    todos = []
    database_todos = await select_all_todos_from_database()
    database_map = await select_all_map_entries_from_database()
    for todo in database_todos:
        tags = []
        for map in database_map:
            if map[1] == todo[0]:
                tag = await select_tag_from_database(map[2])
                tags.append({'id': tag[0], 'title': tag[1], 'url': tag[2]})

        todos.append({'id': todo[0], 'title': todo[1], 'order': todo[2], 'completed': todo[3],
                      'url': todo[4], 'tags': tags})

    await DATABASE.disconnect()
    return web.json_response(todos)


async def remove_all_todos(request):

    await remove_all_todos_from_database()
    await remove_all_map_entries_from_database()

    return web.Response(status=204)


async def get_one_todo(request):
    id = int(request.match_info['id'])
    #await DATABASE.connect()
    if not await todo_exists_in_database(id):
        return web.json_response({'error': 'Todo not found'}, status=404)

    todo = await select_todo_from_database(id)
    tags = []
    database_map = await select_all_map_entries_from_database()
    for map in database_map:
        if map[1] == id:
            tag = await select_tag_from_database(map[2])
            tags.append({'id': tag[0], 'title': tag[1], 'url': tag[2]})

    return web.json_response(
        {'id': todo[0], 'title': todo[1], 'order': todo[2], 'completed': todo[3],
         'url': todo[4], 'tags': tags})


async def create_todo(request):
    data = await request.json()

    order = None

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})

    title = data['title']

    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    data['completed'] = bool(data.get('completed', False))

    if 'order' not in data:
        order = 0
    else:
        order = data['order']

    new_id = await todo_count() + 1

    data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=str(new_id))))

    await insert_todo_into_database(new_id,title,order, data['completed'],data['url'])

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )


async def update_todo(request):
    id = int(request.match_info['id'])
    data = await request.json()

    order = None
    completed = None
    title = None
    url = None

    if not await todo_exists_in_database(id):
        return web.json_response({'error': 'Todo not found'}, status=404)


    if 'order' in data:
        order = data['order']

    if 'title' in data:
        title = data['title']

    if 'completed' in data:
        completed = data['completed']

    if 'url' in data:
        url = data['url']

    await update_todo_in_database(id,title,order,completed,url)

    todo = await select_todo_from_database(id)

    return web.json_response(
        {'id': todo[0], 'title': todo[1], 'order': todo[2], 'completed': todo[3],
         'url': todo[4]})


async def remove_todo(request):
    id = int(request.match_info['id'])
    await DATABASE.connect()

    if not await todo_exists_in_database(id):
        return web.json_response({'error': 'Todo not found'}, status=404)


    await remove_todo_map_entries_from_database(id)

    await remove_todo_from_database(id)

    await DATABASE.disconnect()
    return web.Response(status=204)


###### My code ######

async def remove_all_tags(request):


    await remove_all_tags_from_database()
    await remove_all_map_entries_from_database()

    return web.Response(status=204)


async def get_all_tags(request):
    await DATABASE.connect()
    tags = []
    database_tags = await select_all_tags_from_database()
    database_map = await select_all_map_entries_from_database()

    for tag in database_tags:
        todos = []
        for map in database_map:
            if map[2] == tag[0]:
                todo = await select_todo_from_database(map[1])
                todos.append({'id': todo[0], 'title': todo[1], 'order': todo[2], 'completed': todo[3],'url': todo[4]})

        tags.append({'id': tag[0], 'title': tag[1],'url': tag[2], 'todos': todos})

    await DATABASE.disconnect()

    return web.json_response(tags)

async def create_tag(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})

    title = data['title']

    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    new_id = await tag_count() + 1

    data['url'] = str(request.url.join(request.app.router['one_tag'].url_for(id=str(new_id))))

    await insert_tag_into_database(new_id,title,data['url'])

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )


async def remove_tag(request):
    id = int(request.match_info['id'])
    await DATABASE.connect()

    if not await tag_exists_in_database(id):
        return web.json_response({'error': 'Todo not found'}, status=404)

    await remove_tag_map_entries_from_database(id)

    await remove_tag_from_database(id)

    await DATABASE.disconnect()
    return web.Response(status=204)


async def get_one_tag(request):

    id = int(request.match_info['id'])

    if not await tag_exists_in_database(id):
        return web.json_response({'error': 'Tag not found'}, status=404)

    tag = await select_tag_from_database(id)
    database_map = await select_all_map_entries_from_database()
    todos = []
    for map in database_map:
        if map[2] == tag[0]:
            todo = await select_todo_from_database(map[1])
            todos.append({'id': todo[0], 'title': todo[1], 'order': todo[2], 'completed': todo[3], 'url': todo[4]})

    return web.json_response({'id': tag[0], 'title': tag[1],'url': tag[2],'todos':todos})

async def update_tag(request):
    id = int(request.match_info['id'])
    data = await request.json()
    title = None
    url = None


    if not await tag_exists_in_database(id):
        return web.json_response({'error': 'Todo not found'}, status=404)

    if 'title' in data:
        title = data['title']
    if 'url' in data:
        url = data['url']

    await update_tag_in_database(id, title, url)

    tag = await select_tag_from_database(id)

    return web.json_response({'id': tag[0], 'title': tag[1],'url': tag[2]})


async def get_todos_of_tag(request):
    id = int(request.match_info['id'])

    if not await tag_exists_in_database(id):
        return web.json_response({'error': 'Tag not found'}, status=404)

    tag = await select_tag_from_database(id)
    database_map = await select_all_map_entries_from_database()
    todos = []
    for map in database_map:
        if map[2] == tag[0]:
            todo = await select_todo_from_database(map[1])
            todos.append({'id': todo[0], 'title': todo[1], 'order': todo[2], 'completed': todo[3], 'url': todo[4]})

    return web.json_response(todos)

async def remove_tag_from_todo(request):
    id = int(request.match_info['id'])
    tag_id = int(request.match_info['tag_id'])

    if not await todo_exists_in_database(id):
        return web.json_response({'error': 'Todo not found'}, status=404)

    if not await tag_exists_in_database(tag_id):
        return web.json_response({'error': 'Tag not found'}, status=404)

    await remove_map_entries_from_database(id,tag_id)
    return web.Response(status=204)

async def remove_tags_from_todo(request):
    id = int(request.match_info['id'])

    if not await todo_exists_in_database(id):
        return web.json_response({'error': 'Todo not found'}, status=404)

    await remove_todo_map_entries_from_database(id)
    return web.Response(status=204)



async def get_tags_from_todo(request):
    id = int(request.match_info['id'])

    if not await todo_exists_in_database(id):
        return web.json_response({'error': 'Todo not found'}, status=404)

    database_map = await select_all_map_entries_from_database()
    tags = []
    for map in database_map:
        if map[1] == id:
            tag = await select_tag_from_database(map[2])
            tags.append({'id': tag[0], 'title': tag[1], 'url': tag[2]})

    return web.json_response(tags)


async def associate_tag_to_todo(request):
    data = await request.json()
    print(data)
    id = int(request.match_info['todo_id'])

    if 'id' not in data:
        return web.json_response({'error': '"id" is a required field'})

    if not await todo_exists_in_database(id):
        return web.json_response({'error': 'Todo not found'}, status=404)

    tag_id = data['id']

    await insert_map_entry_into_database(id,tag_id) #reversed
    return web.Response(status=201)


########################
# LINKS
# http://todo.thing.zone/documentation#!/tags/deleteTags
# http://localhost:8080
# http://todospecs.thing.zone/

########################

app = web.Application()

########################

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

ENGINE = sqlalchemy.create_engine('sqlite:///'+DIR_PATH+'\\app_database.db')
if not sqlalchemy_utils.database_exists('sqlite:///'+DIR_PATH+'\\app_database.db'):
    print('No database found. Creating new one.')

    sqlalchemy_utils.create_database('sqlite:///'+DIR_PATH+'\\app_database.db')
    try:
        METADATA.create_all(ENGINE)
    except Exception as e:
        print('Error during table creation.')
        print(e)

CONNECTION = ENGINE.connect()

DATABASE = databases.Database('sqlite:///'+DIR_PATH+'\\app_database.db')


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
