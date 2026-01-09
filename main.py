import asyncio
import pygame as pg

from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:
    def __init__(self):
        pg.init()

        # Browser builds can be picky about grab/relative mouse.
        # Keep them best-effort.
        try:
            pg.mouse.set_visible(False)
        except Exception:
            pass

        self.screen = pg.display.set_mode(RES)

        try:
            pg.event.set_grab(True)
        except Exception:
            pass

        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)

        self.running = True
        self.new_game()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)

        # Music can fail in browser if autoplay is blocked; don't crash.
        try:
            pg.mixer.music.play(-1)
        except Exception:
            pass

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()

        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)

        # Caption is harmless but some environments ignore it
        try:
            pg.display.set_caption(f"{self.clock.get_fps():.1f}")
        except Exception:
            pass

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

    def check_events(self):
        self.global_trigger = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False

            elif event.type == self.global_event:
                self.global_trigger = True

            # keep your existing fire logic
            self.player.single_fire_event(event)

    def shutdown(self):
        # Best-practice quit path (works in desktop + browser)
        try:
            pg.quit()
        except Exception:
            pass


async def main():
    game = Game()

    while game.running:
        game.check_events()
        game.update()
        game.draw()

        # ✅ REQUIRED for pygbag/pygame in browser: yield to event loop each frame
        await asyncio.sleep(0)

    game.shutdown()


if __name__ == "__main__":
    asyncio.run(main())



if __name__ == '__main__':
    game = Game()
    game.run()
