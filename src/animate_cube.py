"""
    This program is made for fun, feel free to edit it.

    All the Rubik Cube's move are made according to this site: https://jperm.net/3x3/moves
    Adapted from the code made by Gabro_29: https://github.com/Gabro29/Rubik

"""

from copy import deepcopy
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import randrange
import threading
import kociemba
from time import time

rubik_cube = list()
solved_cube = list()

COLORS = {"W": "white", "G": "green", "R": "red", "O": "orange", "Y": "yellow", "B": "blue"}


def faces(num_faces: str, face: str, translate: list, rotate: list, color_1="white", color_2="blue", color_3="white",
          color_line="black"):
    """Create the face base on color"""

    facesbuff = (
        (1, -1, -1),
        (1, 1, -1),
        (1, 1, 1),
        (1, -1, 1),  # One face stop len 4
        (-1, -1, 1),
        (-1, 1, 1),  # Two faces stop len 6
        (-1, 1, -1)
    )

    facesbordbuff = (
        (0, 1),
        (0, 3),
        (2, 3),
        (2, 1),  # One face stop len 4
        (2, 5),
        (3, 4),
        (5, 4),  # Two faces stop len 7 = 6 +1
        (5, 6),
        (6, 1)  # three faces stop len 10
    )

    insidefaces = (
        (0, 3, 2, 1),
        (2, 3, 4, 5),
        (1, 2, 5, 6)
    )

    numface = {"one": 4, "two": 7, "three": 10, "ONE": 0, "TWO": 1, "THREE": 2}
    numarea = {"one": 4, "two": 6, "three": 7}
    pair_colors = {"white": (1, 1, 1), "blue": (0, 0, 1), "red": (1, 0.2, 0.3), "orange": (1, 0.5, 0.1),
                   "green": (0, 1, 0), "yellow": (1, 1, 0), "black": (0, 0, 0)}

    glTranslated(translate[0], translate[1], translate[2])
    glRotated(rotate[0], rotate[1], rotate[2], rotate[3])

    glBegin(GL_QUADS)
    if face == "ONE":
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
    elif face == "TWO":
        for vertex in insidefaces[numface.get("ONE")]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_2))
            glVertex3fv(facesbuff[vertex])
    elif face == "THREE":
        for vertex in insidefaces[numface.get("ONE")]:
            glColor3fv(pair_colors.get(color_1))
            glVertex3fv(facesbuff[vertex])
        for vertex in insidefaces[numface.get("TWO")]:
            glColor3fv(pair_colors.get(color_2))
            glVertex3fv(facesbuff[vertex])
        for vertex in insidefaces[numface.get(face)]:
            glColor3fv(pair_colors.get(color_3))
            glVertex3fv(facesbuff[vertex])
    glEnd()

    glBegin(GL_LINES)
    count = 0
    for line in facesbordbuff:
        if count < numface.get(num_faces):
            for point in line:
                glColor3fv(pair_colors.get(color_line))
                glVertex3fv(facesbuff[point])
            count += 1
        else:
            break
    glEnd()

    # glTranslated(-(translate[0]), -(translate[1]), -(translate[2]))
    glRotated(-rotate[0], (rotate[1]), (rotate[2]), (rotate[3]))


def faces_pos(num_faces: str, face: str, translate: list, rotate: list, color_1="white", color_2="blue",
              color_3="white", color_line="black"):
    """Adjust pos of faces on the screen"""

    faces(num_faces, face, translate, rotate, color_1, color_2, color_3, color_line)
    glTranslated(-translate[0], -translate[1], -translate[2])


