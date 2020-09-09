from starlette.applications import Starlette
from starlette.config import Config
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware

import sqlalchemy
# from databases import Database
# from modals.CardEntry import CardEntry, CardEntryEncoder
import json
from dbWrapper import DBWrapper

cards = []
wrapper = DBWrapper()


async def homepage(request):
    return PlainTextResponse("Welcome to Home Page!")

# Fetches all cards


async def getCards(request):
    # for card in cards:
    #     print(card.title, " : ", card.thumbnail)

    rows = await wrapper.fetchCards()
    print(rows)

    contents = [
        {
            "id": str(row['id']),
            "position": row['position'],
            "title": row['title'],
            "thumbnail": row['thumbnail'],
            "slug_type": row['slug_type'],
        }
        for row in rows
    ]

    return JSONResponse(contents)

# fetches card based on position
async def getCardByPosition(request):
    position = int(request.path_params['position'])
    row = await wrapper.fetchCardByPosition(position)
    return JSONResponse({
        'id' : str(row['id']),
        "position": row['position'],
        "title": row['title'],
        "thumbnail": row['thumbnail'],
        "slug_type": row['slug_type'],
    })

def _makeSlug(title):
    # title = "one Of this Type"
    slug_type = title.split()
    print(slug_type)

    slug = ""
    for word in slug_type:
        slug += word.lower() + "-"

    slug = slug[0: len(slug)-1]
    print("final slug : ", slug)
    return slug

# creates a new card based on title, thumbnail and position
async def createCard(request):
    # position = request.path_params['position']
    # title = request.path_params['title']
    # thumbnail = request.path_params['thumbnail']
    form = await request.form()
    position = form['position']
    title = form['title']
    thumbnail = form['thumbnail']

    slug_type = _makeSlug(title)

    value = {
        "position": position,
        "title": title,
        "thumbnail": thumbnail,
        "slug_type": slug_type
    }

    await wrapper.createCard(value)
    row = await wrapper.fetchCardByPosition(position)

    return JSONResponse({
        'id' : str(row['id']),
        "position": row['position'],
        "title": row['title'],
        "thumbnail": row['thumbnail'],
        "slug_type": row['slug_type'],
    })

# Delete card by position number in web grid
async def deleteCard(request):
    position = int(request.path_params['position'])
    card = await wrapper.fetchCardByPosition(position)
    card_title = card['title']

    await wrapper.deleteCard(position)
    return PlainTextResponse("Card " + card_title + " is now deleted")

# Updates card values - title, thumbnail, position .. all based on id as conditional value
async def updateCard(request):
    cardid = int(request.path_params['id'])
    position = int(request.path_params['position'])
    title = request.path_params['title']
    thumbnail = request.path_params['thumbnail']

    await wrapper.updateCard(cardid, position, title, thumbnail)
    row = await wrapper.fetchCardByPosition(position)

    return JSONResponse({
        "id": str(row['id']),
        "position": row['position'],
        "title": row['title'],
        "thumbnail": row['thumbnail'],
        "slug_type": row['slug_type'],
    })

# Route('mapping path', endpoint=None, methods=[''])
routes = [
    Route("/", endpoint=homepage, methods=['GET']),
    Route("/cards/all", endpoint=getCards, methods=['GET']),
    Route("/cards/{position}", endpoint=getCardByPosition, methods=['GET']),

    # Route("/cards/{position}/{title}/{thumbnail}",endpoint=createCard, methods=['POST']),
    Route("/cards",endpoint=createCard, methods=['POST']),
    Route("/cards/{position}", endpoint=deleteCard, methods=['DELETE']),
    Route("/cards/{id}/{position}/{title}/{thumbnail}",
          endpoint=updateCard, methods=['PUT']),

    Mount('/static', StaticFiles(directory='statics')),
    # for all cards
    # Mount('/cards', routes=[
    #     Route('/all', endpoint=getCards, methods=['GET']),
    #     Route("/{position}", endpoint=getCardByPosition, methods=['GET'])
    # ]),

]


async def startops():
    await wrapper.initDB()
    print("Server booted up ... :-)")


def endops():
    wrapper.disconnect()
    print("Server shuting down .. ")


middleware = [
    #   Middleware(TrustedHostMiddleware, allowed_hosts=['localhost:3000']),
    #   Middleware(HTTPSRedirectMiddleware)
    Middleware(CORSMiddleware, allow_origins=['*'])
]

# Starlette(debug=False, routes=None, middleware=None, exception_handlers=None, on_startup=None, on_shutdown=None)
# if __name__ == '__main__':
app = Starlette(
    debug=True,
    middleware=middleware,
    routes=routes,
    on_startup=[startops],
    on_shutdown=[endops],
)
