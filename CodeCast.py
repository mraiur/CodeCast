import sublime
import sublime_plugin
import pickle
import json
import socket

settings = sublime.load_settings("CodeCast.sublime-settings")

HOST = settings.get("SOCKET_SERVER_HOST", "localhost")
PORT = settings.get("SOCKET_SERVER_PORT", 5005)
AUTO_CONNECT = settings.get("AUTO_CONNECT", False)

sock = False;


class CodeCastConnectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.connect()

    def connect(self):
        global sock
        
        print('CodeCast Connecting... ', HOST, PORT)

        try:
            print('CodeCast Connected')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST, PORT))
        except Exception as e:
            sock = False;
            print("CodeCast no server")

class CodeCastDisconnectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.disconnect()

    def disconnect(self):
        global sock
        
        print('CodeCast disconnecting... ', HOST, PORT)

        if sock is not False:
            sock.close();
            sock = False;


if AUTO_CONNECT is True:
    o = CodeCastConnectCommand(sublime_plugin.TextCommand);
    o.connect();

class CodeCastCommand(sublime_plugin.EventListener):
    def msg(self, data):
        global sock

        if sock is not False:
            try:
                sock.send(bytes(json.dumps(data), 'UTF-8'))
            except Exception as e:
                sock = False

    def on_selection_modified(self, view):
        
        sel = view.sel()
        region1 = sel[0]
        selectionText = view.substr(region1)

        data = {
            "action": "select",
            "file": view.file_name(),
            "data" : selectionText,
            "selection": { 
                "start": sel[0].a,
                "end": sel[0].b
            }
        }
        self.msg(data)
        view.set_status('_filename', self.connectionInformation() )

    def on_modified(self, view):
        region = sublime.Region(0, view.size());

        data = {
            "action": "update",
            "file": view.file_name(),
            "data": view.substr(region)
        }
        self.msg(data)

    def connectionInformation(self):
        global sock, HOST, PORT
        if sock is False:
            return ""
        else:
            return "Connected to "+HOST+":"+str(PORT)
    
    def on_activated(self, view):  
        if view.file_name():
            fileHandler = open(view.file_name(), encoding='utf-8');
            contents = fileHandler.read();
            data = {"action": "changefile", "file": view.file_name(), "data": contents }
            self.msg(data)
  
    def onClose(self, view):  
        print("is no more"  )
