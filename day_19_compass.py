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
        end_y = [0, -90, 0]
        end_z = [0, 0, 90]
        origin = [0, 0, 0]
        # define lists to manipulate as we rotate compass
        point_list = [origin, end_x, end_y, end_z]
        edge_list = [origin, end_x, end_y, end_z]

        # call all three functions for rotation maths, this uses the
        # params self.__orient from the parent definition
        point_list = rotate_around_z(self.x_orient, point_list)
        point_list = rotate_around_x(self.y_orient, point_list)
        point_list = rotate_around_y(self.z_orient, point_list)

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
        for this_node in point_list:
            if this_node is end_x:
                label = 'x'
            elif this_node is end_y:
                label = 'y'
            elif this_node is end_z:
                label = 'z'
            else:
                # no label for origin point
                label = ''
            # we push the coordinates out from the triangle for readability
            # this is the top layer and the last use of this_node,
            # so we can change it freely without later consequence
            # we need to determine what quadrant the coordinates are in to add or subtract
            if this_node[0] >= origin[0] and this_node[1] >= origin[1]:
                this_node[0] += 5
                this_node[1] += 5
            elif this_node[0] >= origin[0] and this_node[1] < origin[1]:
                this_node[0] += 5
                this_node[1] -= 5
            elif this_node[0] < origin[0] and this_node[1] >= origin[1]:
                this_node[0] -= 5
                this_node[1] += 5
            else:
                this_node[0] -= 5
                this_node[1] -= 5
            self.cv_compass_art.create_text(this_node[0], this_node[1], text=label, fill='black')

        # move the points back to 0,0,0 origin,
        # so we can perform maths later
        for i in range(len(point_list)):
            for j in range(2):
                point_list[i][j] -= self.compass_center_px
        # refresh canvas with new image
        self.cv_compass_art.update()


def rotate_around_x(y_angle, point_list):
    """
    rotate_around_x() performs trig to move points in 3d space
    :param y_angle: measure in degrees of the y angle from 0 deg
    :param point_list: a list of [x, y, z] coordinates to manipulate
    :return: the manipulated list of coordinates
    """
    if y_angle == 0:
        return point_list

    sin_theta = math.sin(math.radians(y_angle))
    cos_theta = math.cos(math.radians(y_angle))

    # loop through the list of points
    # we start this loop at index 1, not index 0,
    # so we never rotate the origin point
    for i in range(1, len(point_list)):
        this_z = point_list[i][2]
        this_y = point_list[i][1]
        point_list[i][1] = round((this_y * cos_theta) - (this_z * sin_theta))
        point_list[i][2] = round((this_z * cos_theta) + (this_y * sin_theta))
    return point_list


def rotate_around_y(z_angle, point_list):
    """
    rotate_around_y() performs trig to move points in 3d space
    :param z_angle: measure in degrees of the y angle from 0 deg
    :param point_list: a list of [x, y, z] coordinates to manipulate
    :return: the manipulated list of coordinates
    """
    if z_angle == 0:
        return point_list

    sin_theta = math.sin(math.radians(z_angle))
    cos_theta = math.cos(math.radians(z_angle))

    # loop through the list of points
    # we start this loop at index 1, not index 0,
    # so we never rotate the origin point
    for i in range(1, len(point_list)):
        this_z = point_list[i][2]
        this_x = point_list[i][0]
        point_list[i][0] = round((this_x * cos_theta) - (this_z * sin_theta))
        point_list[i][2] = round((this_z * cos_theta) + (this_x * sin_theta))
    return point_list


def rotate_around_z(x_angle, point_list):
    """
    rotate_around_z() performs trig to move points in 3d space
    :param x_angle: measure in degrees of the y angle from 0 deg
    :param point_list: a list of [x, y, z] coordinates to manipulate
    :return: the manipulated list of coordinates
    """
    if x_angle == 0:
        return point_list

    sin_theta = math.sin(math.radians(x_angle))
    cos_theta = math.cos(math.radians(x_angle))

    # loop through the list of points
    # we start this loop at index 1, not index 0,
    # so we never rotate the origin point
    for i in range(1, len(point_list)):
        this_x = point_list[i][0]
        this_y = point_list[i][1]
        point_list[i][0] = round((this_x * cos_theta) - (this_y * sin_theta))
        point_list[i][1] = round((this_y * cos_theta) + (this_x * sin_theta))

    return point_list