import math
import pygame as pg
from pygame.math import Vector2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 0, 0)


class Player(pg.sprite.Sprite):

    def __init__(self, pos=(420, 420)):
        super(Player, self).__init__()
        self.image = pg.Surface((50, 50), pg.SRCALPHA)
        pg.draw.circle(self.image, BLUE, (25, 25), 25)
        pg.draw.circle(self.image, WHITE, (50, 25), 10)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.position = Vector2(pos)
        self.direction = Vector2(1, 0)  # A unit vector pointing rightward.
        self.speed = 10
        self.angle_speed = 0
        self.angle = 0
        self.points_at = None
        self.picked = None

    def update(self):
        if self.angle_speed != 0:
            # Rotate the direction vector and then the image.
            self.direction.rotate_ip(self.angle_speed)
            self.angle += self.angle_speed
            self.image = pg.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
        # Update the position vector and the rect.
        self.position += self.direction * self.speed
        self.rect.center = self.position
        # print(self.direction)

        block_hit_list = pg.sprite.spritecollide(self, self.walls, False)
        if block_hit_list:
            # print(block_hit_list)
            self.position -= self.direction * self.speed
            self.rect.center = self.position

        self.check_direction()

    def check_direction(self):
        self.position += self.direction * 10
        self.rect.center = self.position

        thing_hit_list = pg.sprite.spritecollide(self, self.things, False)
        for thing in thing_hit_list:
            self.points_at = thing
        if not thing_hit_list:
            self.points_at = None

        self.position -= self.direction * 10
        self.rect.center = self.position

    def move(self, top, left):
        self.speed = top * 4
        self.angle_speed = left * 3

    def pick_up(self):
        self.picked = self.points_at
        self.points_at.remove(self.things)
        self.points_at = None

    def drop(self):
        self.picked.rect.center = self.position + self.direction * 20
        self.things.add(self.picked)
        self.picked = None


class Wall(pg.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super(Wall, self).__init__()

        # Make a blue wall, of the size specified in the parameters
        self.image = pg.Surface([width, height])
        self.image.fill(BLACK)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Thing(pg.sprite.Sprite):
    """ Thing the player can pick up and drop. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super(Thing, self).__init__()

        # Make a blue wall, of the size specified in the parameters
        self.image = pg.Surface([width, height])
        # self.image.fill(BLACK)
        pg.draw.circle(self.image, RED, (width // 2, height // 2), min((width, height)) // 2)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


def main():
    pg.init()
    screen = pg.display.set_mode((1280, 720))

    player = Player((420, 420))
    playersprite = pg.sprite.RenderPlain((player))

    # wall setup
    wall_list = pg.sprite.Group()
    wall_top = Wall(0, 0, 1280, 20)
    wall_list.add(wall_top)
    wall_left = Wall(0, 0, 20, 720)
    wall_list.add(wall_left)
    wall_bottom = Wall(0, 700, 1280, 20)
    wall_list.add(wall_bottom)
    wall_right = Wall(1260, 0, 20, 720)
    wall_list.add(wall_right)
    player.walls = wall_list

    things = pg.sprite.Group()
    first_thing = Thing(500, 500, 25, 25)
    things.add(first_thing)
    player.things = things

    top = 0
    left = 0

    clock = pg.time.Clock()
    done = False
    while not done:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    top = 1
                elif event.key == pg.K_DOWN:
                    top = -1
                elif event.key == pg.K_LEFT:
                    left = -1
                elif event.key == pg.K_RIGHT:
                    left = 1
                elif event.key == pg.K_SPACE:
                    if player.points_at:
                        print('picking up %s' % player.points_at)
                        player.pick_up()
                    elif player.picked:
                        print('dropping %s' % player.picked)
                        player.drop()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    top = 0
                elif event.key == pg.K_DOWN:
                    top = 0
                elif event.key == pg.K_LEFT:
                    left = 0
                elif event.key == pg.K_RIGHT:
                    left = 0
                elif event.key == pg.K_SPACE:
                    pass
        player.move(top, left)
        playersprite.update()

        # print(player.points_at)

        screen.fill((30, 30, 30))
        playersprite.draw(screen)
        wall_list.draw(screen)
        things.draw(screen)
        pg.display.flip()

if __name__ == '__main__':
    main()
    pg.quit()
