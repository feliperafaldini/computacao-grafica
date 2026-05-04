import math
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

WIDTH = 800
HEIGHT = 600

def get_color():
    return [random.uniform(0.5, 1.0) for _ in range(3)]

def draw_cube():
    vertices = [
        [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1],
        [1, -1, 1], [1, 1, 1], [-1, -1, 1], [-1, 1, 1]
    ]
    
    faces = [
        (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
        (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
    ]
    
    normals = [
        (0, 0, -1), (-1, 0, 0), (0, 0, 1),
        (1, 0, 0), (0, 1, 0), (0, -1, 0)
    ]

    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glNormal3fv(normals[i])
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    light_pos = [5.0, 5.0, 5.0, 1.0]
    ambient = [0.2, 0.2, 0.2, 1.0]
    diffuse = [1.0, 1.0, 1.0, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)

def main():
    pygame.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Projeto")

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)    
    glTranslatef(0.0, 0.0, -18) 

    glEnable(GL_DEPTH_TEST)
    setup_lighting()

    LIMIT_X = 8.0
    LIMIT_Y = 6.0

    cube_pos = [random.uniform(-LIMIT_X + 1, LIMIT_X -1), random.uniform(-LIMIT_Y + 1, LIMIT_Y - 1), 0.0]
    cube_vel = [0.1, 0.07, 0.0]
    cube_color = get_color()

    rotation_x = 0
    rotation_y = 0

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    rotation_y += event.rel[0]
                    rotation_x -= event.rel[1]

        cube_pos[0] += cube_vel[0]
        cube_pos[1] += cube_vel[1]

        if abs(cube_pos[0]) > LIMIT_X:
            cube_vel[0] *= -1 * random.uniform(0.9, 1.1)
            cube_color = get_color()

        if abs(cube_pos[1]) > LIMIT_Y:
            cube_vel[1] *= -1 * random.uniform(0.9, 1.1)
            cube_color = get_color()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glTranslatef(cube_pos[0], cube_pos[1], 0)
        glRotatef(pygame.time.get_ticks() * 0.1, 1, 1, 1)
        glColor3f(cube_color[0], cube_color[1], cube_color[2])
        draw_cube()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(4, 0, 0)
        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)
        glColor3f(0.4, 0.4, 1.0)
        draw_cube()
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()