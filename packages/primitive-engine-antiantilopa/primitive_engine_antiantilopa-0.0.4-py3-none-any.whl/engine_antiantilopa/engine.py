from .game_object import GameObject, DEBUG
from .surface import SurfaceComponent
from .camera import Camera
from .transform import Transform
from .vmath_mini import Vector2d
import pygame as pg

class Engine:

    def __init__(self, window_size: Vector2d|tuple[int, int] = Vector2d(0, 0)):
        if not isinstance(window_size, Vector2d):
            window_size = Vector2d.from_tuple(window_size)
        pg.init()
        pg.font.init()
        screen = GameObject("main_screen")
        screen.add_component(Transform(Vector2d(0, 0)))
        screen.add_component(SurfaceComponent(window_size))
        screen.get_component(SurfaceComponent).pg_surf = pg.display.set_mode(screen.get_component(SurfaceComponent).pg_surf.get_size())
        GameObject.root = screen
        screen.add_child(Camera)

    def run(self):
        run = True
        while run:
            pg.time.delay(100)
            for event in pg.event.get(eventtype=pg.QUIT):
                if event.type == pg.QUIT:
                    run = False
            self.iteration()
            self.draw()
            pg.display.flip()
            for g_obj in GameObject.objs:
                g_obj.get_component(SurfaceComponent).pg_surf.fill((0, 0, 0, 0))



    def iteration(self):
        for g_obj in GameObject.objs:
            g_obj.iteration()

    def draw(self):
        for g_obj in GameObject.objs:
            g_obj.draw()
        def blit(g_obj: GameObject):
            for child in g_obj.childs:
                blit(child)
            if not (g_obj in GameObject.get_group_by_tag("Camera")):
                g_obj.get_component(SurfaceComponent).blit()
        blit(GameObject.root)
        GameObject.get_group_by_tag("Camera")[0].get_component(SurfaceComponent).blit()
    
    def update(self):
        for g_obj in GameObject.objs:
            g_obj.update()