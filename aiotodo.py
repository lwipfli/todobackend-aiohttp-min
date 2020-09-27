import logging
from aiohttp import web
import aiohttp_cors

TODOS = {
    0: {'title': 'build an API', 'order': 1, 'completed': False, 'url': 'Test Url', 'tags': []},
    1: {'title': '?????', 'order': 2, 'completed': False, 'url': 'Test Url', 'tags': []},
    2: {'title': 'profit!', 'order': 3, 'completed': False, 'url': 'Test Url', 'tags': []}
}

TAGS = {
    0: {'title': 'THE TAG', 'url': 'Test url', 'todos': []},
}


def get_all_todos(request):
    return web.json_response([
        {'id': key, **todo} for key, todo in TODOS.items()
    ])


def remove_all_todos(request):
    TODOS.clear()
    return web.Response(status=204)


def get_one_todo(request):
    id = int(request.match_info['id'])

    if id not in TODOS:
        return web.json_response({'error': 'Todo not found'}, status=404)

    return web.json_response({'id': id, **TODOS[id]})


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
    data['tags'] = []
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

    del TODOS[id]

    return web.Response(status=204)


###### My code ######

def remove_all_tags(request):
    TAGS.clear()
    return web.Response(status=200)


def get_all_tags(request):
    return web.json_response([
        {'id': key, **tag} for key, tag in TAGS.items()
    ])


async def create_tag(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})

    title = data['title']

    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    for item in TAGS:
        if item.title == title:
            return web.json_response({'error': '"title" is already in use'})

    new_id = max(TAGS.keys(), default=0) + 1

    data['url'] = str(request.url.join(request.app.router['one_tag'].url_for(id=str(new_id))))

    data['todos'] = []

    TAGS[new_id] = data

    return web.Response(
        headers={'Location': data['url']},
        status=200
    )


def remove_tag(request):
    id = int(request.match_info['id'])

    if id not in TAGS:
        return web.json_response({'error': 'Tag not found'})

    del TAGS[id]

    return web.Response(status=200)


def get_one_tag(request):
    id = int(request.match_info['id'])

    if id not in TAGS:
        return web.json_response({'error': 'Tag not found'}, status=404)

    return web.json_response({'id': id, **TAGS[id]})

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

    

########################
# TODO Add correct tags and todos instead of id's to get and getall

# http://todo.thing.zone/documentation#!/tags/deleteTags
# https://docs.aiohttp.org/en/latest/web_quickstart.html
# http://demos.aiohttp.org/en/latest/tutorial.html
# https://ilias.unibe.ch/ilias.php?ref_id=1841334&cmd=frameset&cmdClass=ilrepositorygui&cmdNode=113&baseClass=ilRepositoryGUI
# https://ilias.unibe.ch/ilias.php?ref_id=1919292&target=1919292&cmd=showOverview&cmdClass=ilobjexercisegui&cmdNode=e1:qp&baseClass=ilexercisehandlergui

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
