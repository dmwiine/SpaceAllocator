from app.room import Room

class Office(Room):
    def __init__(self, name):
        Room.__init__(self, name)
        self.space_available = 6
        