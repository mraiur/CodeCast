import sublime, sublime_plugin, pickle, json, socket
HOST = "localhost"
PORT = 5005


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
  
class EventDump(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        
        sel = view.sel()
        region1 = sel[0]
        selectionText = view.substr(region1)

        '''a = dict( file=view.file_name(), selection = selectionText);'''
        a = {"file": view.file_name(), "selection" : selectionText}

        s.send(bytes(json.dumps(a), 'UTF-8'))
        print(a)
  
    def onSelectionModified(self, view):  
        print("modified a")

    def onSelectionModifiedAsync(self, view):
        print("async modified")
  
    def onActivated(self, view):  
        print("is now the active view")
  
    def onClose(self, view):  
        print("is no more"  )
