# https://riptutorial.com/gtk3/example/24777/embed-a-video-in-a-gtk-window-in-python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gst  # ,GObject
from view import myView
from model import myModel

from server import myServer

import threading

Gst.init(None)
Gst.init_check(None)


class myController(object):
    def __init__(self, view, model, server):
        self._view = view
        self._model = model
        self._server = server
        

        def run_asyncio():
            # server = Server()
            self._server.run()
    
        self._tServer = threading.Thread(target=run_asyncio)
        self._tServer.daemon = True
        self._tServer.start()

        self._view.connect('button-addChannel-clicked', self._addVideoButton)
        self._view.connect('button-startChannel-clicked', self._startVideo)
        self._view.connect('button-stopChannel-clicked', self._stopVideo)
        self._view.connect('combobox-input-changed', self._inputChanged)
        self._view.connect('destroy', self.on_destroy)
        self._view.connect('button-addClient-clicked', self._addClient)

        # self._server.connect('message', self._message)

    def message(self, message):
        print('got message',message)
        if message=='add':
            self._addVideo()

    def close_all(self):
        # self._server.stop()
        Gtk.main_quit()


    def on_destroy(self, win):
        # print("bye bye")
        # self._tServer.
        # self.tServer.
        self.close_all()


    def _addVideoButton(self, button):        
        self._addVideo()

    def _addVideo(self):
        print("add video")
        # model
        channelNum = self._model._createChannel()
        print(f"channel {channelNum} created")
        # self._channels.append(channel)
        # pass sink to view
        _gtksink = self._model._getGtksink(channelNum)  # TODO remove + dependent
        self._view._addVideoView(channelNum)
        # self._view._setVideoView(gtksink, channelNum)
        self._server.broadcast()



    def _startVideo(self, button, channelNum):
        print("starting video", channelNum)
        # channel = self._channels[arg]
        # channel._stop()
        attributes = self._view._getAttributes(channelNum)
        print(attributes)
        path = attributes["dialogFilePath"]
        print('controller path', path)

        self._model._setAttributes(channelNum, attributes)

        self._model._play(channelNum)

    def _stopVideo(self, button, channelNum):
        print("stopping video", channelNum)
        # channel = self._channels[arg]
        self._model._stop(channelNum)
        # channel._play()

    def _inputChanged(self, combo, channelNum, inputType):
        print("input changed")
        # print(combo)
        print("channel", channelNum)
        print("input", inputType)

        # Model - create channel
        self._model._setInput(channelNum, inputType)

        # pass sink to view
        _gtksink = self._model._getGtksink(channelNum)
        # self._view._addVideoView(_gtksink)

        self._view._setVideoView(_gtksink, channelNum)

    def _addClient(self, button, channelNum, ip, port):
        print(f"controller: channel {channelNum} add client", ip, port)
        self._model._addClient(channelNum, ip,port)



def main():
    view = myView()
    model = myModel()
    server = myServer()
    controller = myController(view, model, server)

    server.setController(controller)
    Gtk.main()

if __name__ == "__main__":
    # window = Gtk.ApplicationWindow()


    main()

    # vbox = Gtk.VBox()

    # window
    # window.add(vbox)

    # model



    # # import asyncio
    # import threading

    # def run_asyncio():
    #     server = Server()
    #     server.run()
    
    # threading.Thread(target=run_asyncio).start()

    
    # asyncio.run(server.main())
    # Create a gstreamer pipeline with no sink. 
    # A sink will be created inside the GstWidget.
    # widget = GstWidget('videotestsrc')
    # widget.set_size_request(200, 200)

    # vbox.add(widget)
    # button = Gtk.Button("Start")
    # button.connect("clicked", controller.addVideo)
    # vbox.add(button)

    # window.show_all()


