import logging
from aiohttp import web
import aiohttp_cors

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
