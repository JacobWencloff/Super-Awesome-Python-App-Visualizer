import random
import pygame
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw 
from array import array

from UI.a_star import *



# from UI.a_star import *




#----Main UI Class(top tool bar)-----

class UI():
    def __init__(self, window):
        self.window = window
        # self.quick_sort = quick_sort(window)
        self.editor = Editor(window)
        self.histogram = Histo_Graph(window, self.editor.data_size, self.editor.range_top, self.editor.range_bot)
        self.quick_sort = Quick_Sort(window, self.editor.data_size, self.editor.range_top, self.editor.range_bot)
        self.a_star = A_start_helper(window)
        self.speed25_enable = False
        self.speed50_enable = False
        self.speed75_enable = False
        self.speed1_enable = True
        self.algo_to_display = None
        self.did_edit_submit = False


        
    def draw(self, dt):

        if self.speed25_enable:
            self.histogram.play_speed = .1
            # print(self.histogram.play_speed)
        if self.speed50_enable:
            self.histogram.play_speed = .05
            # print(self.histogram.play_speed)
        if self.speed75_enable:
            self.histogram.play_speed = .025
            # print(self.histogram.play_speed)
        if self.speed1_enable:
            self.histogram.play_speed = .0001
            # print(self.histogram.play_speed)



        window_size = self.window.get_size()
        imgui.set_next_window_position(0,0)
        imgui.set_next_window_size(window_size[0], 200)

        imgui.begin('Control Panel', False)
        curr_size = imgui.core.get_window_size()
        imgui.begin_child('Open Editor', height=100,width=100,border=False)

        
        if imgui.button('Play >'):
            if self.algo_to_display == "Merge":
                self.histogram.__init__(self.window, self.editor.data_size, self.editor.range_top, self.editor.range_bot)
                self.histogram.start = True
            if self.algo_to_display == "Quick":
                self.quick_sort.start = True

        if imgui.button("Reset") or self.did_edit_submit:

            if self.algo_to_display == "Merge":
                self.histogram.start = False
                self.histogram.__init__(self.window, self.editor.data_size, self.editor.range_top, self.editor.range_bot)
                self.histogram.data_size = self.editor.data_size
                self.histogram.range_top = self.editor.range_top
                self.histogram.range_bot = self.editor.range_bot
                self.histogram.build_stater()

            if self.algo_to_display == "Quick":
                self.quick_sort.start = False
                self.quick_sort.__init__(self.window, self.editor.data_size, self.editor.range_top, self.editor.range_bot)
                self.quick_sort.data_size = self.editor.data_size
                self.quick_sort.range_top = self.editor.range_top
                self.quick_sort.range_bot = self.editor.range_bot
                self.quick_sort.build_starter()
        

        if imgui.button('Select Algo'):
            imgui.open_popup('Algo-Popup')

        imgui.same_line()

        if imgui.begin_popup('Algo-Popup'):
            if imgui.button("Merge-Sort"):
                self.algo_to_display = "Merge"
                imgui.close_current_popup()
            if imgui.button("Quick-Sort"):
                self.algo_to_display = "Quick"
                imgui.close_current_popup()
            if imgui.button("A*"):
                self.algo_to_display = "a_star"
            imgui.end_popup()

        imgui.end_child()
        imgui.same_line()
        imgui.begin_child("Set Speed")
        _ , self.speed25_enable =  imgui.checkbox("Slow", self.speed25_enable)
        _ , self.speed50_enable =  imgui.checkbox("Kinda slow", self.speed50_enable)
        _ , self.speed75_enable =  imgui.checkbox("kinda fast", self.speed75_enable)
        _ , self.speed1_enable =  imgui.checkbox("MEGA FAST", self.speed1_enable)
        imgui.end_child()
        imgui.end()

        imgui.set_next_window_position(0, curr_size[1])
        imgui.set_next_window_size(300, window_size[1]-curr_size[1])
        self.editor.draw()

        if self.algo_to_display == 'Merge':
            imgui.set_next_window_size(window_size[0]-300, window_size[1]-curr_size[1])
            imgui.set_next_window_position(300, curr_size[1])
            self.histogram.draw(dt)

        if self.algo_to_display == "Quick":
            imgui.set_next_window_size(window_size[0]-300, window_size[1]-curr_size[1])
            imgui.set_next_window_position(300, curr_size[1])
            self.quick_sort.draw(dt)

        if self.algo_to_display == 'a_star':
            imgui.set_next_window_size(window_size[0]-300, window_size[1]-curr_size[1])
            imgui.set_next_window_position(300, curr_size[1])
            self.a_star.draw()


class Editor():
    def __init__(self, window):
        self.window = window
        self.data_size = 100
        self.range_bot= 10
        self.range_top= 100
        self.x = 0
        self.y = 0
        self.z = 0
        self.x_check = False
        self.y_check = False
        self.z_check = False


    def draw(self):
        window_size = self.window.get_size()
        imgui.begin("Editor")

        imgui.push_id("0")
        imgui.text('Enter number of Data Points (INTs):')
        changed, self.z = imgui.input_int('', self.z)
        imgui.pop_id()

        imgui.push_id("1")
        imgui.text('Enter Value Range bottom')
        changed, self.y = imgui.input_int('', self.y)
        imgui.pop_id()

        imgui.push_id("2")
        imgui.text('Enter Value Range Top')
        changed, self.x = imgui.input_int('', self.x)
        imgui.pop_id()

        if imgui.button("submit"):
            self.update_vals(self.x, self.y, self.z)

        imgui.end()
        
    def update_vals(self, x, y, z):
        self.range_top = x
        self.range_bot = y
        self.data_size = z
        if self.x == 0:
            self.range_top = 100
        if self.y == 0:
            self.range_bot = 10
        if self.z == 0:
            self.data_size = 100
        
        print(self.x, self.y, self.z)


