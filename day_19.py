import tkinter as tk
import math
import time
import random


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
        self.x_orient, self.y_orient, self.z_orient = 0, 0, 0
        self.compass_square_size = None     # define size of canvas for compass
        self.compass_center_px = None       # define center x,y of canvas
        self.fr_compass = None              # define frame for compass
        self.cv_compass_art = None          # define canvas for compass
        self.init_compass()                 # call to initiate empty compass


        time.sleep(5)
        # test rotation
        while True:
            for i in range(0, random.randint(0, 150), 1):
                # time.sleep(.1)
                self.x_orient += 1
                self.draw_compass()
            for i in range(0, random.randint(0, 150), 1):
                # time.sleep(.1)
                self.y_orient += 1
                self.draw_compass()
            for i in range(0, random.randint(0, 150), 1):
                # time.sleep(.1)
                self.z_orient += 1
                self.draw_compass()


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
        draw_compass() creates the image to render in the fr_compass to show orientations
        :return: None
        """

        # define end points for our three compass lines
        end_x = [90, 0, 0]
        end_y = [0, -90, 0]
        end_z = [0, 0, 90]
        origin = [0, 0, 0]
        point_list = [origin, end_x, end_y, end_z]
        edge_list = [origin, end_x, end_y, end_z]

        # print(f'{self.x_orient},{self.y_orient},{self.z_orient}:::{end_x},{end_y},{end_z}')


        point_list = rotate_around_z(self.x_orient, point_list)
        # print(f':{self.x_orient},{self.y_orient},{self.z_orient}:::{end_x},{end_y},{end_z}')
        point_list = rotate_around_x(self.y_orient, point_list)
        # print(f'::{self.x_orient},{self.y_orient},{self.z_orient}:::{end_x},{end_y},{end_z}')
        point_list = rotate_around_y(self.z_orient, point_list)
        # print(f':::{self.x_orient},{self.y_orient},{self.z_orient}:::{end_x},{end_y},{end_z}')

        # move the points to the center of our canvas
        for i in range(len(point_list)):
            for j in range(2):
                point_list[i][j] += self.compass_center_px
                # if j == 1:
                    # point_list[i][j] *= -1

        # clear previous contents of frame
        self.cv_compass_art.delete('all')
        # start with orienting circle
        self.cv_compass_art.create_oval(self.compass_center_px-20, self.compass_center_px-20,
                                        self.compass_center_px+20, self.compass_center_px+20,
                                        width=1)

        # create the depth-organized list for 3d-render
        # copy point list so we don't alter OG list
        ddd_render_list = point_list[:]
        # sort the list from furthest pt to closest (lowest z to highest)
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
        # draw triangles
        for triangle in vertex_list:
            corner_a = ddd_render_list[triangle[0]]
            corner_b = ddd_render_list[triangle[1]]
            corner_c = ddd_render_list[triangle[2]]
            this_triangle = [corner_a, corner_b, corner_c]
            # find color to use
            # z-x : blue
            # x-y : red
            # y-z :yellow
            if end_z in this_triangle and end_x in this_triangle:
                color = 'light green'
            elif end_x in this_triangle and end_y in this_triangle:
                color = 'light blue'
            else:
                color = 'yellow'
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
        for this_node in point_list:
            if this_node is end_x:
                label = 'x'
            elif this_node is end_y:
                label = 'y'
            elif this_node is end_z:
                label = 'z'
            else:
                label = ''
            self.cv_compass_art.create_text(this_node[0], this_node[1], text=label, fill='black')

        # move the points back to 0,0,0 origin
        # so we can perform maths later
        for i in range(len(point_list)):
            for j in range(2):
                # if j == 1:
                    # point_list[i][j] *= -1
                point_list[i][j] -= self.compass_center_px
        # refresh canvas with new image
        self.cv_compass_art.update()


def rotate_around_x(y_angle, point_list):
    # print('rot_x', end=' ')
    if y_angle == 0:
        # print('exited', end = ' ')
        return point_list
    sin_theta = math.sin(math.radians(y_angle))
    cos_theta = math.cos(math.radians(y_angle))
    for i in range(1, len(point_list)):
        this_z = point_list[i][2]
        this_y = point_list[i][1]
        point_list[i][1] = round((this_y * cos_theta) - (this_z * sin_theta))
        point_list[i][2] = round((this_z * cos_theta) + (this_y * sin_theta))
    # print('mainp', end=' ')
    return point_list


def rotate_around_y(z_angle, point_list):
    # print('rot y', end=' ')
    if z_angle == 0:
        # print('exited', end=' ')
        return point_list

    sin_theta = math.sin(math.radians(z_angle))
    cos_theta = math.cos(math.radians(z_angle))

    for i in range(1, len(point_list)):
        this_z = point_list[i][2]
        this_x = point_list[i][0]
        point_list[i][0] = round((this_x * cos_theta) - (this_z * sin_theta))
        point_list[i][2] = round((this_z * cos_theta) + (this_x * sin_theta))
    # print('manip', end=' ')
    return point_list


def rotate_around_z(x_angle, point_list):
    # print('rot z', end=' ')
    if x_angle == 0:
        # print('exited', end=' ')
        return point_list

    sin_theta = math.sin(math.radians(x_angle))
    cos_theta = math.cos(math.radians(x_angle))

    for i in range(1, len(point_list)):
        this_x = point_list[i][0]
        this_y = point_list[i][1]
        point_list[i][0] = round((this_x * cos_theta) - (this_y * sin_theta))
        point_list[i][1] = round((this_y * cos_theta) + (this_x * sin_theta))

    # print('manip', end=' ')
    return point_list


if __name__ == '__main__':

    # call class to create window
    root = Root()
    # start mainloop
    root.mainloop()

    print('Exiting...')
