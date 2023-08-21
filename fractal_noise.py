from noise import pnoise1
import pyglet
from pyglet.gl import (glMatrixMode, glLoadIdentity, gluPerspective, glMatrixMode,
                       glViewport, glTranslatef, glBegin, glVertex3f, glEnd)
from pyglet.gl import (GL_PROJECTION, GL_MODELVIEW,  GL_LINE_STRIP)
from math import inf

class FractalNoiseGenerator(pyglet.window.Window):
    def __init__(self, midi_out_min=0, midi_out_max=127, points=256, span=5.0, speed=1.0, octaves=4, dt=1.0/30.0, debug_window=False):
        self._debug_window = debug_window
        self._midi_out_min = midi_out_min
        self._midi_out_max = midi_out_max
        self._points = points
        self._span = span
        self._speed = speed
        self._octaves = octaves
        self._base = 0
        self._max = -inf
        self._min = inf
        self._dt = dt
        self._track_min_max = False
        if self._debug_window:
            super().__init__(width=512, height=512,visible=False)
            self.on_draw = self.event(self.on_draw)
            self.on_resize = self._on_resize
            self.set_visible()
            self._run()

    def map_range(self, x):
        # @TODO: find better values via self._track_min_max, or calculate theoretically
        in_min = -0.79
        in_max = 0.79
        return (x - in_min) * (self._midi_out_max - self._midi_out_min) // (in_max - in_min) + self._midi_out_min
    
    def next_point(self, x):
        return pnoise1(x + self._base, self._octaves)

    def on_draw(self):
        self.clear()
        glLoadIdentity()
        glTranslatef(0, 0, -1)
        r = range(256)
        glBegin(GL_LINE_STRIP)
        for i in r:
            x = float(i) * self._span / self._points - 0.5 * self._span
            y = self.next_point(x)
            if self._track_min_max:
                if y > self._max:
                    self._max = y
                if y < self._min:
                    self._min = y
            glVertex3f(x * 2.0 / self._span, y, 0)
        # print(f"x: {self._base}")
        glEnd()
        if self._track_min_max:
            print(f"min: {self._min}, max: {self._max}")

    def _on_resize(self, width, height):
        """Setup 3D viewport"""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, 1.0*width/height, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def _update(self, dt):
        self._base += dt * self._speed
    
    def _run(self):
        if self._debug_window:
            pyglet.clock.schedule_interval(self._update, self._dt)
            # Uncomment to let pyglet run the event loop, graph makes more sense but blocks run.py
            # pyglet.app.run()
    
    def get_last_base(self):
        return self._base
    
    def return_next_point(self):
        next_point = self.next_point(255.0 * self._span / self._points - 0.5 * self._span)
        next_point = self.map_range(next_point)
        return int(next_point)

    def my_step(self):
        self._update(self._dt)
        if not self._debug_window:
            return
        pyglet.clock.tick(poll=True)
        # Just fuckin guessing here 
        # timeout = pyglet.app.event_loop.idle()
        # timeout = self._dt
        # pyglet.app.platform_event_loop.step(timeout)

        for window in pyglet.app.windows:
            window.switch_to()
            window.dispatch_events()
            window.dispatch_event('on_draw')
            window.flip()
        