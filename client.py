import asyncio
@asyncio.coroutine
def tcp_echo_client(message,loop):
# async def tcp_echo_client(message,loop):
    # reader, writer = await asyncio.open_connection(
    #     '127.0.0.1', 8888)
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888,
                                                        loop=loop)

    while(True):
        # inp = input(">")
        # if inp == "close":
        #     writer.write("close".encode())
        #     break

        # writer.write(inp.encode())
        # data = await reader.read(100)

        data =  yield from  reader.read(100)
        print(f'server>{data!r}')
    # print(f'Send: {message!r}')
    # writer.write(message.encode())

    # data = await reader.read(100)
    # print(f'Received: {data.decode()!r}')

    # print(f'Send: {message!r}')
    # writer.write(message.encode())

    # data = await reader.read(100)
    # print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()

message = 'Hello World!'
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()

# asyncio.run(tcp_echo_client('Hello World!'))