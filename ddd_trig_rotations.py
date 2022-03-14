import math

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
