import sys
from aiohttp import web
import asyncio


mySavedGames=dict()
routes = web.RouteTableDef()

@asyncio.coroutine
@routes.get('/list')
async def list(request):
    res = []
    for id, name in mySavedGames.items():
        res.append({"id": id, "name": name.nameOfGame})

    return  web.json_response(res)


@asyncio.coroutine
@routes.get('/start')
async def startGame(request):
    mySavedGames[str(len(mySavedGames) + 1)] = myPlayground()
    try:
        mySavedGames[str(len(mySavedGames))].setName(request.rel_url.query['name'])
    except:
        mySavedGames[str(len(mySavedGames))].setName("")


    return web.json_response({"id": len(mySavedGames)})

@asyncio.coroutine
@routes.get('/status')
async def statusGame(request):

    try:
        statusGame = mySavedGames[request.rel_url.query['game']]
    except:
        return web.Response(text="Wrong arguments", status=422)

    if statusGame.winner is None:
       
        return web.json_response(dict([('board',statusGame.board),('next',int(statusGame.next))]))
    else:
        return web.json_response(dict([('winner',  int(statusGame.winner))]))


@asyncio.coroutine
@routes.get('/play')
async def playGame(request):
    try:
        playGame = mySavedGames[request.rel_url.query['game']]
    except:
        return web.Response(text="Wrong arguments", status=422)

    if playGame.winner is None:
        try:
            player = int(request.rel_url.query['player'])
        except:
            return web.json_response(dict([('status', "bad"), ("message", "Wrong argument for player")]))

        if player == 1 or player == 2 :
            if playGame.next != player:
                return web.json_response(dict([('status', "bad"), ("message", "Its not your turn!")]))


        else:
            return web.json_response(
                dict([('status', "bad"), ("message", "Only two players play, choose player 1 or 2")]))

        try:
            y= int(request.rel_url.query['y'])
            if y < 0 or y > 2:
                return web.json_response(dict([('status', "bad"), ("message", "Y is not correct")]))


            x = int(request.rel_url.query['x'])
            if x < 0 or x > 2:
                return web.json_response(dict([('status', "bad"), ("message", "X is not correct")]))
        except:
            return web.json_response(dict([('status', "bad"), ("message", "X or Y is incorrect")]))

        if playGame.board[x][y] != 0:
            return web.json_response(dict([('status', "bad"), ("message", "Somebody played here, choose different field")]))
        if player==2:
            playGame.board[x][y]=2
            playGame.next = 1
        elif player==1:
            playGame.board[x][y] = 1
            playGame.next=2

        myBoard=playGame.getBoard()




        isDraw=True
        for row in myBoard:
            if 0 in row:
                isDraw=False
                break;
        if isDraw is True:
            playGame.winner=0

        if player==myBoard[0][y] == myBoard[1][y] == myBoard[2][y]:
            playGame.winner=player
        if player==myBoard[x][0] == myBoard[x][1] == myBoard[x][2]:
            playGame.winner = player
        if player==myBoard[0][0] == myBoard[1][1] == myBoard[2][2]:
            playGame.winner = player
        if player==myBoard[0][2] == myBoard[1][1] == myBoard[2][0]:
            playGame.winner = player

   
        return web.json_response(dict([('status', "ok")]))
    else:
        return web.json_response(dict([('status', "bad"),("message","Game is over")]))

class myPlayground:
    def __init__(self):
        self.board=[[0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0]]
        self.nameOfGame=""
        self.next=1
        self.winner = None
    def setName(self,nameOfGame):
        self.nameOfGame=nameOfGame

    def getBoard(self):
        return self.board
def main():
    if len(sys.argv) == 2:
        app = web.Application()
        app.add_routes(routes)
        web.run_app(app,port=int(sys.argv[1]) )


    else:
        print("Wrong arguments")
        exit(1)


if __name__ == '__main__':
    main()