def f_layer(layer: list):
    """Create the first layer"""

    faces_pos("three", "THREE", [0, 3, 0], [90, 0, -1, 0], layer[0][0], layer[0][1], layer[0][2])

    faces_pos("two", "TWO", [2, 3, 0], [90, 0, 0, 1], layer[1][0], layer[1][1])

    faces_pos("three", "THREE", [4, 3, 0], [0, 0, 0, 0], layer[2][0], layer[2][1], layer[2][2])

    faces_pos("two", "TWO", [4, 3, -2], [90, -1, 0, 0], layer[3][0], layer[3][1])

    faces_pos("three", "THREE", [4, 3, -4], [90, -1, 0, 0], layer[4][0], layer[4][1], layer[4][2])

    faces_pos("two", "TWO", [2, 3, -4], [180, 1, 1, 0], layer[5][0], layer[5][1])

    faces_pos("three", "THREE", [0, 3, -4], [180, 0, -1, 0], layer[6][0], layer[6][1], layer[6][2])

    faces_pos("two", "TWO", [0, 3, -2], [180, 0, 1, 1], layer[7][0], layer[7][1])

    faces_pos("one", "ONE", [2, 3, -2], [180, 1, 1, 0], layer[8][0])


def s_layer(layer: list):
    """Create the second layer"""

    faces_pos("two", "TWO", [0, 1, 0], [90, 0, -1, 0], layer[0][0], layer[0][1])

    faces_pos("one", "ONE", [2, 1, 2], [90, 0, 1, 0], layer[1][0])

    faces_pos("two", "TWO", [4, 1, 0], [180, 1, 0, 1], layer[2][0], layer[2][1])

    faces_pos("one", "ONE", [4, 1, -2], [0, 0, 0, 0], layer[3][0])

    faces_pos("two", "TWO", [4, 1, -4], [90, 0, 1, 0], layer[4][0], layer[4][1])

    faces_pos("one", "ONE", [2, 1, -4], [90, 0, 1, 0], layer[5][0])

    faces_pos("two", "TWO", [0, 1, -4], [180, 1, 0, -1], layer[6][0], layer[6][1])

    faces_pos("one", "ONE", [-2, 1, -2], [0, 0, 0, 0], layer[7][0])


def t_layer(layer: list):
    """Create the third layer"""

    faces_pos("three", "THREE", [0, -1, 0], [180, 0, 0, 1], layer[0][0], layer[0][1], layer[0][2])

    faces_pos("two", "TWO", [2, -1, 0], [90, 0, 0, -1], layer[1][0], layer[1][1])

    faces_pos("three", "THREE", [4, -1, 0], [90, 0, 0, -1], layer[2][0], layer[2][1], layer[2][2])

    faces_pos("two", "TWO", [4, -1, -2], [90, 1, 0, 0], layer[3][0], layer[3][1])

    faces_pos("three", "THREE", [4, -1, -4], [180, -100, -1, 0], layer[4][0], layer[4][1], layer[4][2])

    faces_pos("two", "TWO", [2, -1, -4], [180, -100, 100, -1], layer[5][0], layer[5][1])

    faces_pos("three", "THREE", [0, -1, -4], [180, -1, 1, 0], layer[6][0], layer[6][1], layer[6][2])

    faces_pos("two", "TWO", [0, -1, -2], [180, 0, -100, 100], layer[7][0], layer[7][1])

    faces_pos("one", "ONE", [2, -3, -2], [90, 0, -1, 100], layer[8][0])


def u_first_animation(m, cube: list):
    """U' animation"""

    if type(m) == list:
        k = 0
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        while k < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            s_layer(cube[9:17])
            t_layer(cube[17:])
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, -2)
            glRotated(k, 0, 1, 0)
            glTranslated(-2, 0, 2)
            f_layer(cube[:9])
            glPopMatrix()
            drawText(50, 120, f"Shuffling cube for {m[2]}/{m[1]} cycles", m[0])
            k += 20
            pygame.display.flip()
    else:
        while m < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            s_layer(cube[9:17])
            t_layer(cube[17:])
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, -2)
            glRotated(m, 0, 1, 0)
            glTranslated(-2, 0, 2)
            f_layer(cube[:9])
            glPopMatrix()
            m += 3
            pygame.display.flip()


def u_animation(m: int, cube: list):
    """U animation"""

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        s_layer(cube[9:17])
        t_layer(cube[17:])
        # Move first layer
        glPushMatrix()
        glTranslated(2, 0, -2)
        glRotated(m, 0, -1, 0)
        glTranslated(-2, 0, 2)
        f_layer(cube[:9])
        glPopMatrix()
        m += 3
        pygame.display.flip()


