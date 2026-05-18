import math
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

WIDTH  = 800
HEIGHT = 600

LIMIT_X = 10.0
LIMIT_Y = 7.0

PADDLE_W = 0.4
PADDLE_D = 0.4
BALL_RADIUS = 0.45

PADDLE_SPEED    = 0.15
BALL_SPEED_INIT = 0.12

PADDLE_H_DEFAULT = 1.5
PADDLE_H_MIN     = 0.3
PADDLE_H_PENALTY = 0.3

QUESTIONS = [
    {"q": "Qual funcao OpenGL ativa o teste de profundidade?",
     "options": ["glEnable(GL_DEPTH_TEST)", "glDepthFunc(GL_LESS)", "glClear(GL_DEPTH_BUFFER_BIT)", "glDepthMask(GL_TRUE)"],
     "answer": "glEnable(GL_DEPTH_TEST)"},

    {"q": "O que faz gluPerspective?",
     "options": ["Define a matriz de projecao perspectiva", "Move a camera no espaco", "Aplica uma textura", "Configura a iluminacao"],
     "answer": "Define a matriz de projecao perspectiva"},

    {"q": "Qual primitiva OpenGL desenha um quadrilatero?",
     "options": ["GL_TRIANGLES", "GL_QUADS", "GL_POLYGON", "GL_LINES"],
     "answer": "GL_QUADS"},

    {"q": "O que e o Z-buffer?",
     "options": ["Buffer de cor da cena", "Buffer que armazena profundidade por pixel", "Buffer de vertices", "Buffer de normais"],
     "answer": "Buffer que armazena profundidade por pixel"},

    {"q": "Qual chamada salva a matriz atual na pilha?",
     "options": ["glLoadIdentity()", "glPushMatrix()", "glPopMatrix()", "glMatrixMode()"],
     "answer": "glPushMatrix()"},

    {"q": "glTranslatef(2,0,0) move o objeto em qual eixo?",
     "options": ["Y", "Z", "X", "Nenhum"],
     "answer": "X"},

    {"q": "O que e uma normal de superficie?",
     "options": ["Vetor perpendicular a superficie", "Vetor tangente a curva", "Coordenada de textura", "Cor do fragmento"],
     "answer": "Vetor perpendicular a superficie"},

    {"q": "Qual modelo de iluminacao considera reflexao especular?",
     "options": ["Lambert", "Phong", "Gouraud apenas", "Flat shading"],
     "answer": "Phong"},

    {"q": "O que e rasterizacao?",
     "options": ["Converter geometria vetorial em pixels", "Carregar texturas na GPU", "Calcular sombras em tempo real", "Definir vertices de um mesh"],
     "answer": "Converter geometria vetorial em pixels"},

    {"q": "GL_COLOR_BUFFER_BIT em glClear limpa o que?",
     "options": ["Buffer de profundidade", "Buffer de cor (framebuffer)", "Buffer de stencil", "Buffer de vertices"],
     "answer": "Buffer de cor (framebuffer)"},

    {"q": "O que e uma matriz de projecao ortografica?",
     "options": ["Projecao que preserva paralelismo, sem perspectiva", "Projecao com ponto de fuga", "Matriz identidade", "Matriz de rotacao"],
     "answer": "Projecao que preserva paralelismo, sem perspectiva"},

    {"q": "Qual eixo aponta 'para fora da tela' no OpenGL padrao?",
     "options": ["X positivo", "Y positivo", "Z positivo", "Z negativo"],
     "answer": "Z positivo"},

    {"q": "O que e texture mapping?",
     "options": ["Projetar uma imagem sobre uma superficie 3D", "Calcular normais automaticamente", "Converter sRGB para linear", "Subdiviir malhas poligonais"],
     "answer": "Projetar uma imagem sobre uma superficie 3D"},

    {"q": "Qual componente de luz nao depende do angulo de visao?",
     "options": ["Especular", "Difusa", "Ambiente", "Emissiva"],
     "answer": "Ambiente"},

    {"q": "glRotatef(90, 0, 1, 0) rotaciona em torno de qual eixo?",
     "options": ["X", "Y", "Z", "Diagonal"],
     "answer": "Y"},

    {"q": "O que e backface culling?",
     "options": ["Remover faces voltadas para longe da camera", "Suavizar normais do mesh", "Criar sombras projetadas", "Calcular MIP maps"],
     "answer": "Remover faces voltadas para longe da camera"},

    {"q": "Qual e a ordem padrao das multiplicacoes de matrizes em OpenGL (legado)?",
     "options": ["Model -> View -> Projection", "Projection -> View -> Model", "View -> Model -> Projection", "Nenhuma ordem fixa"],
     "answer": "Model -> View -> Projection"},

    {"q": "O que faz gluLookAt?",
     "options": ["Define posicao e orientacao da camera", "Carrega uma textura", "Cria uma luz pontual", "Aplica transformacao de escala"],
     "answer": "Define posicao e orientacao da camera"},

    {"q": "Qual funcao cria uma esfera em GLU?",
     "options": ["gluCylinder()", "gluSphere()", "glutSolidSphere()", "glSphere()"],
     "answer": "gluSphere()"},

    {"q": "O que e um fragment shader?",
     "options": ["Programa que processa cada pixel/fragmento", "Programa que processa cada vertice", "Rotina que carrega geometria", "Funcao de colisao na CPU"],
     "answer": "Programa que processa cada pixel/fragmento"},

    {"q": "O que e o espaco de coordenadas NDC?",
     "options": ["Normalized Device Coordinates: cubo [-1,1]^3", "Normal Direction Cube", "Node Data Container", "Near-Distance Clipping"],
     "answer": "Normalized Device Coordinates: cubo [-1,1]^3"},

    {"q": "Qual primitive mode desenha triangulos independentes?",
     "options": ["GL_TRIANGLE_STRIP", "GL_TRIANGLE_FAN", "GL_TRIANGLES", "GL_QUADS"],
     "answer": "GL_TRIANGLES"},

    {"q": "O que e um VBO (Vertex Buffer Object)?",
     "options": ["Buffer na GPU para armazenar dados de vertices", "Variavel uniforme no shader", "Objeto de framebuffer", "Estrutura de textura"],
     "answer": "Buffer na GPU para armazenar dados de vertices"},

    {"q": "Qual tecnica suaviza arestas entre poligonos adjacentes?",
     "options": ["Flat shading", "Gouraud shading", "Wireframe", "Depth sorting"],
     "answer": "Gouraud shading"},

    {"q": "O que e anti-aliasing?",
     "options": ["Tecnica para reduzir serrilhado em bordas", "Compressao de texturas", "Calculo de sombras suaves", "Projecao paralela"],
     "answer": "Tecnica para reduzir serrilhado em bordas"},
]


