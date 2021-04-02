import asyncio
from gi.repository import Gtk, GObject
import time
class myServer:
    def __init__(self, controller):
        self._controller=controller
        self._users = {}
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)      


    def broadcast(self):
        coro = self.broadcast_async()
        # self.loop.
        # loop = asyncio.get_event_loop()
        # future = asyncio.run_coroutine_threadsafe(coro,loop)
        # asyncio.run(coro)
        asyncio.run_coroutine_threadsafe(coro, self._loop)
        # future.result()


    def broadcast_async(self):
        print('broadcasting')
        for user in self._users.keys():
            writer = self._users[user]['writer']
            data = 'hello'.encode()
            writer.write(data)
            yield from writer.drain()
        return "done"

    @asyncio.coroutine
    def handle_echo(self,reader, writer):
        writer.write("hello".encode())
        addr = writer.get_extra_info('peername')
        self._users[addr]={'reader':reader,'writer':writer}
        while True:
            data = yield from reader.read(100)
            message = data.decode()
            if message=="close":
                break

            print(f"Received {message!r} from {addr!r}")
            
            self._controller.message("add")
            
            
            print(f"Send: {message!r}")
            writer.write(data)
            yield from writer.drain()

        print("Close the connection")
        writer.close()



    def run(self):
        coro = asyncio.start_server(self.handle_echo, '0.0.0.0', 8888, loop=self._loop)
        server = self._loop.run_until_complete(coro)
        self.aServer = server
        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            pass

        # Close the server
        server.close()
        self._loop.run_until_complete(server.wait_closed())
        self._loop.close()

    def stop(self):
        print('stopping asyncio')
        self.aServer.close()
        # await self.aServer.wait_closed()
        # while self.aServer.wait_closed() == False:
        #     print("waiting for server to close")
        #     time.sleep(1)

        
        # self.loop.close()
        # loop = asyncio.get_event_loop()
        # loop.close()
        # t = asyncio.current_task()
        # t.cancel()
        # asyncio.stop()

if __name__ == "__main__":
    server = Server(None)

    # asyncio.run(server.main())
    server.run()
    print("closing server")