def r_animation(m: int, cube: list):
    """R animation"""

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        s_layer([cube[9], cube[10], cube[20], cube[12], cube[3], cube[14], cube[15], cube[16]])
        t_layer([cube[17], cube[18], cube[21], cube[13], cube[4], cube[22], cube[23], cube[24], cube[25]])
        # Move first layer
        glPushMatrix()
        glTranslated(2, 0, -2)
        glRotated(m, 1, 0, 0)
        f_layer([cube[0], cube[1], cube[19], cube[11], cube[2], cube[5], cube[6], cube[7], cube[8]])
        glTranslated(-2, 0, 2)
        glPopMatrix()
        m += 3
        pygame.display.flip()


def m_animation(m: int, cube: list):
    """M animation"""

    z_animation(m, cube)
    cube = z_move(cube)

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        f_layer(cube[:9])
        t_layer(cube[17:])
        # Move first layer
        glPushMatrix()
        glTranslated(2, 0, -2)
        glRotated(m, 0, -1, 0)
        glTranslated(-2, 0, 2)
        s_layer(cube[9:17])
        glPopMatrix()
        m += 3
        pygame.display.flip()


def m_first_animation(m: int, cube: list):
    """M' animation"""

    z_animation(m, cube)
    cube = z_move(cube)

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        f_layer(cube[:9])
        t_layer(cube[17:])
        # Move first layer
        glPushMatrix()
        glTranslated(2, 0, -2)
        glRotated(m, 0, 1, 0)
        glTranslated(-2, 0, 2)
        s_layer(cube[9:17])
        glPopMatrix()
        m += 3
        pygame.display.flip()


def e_animation(m, cube: list):
    """E animation"""

    if type(m) == list:
        k = 0
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        while k < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            f_layer(cube[:9])
            t_layer(cube[17:])
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, -2)
            glRotated(k, 0, -1, 0)
            glTranslated(-2, 0, 2)
            s_layer(cube[9:17])
            glPopMatrix()
            drawText(50, 120, f"Shuffling cube for {m[2]}/{m[1]} cycles", m[0])
            k += 20
            pygame.display.flip()
    else:
        while m < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            f_layer(cube[:9])
            t_layer(cube[17:])
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, -2)
            glRotated(m, 0, -1, 0)
            glTranslated(-2, 0, 2)
            s_layer(cube[9:17])
            glPopMatrix()
            m += 3
            pygame.display.flip()


def d_animation(m: int, cube: list):
    """D animation"""

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        f_layer(cube[:9])
        s_layer(cube[9:17])
        # Move first layer
        glPushMatrix()
        glTranslated(2, 0, -2)
        glRotated(m, 0, -1, 0)
        glTranslated(-2, 0, 2)
        t_layer(cube[17:])
        glPopMatrix()
        m += 3
        pygame.display.flip()


def x_first_animation(m: int, cube: list):
    """X' animation"""

    while m < 90:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Move first layer
        glPushMatrix()
        glTranslated(-2, 0, -2)
        glRotated(m, 1, 0, 0)
        glTranslated(2, 0, 2)
        f_layer(cube[:9])
        s_layer(cube[9:17])
        t_layer(cube[17:])
        glPopMatrix()
        m += 3
        pygame.display.flip()


def z_animation(m, cube: list):
    """Z animation"""

    if type(m) == list:
        k = 0
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        while k < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, 2)
            glRotated(k, 0, 0, -1)
            glTranslated(-2, 0, -2)
            f_layer(cube[:9])
            s_layer(cube[9:17])
            t_layer(cube[17:])
            glPopMatrix()
            drawText(50, 120, f"Shuffling cube for {m[2]}/{m[1]} cycles", m[0])
            k += 20
            pygame.display.flip()
    else:

        while m < 90:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # Move first layer
            glPushMatrix()
            glTranslated(2, 0, 2)
            glRotated(m, 0, 0, -1)
            glTranslated(-2, 0, -2)
            f_layer(cube[:9])
            s_layer(cube[9:17])
            t_layer(cube[17:])
            glPopMatrix()
            m += 3
            pygame.display.flip()


