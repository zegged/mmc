import asyncio
from gi.repository import Gtk, GObject
import time
class myServer:
    def __init__(self, controller):
        self._controller=controller
        self._users = {}
        self.loop = None       


    def broadcast(self):
        coro = self.broadcast_async()
        # self.loop.
        # loop = asyncio.get_event_loop()
        # future = asyncio.run_coroutine_threadsafe(coro,loop)
        asyncio.run(coro)
        # future.result()


    async def broadcast_async(self):
        print('broadcasting')
        for user in self._users.keys():
            writer = self._users[user]['writer']
            data = 'hello'.encode()
            writer.write(data)
            await writer.drain()
        return "done"

    
    async def handle_echo(self,reader, writer):
        writer.write("hello".encode())
        addr = writer.get_extra_info('peername')
        self._users[addr]={'reader':reader,'writer':writer}
        while True:
            data = await reader.read(100)
            message = data.decode()
            if message=="close":
                break

            print(f"Received {message!r} from {addr!r}")
            def test():
                self._controller.message("add")
            GObject.idle_add(test)
            
            print(f"Send: {message!r}")
            writer.write(data)
            await writer.drain()

        print("Close the connection")
        writer.close()

    async def main(self):
        server = await asyncio.start_server(
            self.handle_echo, '127.0.0.1', 8888)
        self.aServer = server
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

    def run(self):
        self.loop = asyncio.run(self.main()) 
        print('done')   

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
    server = Server()

    # asyncio.run(server.main())
    server.run()
    print("closing server")