class Histo_Graph():
    def __init__(self, window, data_size, range_top, range_bot):
        self.window = window
        self.keys = []
        self.arr = []
        self.data_size = data_size
        self.range_top = range_top
        self.range_bot = range_bot
        self.build_stater()
        self.arr_copy = array("f", self.arr.copy())
        self.mergeSort(self.arr , 0, (len(self.arr) - 1))
        self.elapsed = 0
        self.cur_key_index = 0
        self.start = False
        self.play_speed = .000001


    def update_vals(self, r_top, r_bot, val_nums):
        self.range_top = r_top
        self.range_bot = r_bot
        self.data_size = val_nums


    def draw(self, dt):
        self.curr_size = imgui.core.get_window_size()
        window_size = self.window.get_size()
        # imgui.set_next_window_position(edit_x, gui_y) 
        # imgui.set_next_window_size(window_size[0]-300, window_size[1]-200)

        if self.start:
            if (self.cur_key_index < len(self.keys)) and (self.elapsed > self.play_speed):
                key = self.keys[self.cur_key_index ]
                self.arr_copy[key[0]] = key[1]
                self.cur_key_index = self.cur_key_index + 1
                self.arr_copy[key[0]] = key[1]
                self.elapsed = 0
            else:
                self.elapsed = self.elapsed + dt

        imgui.begin("Merge Sort", flags = imgui.WINDOW_NO_TITLE_BAR)

        imgui.plot_histogram(
        "",
        self.arr_copy,
        overlay_text="Merge Sort",
        # offset by one item every milisecond, plot values
        # buffer its end wraps around
        graph_size=(window_size[0]-320, window_size[1]-230),
     )
        
        imgui.end()
    

    def merge(self, arr, start, mid, end):
        start2 = mid + 1
        # If the direct merge is already sorted
        if (arr[mid] <= arr[start2]):
            return
        # Two pointers to maintain start
        # of both arrays to merge
        while (start <= mid and start2 <= end):  
            # If element 1 is in right place
            if (arr[start] <= arr[start2]):
                start += 1
            else:
                value = arr[start2]
                index = start2
                # Shift all the elements between element 1
                # element 2, right by 1.
                while (index != start):
                    arr[index] = arr[index - 1]
                    self.keys.append([index, arr[index-1]])
                    index -= 1

                arr[start] = value
                self.keys.append([index, value])
                # Update all the pointers
                start += 1
                mid += 1
                start2 += 1

        
    def mergeSort(self, arr, l, r):
        if (l < r):
            m = l + (r - l) // 2

            self.mergeSort(arr, l, m)
            self.mergeSort(arr, m + 1, r)
    
            self.merge(arr, l, m, r)

    def build_stater(self):
        print(self.data_size)
        for i in range(0, self.data_size):
            self.arr.append(random.randint(self.range_bot, self.range_top))



# ---- Quick Sort -----

class Quick_Sort():
    def __init__(self, window, data_size, range_top, range_bot):
        self.window = window
        self.data_size = data_size
        self.range_top = range_top
        self.range_bot = range_bot
        self.keys = []
        self.arr = []
        self.build_starter()
        self.arr_copy = array("f", self.arr.copy())
        self.quicksort(0, len(self.arr)-1, self.arr)
        self.elapsed = 0
        self.cur_key_index = 0
        self.start = False
        self.play_speed = .000001

    def draw(self, dt):
        self.curr_size = imgui.core.get_window_size()
        window_size = self.window.get_size()


        if self.start:
            if (self.cur_key_index < len(self.keys)) and (self.elapsed > self.play_speed):
                key = self.keys[self.cur_key_index ]
                self.arr_copy[key[0]] = key[1]
                self.elapsed = 0
                self.cur_key_index = self.cur_key_index + 1
            else:
                self.elapsed = self.elapsed + dt

        imgui.begin("Plot example", flags = imgui.WINDOW_NO_TITLE_BAR)

        imgui.plot_histogram(
        "",
        self.arr_copy,
        overlay_text="Quick Sort",

        graph_size=(window_size[0]-320, window_size[1]-230),
     )
        imgui.end()

    def partition(self, l, r, nums):

        pivot, ptr = nums[r], l
        for i in range(l, r):
            if nums[i] <= pivot:

                self.keys.append([i,nums[ptr]])
                self.keys.append([ptr, nums[i]])
                nums[i], nums[ptr] = nums[ptr], nums[i]
                ptr += 1

        self.keys.append([ptr, nums[r]])
        self.keys.append([r, nums[ptr]])
        nums[ptr], nums[r] = nums[r], nums[ptr]
        return ptr
 

    
    
    def quicksort(self, l, r, nums):
        if len(nums) == 1:  
            return nums
        if l < r:
            pi = self.partition(l, r, nums)
            self.quicksort(l, pi-1, nums)  
            self.quicksort(pi+1, r, nums) 
          
        return nums

    def build_starter(self):
        
        for i in range(0, self.data_size):
            self.arr.append(random.randint(self.range_bot,self.range_top))


class A_start_helper():
    def __init__(self, window) -> None:
        self
        self.window = window
        self.a_star = a_star_build()
    def draw(self):
        curr_size = imgui.core.get_window_size()
        window_size = self.window.get_size()
        
        WIDTH = int(window_size[1]-curr_size[1]    )      
        WIN = pygame.display.set_mode((WIDTH,WIDTH))

        imgui.begin("A*", flags= imgui.WINDOW_NO_TITLE_BAR)

        self.a_star.main(WIN, WIDTH)

        imgui.end()