def shuffle_animation(cycle: int, m: int, cube: list, font):
    """Shuffle the cube"""

    k = 1
    while k < cycle:
        u_first_animation([font, cycle, k], cube)
        cube = u_first_move(cube)
        z_animation([font, cycle, k], cube)
        cube = z_move(cube)
        if k % 5 == 0:
            e_animation([font, cycle, k], cube)
            cube = e_move(cube)
        k += 1


def sexy_animation(m: int, cube: list):
    """Do the Sexy Move"""

    z_animation(m, cube)
    cube = z_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    u_animation(m, cube)
    cube = u_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    u_animation(m, cube)
    cube = u_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    u_first_animation(m, cube)
    cube = u_first_move(cube)
    z_animation(m, cube)
    cube = z_move(cube)
    u_first_animation(m, cube)
    cube = u_first_move(cube)


def u_first_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if len(face) == 2 and 0 <= count < 9:
            temp_cube.append([face[1], face[0]])
        elif count == 2:
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 4:
            temp_cube.append([face[2], face[0], face[1]])
        else:
            temp_cube.append(face)

        count += 1

    # Change 3 faces
    temp_0 = temp_cube[0]
    temp_cube[0] = temp_cube[6]
    temp_2 = temp_cube[2]
    temp_cube[2] = temp_0
    temp_4 = temp_cube[4]
    temp_cube[4] = temp_2
    temp_cube[6] = temp_4

    # Change 2 faces
    temp_1 = temp_cube[1]
    temp_cube[1] = temp_cube[7]
    temp_3 = temp_cube[3]
    temp_cube[3] = temp_1
    temp_5 = temp_cube[5]
    temp_cube[5] = temp_3
    temp_cube[7] = temp_5

    return temp_cube


def u_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if len(face) == 2 and 0 <= count < 9:
            temp_cube.append([face[1], face[0]])
        elif count == 2:
            temp_cube.append([face[0], face[1], face[2]])
        elif count == 4:
            temp_cube.append([face[2], face[0], face[1]])
        elif count == 6:
            temp_cube.append([face[1], face[2], face[0]])
        else:
            temp_cube.append(face)
        count += 1

    # Change 3 faces
    temp_6 = temp_cube[6]
    temp_cube[6] = temp_cube[0]
    temp_4 = temp_cube[4]
    temp_cube[4] = temp_6
    temp_2 = temp_cube[2]
    temp_cube[2] = temp_4
    temp_cube[0] = temp_2

    # Change 2 faces
    temp_7 = temp_cube[7]
    temp_cube[7] = temp_cube[1]
    temp_5 = temp_cube[5]
    temp_cube[5] = temp_7
    temp_3 = temp_cube[3]
    temp_cube[3] = temp_5
    temp_cube[1] = temp_3

    return temp_cube


def r_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if count in (11, 20, 13, 3):
            temp_cube.append([face[1], face[0]])
        elif count == 19:
            temp_cube.append([face[2], face[0], face[1]])
        elif count == 4:
            temp_cube.append([face[0], face[1], face[2]])
        elif count == 21:
            temp_cube.append([face[1], face[2], face[0]])
        else:
            temp_cube.append(face)

        count += 1

    # 3 faces
    temp_2 = temp_cube[2]
    temp_cube[2] = temp_cube[19]
    temp_cube[19] = temp_cube[21]
    temp_cube[21] = temp_cube[4]
    temp_cube[4] = temp_2

    # 2 faces
    temp_3 = temp_cube[3]
    temp_cube[3] = temp_cube[11]
    temp_cube[11] = temp_cube[20]
    temp_cube[20] = temp_cube[13]
    temp_cube[13] = temp_3

    return temp_cube


