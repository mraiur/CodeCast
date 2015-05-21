import sublime, sublime_plugin
  
class EventDump(sublime_plugin.EventListener):
    def onLoad(self, view):
        print("just got loaded")

    def onPreSave(self, view): 
        print("is about to be saved"  )
  
    def onPostSave(self, view):  
        print("just got saved"  )
          
    def onNew(self, view):  
        print("new file"  )

    def on_selection_modified(self, view):
        print("DADA")
  
    def onSelectionModified(self, view):  
        print("modified a")

    def onSelectionModifiedAsync(self, view):
        print("async modified")
  
    def onActivated(self, view):  
        print("is now the active view")
  
    def onClose(self, view):  
        print("is no more"  )
  
    def onClone(self, view):  
        print("just got cloned" )