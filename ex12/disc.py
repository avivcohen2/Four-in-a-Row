class Disc:
    """class for Disc type objects, has location an color as attributes."""

    def __init__(self, color, location):
        self.__location = location
        self.__color = color

    def get_location(self):
        """returns the location of the disc"""
        return self.__location

    def get_color(self):
        """returns the color of the disc"""
        return self.__color

    def move_disc(self, new_loc):
        """moves disc to the new given location"""
        self.__location = new_loc
