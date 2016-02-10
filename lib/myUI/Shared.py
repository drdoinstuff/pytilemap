
## UIShared #############################################################
class UIShared(object):

    window_manager = None
    
    focused_window = None
    focused_widget = None
    
    @classmethod
    def set_window_manager(self, obj):
        self.window_manager = obj   
        
    @classmethod
    def set_focused_window(self, obj):
        self.focused_window = obj
        
    @classmethod
    def set_focused_widget(self, widget):
        self.focused_widget = widget