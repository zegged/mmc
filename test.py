import asyncio

class myServer:
    def __init__(self,controller):
        self._controller=controller

    @asyncio.coroutine
    def handle_echo(reader, writer):
        data = yield from reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        print("Send: %r" % message)
        writer.write(data)
        yield from writer.drain()

        print("Close the client socket")
        writer.close()

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.handle_echo, '127.0.0.1', 8888, loop=loop)
        server = loop.run_until_complete(coro)

        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()



def main():
    s  = myServer()
    s.run()

if __name__=="__main__":
    main()