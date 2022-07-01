from multiprocessing.spawn import import_main_path
# import glfw
import pygame
import OpenGL.GL as gl
import imgui
from imgui.integrations.pygame import PygameRenderer
import sys
from UI.ui import *


def main():
    pygame.init()
    display_info = pygame.display.Info()
    w, h = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode((w , h), pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN, 0, 0)
    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = (w, h)
    last_frame_time = pygame.time.get_ticks()
    nav = UI(screen)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            impl.process_event(event)

        imgui.new_frame()
        now = pygame.time.get_ticks()
        dt = (now - last_frame_time) / 1000
        last_frame_time = now

    #     imgui.new_frame()
    #     #UI is here

        # ui()
        nav.draw(dt)

        gl.glClearColor(.3, .3, .3, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        pygame.display.flip()

    # impl.shutdown()
    # glfw.terminate()


# def glfw_init():
#     if not glfw.init():
#         print('Could not initialize OpenGl context')
#         exit(1)

#     glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
#     glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
#     glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

#     glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

#     monitor = glfw.get_primary_monitor()

#     video_mode = glfw.get_video_mode(monitor)

#     width, height = video_mode.size.width, video_mode.size.height
#     window_name = 'test'
    
#     window = glfw.create_window(
#         int(width) , int(height), window_name, monitor, None 
#     )
#     glfw.make_context_current(window)

#     if not window:
#         glfw.terminate()
#         print('Could not initialize')
#         exit(1)

#     return window



if __name__ == "__main__":
    main()