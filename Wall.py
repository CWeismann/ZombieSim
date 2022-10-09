import constants
import arcade

class Wall(arcade.Sprite):
    def __init__(self, image, scale, left, top):
        """
        Initializes a new Wall sprite
        Inputs: the starting sprite image, the scaling of the screen,
                the x coordinate of the left of the sprite, and the y
                coordinate of the top of the sprite
        """
        super().__init__(image, scale)
        self.left = left
        self.top = top

        self.vert_texture = arcade.load_texture("images/vert.png")
        self.horiz_texture = arcade.load_texture("images/horiz.png")
        self.vert_door_texture = arcade.load_texture("images/dashVert.png")
        self.horiz_door_texture = arcade.load_texture("images/dashHoriz.png")
        if image == "images/vert.png":
            self.texture = self.vert_texture
        elif image == "images/horiz.png":
            self.texture = self.horiz_texture
        elif image == "images/dashVert.png":
            self.texture = self.vert_door_texture
        elif image == "images/dashHoriz.png":
            self.texture = self.horiz_door_texture

    def get_texture(self):
        if self.texture == self.vert_texture:
            return "vert"
        elif self.texture == self.horiz_texture:
            return "horiz"
        elif self.texture == self.vert_door_texture:
            return "vert_door"
        elif self.texture == self.horiz_door_texture:
            return "horiz_door"

    def lock_door(self):
        if self.get_texture() == "vert_door":
            self.texture = self.vert_texture
        elif self.get_texture() == "horiz_door":
            self.texture = self.horiz_texture