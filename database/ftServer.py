#Basic socket-based server.
#Listens for attempted connections
#calls necessary functions depending on start of message

import websockets
import asyncio
import FinalTakeDBHandler


handler = FinalTakeDBHandler DBHandler()
#server data

port = 7000

print ("Server initialized, listening on port " + str(port))

async def echo(websocket, path):
    print ("Connection w/ new client")
    async for message in websocket:
        print("recieved message: "+str(message))

        if ("MediaSearch" in message):
            #Format of mediasearch message: "mediasearch:,[mediatype]:,[name]:,[release/publish year]"
            dataElements = message[13:].split(":,")
            # dataElements[0] = mediatype, [1] = name [2] = release.
            table = dataElementas[0]
            name = dataElements[1]
            yor = null
            if (dataElements[2]):
                yor = dataElements[2]
            handler.search(name, yor, table)

        if ("UserSignup" in message):
            #Format of signup message: "usersignup:,[email]:,[password]:,[username]"
            dataElements = message[11:].split(":,")
            # dataElements[0] = email [1] = password [2] = username
            handler.signup(dataElements[0], dataElements[1], dataElements[2])
        
        if ("UserLogin" in message):
            #Format of signup message: "usersignup:,[email]:,[password]:,[username]"
            dataElements = message[11:].split(":,")
            # dataElements[0] = email [1] = password
            handler.login(dataElements[0], dataElements[1])



start_server = websockets.serve(echo, "localhost", port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()