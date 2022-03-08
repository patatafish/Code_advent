import tkinter as tk
import math
import time


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
        self.init_compass()


        # test rotation
        for i in range(650):
            time.sleep(.01)
            self.draw_compass(x_orient=i/100)

        for i in range(650):
            time.sleep(.01)
            self.draw_compass(y_orient=i/100)

        for i in range(650):
            time.sleep(.01)
            self.draw_compass(z_orient=i/100)

    def init_compass(self):

        # define the size of the canvas, and find center mass
        self.compass_square_size = 190
        self.compass_center_px = self.compass_square_size / 2

        self.fr_compass = tk.Frame(self.fr_background,
                                   bg='light gray',
                                   relief=tk.RAISED,
                                   border=5,
                                   height=195, width=195)
        self.cv_compass_art = tk.Canvas(self.fr_compass,
                                   bg='white',
                                   height=self.compass_square_size, width=self.compass_square_size)

        self.fr_compass.place(x=50, y=945)
        self.cv_compass_art.pack()
        # initiate compass with 0 orientation
        self.draw_compass()


    def draw_compass(self, x_orient=0, y_orient=0, z_orient=0):
        """
        draw_compass() creates the image to render in the fr_compass to show orientations
        :param x_orient: x offset (0 to 359)
        :param y_orient: y offset (0 to 359)
        :param z_orient: z offset (0 to 359)
        :return: None
        """

        # define end points for our three compass lines
        end_x = [90, 0, 0]
        end_y = [0, -90, 0]
        end_z = [0, 0, 90]
        origin = [0, 0, 0]
        point_list = [origin, end_x, end_y, end_z]
        edge_list = [end_x, end_y, end_z]


        # if there is a variable around x, call changing x
        if x_orient:
            point_list = rotate_around_z(x_orient, point_list)
        # if there is a variable around y, call changing y
        if y_orient:
            point_list = rotate_around_x(y_orient, point_list)
        # if there is a variable around z, call changing z
        if z_orient:
            point_list = rotate_around_y(z_orient, point_list)

        print(f'{x_orient},{y_orient},{z_orient}:::{end_x},{end_y},{end_z}')


        # move the points to the center of our canvas
        for i in range(len(point_list)):
            for j in range(2):
                point_list[i][j] += self.compass_center_px

        # clear previous contents of frame
        self.cv_compass_art.delete('all')
        # start with orienting circle
        self.cv_compass_art.create_oval(self.compass_center_px-20, self.compass_center_px-20,
                                        self.compass_center_px+20, self.compass_center_px+20,
                                        width=1)
        # draw lines for compass
        for this_edge in edge_list:
            self.cv_compass_art.create_line(origin[0], origin[1],
                                            this_edge[0], this_edge[1],
                                            width=2, fill='light green')
        # draw end points for compass
        for this_node in point_list:
            self.cv_compass_art.create_oval(this_node[0]-3, this_node[1]-3,
                                            this_node[0]+3, this_node[1]+3,
                                            width=2, outline='black')
        # move the points back to 0,0,0 origin
        for i in range(len(point_list)):
            for j in range(2):
                point_list[i][j] -= self.compass_center_px
        # refresh canvas with new image
        self.cv_compass_art.update()


def rotate_around_x(y_angle, point_list):
    sin_theta = math.sin(y_angle)
    cos_theta = math.cos(y_angle)

    for i in range(1, len(point_list)):
        this_z = point_list[i][2]
        this_y = point_list[i][1]
        point_list[i][0] = round((this_y * cos_theta) - (this_z * sin_theta))
        point_list[i][1] = round((this_z * cos_theta) + (this_y * sin_theta))

    return point_list


def rotate_around_y(z_angle, point_list):
    sin_theta = math.sin(z_angle)
    cos_theta = math.cos(z_angle)

    for i in range(1, len(point_list)):
        this_z = point_list[i][2]
        this_x = point_list[i][0]
        point_list[i][0] = round((this_x * cos_theta) - (this_z * sin_theta))
        point_list[i][1] = round((this_z * cos_theta) + (this_x * sin_theta))

    return point_list


def rotate_around_z(x_angle, point_list):

    sin_theta = math.sin(x_angle)
    cos_theta = math.cos(x_angle)

    for i in range(1, len(point_list)):
        this_x = point_list[i][0]
        this_y = point_list[i][1]
        point_list[i][0] = round((this_x * cos_theta) - (this_y * sin_theta))
        point_list[i][1] = round((this_y * cos_theta) + (this_x * sin_theta))

    return point_list


if __name__ == '__main__':


    # call class to create window
    root = Root()
    # start mainloop
    root.mainloop()


    print('Exiting...')