def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_POSITION, [6.0, 10.0, 8.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.15, 0.15, 0.15, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])


def draw_box(sx, sy, sz):
    v = [
        [ sx, -sy, -sz], [ sx,  sy, -sz], [-sx,  sy, -sz], [-sx, -sy, -sz],
        [ sx, -sy,  sz], [ sx,  sy,  sz], [-sx, -sy,  sz], [-sx,  sy,  sz],
    ]
    faces   = [(0,1,2,3),(3,2,7,6),(6,7,5,4),(4,5,1,0),(1,5,7,2),(4,0,3,6)]
    normals = [(0,0,-1),(-1,0,0),(0,0,1),(1,0,0),(0,1,0),(0,-1,0)]
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glNormal3fv(normals[i])
        for idx in face:
            glVertex3fv(v[idx])
    glEnd()


def draw_sphere():
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, BALL_RADIUS, 32, 32)
    gluDeleteQuadric(quad)


def draw_field_lines():
    glDisable(GL_LIGHTING)
    glColor3f(0.25, 0.25, 0.35)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex3f(-LIMIT_X, -LIMIT_Y, 0); glVertex3f(LIMIT_X, -LIMIT_Y, 0)
    glVertex3f(-LIMIT_X,  LIMIT_Y, 0); glVertex3f(LIMIT_X,  LIMIT_Y, 0)
    glEnd()
    glColor3f(0.18, 0.18, 0.26)
    glLineWidth(1.5)
    glBegin(GL_LINES)
    y, seg = -LIMIT_Y, 0.6
    while y < LIMIT_Y:
        glVertex3f(0, y, 0)
        glVertex3f(0, min(y + seg, LIMIT_Y), 0)
        y += seg * 2
    glEnd()
    glEnable(GL_LIGHTING)


