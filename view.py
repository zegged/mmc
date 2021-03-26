import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GObject



class Handler:
    def __init__(self,view, channelNumber, builder):
        self.view = view
        self.channelNumber = channelNumber
        self.builder = builder

    def onDestroy(self, *args):
        print("view destroy")
        # Gtk.main_quit()
        self.view.emit("destroy")

    def onButtonPressed(self, button):
        print("Hello World!")
        self.view.emit("button-addChannel-clicked")

    def on_inputBox_changed(self, box):
        source = box.get_active_text()
        print(f"channel {self.channelNumber} input changed to {source}")
        self.view.emit('combobox-input-changed', int(self.channelNumber), str(source))

        # handle attributes:
        # hide att window
        attributesBox = self.builder.get_object("attributesBox")
        for att in attributesBox:
            print(att)
            att.hide()

        # show relevant attribute
        if source == "USB-Camera(Windows)":
            print("USB-Camera(Windows)")
            cameraList = self.builder.get_object("cameraList")
            cameraList.append(None,"0")
            cameraList.append(None,"1")
            cameraList.append(None,"2")
            cameraList.show()


        elif source == "USB-Camera":
            print("USB-Camera(Windows)")
            cameraList = self.builder.get_object("cameraList")
            cameraList.append(None,"/dev/camera0")
            cameraList.append(None,"/dev/camera1")
            cameraList.append(None,"/dev/camera2")
            cameraList.show()  

        elif source == 'UDP':
            print("UDP")
            port = self.builder.get_object("sourcePort")
            port.show()
        elif source == 'local file':
            print('local file')
            # filePath = self.builder.get_object("filePath")
            # filePath.show()

            # filePathDialog = self.builder.get_object("filePathDialog")
            # print(filePathDialog)
            # filePathDialog.show()
            filePathBox = self.builder.get_object("filePathBox")
            filePathBox.show_all()

    def on_playButton_clicked(self, button):
        arg = self.channelNumber
        print("VIEW: button-startChannel-pressed", arg)
        self.view.emit('button-startChannel-clicked', int(arg))

    def on_stopButton_clicked(self, button):
        arg = self.channelNumber
        print("VIEW: button-stopChannel-pressed", arg)
        self.view.emit('button-stopChannel-clicked', int(arg))

    def on_addClient_clicked(self, button):
        # get ip, port fields and client list
        parent = button.get_parent()
        # print(parent)
        ipWidget = self.builder.get_object("sinkIP")
        portWidget = self.builder.get_object("sinkPort")
        ip = ipWidget.get_text()
        port = portWidget.get_text()
        print(ip, port)

        # check ip
        import socket
        try:
            if ip != "localhost":
                socket.inet_aton(ip)
            # legal
            print('legal ip')
        except socket.error:
            # Not legal
            print('invalid ip')
            return

        # check port

        try:
            intPort = int(port)
            if intPort < 0 or intPort > 65536:
                assert()
        except Exception as e:
            print('invalid port')
            return
        
        clientList = self.builder.get_object("clientList")

        row1 = Gtk.ListBoxRow()
        label1 = Gtk.Label(f"{ip}:{port}")
        row1.add(label1)

        clientList.add(row1)

        self.view._update()

       
        self.view.emit('button-addClient-clicked', int(self.channelNumber), ip, port)

        



    def cameraSourceSelected():
        pass

    def rtspSourceSelected():
        pass

    def testSourceSelected():
        pass

    def localSourceSelected():
        pass

    def captureSourceSelected():
        pass

    def youtubeSourceSelected():
        pass