def m_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if count in (1, 5, 18, 22):
            temp_cube.append([face[1], face[0]])
        else:
            temp_cube.append(face)
        count += 1

    temp_1 = temp_cube[1]
    temp_cube[1] = temp_cube[5]
    temp_8 = temp_cube[8]
    temp_cube[8] = temp_cube[14]
    temp_cube[5] = temp_cube[22]
    temp_cube[14] = temp_cube[25]
    temp_cube[22] = temp_cube[18]
    temp_cube[25] = temp_cube[10]
    temp_cube[18] = temp_1
    temp_cube[10] = temp_8

    temp_cube = z_move(temp_cube)

    return temp_cube


def m_first_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if count in (1, 5, 18, 22):
            temp_cube.append([face[1], face[0]])
        else:
            temp_cube.append(face)
        count += 1

    # Change central faces
    temp_5 = temp_cube[5]
    temp_cube[5] = temp_cube[1]
    temp_14 = temp_cube[14]
    temp_cube[14] = temp_cube[8]
    temp_22 = temp_cube[22]
    temp_cube[22] = temp_5
    temp_25 = temp_cube[25]
    temp_cube[25] = temp_14
    temp_18 = temp_cube[18]
    temp_cube[18] = temp_22
    temp_10 = temp_cube[10]
    temp_cube[10] = temp_25
    temp_cube[1] = temp_18
    temp_cube[8] = temp_10

    temp_cube = z_move(temp_cube)

    return temp_cube


def e_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if count in (9, 11, 13, 15):
            temp_cube.append([face[1], face[0]])
        else:
            temp_cube.append(face)
        count += 1

    # Change central faces
    temp_9 = temp_cube[9]
    temp_cube[9] = temp_cube[11]
    temp_10 = temp_cube[10]
    temp_cube[10] = temp_cube[12]
    temp_11 = temp_cube[11]
    temp_cube[11] = temp_cube[13]

    temp_cube[12] = temp_cube[14]
    temp_cube[13] = temp_cube[15]
    temp_cube[14] = temp_cube[16]
    temp_cube[15] = temp_9
    temp_cube[16] = temp_10

    return temp_cube


def d_move(cube: list):
    """Take the cube, do a movement and give it back with update position"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if count in (18, 20, 22, 24):
            temp_cube.append([face[1], face[0]])
        elif count == 19:
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 21:
            temp_cube.append([face[2], face[0], face[1]])
        elif count == 23:
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 17:
            temp_cube.append([face[2], face[0], face[1]])
        else:
            temp_cube.append(face)
        count += 1

    # Change central faces
    temp_17 = temp_cube[17]
    temp_cube[17] = temp_cube[19]
    temp_cube[19] = temp_cube[21]
    temp_cube[21] = temp_cube[23]
    temp_cube[23] = temp_17

    temp_18 = temp_cube[18]
    temp_cube[18] = temp_cube[20]
    temp_cube[20] = temp_cube[22]
    temp_cube[22] = temp_cube[24]
    temp_cube[24] = temp_18

    return temp_cube


def x_first_move(cube: list):
    """Take the cube and rotate it, so place on top the face to move"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if len(face) == 2:
            temp_cube.append([face[1], face[0]])
        elif count in (0, 17, 2):
            temp_cube.append([face[1], face[2], face[0]])
        elif count in (6, 23, 19):
            temp_cube.append([face[2], face[0], face[1]])
        else:
            temp_cube.append(face)
        count += 1

    # Central line
    temp_10 = temp_cube[10]
    temp_cube[10] = temp_cube[8]
    temp_cube[8] = temp_cube[14]
    temp_cube[14] = temp_cube[25]
    temp_cube[25] = temp_10

    temp_18 = temp_cube[18]
    temp_cube[18] = temp_cube[1]
    temp_cube[1] = temp_cube[5]
    temp_cube[5] = temp_cube[22]
    temp_cube[22] = temp_18

    # Edge
    temp_19 = temp_cube[19]
    temp_cube[19] = temp_cube[2]
    temp_cube[2] = temp_cube[4]
    temp_cube[4] = temp_cube[21]
    temp_cube[21] = temp_19

    temp_11 = temp_cube[11]
    temp_cube[11] = temp_cube[3]
    temp_cube[3] = temp_cube[13]
    temp_cube[13] = temp_cube[20]
    temp_cube[20] = temp_11

    temp_17 = temp_cube[17]
    temp_cube[17] = temp_cube[0]
    temp_cube[0] = temp_cube[6]
    temp_cube[6] = temp_cube[23]
    temp_cube[23] = temp_17

    temp_9 = temp_cube[9]
    temp_cube[9] = temp_cube[7]
    temp_cube[7] = temp_cube[15]
    temp_cube[15] = temp_cube[24]
    temp_cube[24] = temp_9

    return temp_cube