def render_surface_2d(surface, x, y):
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix(); glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix(); glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    data = pygame.image.tostring(surface, "RGBA", True)
    tw, th = surface.get_size()
    glRasterPos2i(x, y)
    glDrawPixels(tw, th, GL_RGBA, GL_UNSIGNED_BYTE, data)

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION); glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING)


def draw_paddle_bars(paddle_h_l, paddle_h_r, font_small):
    def bar(current_h, bar_x, label):
        ratio  = max(0.0, current_h / PADDLE_H_DEFAULT)
        bar_w, bar_h = 90, 11
        filled = int(bar_w * ratio)
        color  = (80, 220, 120) if ratio > 0.6 else (220, 180, 50) if ratio > 0.3 else (220, 60, 60)

        bg = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
        bg.fill((30, 30, 50, 200))
        render_surface_2d(bg, bar_x, 20)

        if filled > 0:
            fg = pygame.Surface((filled, bar_h), pygame.SRCALPHA)
            fg.fill((*color, 230))
            render_surface_2d(fg, bar_x, 20)

        lbl = font_small.render(label, True, (150, 150, 185))
        render_surface_2d(lbl, bar_x, 35)

    bar(paddle_h_l, 28,          "P1 paddle")
    bar(paddle_h_r, WIDTH - 122, "P2 paddle")


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def reset_ball():
    angle     = random.uniform(-25, 25)
    direction = random.choice([-1, 1])
    rad = math.radians(angle)
    return [0.0, 0.0, 0.0], [direction * BALL_SPEED_INIT * math.cos(rad),
                               BALL_SPEED_INIT * math.sin(rad), 0.0]


def check_paddle_collision(ball_pos, ball_vel, paddle_x, paddle_y, paddle_h):
    if (abs(ball_pos[0] - paddle_x) < PADDLE_W + BALL_RADIUS and
            abs(ball_pos[1] - paddle_y) < paddle_h + BALL_RADIUS):
        hit_offset = (ball_pos[1] - paddle_y) / paddle_h
        angle  = hit_offset * 65
        speed  = min(math.hypot(ball_vel[0], ball_vel[1]) * random.uniform(1.03, 1.07),
                     BALL_SPEED_INIT * 3.2)
        rad    = math.radians(angle)
        new_vx = math.copysign(speed * math.cos(rad), -ball_vel[0])
        new_vy = speed * math.sin(rad)
        return True, [new_vx, new_vy, 0.0]
    return False, ball_vel


