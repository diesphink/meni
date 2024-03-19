from event_bus import EventBus

class Bus(EventBus):
    def __init__(self):
        super().__init__()

    def on_library_path_changed(self, func):
        self.add_event(func, "library_path_changed")
        
    def library_path_changed(self, value):
        self.emit("library_path_changed", value)