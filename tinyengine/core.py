import pygame

import tinyengine.engine as engine


class Core:
    def __init__(self, name='NewGameObject'):
        self.name = name
        self.transform = Transform()
        self.components = dict()

    def __str__(self):
        return self.name

    def add_component(self, component):
        try:
            self.components[str(component)] = component
            print('component {}'.format(type(component)))
        except NameError as err:
            raise ValueError(err)

    def get_component(self, component):
        try:
            return self.components[str(component)]
        except NameError as err:
            raise ValueError(err)

    def update(self):
        for component in self.components.values():
            component.run(self)

    def start(self):
        pass


class Transform:
    def __init__(self):
        self.position = Vector().zero
        self.rotation = Vector().zero
        self.scale = Vector().zero

    def move(self, move_direction):
        self.position = Vector(move_direction[0], move_direction[1])


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    @property
    def position(self):
        return self.x, self.y

    @property
    def up(self):
        self.y -= 1
        return self.position

    @property
    def down(self):
        self.y += 1
        return self.position

    @property
    def right(self):
        self.x += 1
        return self.position

    @property
    def left(self):
        self.x -= 1
        return self.position

    @property
    def zero(self):
        self.x = 0
        self.y = 0
        return self.position


class RGB:
    def __init__(self, red=0, green=0, blue=0):
        red = 0 if red < 0 else red
        green = 0 if green < 0 else green
        blue = 0 if blue < 0 else blue

        self.red_palette = red
        self.green_palette = green
        self.blue_palette = blue

    def __str__(self):
        return f"RGB({self.red_palette}, {self.green_palette}, {self.blue_palette})"

    @property
    def value(self):
        return self.red_palette, self.green_palette, self.blue_palette

    @property
    def black(self):
        return 0, 0, 0

    @property
    def white(self):
        return 255, 255, 255

    @property
    def red(self):
        return 255, 0, 0

    @property
    def green(self):
        return 0, 255, 0

    @property
    def blue(self):
        return 0, 0, 255


class Square:
    def __init__(self, width, height, color=RGB().white):
        self.width = width
        self.height = height
        self.color = color

    def __str__(self):
        return 'square'

    def run(self, obj):
        pygame.draw.rect(engine.screen,
                         self.color,
                         pygame.Rect(obj.transform.position.x - self.width / 2,
                                     obj.transform.position.y - self.height / 2,
                                     self.width,
                                     self.height
                                     )
                         )


class Sprite:
    def __init__(self, sprite_path=None, size=1):
        self.sprite_path = f"../art/{sprite_path}"
        self.sprite = pygame.image.load(self.sprite_path)
        self.size = size
        self.sprite_scaled_width = round(self.sprite.get_rect().width * self.size)
        self.sprite_scaled_height = round(self.sprite.get_rect().height * self.size)
        self.scaled_sprite = pygame.transform.scale(
            self.sprite, (
                self.sprite_scaled_width,
                self.sprite_scaled_height
            )
        )

    def __str__(self):
        return 'sprite'

    def run(self, obj):
        engine.screen.blit(
            self.scaled_sprite,
            (obj.transform.position.x - round((self.sprite_scaled_width / 2)),
             obj.transform.position.y - round((self.sprite_scaled_height / 2)))
        )


class Input:
    def __init__(self):
        pass

    def get_key(key):
        for event in pygame.event.get():
            pass

        keys = pygame.key.get_pressed()

        if keys[engine.key_map[key]]:
            return True

    def get_key_down(key):
        for event in pygame.event.get(pygame.KEYDOWN):
            if pygame.key.get_pressed()[engine.key_map[key]]:
                return True

    def get_key_up(key):
        for event in pygame.event.get(pygame.KEYUP):
            if event.key == ord(key.lower()):
                return True


def update(f):
    def wrapper(*args):
        super(args[0].__class__, args[0]).update()
        return f(*args)

    return wrapper


def start(f):
    def wrapper(*args):
        super(args[0].__class__, args[0]).start()
        return f(*args)

    return wrapper