def show_question_popup(question_data, scorer_name, loser_name):
    font_title = pygame.font.SysFont("monospace", 19, bold=True)
    font_q     = pygame.font.SysFont("monospace", 15, bold=True)
    font_opt   = pygame.font.SysFont("monospace", 14)

    box_w, box_h = 520, 300
    box_x = (WIDTH  - box_w) // 2
    box_y = (HEIGHT - box_h) // 2

    options  = question_data["options"]
    selected = 0
    answered = False
    correct  = False
    result_timer = 0
    clock = pygame.time.Clock()

    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix(); glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix(); glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()
            if not answered and event.type == KEYDOWN:
                if event.key in (K_UP, K_w):
                    selected = (selected - 1) % len(options)
                if event.key in (K_DOWN, K_s):
                    selected = (selected + 1) % len(options)
                if event.key in (K_RETURN, K_SPACE):
                    answered     = True
                    correct      = (options[selected] == question_data["answer"])
                    result_timer = 100

        if answered:
            result_timer -= 1
            if result_timer <= 0:
                running = False

        s = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        s.fill((14, 14, 26, 240))
        pygame.draw.rect(s, (70, 70, 130), (0, 0, box_w, box_h), 2, border_radius=8)

        title_col = (90, 195, 255) if "1" in scorer_name else (255, 135, 55)
        t = font_title.render(f"{scorer_name} marcou ponto!", True, title_col)
        s.blit(t, ((box_w - t.get_width()) // 2, 13))

        sub = font_opt.render(f"Pergunta para {loser_name} — erre e seu paddle encolhe:", True, (140, 140, 180))
        s.blit(sub, ((box_w - sub.get_width()) // 2, 36))

        words  = question_data["q"].split()
        lines, line = [], ""
        for w in words:
            test = (line + " " + w).strip()
            if font_q.size(test)[0] < box_w - 40:
                line = test
            else:
                lines.append(line); line = w
        if line:
            lines.append(line)

        qy = 60
        for ql in lines:
            qs = font_q.render(ql, True, (225, 225, 225))
            s.blit(qs, ((box_w - qs.get_width()) // 2, qy))
            qy += 20

        opt_y = qy + 8
        for i, opt in enumerate(options):
            is_sel = (i == selected)
            if answered:
                if opt == question_data["answer"]:
                    col, bg_col = (60, 220, 100),  (18, 55, 28, 210)
                elif is_sel:
                    col, bg_col = (220, 60,  60),  (55, 18, 18, 210)
                else:
                    col, bg_col = (110, 110, 130), (28, 28, 42, 180)
            else:
                col    = (230, 225, 90) if is_sel else (175, 175, 200)
                bg_col = (48, 48, 78, 210) if is_sel else (28, 28, 42, 180)

            row = pygame.Surface((box_w - 36, 26), pygame.SRCALPHA)
            row.fill(bg_col)
            s.blit(row, (18, opt_y - 3))
            marker = "> " if is_sel and not answered else "  "
            s.blit(font_opt.render(f"{marker}[{chr(65+i)}] {opt}", True, col), (26, opt_y))
            opt_y += 32

        if answered:
            msg = "Correto! Paddle intacto." if correct else "Errado! Paddle encolheu."
            col = (70, 215, 95) if correct else (215, 70, 70)
            rs  = font_q.render(msg, True, col)
            s.blit(rs, ((box_w - rs.get_width()) // 2, box_h - 30))
        else:
            hint = font_opt.render("W / S  para mover   |   ENTER para confirmar", True, (70, 70, 105))
            s.blit(hint, ((box_w - hint.get_width()) // 2, box_h - 20))

        data = pygame.image.tostring(s, "RGBA", True)
        glRasterPos2i(box_x, HEIGHT - box_y - box_h)
        glDrawPixels(box_w, box_h, GL_RGBA, GL_UNSIGNED_BYTE, data)

        pygame.display.flip()
        clock.tick(60)

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION); glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING)

    return correct


def show_victory_screen(winner_name):
    font_big  = pygame.font.SysFont("monospace", 36, bold=True)
    font_sub  = pygame.font.SysFont("monospace", 18)

    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix(); glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix(); glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()
            if event.type == KEYDOWN and event.key in (K_RETURN, K_ESCAPE, K_SPACE):
                running = False

        glClearColor(0.04, 0.04, 0.10, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        box_w, box_h = 440, 160
        box_x = (WIDTH  - box_w) // 2
        box_y = (HEIGHT - box_h) // 2

        s = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        s.fill((14, 14, 30, 245))
        pygame.draw.rect(s, (100, 100, 180), (0, 0, box_w, box_h), 2, border_radius=10)

        col = (90, 195, 255) if "1" in winner_name else (255, 135, 55)
        title = font_big.render(f"{winner_name} VENCEU!", True, col)
        s.blit(title, ((box_w - title.get_width()) // 2, 38))

        sub = font_sub.render("O paddle do adversario chegou ao limite.", True, (170, 170, 200))
        s.blit(sub, ((box_w - sub.get_width()) // 2, 90))

        hint = font_sub.render("ENTER para sair", True, (80, 80, 120))
        s.blit(hint, ((box_w - hint.get_width()) // 2, 124))

        data = pygame.image.tostring(s, "RGBA", True)
        glRasterPos2i(box_x, HEIGHT - box_y - box_h)
        glDrawPixels(box_w, box_h, GL_RGBA, GL_UNSIGNED_BYTE, data)

        pygame.display.flip()
        clock.tick(60)

    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION); glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING)


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Pong 3D")

    font_small = pygame.font.SysFont("monospace", 12)

    gluPerspective(45, WIDTH / HEIGHT, 0.1, 80.0)
    glTranslatef(0.0, 0.0, -22)
    glEnable(GL_DEPTH_TEST)
    setup_lighting()

    PADDLE_X_L = -(LIMIT_X - 1.0)
    PADDLE_X_R =   LIMIT_X - 1.0

    paddle_l_y = 0.0
    paddle_r_y = 0.0
    paddle_h_l = PADDLE_H_DEFAULT
    paddle_h_r = PADDLE_H_DEFAULT

    ball_pos, ball_vel = reset_ball()
    ball_rot   = [0.0, 0.0, 0.0]
    goal_flash = 0
    used_qs    = []

    clock   = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[K_w]:    paddle_l_y += PADDLE_SPEED
        if keys[K_s]:    paddle_l_y -= PADDLE_SPEED
        if keys[K_UP]:   paddle_r_y += PADDLE_SPEED
        if keys[K_DOWN]: paddle_r_y -= PADDLE_SPEED

        paddle_l_y = clamp(paddle_l_y, -(LIMIT_Y - paddle_h_l), LIMIT_Y - paddle_h_l)
        paddle_r_y = clamp(paddle_r_y, -(LIMIT_Y - paddle_h_r), LIMIT_Y - paddle_h_r)

        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
        ball_rot[0] += ball_vel[1] * 5
        ball_rot[1] += ball_vel[0] * 5

        if ball_pos[1] > LIMIT_Y - BALL_RADIUS:
            ball_pos[1] = LIMIT_Y - BALL_RADIUS; ball_vel[1] *= -1
        if ball_pos[1] < -(LIMIT_Y - BALL_RADIUS):
            ball_pos[1] = -(LIMIT_Y - BALL_RADIUS); ball_vel[1] *= -1

        if ball_vel[0] < 0:
            hit, ball_vel = check_paddle_collision(ball_pos, ball_vel, PADDLE_X_L, paddle_l_y, paddle_h_l)
            if hit:
                ball_pos[0] = PADDLE_X_L + PADDLE_W + BALL_RADIUS + 0.01

        if ball_vel[0] > 0:
            hit, ball_vel = check_paddle_collision(ball_pos, ball_vel, PADDLE_X_R, paddle_r_y, paddle_h_r)
            if hit:
                ball_pos[0] = PADDLE_X_R - PADDLE_W - BALL_RADIUS - 0.01

        def pick_q():
            pool = [q for q in QUESTIONS if q not in used_qs]
            if not pool:
                used_qs.clear()
                pool = QUESTIONS[:]
            q = random.choice(pool)
            used_qs.append(q)
            return q

        if ball_pos[0] > LIMIT_X:
            goal_flash = 20
            correct = show_question_popup(pick_q(), "Jogador 1", "Jogador 2")
            if not correct:
                paddle_h_r = max(PADDLE_H_MIN, paddle_h_r - PADDLE_H_PENALTY)
                if paddle_h_r <= PADDLE_H_MIN:
                    show_victory_screen("Jogador 1")
                    running = False
            ball_pos, ball_vel = reset_ball()

        if ball_pos[0] < -LIMIT_X:
            goal_flash = 20
            correct = show_question_popup(pick_q(), "Jogador 2", "Jogador 1")
            if not correct:
                paddle_h_l = max(PADDLE_H_MIN, paddle_h_l - PADDLE_H_PENALTY)
                if paddle_h_l <= PADDLE_H_MIN:
                    show_victory_screen("Jogador 2")
                    running = False
            ball_pos, ball_vel = reset_ball()

        if goal_flash > 0:
            goal_flash -= 1

        glClearColor(*(0.05, 0.05, 0.10, 1.0) if goal_flash == 0 else (0.13, 0.04, 0.04, 1.0))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_field_lines()

        glPushMatrix()
        glTranslatef(PADDLE_X_L, paddle_l_y, 0)
        glColor3f(0.2, 0.8, 1.0)
        draw_box(PADDLE_W, paddle_h_l, PADDLE_D)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(PADDLE_X_R, paddle_r_y, 0)
        glColor3f(1.0, 0.5, 0.1)
        draw_box(PADDLE_W, paddle_h_r, PADDLE_D)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(ball_pos[0], ball_pos[1], 0)
        glRotatef(ball_rot[0], 1, 0, 0)
        glRotatef(ball_rot[1], 0, 1, 0)
        glColor3f(1.0, 1.0, 1.0)
        draw_sphere()
        glPopMatrix()

        draw_paddle_bars(paddle_h_l, paddle_h_r, font_small)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()