class myView(Gtk.Window):
    __gsignals__ = {
        'button-addChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, ()),
        'button-startChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'button-stopChannel-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        'combobox-input-changed': (GObject.SignalFlags.RUN_FIRST, None, (int, str,)),
        'button-addClient-clicked': (GObject.SignalFlags.RUN_FIRST, None, (int, str, str,))
    }
    def __init__(self, **kw):
        super(myView, self).__init__(
            default_width=100, default_height=100, **kw)

        self._channels = {}
        self.channelNumber = 0
        

        self._inputs = ["none", "test-src", "local file", "DVB",
            "Screen Capture", "USB-Camera", "USB-Camera(Windows)", "youtube", "torrent",
            "UDP", "TCP", "RTSP", "Audio"]
        self._outputs = ["multi UDP sink"]

        # self._attributes = ["file path","ip","port","cameras","protocol","pattern","uri"]


        self.builder = Gtk.Builder()
        self.builder.add_from_file("main.glade")
        self.builder.connect_signals(Handler(self, self.channelNumber, self.builder))
  
        self.window = self.builder.get_object("window")



        self.channelsBox = self.builder.get_object("channelsBox")


    



        # self.setInputBox(self.builder)
        # self.setOutputBox(self.builder)


        '''
        #### list
        lst = self.builder.get_object("sinkList")

        row1 = Gtk.ListBoxRow()
        label1 = Gtk.Label("test-1")
        row1.add(label1)

        row2 = Gtk.ListBoxRow()
        label2 = Gtk.Label("test-2")
        row2.add(label2)

        row3 = Gtk.ListBoxRow()
        label3 = Gtk.Label("test-3")
        row3.add(label3)



        lst.add(row1)
        lst.add(row2)
        lst.add(row3)
        '''

        # window.show_all()
        self._update()


        # self._hideAttributes()


    def _update(self):
        self.window.show_all()

    def _getAttributes(self, channelNum):
        attributes = {}
        builder = self._channels[channelNum]["builder"]

        # source port
        sourcePort = builder.get_object("sourcePort")
        port = sourcePort.get_text()
        print(port)
        attributes["sourcePort"]=port

        # filePath
        filePath = builder.get_object("filePath")
        path = filePath.get_text()
        print(path)
        attributes["filePath"] = path

        # filePathDialog
        dialog = builder.get_object("filePathDialog")
        s = dialog.get_filename()
        print(s)
        attributes["dialogFilePath"]=s

        # selected camera
        cameraList = builder.get_object("cameraList")
        camera = cameraList.get_active_text()
        print(f"camera {camera}")
        attributes['device-index']=camera



        return attributes

    def _hideAttributes(self, builder):

        cameraList = builder.get_object("cameraList")
        sourcePort = builder.get_object("sourcePort")
        filePath = builder.get_object("filePath")

        cameraList.hide()
        sourcePort.hide()
        filePath.hide()

    ### input
    def setInputBox(self, builder):
        combobox = builder.get_object("inputBox")
        for i in range(len(self._inputs)):
            combobox.append(None,str(self._inputs[i]))

    def setOutputBox(self, builder):
        combobox = builder.get_object("outputBox")
        for i in range(len(self._outputs)):
            combobox.append(None,str(self._outputs[i]))




    # add a new gst channel
    def _addVideoView(self, channelNum):
        tBuilder = Gtk.Builder()
        tBuilder.add_from_file("channelView.glade")
        
        # self.channelNumber += 1
        
        tBuilder.connect_signals(Handler(self, channelNum, tBuilder))

        tChannelBox = tBuilder.get_object("channelBox")
        # remove from old container TODO fix
        tChannelsBox = tBuilder.get_object("window")
        tChannelsBox.remove(tChannelBox)

        video_box = tBuilder.get_object("videoBox")

        self._channels[channelNum] = {
            'video_box': video_box,
            'builder': tBuilder
        }

        self.channelsBox.add(tChannelBox)

        self.setInputBox(tBuilder)
        self.setOutputBox(tBuilder)

        # hide attributes
        # tPort = tBuilder.get_object("sourcePort")
        # tPort.hide()
        self._hideAttributes(tBuilder)


        # Gtk.main()

        # print(lst.get_selected_row())

    def _setVideoView(self,gtksink, channelNum):
        video_box = self._channels.get(channelNum)['video_box']
        children = video_box.get_children ()
        for element in children:
            video_box.remove (element)

        video_widget = gtksink.get_property("widget")
        video_widget.set_size_request(200, 200)
        video_box.add(video_widget)
        # self._update()
        video_box.show_all()

        # hide attributes
        tBuilder = self._channels[channelNum]["builder"]
        self._hideAttributes(tBuilder)
