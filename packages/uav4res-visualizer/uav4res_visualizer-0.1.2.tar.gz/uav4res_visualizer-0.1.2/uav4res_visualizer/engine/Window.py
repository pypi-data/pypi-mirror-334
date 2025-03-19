import pygame


class Window:
    def __init__(self, width, height, FPS):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.FPS = FPS
        self.background_image = None

    def set_background_image(self, img_path):
        self.background_image = pygame.image.load(img_path)
        self.background_image = pygame.transform.scale(
            self.background_image, (self.width, self.height)
        )

    def draw_background_image(self):
        if not self.background_image is None:
            self.screen.blit(self.background_image, (0, 0))

    def draw_image(self, texture, position, scale=None, rotation=0):
        """
        Draw an image at a specific position on the screen.

        Args:
            img_path (str): Path to the image file.
            position (tuple): (x, y) position to draw the image.
            scale (tuple): (width, height) to resize the image (optional).
            rotation (float): Degrees to rotate the image (optional).
        """
        if scale is not None:
            texture = pygame.transform.scale(texture, scale)
        if rotation != 0:
            texture = pygame.transform.rotate(texture, rotation)
        self.screen.blit(texture, position)

    def draw_box_with_radius(self, color, rect, radius, border=0, border_color="black"):
        """
        Draw a box with rounded corners.

        Args:
            color (tuple): The color of the box as an (R, G, B) tuple.
            rect (tuple): The rectangle dimensions (x, y, width, height).
            radius (int): The corner radius in pixels.
            border (int): Width of the border (0 for no border).
            border_color (tuple): Border color as an (R, G, B) tuple (optional).
        """
        # Draw the main box
        pygame.draw.rect(self.screen, color, rect, border_radius=radius)

        # Draw the border if specified
        if border > 0 and border_color is not None:
            pygame.draw.rect(
                self.screen,
                border_color,
                rect,
                width=border,
                border_radius=radius,
            )

    def fill(self, color: pygame.Color):
        self.screen.fill(color)

    def handle_FPS(self):
        self.clock.tick(self.FPS)

    def getScreen(self):
        return self.screen