def z_move(cube: list):
    """Take the cube and rotate it, so place on top the face to move"""

    temp_cube = list()
    temp_pos = list()
    count = 0
    for face in cube:
        if len(face) == 2:
            temp_cube.append([face[1], face[0]])
        elif count == 17:
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 0:
            temp_cube.append([face[2], face[0], face[1]])
        elif count == 4:
            temp_cube.append([face[1], face[2], face[0]])
        elif count == 6:
            temp_cube.append([face[2], face[0], face[1]])
        else:
            temp_cube.append(face)
        count += 1

    # Central Single
    temp_12 = temp_cube[12]
    temp_cube[12] = temp_cube[8]
    temp_cube[8] = temp_cube[16]
    temp_cube[16] = temp_cube[25]
    temp_cube[25] = temp_12

    # Central edges
    temp_20 = temp_cube[20]
    temp_cube[20] = temp_cube[3]
    temp_cube[3] = temp_cube[7]
    temp_cube[7] = temp_cube[24]
    temp_cube[24] = temp_20

    # Right edges

    temp_21 = temp_cube[21]
    temp_cube[21] = temp_cube[4]
    temp_cube[4] = temp_cube[6]
    temp_cube[6] = temp_cube[23]
    temp_cube[23] = temp_21

    # Right central

    temp_13 = temp_cube[13]
    temp_cube[13] = temp_cube[5]
    temp_cube[5] = temp_cube[15]
    temp_cube[15] = temp_cube[22]
    temp_cube[22] = temp_13

    # Left edges

    temp_19 = temp_cube[19]
    temp_cube[19] = temp_cube[2]
    temp_cube[2] = temp_cube[0]
    temp_cube[0] = temp_cube[17]
    temp_cube[17] = temp_19

    # Left central

    temp_11 = temp_cube[11]
    temp_cube[11] = temp_cube[1]
    temp_cube[1] = temp_cube[9]
    temp_cube[9] = temp_cube[18]
    temp_cube[18] = temp_11

    return temp_cube


def sexy_move(cube: list):
    """Do sexy move"""

    cube = z_move(cube)
    cube = z_move(cube)
    cube = z_move(cube)
    cube = u_move(cube)
    cube = z_move(cube)
    cube = u_move(cube)
    cube = z_move(cube)
    cube = z_move(cube)
    cube = z_move(cube)
    cube = u_first_move(cube)
    cube = z_move(cube)
    cube = u_first_move(cube)

    return cube


def drawText(x: int, y: int, text: str, font):
    """Print on the screen how many times is shuffling the cube"""

    textSurface = font.render(text, True, (255, 255, 66, 255)).convert_alpha()
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def shuffle(cycle, cube: list):
    """Take the cube and move the faces to messy the all cube"""

    k = 1
    while k < cycle:
        cube = u_first_move(cube)
        cube = z_move(cube)
        if k % 5 == 0:
            cube = e_move(cube)
        k += 1

    return cube

