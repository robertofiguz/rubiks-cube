""" PyCube
Author: Michael King

Based and modified from original version found at:
http://stackoverflow.com/questions/30745703/rotating-a-cube-using-quaternions-in-pyopengl
"""
import sys
import copy
from quat import *
from geometry import *
#import keypress

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
#from OpenGL.GLUT import *

moves = ''

class PyCube:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.movements = []
        self.reverse_moves = {
            'U': 'U\'',
            'U\'': 'U',
            'D': 'D\'',
            'D\'': 'D',
            'L': 'L\'',
            'L\'': 'L',
            'R': 'R\'',
            'R\'': 'R',
            'F': 'F\'',
            'F\'': 'F',
            'B': 'B\'',
            'B\'': 'B',
        }
        self.last_moves = []
        self.text = None
        self.screen=pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        
        pygame.display.set_caption('PyCube')
        # glClearColor(0.35, 0.35, 0.35, 1.0)
        glClearColor(1, 1, 1, 0)
        # Using depth test to make sure closer colors are shown over further ones
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        # glutInit()
        # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);

        # Default view
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.width / self.height), 0.5, 40)
        glTranslatef(0.0, 0.0, -17.5)
        padding(0.3)

    def create_window(self, width, height):
        '''Updates the window width and height '''
        # pygame.display.set_caption("Press ESC to quit")
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL | RESIZABLE)
        gluPerspective(45, (width / height), 0.5, 40)
    def reverse(self, moves):
        result = []
        #reverse moves list
        moves = moves[::-1]
        #reverse each move
        #mapping

        for i in moves:
            try:
                result.append(self.reverse_moves[i])
            except KeyError:
                if i[1] == '2':
                    result.append(i[0])
                    result.append(i[0])
            
        self._reverse = True
        return result

    def animate(self, move, moves, theta, theta_inc, reverse):

        inc_x = 0
        inc_y = 0
        accum = (1, 0, 0, 0)
        zoom = 1

        def update():

            pygame.mouse.get_rel()  # prevents the cube from instantly rotating to a newly clicked mouse coordinate

            rot_x = normalize(axisangle_to_q((1.0, 0.0, 0.0), inc_x))
            rot_y = normalize(axisangle_to_q((0.0, 1.0, 0.0), inc_y))

            nonlocal accum
            accum = q_mult(accum, rot_x)
            accum = q_mult(accum, rot_y)
            # print(accum)

            glMatrixMode(GL_MODELVIEW)
            glLoadMatrixf(q_to_mat4(accum))
            glScalef(zoom, zoom, zoom)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.draw_cube()
            # Draw the text onto the screen
            if self.text:
                self.screen.blit(self.text, (500, 500))
            # glutSolidSphere(3.0, 50, 50);
            # draw_face()
            # self.draw_axis()
            if not self._reverse:
                pygame.display.flip()
            
            #make pygame slower
            
        if move =='F':
            if reverse:
                moves += 'F'
                sys.stdout.write("F\'")
                theta *= 1
            else:
                moves += 'f'
                sys.stdout.write("F")
                theta *= -1
            for x in range(theta_inc):
                for i in range(8):
                    center_pieces[0][i] = z_rot(center_pieces[0][i], theta)

                for axis in edge_pieces:
                    for piece in axis:
                        flag = True
                        for vertex in piece:
                            if vertex[2] < 0:
                                flag = False
                                break
                        if flag:
                            for i in range(8):
                                piece[i] = z_rot(piece[i], theta)
                for piece in corner_pieces:
                    flag = True
                    for vertex in piece:
                        if vertex[2] < 0:
                            flag = False
                            break
                    if flag:
                        for i in range(8):
                            piece[i] = z_rot(piece[i], theta)

                update()

        if move =='L':
            if reverse:
                moves += 'L'
                sys.stdout.write("L\'")
                theta *= -1
            else:
                moves += 'l'
                sys.stdout.write("L")
                theta *= 1
            for x in range(theta_inc):
                for i in range(8):
                    center_pieces[1][i] = x_rot(center_pieces[1][i], theta)

                for axis in edge_pieces:
                    for piece in axis:
                        flag = True
                        for vertex in piece:
                            if vertex[0] > 0:
                                flag = False
                                break
                        if flag:
                            for i in range(8):
                                piece[i] = x_rot(piece[i], theta)
                for piece in corner_pieces:
                    flag = True
                    for vertex in piece:
                        if vertex[0] > 0:
                            flag = False
                            break
                    if flag:
                        for i in range(8):
                            piece[i] = x_rot(piece[i], theta)

                update()

        if move =='B':
            if reverse:
                moves += 'B'
                sys.stdout.write("B\'")
                theta *= -1
            else:
                moves += 'b'
                sys.stdout.write("B")
                theta *= 1
            for x in range(theta_inc):
                for i in range(8):
                    center_pieces[2][i] = z_rot(center_pieces[2][i], theta)

                for axis in edge_pieces:
                    for piece in axis:
                        flag = True
                        for vertex in piece:
                            if vertex[2] > 0:
                                flag = False
                                break
                        if flag:
                            for i in range(8):
                                piece[i] = z_rot(piece[i], theta)
                for piece in corner_pieces:
                    flag = True
                    for vertex in piece:
                        if vertex[2] > 0:
                            flag = False
                            break
                    if flag:
                        for i in range(8):
                            piece[i] = z_rot(piece[i], theta)

                update()

        if move =='R':
            if reverse:
                moves += 'R'
                sys.stdout.write("R\'")
                theta *= 1
            else:
                moves += 'r'
                sys.stdout.write("R")
                theta *= -1
            for x in range(theta_inc):
                for i in range(8):
                    center_pieces[3][i] = x_rot(center_pieces[3][i], theta)

                for axis in edge_pieces:
                    for piece in axis:
                        flag = True
                        for vertex in piece:
                            if vertex[0] < 0:
                                flag = False
                                break
                        if flag:
                            for i in range(8):
                                piece[i] = x_rot(piece[i], theta)
                for piece in corner_pieces:
                    flag = True
                    for vertex in piece:
                        if vertex[0] < 0:
                            flag = False
                            break
                    if flag:
                        for i in range(8):
                            piece[i] = x_rot(piece[i], theta)

                update()

        if move =='U':
            if reverse:
                moves += 'U'
                sys.stdout.write("U\'")
                theta *= 1
            else:
                moves += 'u'
                sys.stdout.write("U")
                theta *= -1
            for x in range(theta_inc):
                for i in range(8):
                    center_pieces[4][i] = y_rot(center_pieces[4][i], theta)

                for axis in edge_pieces:
                    for piece in axis:
                        flag = True
                        for vertex in piece:
                            if vertex[1] < 0:
                                flag = False
                                break
                        if flag:
                            for i in range(8):
                                piece[i] = y_rot(piece[i], theta)
                for piece in corner_pieces:
                    flag = True
                    for vertex in piece:
                        if vertex[1] < 0:
                            flag = False
                            break
                    if flag:
                        for i in range(8):
                            piece[i] = y_rot(piece[i], theta)

                update()

        if move =='D':
            if reverse:
                moves +='D'
                sys.stdout.write("D\'")
                theta *= -1
            else:
                moves += 'd'
                sys.stdout.write("D")
                theta *= 1
            for x in range(theta_inc):
                for i in range(8):
                    center_pieces[5][i] = y_rot(center_pieces[5][i], theta)

                for axis in edge_pieces:
                    for piece in axis:
                        flag = True
                        for vertex in piece:
                            if vertex[1] > 0:
                                flag = False
                                break
                        if flag:
                            for i in range(8):
                                piece[i] = y_rot(piece[i], theta)
                for piece in corner_pieces:
                    flag = True
                    for vertex in piece:
                        if vertex[1] > 0:
                            flag = False
                            break
                    if flag:
                        for i in range(8):
                            piece[i] = y_rot(piece[i], theta)

                update()
        return move, moves, theta, theta_inc, reverse
    
    def run(self, movements):
        movements = [str(i) for i in movements]
        _save_moves = copy.deepcopy(movements)
        self.movements = self.reverse(movements)
        # set initial rotation
        #glRotate(90, 1, 0, 0)
        # glRotate(-15, 0, 0, 1)
        # glRotate(15, 1, 0, 0)

        global moves
        

        pad_toggle = False
        inc_x = 0
        inc_y = 0
        accum = (1, 0, 0, 0)
        zoom = 1

        def update():

            pygame.mouse.get_rel()  # prevents the cube from instantly rotating to a newly clicked mouse coordinate

            rot_x = normalize(axisangle_to_q((1.0, 0.0, 0.0), inc_x))
            rot_y = normalize(axisangle_to_q((0.0, 1.0, 0.0), inc_y))

            nonlocal accum
            accum = q_mult(accum, rot_x)
            accum = q_mult(accum, rot_y)
            # print(accum)

            glMatrixMode(GL_MODELVIEW)
            glLoadMatrixf(q_to_mat4(accum))
            glScalef(zoom, zoom, zoom)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.draw_cube()
            # Draw the text onto the screen
            if self.text:
                self.screen.blit(self.text, (500, 500))
            # glutSolidSphere(3.0, 50, 50);
            # draw_face()
            # self.draw_axis()
            if not self._reverse:
                pygame.display.flip()
            
            #make pygame slower    

        # for v in left_face:
        #     print(v)


        # Set the font and font size
        font_name = "Arial"
        font_size = 36
        font = pygame.font.SysFont(font_name, font_size)

        # Set the text message
        text_message = "Let's Solve the Cube!"

        # Render the text to a surface
        self.text= font.render(text_message, True, (0, 255, 0))

        # Get the size of the text surface
        text_width, text_height = self.text.get_size()

        # Draw the text onto the screen
        self.screen.blit(self.text, (50, 50))

        while True:
    
            theta_inc = 7
            theta = pi / 2 / theta_inc
            for event in pygame.event.get():
                #check if enter is pressed

                if event.type == pygame.QUIT:
                
                    pygame.quit()
                    quit()
                    # elif event.type == VIDEORESIZE:
                    # self.CreateWindow(event.w, event.h)
                    # update()
                pygame.event.clear()
                if self._reverse:
                    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)) #add the event to the queue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            move = self.movements.pop(0)

                            # Set the text message
                            text_message = str(move)

                            # Render the text to a surface
                            text_surface = font.render(text_message, True, (0, 0, 0))

                            # Get the size of the text surface
                            text_width, text_height = text_surface.get_size()

                            self.last_moves.append(move)
                            reverse = False
                            if len(move) == 2:
                                move = move[0]
                                reverse = True

                        except IndexError:
                            print("No more moves")
                            self._reverse = False
                            self.movements = _save_moves
                            self.last_moves = []
                            break
                        try:
                            # Rotating about the x axis
                            if event.key == pygame.K_UP:  # or event.key == pygame.K_w:
                                inc_x = pi / 100
                            if event.key == pygame.K_DOWN:  # or event.key == pygame.K_s:
                                inc_x = -pi / 100

                            # Rotating about the y axis
                            if event.key == pygame.K_LEFT:  # or event.key == pygame.K_a:
                                inc_y = pi / 100
                            if event.key == pygame.K_RIGHT:  # or event.key == pygame.K_d:
                                inc_y = -pi / 100
                        except:
                            pass

                        move, moves, theta, theta_inc, reverse = self.animate(move, moves, theta, theta_inc, reverse)

                    if event.key == pygame.K_BACKSPACE:
                        if len(self.last_moves) == 0:
                            continue
                        last_move = self.last_moves.pop(-1)
                        # Set the text message
                        text_message = str(move)

                        # Render the text to a surface
                        text_surface = font.render(text_message, True, (0, 0, 0))

                        # Get the size of the text surface
                        text_width, text_height = text_surface.get_size()
                        self.movements.insert(0, last_move)
                        move = self.reverse_moves[last_move]
                        reverse = False
                        if len(move) == 2:
                            move = move[0]
                            reverse = True
                        move, moves, theta, theta_inc, reverse = self.animate(move, moves, theta, theta_inc, reverse)


                    # if event.key == pygame.K_e:
                    #     pad_toggle = not pad_toggle

                    # Reset to default view
                    if event.key == pygame.K_SPACE:
                        inc_x = 0
                        inc_y = 0
                        accum = (1, 0, 0, 0)
                        zoom = 1
        
                    if event.type == pygame.KEYUP:
                        # Stoping rotation
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN or \
                                        event.key == pygame.K_w or event.key == pygame.K_s:
                            inc_x = 0.0
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                                        event.key == pygame.K_a or event.key == pygame.K_d or \
                                        event.key == pygame.K_l or event.key == pygame.K_f:
                            inc_y = 0.0

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Increase scale (zoom) value
                        if event.button == 4 and zoom < 1.6 and not (reverse):
                            zoom += 0.05
                            # print('scroll up', zoom)
                        if event.button == 5 and zoom > 0.3 and not (reverse):
                            zoom -= 0.05
            

            # Get relative movement of mouse coordinates and update x and y incs
            if pygame.mouse.get_pressed()[0] == 1:
                (tmp_x, tmp_y) = pygame.mouse.get_rel()
                # print(tmp_x, tmp_y)
                inc_x = -tmp_y * pi / 450
                inc_y = -tmp_x * pi / 450

            if pad_toggle and abs(center_pieces[0][0][2]) <= 6:
                padding(0.3)
            elif abs(center_pieces[0][0][2]) > 3.3 and not pad_toggle:
                padding(-0.3)

            update()
            sys.stdout.flush()

            

    def draw_cube(self):

        glLineWidth(GLfloat(6.0))
        glBegin(GL_LINES)
        glColor3fv((0.0, 0.0, 0.0))

        for axis in edge_pieces:
            for piece in axis:
                for edge in cube_edges:
                    for vertex in edge:
                        glVertex3fv(piece[vertex])
        for piece in center_pieces:
            for edge in cube_edges:
                for vertex in edge:
                    glVertex3fv(piece[vertex])
        for piece in corner_pieces:
            for edge in cube_edges:
                for vertex in edge:
                    glVertex3fv(piece[vertex])
        glEnd()
        self.draw_stickers()
    #TODO: Fix stickers to match initial cube
    def draw_stickers(self):
        glBegin(GL_QUADS)
        i = 0
        for color, surface in zip(cube_colors, cube_surfaces):
            glColor3fv((color))
            for vertex in surface:
                glVertex3fv(center_pieces[i][vertex])
            j = 0
            for piece in center_pieces:
                glColor3fv((0, 0, 0))
                for vertex in surface:
                    glVertex3fv(center_pieces[j][vertex])
                j += 1
            i += 1

        for color, surface, face in zip(cube_colors, cube_surfaces, edges):
            glColor3fv((color))
            for piece in face:
                for vertex in surface:
                    glVertex3fv(edge_pieces[piece[0]][piece[1]][vertex])

        # Black inner sides of edge pieces
        edge_black_pat = [
            [0, 1, 2, 3, 4, 5],
            [0, 1, 2, 3, 4, 5],
            [0, 1, 2, 3, 4, 5]
            # [4, 5],
            # [0, 2]
        ]

        glColor3fv((0, 0, 0))

        for i in range(len(edge_black_pat)):
            for face in edge_black_pat[i]:
                for piece in edge_pieces[i]:
                    for vertex in cube_surfaces[face]:
                        glVertex3fv(piece[vertex])

        corner_color_pat = [
            [0, 1, 5],  # 0
            [0, 1, 4],  # 1
            [0, 3, 4],  # 2
            [0, 3, 5],  # 3
            [2, 1, 5],  # 4
            [2, 1, 4],  # 5
            [2, 3, 4],  # 6
            [2, 3, 5],  # 7
        ]

        corner_black_pat = [
            [2, 3, 4],  # 0
            [2, 3, 5],  # 1
            [2, 1, 5],  # 2
            [2, 1, 4],  # 3
            [0, 3, 4],  # 4
            [0, 3, 5],  # 5
            [0, 1, 5],  # 6
            [0, 1, 4],  # 7
        ]

        for i in range(len(corner_color_pat)):
            for face in corner_color_pat[i]:
                glColor3fv((cube_colors[face]))
                for vertex in cube_surfaces[face]:
                    glVertex3fv(corner_pieces[i][vertex])
        glColor3fv((0, 0, 0))
        for i in range(len(corner_black_pat)):
            for face in corner_black_pat[i]:
                for vertex in cube_surfaces[face]:
                    glVertex3fv(corner_pieces[i][vertex])

        glEnd()

    def draw_axis(self):
        glLineWidth(GLfloat(1.0))
        glBegin(GL_LINES)

        for color, axis in zip(axis_colors, axes):
            glColor3fv(color)
            for point in axis:
                glVertex3fv(axis_verts[point])
        glEnd()
