#Basic socket-based server.
#Listens for attempted connections
#calls necessary functions depending on start of message

from websockets.asyncio.server import serve
import asyncio
import FinalTakeDBHandler


port = 7000




async def clientHandler(websocket):
    print ("Connection w/ new client")
    handler = FinalTakeDBHandler.DBHandler()
    async for message in websocket:
        print("recieved message: "+str(message))

        dataElements = message.split("::")
        #Intended structure of dataElements:
        #AuthToken::UserID::[specificRequest]

        match dataElements[2]:
            case ("MediaSearch"):
                #Format of mediasearch specific request: "mediasearch::[mediatype]::[name]::[release/publish year]"
                # dataElements[3] = mediatype, [4] = name [5] = release.
                table = dataElementas[3]
                name = null
                if (dataElements[4]):
                    name = dataElements[4]
                yor = null
                if (dataElements[5]):
                    yor = dataElements[5]

                mediaID = handler.search(name, yor, table)

                if mediaID == -1:
                    response = "NoResults"
                else:
                    response = "Results::"+"::".join(mediaID)
                await websocket.send(response)
                    
            case ("UserSignup"):
                #Format of signup message: "usersignup::[email]::[password]::[username]"
                # dataElements[3] = email [4] = password [5] = username
                handler.signup(dataElements[3], dataElements[4], dataElements[5])
                await websocket.send("Successful user signup")


            case ("UserLogin"):
                #Format of login message: "userlogin::[email]::[password]::[username]"
                # dataElements[3] = email [4] = password
                sessionID = handler.login(dataElements[3], dataElements[4])
                match sessionID:
                    case -1:
                        response = ("EmailNotFound")
                    case 0:
                        response = ("PasswordIncorrect")
                    case _:
                        response = (f"SuccessfulLogin::{sessionID}")
                await websocket.send(response)


            case ("UserLogout"):
                #Format of logout message: "userlogout
                handler.logout(dataElements[1])
                await websocket.send("Successful logout")


            case ("AuthTest"):
                #This is a test for pre-front end integration. Auth should be worked into all search requests and 
                #all review actions.

                print(dataElements[0])
                print(dataElements[1])
                authorized = handler.authenticate(dataElements[0],dataElements[1])
                print(f"authorized: {authorized}")
                match authorized:
                    case -1:
                        response = "NotAuthorized"
                    case 1:
                        response = "Authorized"
                print (response)
                await websocket.send(response)




async def main():
    print("running main")
    async with serve(clientHandler, "localhost", port) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())