def main(cube, solution):
    """Main code"""

    # Manual definition of layers
    first_layer = [ [COLORS[cube[18]], COLORS[cube[11]], COLORS[cube[6]]], #18,11,6
                    [COLORS[cube[7]], COLORS[cube[19]]], #7,19
                    [COLORS[cube[27]], COLORS[cube[20]], COLORS[cube[8]]],#27,20,8
                    [COLORS[cube[28]], COLORS[cube[5]]], #28,5
                    [COLORS[cube[29]],COLORS[cube[2]], COLORS[cube[36]]], #29,2,36
                    [COLORS[cube[1]], COLORS[cube[37]]], #1,37
                    [COLORS[cube[9]], COLORS[cube[38]], COLORS[cube[0]]],#9,38,0
                    [COLORS[cube[10]], COLORS[cube[3]]], #10,3
                    [COLORS[cube[4]]] #4
                   ]

    second_layer = [[COLORS[cube[21]], COLORS[cube[14]]], #21, 14
                    [COLORS[cube[22]]], #22
                    [COLORS[cube[23]], COLORS[cube[30]]], #23, 30
                    [COLORS[cube[31]]], #31
                    [COLORS[cube[39]], COLORS[cube[32]]], #39, 32
                    [COLORS[cube[40]]],#40
                    [COLORS[cube[41]], COLORS[cube[12]]], #41, 12
                    [COLORS[cube[13]]] #13
                    ]

    third_layer = [[COLORS[cube[17]], COLORS[cube[24]], COLORS[cube[51]]], #17,24,51
                   [COLORS[cube[52]], COLORS[cube[25]]],#52,25
                   [COLORS[cube[53]], COLORS[cube[26]], COLORS[cube[33]]],#53,26,33
                   [COLORS[cube[34]], COLORS[cube[50]]],#34,50
                   [COLORS[cube[35]], COLORS[cube[42]], COLORS[cube[47]]],#35,42,47
                   [COLORS[cube[46]], COLORS[cube[43]]],#46,43
                   [COLORS[cube[45]], COLORS[cube[44]], COLORS[cube[15]]],#45,44,15
                   [COLORS[cube[16]], COLORS[cube[48]]],#16,48
                   [COLORS[cube[49]]] #49
                   ]

    # Build the cube base on previous layers
    global rubik_cube
    global solved_cube
    for layer in (first_layer, second_layer, third_layer):
        lay = layer
        for face in lay:
            rubik_cube.append(face)

    solved_cube = rubik_cube

    # Initialize pygame gui
    pygame.init()
    pygame.font.init()
    display = (800, 600)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    icon = pygame.image.load('resources/rubik.png')
    pygame.display.set_icon(icon)
    font = pygame.font.SysFont('lucinda console', 64)
    pygame.display.set_caption("Rubik Cube")

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0, -20)  # Camera view
    glRotatef(45, 1, 1, 1)  # Prospective view

    # No overlapping
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Extra variables
    u_first_key = False
    u_key = False
    r_key = False
    m_key = False
    m_first_key = False
    z_key = False
    x_first_key = False
    shuffle_key = False
    sexy_key = False
    first_white_key = False
    cycle = 0
    m = 1
    prev_pos_x = 0
    prev_pos_y = 0

    movement_idx = 0

    # Show the cube on screen
    while True:

        # Check for pressed keys
        for event in pygame.event.get():
            # print(rubik_cube)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:  # Change camera view
                    glRotatef(20, 0, -1, 0)
                if event.key == pygame.K_f:  # Change camera view
                    glRotatef(20, 0, 1, 0)
                # if event.key == pygame.K_s:  # Change camera view
                #     glRotatef(10, 0, 2, 1)
                if event.key == pygame.K_d:  # Change camera view
                    glRotatef(90, 1, 0, 0)
                if event.key == pygame.K_ESCAPE:  # Exit
                    exit()

                if event.key == pygame.K_RIGHT:
                    #TODO: Do the animations right
                    print("Right Arrow Pressed")
                    if movement_idx < len(solution):
                        move = solution[movement_idx]
                        movement_idx += 1
                        print(movement_idx)
                        print(move)
                        if move == "U":
                            u_animation(m, rubik_cube)
                            u_key = True
                        elif move == "R":
                            r_animation(m, rubik_cube)
                            r_key = True
                        elif move == "U'":
                            u_first_animation(m, rubik_cube)
                            u_first_key = True
                        elif move == "R'":
                            #r_first_animation(m, rubik_cube)
                            r_first_key = True
                        elif move == "L":
                            pass
                        
                        

                if event.key == pygame.K_LEFT:
                    print("Left Arrow Pressed")
                    if movement_idx > 0:
                        last_move = solution[movement_idx]
                        movement_idx -= 1
                        print(movement_idx)
                        print(rubik_cube)

                # U' Move
                if event.key == pygame.K_o:
                    u_first_animation(m, rubik_cube)
                    u_first_key = True

                # U Move
                if event.key == pygame.K_p:
                    u_animation(m, rubik_cube)
                    u_key = True

                if event.key == pygame.K_r:
                    d_animation(m, rubik_cube)
                    r_key = True

                # M Move
                if event.key == pygame.K_v:
                    m_animation(m, rubik_cube)
                    rubik_cube = m_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    m_key = True

                # M' Move
                if event.key == pygame.K_c:
                    m_first_animation(m, rubik_cube)
                    rubik_cube = m_first_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    z_animation(m, rubik_cube)
                    rubik_cube = z_move(rubik_cube)
                    m_first_key = True

                # Z Move
                if event.key == pygame.K_t:
                    z_animation(m, rubik_cube)
                    z_key = True

                # X' Move
                if event.key == pygame.K_w:
                    x_first_animation(m, rubik_cube)
                    x_first_key = True

                # Sexy Move
                if event.key == pygame.K_s:
                    sexy_animation(m, rubik_cube)
                    sexy_key = True

                # Shuffle Move
                if event.key == pygame.K_a:
                    cycle = randrange(5, 100)
                    shuffle_animation(cycle, m, rubik_cube, font)
                    shuffle_key = True

                # First White
                if event.key == pygame.K_q:
                    first_white_key = True

        # Mouse Camera
        for event in pygame.mouse.get_pressed(3):
            if event:
                if abs(prev_pos_x - pygame.mouse.get_pos()[0]) == 0:
                    glRotatef(20, 1, 0, 0)  # Camera view
                elif abs(prev_pos_y - pygame.mouse.get_pos()[1]) == 0:
                    glRotatef(20, 0, 1, 0)  # Camera view
                elif abs(prev_pos_y - pygame.mouse.get_pos()[1]) > 1 and abs(
                        prev_pos_x - pygame.mouse.get_pos()[0]) > 1:
                    glRotatef(20, 1, 1, 0)  # Camera view
            prev_pos_x = pygame.mouse.get_pos()[0]
            prev_pos_y = pygame.mouse.get_pos()[1]

        # Clear view
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if u_first_key:
            rubik_cube = u_first_move(rubik_cube)
            u_first_key = False
        elif u_key:
            rubik_cube = u_move(rubik_cube)
            u_key = False
        elif r_key:
            rubik_cube = d_move(rubik_cube)
            r_key = False
        elif m_key:
            m_key = False
        elif m_first_key:
            m_first_key = False
        elif x_first_key:
            rubik_cube = x_first_move(rubik_cube)
            x_first_key = False
        elif z_key:
            rubik_cube = z_move(rubik_cube)
            z_key = False
        elif shuffle_key:
            rubik_cube = shuffle(cycle, rubik_cube)
            shuffle_key = False
        elif sexy_key:
            rubik_cube = sexy_move(rubik_cube)
            sexy_key = False
        elif first_white_key:
            threading.Thread(target=solving()).start()
            first_white_key = False

        # Show updated layer
        f_layer(rubik_cube[:9])
        s_layer(rubik_cube[9:17])
        t_layer(rubik_cube[17:])
        pygame.display.flip()
        pygame.time.wait(20)


if __name__ == '__main__':
    #Test values
    cube_string = "GGGGGGGGGRRRRRRRRRWWWWWWWWWBBBBBBBBBOOOOOOOOOYYYYYYYYY"

    kociemba_string = deepcopy(cube_string)
    kociemba_string = kociemba_string.replace("G", "U")
    kociemba_string = kociemba_string.replace("R", "R")
    kociemba_string = kociemba_string.replace("W", "F")
    kociemba_string = kociemba_string.replace("O", "L")
    kociemba_string = kociemba_string.replace("B", "D")
    kociemba_string = kociemba_string.replace("Y", "B")
    print(kociemba_string)

    print("Solving the cube...")
    solution = kociemba.solve(kociemba_string).split()
    print(solution)

    main(cube_string, solution)