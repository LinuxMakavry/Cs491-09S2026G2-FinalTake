from websockets.asyncio.client import connect
import asyncio


async def serverTest():
    async with connect("ws://localhost:7000") as ws:
        print ("Connection formed")
        userMessage =""
        authToken ="0"
        User = "0"
        result = ""
        while(userMessage != "quit"):
            print("List of functions:\n")
            print("1. Signup:\n2)Login\n3)AuthTest\n4)Search\n5)Logout\nType 'quit' to quit.")
            userMessage = input()
            requestElements = []
            requestElements.append(authToken)
            requestElements.append(User)
            match userMessage:
                case '1':
                    requestElements.append("UserSignup")
                    print("Email: ")
                    email = input()
                    print("username: ")
                    username = input()
                    print("password: ")
                    password = input()
                    
                    requestElements.append(email)
                    requestElements.append(password)
                    requestElements.append(username)

                    request = "::".join(requestElements)

                    print(request+"\n")
                    await ws.send(request)
                    result = await ws.recv()
                case '2':
                    requestElements.append("UserLogin")
                    print("Email: ")
                    email = input()
                    print("password: ")
                    password = input()
                    
                    requestElements.append(email)
                    requestElements.append(password)

                    request = "::".join(requestElements)    
                    print(request+"\n")
                    await ws.send(request)
                    result =  await ws.recv()
                    dataElements = result.split("::")
                    if(len(dataElements) > 1):
                        User = dataElements[1]
                        authToken = dataElements[2]
                        print(f"User = {dataElements[1]}")
                        print("Logged in, sessionid: " + authToken)
                    else:
                        print("Login Failed: "+result)
                case '3':
                    requestElements.append("AuthTest")
                    request = "::".join(requestElements)
                    print(request)
                    await ws.send(request)
                    result = await ws.recv()
                case '4':
                    requestElements.append("MediaSearch")
                    print("Type -1 if not using a criteria\n")
                    print("Media type: ")
                    mediatype = input()
                    print("Title: ")
                    title = input()
                    print("Year of release: ")
                    yor = input()
                    request = "::".join(requestElements)
                    await ws.send(request)
                    result = await ws.recv()
                case '5':
                    requestElements.append("UserLogout")
                    request = "::".join(requestElements)
                    await ws.send(request)
                    result = await ws.recv()
                case "quit":
                    await ws.close()
            
            print ("Received '%s'" % result)

if __name__ == "__main__":
    asyncio.run(serverTest())