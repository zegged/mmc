import asyncio
from gi.repository import Gtk, GObject
class myServer:
    def setController(self, controller):
        self._controller=controller

    async def handle_echo(self,reader, writer):
        while True:
            data = await reader.read(100)
            message = data.decode()
            if message=="close":
                break
            addr = writer.get_extra_info('peername')

            print(f"Received {message!r} from {addr!r}")
            self._controller.message(message)
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