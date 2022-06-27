import random
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw 
from array import array



#----Main UI Class(top tool bar)-----

class UI():
    def __init__(self, window):
        self.window = window
        # self.quick_sort = quick_sort(window)
        self.histogram = Histo_Graph(window)
        self.editor = Editor(window)
        self.quick_sort = Quick_Sort(window)
        self.speed25_enable = False
        self.speed50_enable = False
        self.speed75_enable = False
        self.speed1_enable = True
        self.algo_to_display = None


        
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

        window_size = glfw.get_window_size(self.window)
        imgui.set_next_window_position(0,0)
        imgui.set_next_window_size(window_size[0], 200)

        imgui.begin('Control Panel', False)
        curr_size = imgui.core.get_window_size()
        imgui.begin_child('Open Editor', height=100,width=100,border=False)

        if imgui.button('Play >'):
            if self.algo_to_display == "Merge":
                self.histogram.start = True
            if self.algo_to_display == "Quick":
                self.quick_sort.start = True

        if imgui.button("Reset"):
            self.histogram.start = False
            self.histogram.__init__(self.window, self.editor.data_size, self.editor.range_top, self.editor.range_bot)
            
            if self.histogram.data_size != '':
                self.histogram.data_size = self.editor.data_size
            if self.histogram.range_top != '': 
                self.histogram.range_top = self.editor.range_top
            if self.histogram.range_bot != '':
                self.histogram.range_bot = self.editor.range_bot
            self.histogram.build_stater()

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
            imgui.end_popup()

        imgui.end_child()
        imgui.same_line()
        imgui.begin_child("Set Speed")
        _ , self.speed25_enable =  imgui.checkbox("Speed 25%", self.speed25_enable)
        _ , self.speed50_enable =  imgui.checkbox("Speed 50%", self.speed50_enable)
        _ , self.speed75_enable =  imgui.checkbox("Speed 75%", self.speed75_enable)
        _ , self.speed1_enable =  imgui.checkbox("Speed WINDE OPEN", self.speed1_enable)
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


class Editor():
    def __init__(self, window):
        self.window = window
        self.data_size = 100
        self.range_bot= 10
        self.range_top= 100
        self.x = 0
        self.y = 0
        self.z = 0


    def draw(self):
        window_size = glfw.get_window_size(self.window)
        imgui.begin("Editor")

        imgui.push_id("0")
        imgui.text('Enter number of Data Points (INTs):')
        changed, self.z = imgui.input_int('', self.data_size)
        imgui.pop_id()

        imgui.push_id("1")
        imgui.text('Enter Value Range bottom')
        changed, self.y = imgui.input_int('', self.range_bot)
        imgui.pop_id()

        imgui.push_id("2")
        imgui.text('Enter Value Range Top')
        changed, self.x = imgui.input_int('', self.range_top)
        imgui.pop_id()

        if imgui.button("submit"):
            self.update_vals(self.x, self.y, self.z)

        imgui.end()
        
    def update_vals(self, x, y, z):
        self.range_top = x
        self.range_bot = y
        self.data_size = z
        print(self.x, self.y, self.z)


class Histo_Graph():
    def __init__(self, window, data_size=100, range_top=100, range_bot=10):
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
        window_size = glfw.get_window_size(self.window)
        # imgui.set_next_window_position(edit_x, gui_y) 
        # imgui.set_next_window_size(window_size[0]-300, window_size[1]-200)

        if self.start:
            if (self.cur_key_index < len(self.keys)) and (self.elapsed > self.play_speed):
                key = self.keys[self.cur_key_index ]
                self.arr_copy[key[0]] = key[1]
                self.elapsed = 0
                self.cur_key_index = self.cur_key_index + 1
            else:
                self.elapsed = self.elapsed + dt
        # flags = imgui.WINDOW_NO_TITLE_BAR = 1

        imgui.begin("Plot example", flags = imgui.WINDOW_NO_TITLE_BAR)

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
            self.arr.append(random.randint(10, 100))



# ---- Quick Sort -----

class Quick_Sort():
    def __init__(self, window, data_size = 100):
        self.window = window
        self.data_size = data_size
        self.arr = []
        self.arr_copy = array('f', self.arr.copy())
        self.build_starter()



    def draw(self, dt):
        self.curr_size = imgui.core.get_window_size()
        window_size = glfw.get_window_size(self.window)
        imgui.begin("Plot example", flags = imgui.WINDOW_NO_TITLE_BAR)

        imgui.plot_histogram(
        "",
        self.arr_copy,
        overlay_text="Quick Sort",
        # offset by one item every milisecond, plot values
        # buffer its end wraps around
        graph_size=(window_size[0]-320, window_size[1]-230),
     )
        imgui.end()

    def partition(self, l, r, nums):
    # Last element will be the pivot and the first element the pointer
        pivot, ptr = nums[r], l
        for i in range(l, r):
            if nums[i] <= pivot:
                # Swapping values smaller than the pivot to the front
                nums[i], nums[ptr] = nums[ptr], nums[i]
                ptr += 1
        # Finally swapping the last element with the pointer indexed number
        nums[ptr], nums[r] = nums[r], nums[ptr]
        return ptr
 
    # With quicksort() function, we will be utilizing the above code to obtain the pointer
    # at which the left values are all smaller than the number at pointer index and vice versa
    # for the right values.
    
    
    def quicksort(self, l, r, nums):
        if len(nums) == 1:  # Terminating Condition for recursion. VERY IMPORTANT!
            return nums
        if l < r:
            pi = self.partition(l, r, nums)
            self.quicksort(l, pi-1, nums)  # Recursively sorting the left values
            self.quicksort(pi+1, r, nums)  # Recursively sorting the right values
        return nums

    def build_starter(self):
        for i in range(self.data_size):
            self.arr.append(random.randint(10,100))
    
    # example = [4, 5, 1, 2, 3]
    # result = [1, 2, 3, 4, 5]
    # print(quicksort(0, len(example)-1, example))
    
    # example = [2, 5, 6, 1, 4, 6, 2, 4, 7, 8]
    # result = [1, 2, 2, 4, 4, 5, 6, 6, 7, 8]
    # # As you can see, it works for duplicates too
    # print(quicksort(0, len(example)-1, example))

        