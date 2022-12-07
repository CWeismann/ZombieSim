import arcade
import constants

class Item(arcade.Sprite):
    def __init__(self, image, scale, x, y):
        """
        Initializes a new Item sprite
        Inputs: the starting sprite image, and the scaling of the screen
        """
        super().__init__(image, scale)

        self.center_x = x
        self.center_y = y

        self.antidote_texture = arcade.load_texture("images/antidote.png")
        self.bicycle_texture = arcade.load_texture("images/bicycle.png")
        self.binoculars_texture = arcade.load_texture("images/binoculars.png")
        self.bullets_texture = arcade.load_texture("images/bullets.png")
        self.disguise_texture = arcade.load_texture("images/disguise.png")
        self.dog_texture = arcade.load_texture("images/dog.png")
        self.gun_texture = arcade.load_texture("images/gun.png")
        self.key_texture = arcade.load_texture("images/key.png")
        self.knife_texture = arcade.load_texture("images/knife.png")
        self.medpack_texture = arcade.load_texture("images/medpack.png")
        self.scanner_texture = arcade.load_texture("images/scanner.png")

    # Returns the current texture of the sprite
    def get_texture(self):
        if self.texture == self.antidote_texture:
            return "antidote"
        elif self.texture == self.bicycle_texture:
            return "bicycle"
        elif self.texture == self.binoculars_texture:
            return "binoculars"
        elif self.texture == self.bullets_texture:
            return "bullets"
        elif self.texture == self.gun_texture:
            return "gun"
        elif self.texture == self.key_texture:
            return "key"
        elif self.texture == self.knife_texture:
            return "knife"
        else:
            return "other"
