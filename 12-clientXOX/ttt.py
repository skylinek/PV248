#!/usr/bin/python3

import sys
import json
from aiohttp import web

port = int(sys.argv[1])
games = dict()
routes = web.RouteTableDef()

class Game:
  def __init__(self, name):
    self.name = name
    self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    self.next = 1 #who plays next
    self.winner = None

def check_tie(board):
    if not any(0 in row for row in board):
        return True
    return False

def check_winner(board, player):
    # Diagonal check
    if board[0][0] == board[1][1] == board[2][2] == player or \
            board[2][0] == board[1][1] == board[0][2] == player:
        return True

    # Horizontal and Vertical check
    for x in range(3):
        if board[x][0] == board[x][1] == board[x][2] == player or \
                board[0][x] == board[1][x] == board[2][x] == player:
            return True

    return False

@routes.get('/start')
async def start_new_game(request):
    try:
        name = request.rel_url.query['name']
    except:
        name = ''

    game_id = str(len(games) + 1)
    games[game_id] = Game(name)
    res = {"id": int(game_id)}
    return web.json_response(res)

@routes.get('/status')
async def status(request):
    try:
        game_id = request.rel_url.query['game']
    except:
        return web.Response(text="missing game id", status=400)

    try:
        game = games[str(game_id)]
    except:
        return web.Response(text="non-existing game id", status=404)

    res = {}
    if game.winner is not None:
        res["winner"] = int(game.winner)
    else:
        res["board"] = game.board
        res["next"] = int(game.next)

    return web.json_response(res)

@routes.get('/play')
async def play(request):
    try:
        game_id = request.rel_url.query['game']
    except:
        return web.Response(text="missing game id", status=400)

    try:
        game = games[str(game_id)]
    except:
        return web.Response(text="non-existing game id", status=404)

    if games[str(game_id)].winner is not None:
        return web.json_response({"status": "bad", "message": "Game already ended!"})

    try:
        player = int(request.rel_url.query['player'])

        if player != 1 and player != 2:
             return web.json_response({"status": "bad", "message": "Player must be number 1 or 2!"})

        if games[game_id].next != player:
            message = "Player " + str(player) + " is not on turn!"
            return web.json_response({"status": "bad", "message": message})
    except:
        return web.json_response({"status": "bad", "message": "Player not specified or not a number!"})

    try:
        x = int(request.rel_url.query['x'])
        if x < 0 or x > 2:
            return web.json_response({"status": "bad", "message": "X coordinate is out of the board!"})
    except:
        return web.json_response({"status": "bad", "message": "Missing or not numeric x coordinate!"})

    try:
        y = int(request.rel_url.query['y'])
        if y < 0 or y > 2:
            return web.json_response({"status": "bad", "message": "Y coordinate is out of the board!"})
    except:
        return web.json_response({"status": "bad", "message": "Missing or not numeric y coordinate!"})

    if games[game_id].board[x][y] != 0:
        return web.json_response({"status": "bad", "message": "Cell is already used!"})

    #save player move
    games[game_id].board[x][y] = player

    #set who plays next
    if player == 1:
        games[game_id].next = 2
    else:
        games[game_id].next = 1

    #check if there is a winner or tie
    if check_winner(games[game_id].board, player):
        games[game_id].winner = player
    elif check_tie(games[game_id].board):
        games[game_id].winner = 0

    return web.json_response({"status": "ok"})

# @routes.get('/list')
# async def list(request):
#     res = []
#     for key, game in games.items():
#         res.append({"id": key, "name": game.name})
#
#     return web.json_response(#TODO)

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=port)
