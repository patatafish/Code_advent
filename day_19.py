import tkinter as tk
import time
import random
from ddd_trig_rotations import *


class Root(tk.Tk):
    """
    overall class for visualization of data, using Tkinter library
    """

    def __init__(self):
        """
        self init package, establishes main window size, defines no resize, and calls main elements
        for rendering program:
        pack() items:
        fr_background - main background for window, creates size of window
        grid() items:
        fr_controls - background frame for buttons
        fr_display - background frame for data visualization
        place() items:
        fr_compass - background frame for compass orientation
        """
        super().__init__()
        self.resizable(False, False)
        # bind mouse motion to the window
        self.mouse_move_flag = False
        # initiate variables to track mouse movement over time
        self.prev_x, self.prev_y = None, None
        self.bind('<Motion>', self.mouse_move)
        self.bind('<Button-1>', self.mouse_move_start)
        self.bind('<ButtonRelease-1>', self.mouse_move_stop)
        # base frame for background
        self.fr_background = tk.Frame(self, bg='gray', border=0, height=1200, width=1800)
        self.fr_background.pack()
        # draw background for controls, display, and compass
        self.fr_controls = tk.Frame(self.fr_background,
                                    bg='red',
                                    relief=tk.RAISED,
                                    border=5,
                                    height=200, width=1790)
        self.fr_display = tk.Frame(self.fr_background,
                                   bg='blue',
                                   relief=tk.RAISED,
                                   border=5,
                                   height=980, width=1790)

        # set out frames
        self.fr_controls.grid(row=0, column=0, sticky='ew')
        self.fr_display.grid(row=1, column=0, sticky='ew')

        # initiate attributes and call function to initiate compass window
        # these params are the angle of rotations across all three axis, init as 0 deg
        self.x_orient, self.y_orient, self.z_orient = 0, 0, 0
        self.compass_square_size = None     # define size of canvas for compass
        self.compass_center_px = None       # define center x,y of canvas
        self.fr_compass = None              # define frame for compass
        self.cv_compass_art = None          # define canvas for compass
        self.init_compass()                 # call to initiate empty compass




    def mouse_move_start(self, event):
        self.mouse_move_flag = True
        self.prev_x = event.x
        self.prev_y = event.y

    def mouse_move(self, event):
        self.unbind('<Motion>')
        if self.mouse_move_flag is True:
            x, y = event.x, event.y
            if x > self.prev_x:
                self.z_orient -= 2
            elif x < self.prev_x:
                self.z_orient += 2
            if y > self.prev_y:
                self.y_orient -= 2
                self.x_orient += 2
            elif y < self.prev_y:
                self.y_orient += 2
                self.x_orient -= 2

            self.prev_x, self.prev_y = x, y
            self.draw_compass()
        self.bind('<Motion>', self.mouse_move)

    def mouse_move_stop(self, event):
        self.mouse_move_flag = False


    def init_compass(self):
        # define the size of the canvas, and find center mass
        self.compass_square_size = 220
        self.compass_center_px = self.compass_square_size / 2

        self.fr_compass = tk.Frame(self.fr_background,
                                   bg='light gray',
                                   relief=tk.RAISED,
                                   border=5,
                                   height=self.compass_square_size-5, width=self.compass_square_size-5)
        self.cv_compass_art = tk.Canvas(self.fr_compass,
                                        bg='white',
                                        height=self.compass_square_size, width=self.compass_square_size)

        self.fr_compass.place(x=50, y=925)
        self.cv_compass_art.pack()
        # initiate compass with 0 orientation
        self.draw_compass()

    def draw_compass(self):
        """
        draw_compass() creates the image to render in fr_compass to show orientations and then refreshes the canvas
        :return: None
        """

        # define end points for our three compass lines
        end_x = [90, 0, 0]
        label_x = [100, 0, 0]
        end_y = [0, -90, 0]
        label_y = [0, -100, 0]
        end_z = [0, 0, 90]
        label_z = [0, 0, 100]
        origin = [0, 0, 0]
        label_o = [0, 0, 0]
        # define lists to manipulate as we rotate compass
        point_list = [origin, end_x, end_y, end_z]
        label_list = [label_o, label_x, label_y, label_z]
        edge_list = [origin, end_x, end_y, end_z]

        # call all three functions for rotation maths, this uses the
        # params self.__orient from the parent definition
        point_list = rotate_around_z(self.x_orient, point_list)
        label_list = rotate_around_z(self.x_orient, label_list)
        point_list = rotate_around_x(self.y_orient, point_list)
        label_list = rotate_around_x(self.y_orient, label_list)
        point_list = rotate_around_y(self.z_orient, point_list)
        label_list = rotate_around_y(self.z_orient, label_list)

        # move the points to the center of our canvas
        for i in range(len(point_list)):
            for j in range(2):
                point_list[i][j] += self.compass_center_px
                label_list[i][j] += self.compass_center_px

        # clear previous contents of frame
        self.cv_compass_art.delete('all')
        # start with orienting circle
        self.cv_compass_art.create_oval(self.compass_center_px-20, self.compass_center_px-20,
                                        self.compass_center_px+20, self.compass_center_px+20,
                                        width=1)

        # create the depth-organized list for 3d-render
        # copy point list, so we don't alter OG list
        ddd_render_list = point_list[:]
        # sort the list from the farthest pt to closest (lowest z to highest)
        ddd_render_list.sort(key=lambda item: item[2])
        # find the origin point, this anchors all three triangles
        anchor_index = ddd_render_list.index(origin)
        # build list of triangle vertices for draw
        if anchor_index == 0:
            vertex_list = [[0, 1, 2], [0, 1, 3], [0, 2, 3]]
        elif anchor_index == 1:
            vertex_list = [[0, 1, 2], [0, 1, 3], [1, 2, 3]]
        elif anchor_index == 2:
            vertex_list = [[0, 1, 2], [0, 2, 3], [1, 2, 3]]
        else:
            vertex_list = [[0, 1, 3], [0, 2, 3], [1, 2, 3]]
        # print(f'3d: {ddd_render_list}, o at {anchor_index}')
        # draw triangles from furthest to closest,
        # as determined by sorted ddd_render_list and
        # subsequent vertex_list
        for triangle in vertex_list:
            # name each corner in the triangle
            corner_a = ddd_render_list[triangle[0]]
            corner_b = ddd_render_list[triangle[1]]
            corner_c = ddd_render_list[triangle[2]]
            # name triangle ABC
            this_triangle = [corner_a, corner_b, corner_c]
            # find color to use based on the hypotenuse between axis end points
            if end_z in this_triangle and end_x in this_triangle:
                color = 'light green'
            elif end_x in this_triangle and end_y in this_triangle:
                color = 'light blue'
            else:
                color = 'yellow'
            # draw the triangle
            self.cv_compass_art.create_polygon(corner_a[0], corner_a[1],
                                               corner_b[0], corner_b[1],
                                               corner_c[0], corner_c[1],
                                               outline='black', width=3, fill=color)

        # draw lines for compass 'see through' effect
        for from_edge in edge_list:
            for to_edge in edge_list:
                self.cv_compass_art.create_line(from_edge[0], from_edge[1],
                                                to_edge[0], to_edge[1],
                                                width=1, fill='black',
                                                dash=(4, 2))

        # draw end points for compass
        # determine which label we are drawing
        for i in range(4):
            # note the coordinates for the label from label_list and label_ pair
            this_node = label_list[i]
            if point_list[i] is end_x:
                label = 'x'
            elif point_list[i] is end_y:
                label = 'y'
            elif point_list[i] is end_z:
                label = 'z'
            else:
                # no label for origin point
                label = ''
            # we push the coordinates out from the triangle for readability
            self.cv_compass_art.create_text(this_node[0], this_node[1], text=label, fill='black')

        # refresh canvas with new image
        self.cv_compass_art.update()


if __name__ == '__main__':

    # call class to create window
    root = Root()
    # start mainloop
    root.mainloop()

    print('Exiting...')
