import sys
import aiohttp
import asyncio
import json

hostname=sys.argv[1]
port=sys.argv[2]
MYhostname = hostname + ':' + port

async def printList(list):
    for game in list:
        myStatus = await callServer("/status?game=" + str(game["id"]))
        if not "winner" in myStatus:
            clear = True
            if "board" in myStatus:
                for row in myStatus["board"]:
                    for col in row:
                        if col!=0:
                            clear=False

            if clear==True:
                print(game["id"]+" "+game["name"])


def printGame(game):
    print("print Game")
    boardSymbols = ['_', 'x', 'o']
    board=game["board"]
    for row in board:
        for numberSymbol in row:
            print(boardSymbols[numberSymbol]+"",end='')
        print()

async def StartGame():
    print("Write [ID] or new [ nameGame ]'")
    while True:
        text= input()

        if text.startswith("new"):
            player = 1
            spiltted = text.split(" ")
            if len(spiltted) == 2:
                game = await callServer("/start?name=" + spiltted[1])
            else:
                game = await callServer("/start?name=" + "")
            gameID=game["id"]

            break
        elif text.isdigit():
            player = 2
            gameID = text
            break
        else:
            print("Invalid command. Try again")
    return gameID,player

def checkCountGames(listOfGames):
    if(len(listOfGames)>0):
        print("Here are your games")
    else:
        print("start a new game")

async def callServer(parameters):

    async with aiohttp.ClientSession() as session:
        async with session.get('http://'+MYhostname+parameters) as resp:
            # print(resp.sttatus)
            return  json.loads(await resp.text())

@asyncio.coroutine
async def main():
    gameID=0
    player=0
    winner=None

    isBoardPrinted=False
    myList =  await callServer("/list")
    checkCountGames(myList)
    await printList(myList)
    gameID,player = await StartGame()
    if player == 1:
        isBoardPrinted=True

    while True:
        myStatus = await callServer("/status?game=" + str(gameID))
        if  "next" in myStatus and  myStatus["next"] != player and isBoardPrinted == False:
            print("waiting for the other player")
            isBoardPrinted = True


        if "winner" not in myStatus and isBoardPrinted ==True :

            if  "next" in myStatus and myStatus["next"]==player:
                printGame(myStatus)
                print()
                if player==1:
                    print("your turn (x):")
                else:
                    print("your turn (o):")

                inputUser = input()
                inputUser=inputUser.split(" ")
                if not inputUser[0].isdigit():
                    print("invalid input")
                    continue
                if len(inputUser) != 2:
                    print("invalid input")
                    continue
                if not inputUser[1].isdigit():
                    print("invalid input")
                    continue

                responsFromPlay = await callServer('/play?game=' + str(gameID) +
                            '&player=' + str(player) + '&x=' + str(inputUser[0]) + '&y=' + str(inputUser[1]))

                if responsFromPlay['status'] == 'bad':
                    print("invalid input")
                else:
                    isBoardPrinted = False




        else:
            if "winner" in myStatus:
                if myStatus["winner"] == player:
                    print("you win")
                elif myStatus["winner"] == 0:
                    print("draw")
                else:
                    print("you lose")
                break




        #await asyncio.sleep(1)




if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())