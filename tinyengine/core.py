import pygame
from pygame.locals import *
import engine


class Core():
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


class Transform():
    def __init__(self):
        self.position = Vector().zero
        self.rotation = Vector().zero
        self.scale = Vector().zero


class Vector():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def zero(self):
        return Vector(0, 0)


class RGB():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @property
    def black(self):
        return (0, 0, 0)

    @property
    def white(self):
        return (255, 255, 255)

    @property
    def red(self):
        return (255, 0, 0)

    @property
    def green(self):
        return (0, 255, 0)

    @property
    def blue(self):
        return (0, 0, 255)


class Square():
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


class Sprite():
    def __init__(self):
        self.sprite = None

    def __str__(self):
        return 'sprite'


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