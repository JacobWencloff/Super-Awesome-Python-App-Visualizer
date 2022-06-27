from multiprocessing.spawn import import_main_path
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
from UI.ui import *


def main():
    imgui.create_context()
    window = glfw_init()
    impl = GlfwRenderer(window)
    last_frame_time = glfw.get_time()
    nav = UI(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        impl.process_inputs()
        now = glfw.get_time()
        dt = now - last_frame_time
        last_frame_time = now

        imgui.new_frame()
        #UI is here

        # ui()
        nav.draw(dt)



        gl.glClearColor(.3, .3, .3, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown()
    glfw.terminate()


def glfw_init():
    if not glfw.init():
        print('Could not initialize OpenGl context')
        exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    monitor = glfw.get_primary_monitor()

    video_mode = glfw.get_video_mode(monitor)

    width, height = video_mode.size.width, video_mode.size.height
    window_name = 'test'
    
    window = glfw.create_window(
        int(width) , int(height), window_name, monitor, None 
    )
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print('Could not initialize')
        exit(1)

    return window



if __name__ == "__main__":
    main()