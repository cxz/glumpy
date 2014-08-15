# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import sys
from glumpy import gl
from glumpy.log import log
from glumpy.app.window import key
from glumpy.app.window import mouse
from glumpy.app import configuration
from glumpy.app.window.viewport import Viewport


class Window(Viewport):
    """
    Platform independent window.

    The content area of a window is filled entirely with an OpenGL viewport.
    Applications have no access to operating system widgets or controls; all
    rendering must be done via OpenGL.

    Windows may appear as floating regions or can be set to fill an entire
    screen (fullscreen).  When floating, windows may appear borderless or
    decorated with a platform-specific frame (including, for example, the
    title bar, minimize and close buttons, resize handles, and so on).

    While it is possible to set the location of a window, it is recommended
    that applications allow the platform to place it according to local
    conventions.  This will ensure it is not obscured by other windows,
    and appears on an appropriate screen for the user.

    It is the responsability of the window backend to dispatch the following
    events when necessary:

    Keyboard::

      def on_key_press(symbol, modifiers):
          'A key on the keyboard was pressed.'
          pass

      def on_key_release(symbol, modifiers):
          'A key on the keyboard was released.'
          pass

      def on_character(text):
          'A character has been typed'
          pass

    Mouse::

      def on_mouse_press(self, x, y, button):
          'A mouse button was pressed.'
          pass

      def on_mouse_release(self, x, y, button):
          'A mouse button was released.'
          pass

      def on_mouse_motion(x, y, dx, dy):
          'The mouse was moved with no buttons held down.'
          pass

      def on_mouse_drag(x, y, dx, dy, buttons):
          'The mouse was moved with some buttons pressed.'
          pass

      def on_mouse_scroll(self, dx, dy):
          'The mouse wheel was scrolled by (dx,dy).'
          pass


    Window::

      def on_init(self):
          'The window has just initialized iself.'
          pass

      def on_show(self):
          'The window was shown.'
          pass

      def on_hide(self):
          'The window was hidden.'
          pass

      def on_close(self):
          'The user closed the window.'
          pass

      def on_resize(self, width, height):
          'The window was resized to (width,height)'
          pass

      def on_draw(self, dt):
          'The window contents must be redrawn.'
          pass

      def on_idle(self, dt):
          'The window is inactive.'
          pass
    """

    def __init__(self, width=256, height=256, title=None, visible=True, aspect=None,
                 decoration=True, fullscreen=False, config=None, context=None, color=(0,0,0,1)):
        """
        Create a window.

        Parameters
        ----------

        width: int
            Window initial width

        height: int
            Window initial height

        title: int
            Window title

        visible: bool
            Window initial visibility status

        decoration: bool
            Window decoration (close button, maximize button, etc.)

        fullscreen: bool
            Window initial fullscreen mode

        config: Configuration
            GL Configuration

        context: Window
            Another window to share GL context with
        """

        Viewport.__init__(self, size=(width,height), aspect=aspect)
        self._mouse_x = 0
        self._mouse_y = 0
        self._button = mouse.NONE
        self._x = 0
        self._y = 0
        self._width = width
        self._height = height
        self._title = title or sys.argv[0]
        self._visible = visible
        self._fullscreen = fullscreen
        self._decoration = decoration
        self._clock = None
        self._timer_stack = []
        self._timer_date = []
        self._backend = None
        self.color = color

        self._clearflags = gl.GL_COLOR_BUFFER_BIT
        if config._depth_size:
            self._clearflags |= gl.GL_DEPTH_BUFFER_BIT
        if config._stencil_size:
            self._clearflags |= gl.GL_STENCIL_BUFFER_BIT


    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def fps(self):
        return self._clock.get_fps()

    @property
    def config(self):
        return self._config

    def clear(self):
        """ Clear the whole window """

        gl.glClearColor(*self.color)
        gl.glClear(self._clearflags)

    def show(self):
        """ Make the window visible """
        log.warn('%s backend cannot show window' % self._backend.name())

    def hide(self):
        """ Hide the window """
        log.warn('%s backend cannot hide window' % self._backend.name())

    def close(self):
        """ Close (destroy) the window """
        log.warn('%s backend cannot close window' % self._backend.name())

    def set_title(self, title):
        """ Set window title """
        log.warn('%s backend cannot set window title' % self._backend.name())

    def get_title(self):
        """ Get window title """
        log.warn('%s backend cannot get window title' % self._backend.name())

    def set_size(self, width, height):
        """ Set window size """
        log.warn('%s backend cannot set window size' % self._backend.name())

    def get_size(self):
        """ Get window size """
        log.warn('%s backend cannot get window size' %  self._backend.name())

    def set_position(self, x, y):
        """ Set window position """
        log.warn('%s backend cannot set window position' %  self._backend.name())

    def get_position(self):
        """ Get window position """
        log.warn('%s backend cannot get position' %  self._backend.name())

    def set_fullscreen(self, fullsrceen):
        """ Set window fullscreen mode """
        log.warn('%s backend cannot set fullscreen mode' % self._backend.name())

    def get_fullscreen(self):
        """ Get window fullscreen mode """
        log.warn('%s backend cannot get fullscreen mode' % self._backend.name())

    def swap(self):
        """ Swap GL buffers """
        log.warn('%s backend cannot swap buffers' % self._backend.name())

    def activate(self):
        """ Activate window """
        log.warn('%s backend cannot make window active' % self._backend.name())

    def timer(self, delay):
        """Function decorator for timed handlers.

        :Parameters:

            ``delay``: int
                Delay in second

        Usage::

            window = window.Window()

            @window.timer(0.1)
            def timer(dt):
                do_something ...
        """

        def decorator(func):
            self._timer_stack.append((func, delay))
            self._timer_date.append(0)
            return func
        return decorator