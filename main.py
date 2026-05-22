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

PADDLE_R        = 0.42
PADDLE_H_DEFAULT = 1.5
PADDLE_H_MIN     = 0.3
PADDLE_H_PENALTY = 0.3
MAX_PENALTIES    = 4

BALL_RADIUS     = 0.45
PADDLE_SPEED    = 0.18
BALL_SPEED_INIT = 0.15

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
    {"q": "Qual chamada salva a matriz atual na pilha OpenGL?",
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
    {"q": "O que e uma projecao ortografica?",
     "options": ["Preserva paralelismo, sem perspectiva", "Projecao com ponto de fuga", "Matriz identidade", "Matriz de rotacao"],
     "answer": "Preserva paralelismo, sem perspectiva"},
    {"q": "Qual eixo aponta para fora da tela no OpenGL padrao?",
     "options": ["X positivo", "Y positivo", "Z positivo", "Z negativo"],
     "answer": "Z positivo"},
    {"q": "O que e texture mapping?",
     "options": ["Projetar uma imagem sobre uma superficie 3D", "Calcular normais automaticamente", "Converter sRGB para linear", "Subdividir malhas poligonais"],
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
    {"q": "Ordem padrao de transformacoes em OpenGL legado?",
     "options": ["Model > View > Projection", "Projection > View > Model", "View > Model > Projection", "Nenhuma ordem fixa"],
     "answer": "Model > View > Projection"},
    {"q": "O que faz gluLookAt?",
     "options": ["Define posicao e orientacao da camera", "Carrega uma textura", "Cria uma luz pontual", "Aplica escala"],
     "answer": "Define posicao e orientacao da camera"},
    {"q": "Qual funcao cria uma esfera em GLU?",
     "options": ["gluCylinder()", "gluSphere()", "glutSolidSphere()", "glSphere()"],
     "answer": "gluSphere()"},
    {"q": "O que e um fragment shader?",
     "options": ["Processa cada pixel/fragmento", "Processa cada vertice", "Carrega geometria", "Funcao de colisao na CPU"],
     "answer": "Processa cada pixel/fragmento"},
    {"q": "O que significa NDC em computacao grafica?",
     "options": ["Normalized Device Coordinates", "Normal Direction Cube", "Node Data Container", "Near-Distance Clipping"],
     "answer": "Normalized Device Coordinates"},
    {"q": "Qual modo desenha triangulos independentes?",
     "options": ["GL_TRIANGLE_STRIP", "GL_TRIANGLE_FAN", "GL_TRIANGLES", "GL_QUADS"],
     "answer": "GL_TRIANGLES"},
    {"q": "O que e um VBO?",
     "options": ["Buffer na GPU para vertices", "Variavel uniforme no shader", "Objeto de framebuffer", "Estrutura de textura"],
     "answer": "Buffer na GPU para vertices"},
    {"q": "Qual tecnica suaviza arestas entre poligonos adjacentes?",
     "options": ["Flat shading", "Gouraud shading", "Wireframe", "Depth sorting"],
     "answer": "Gouraud shading"},
    {"q": "O que e anti-aliasing?",
     "options": ["Reduz serrilhado em bordas", "Comprime texturas", "Calcula sombras suaves", "Projecao paralela"],
     "answer": "Reduz serrilhado em bordas"},
    {"q": "O que e mipmapping?",
     "options": ["Pre-calcular texturas em multiplas resolucoes", "Tecnica de sombras suaves", "Compressao de geometria", "Subdivisao de malha"],
     "answer": "Pre-calcular texturas em multiplas resolucoes"},
    {"q": "O que e clipping em computacao grafica?",
     "options": ["Remover partes fora do volume de visao", "Recortar texturas", "Reduzir poligonos", "Filtrar ruido na imagem"],
     "answer": "Remover partes fora do volume de visao"},
    {"q": "O que representa a matriz Model em OpenGL?",
     "options": ["Transformacoes do objeto no mundo", "Posicao da camera", "Projecao na tela", "Cor do material"],
     "answer": "Transformacoes do objeto no mundo"},
    {"q": "O que e ray tracing?",
     "options": ["Simular raios de luz para renderizacao realista", "Tecnica de compressao de malhas", "Algoritmo de busca em grafos", "Metodo de suavizacao de texturas"],
     "answer": "Simular raios de luz para renderizacao realista"},
    {"q": "O que e o pipeline grafico?",
     "options": ["Sequencia de etapas para transformar 3D em 2D", "Ferramenta de modelagem 3D", "Linguagem de shader", "Biblioteca de matematica"],
     "answer": "Sequencia de etapas para transformar 3D em 2D"},
    {"q": "Qual componente Phong depende do angulo entre reflexo e visao?",
     "options": ["Ambiente", "Difuso", "Especular", "Emissivo"],
     "answer": "Especular"},
    {"q": "O que e um mesh poligonal?",
     "options": ["Conjunto de vertices, arestas e faces", "Imagem de textura", "Buffer de sombra", "Programa de shader"],
     "answer": "Conjunto de vertices, arestas e faces"},
    {"q": "Para que serve glScalef?",
     "options": ["Escalar um objeto nos eixos X, Y, Z", "Mover o objeto", "Rotacionar o objeto", "Projetar na tela"],
     "answer": "Escalar um objeto nos eixos X, Y, Z"},
    {"q": "O que e depth testing?",
     "options": ["Verificar qual fragmento esta mais proximo da camera", "Testar se texturas carregaram", "Checar colisoes fisicas", "Validar normais da malha"],
     "answer": "Verificar qual fragmento esta mais proximo da camera"},
]

TEX_BALL   = None
TEX_PADDLE = None
TEX_FIELD  = None


def upload_texture(pixels, w, h):
    tid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tid)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes(pixels))
    return tid


def clamp_byte(v):
    return min(255, max(0, int(v)))


def make_metal_texture(size=128):
    pixels = []
    for y in range(size):
        for x in range(size):
            streak = math.sin((y / size) * math.pi * 18) * 22
            grain  = random.randint(-6, 6)
            base   = 185
            v = int(min(255, max(120, base + streak + grain)))
            hi = min(255, v + 30)
            pixels += [v, v, hi, 255]
    return pixels, size, size


def make_air_hockey_field(w=256, h=256):
    pixels = []
    cx, cy = w / 2, h / 2
    for y in range(h):
        for x in range(w):
            nx = (x - cx) / cx
            ny = (y - cy) / cy

            dist_center = math.sqrt(nx*nx + ny*ny)
            glow = max(0.0, 1.0 - dist_center * 1.1)

            base_r = int(10  + glow * 18)
            base_g = int(18  + glow * 38)
            base_b = int(48  + glow * 80)

            # Reflexo radial suave
            radial = math.sin(dist_center * math.pi * 3) * 0.5 + 0.5
            spec   = int(radial * 12)

            # Linhas de grade finas (air hockey tem linhas de brilho)
            grid_x = abs(math.sin(nx * math.pi * 14)) ** 16
            grid_y = abs(math.sin(ny * math.pi * 10)) ** 16
            grid   = int((grid_x + grid_y) * 14)

            r = min(255, base_r + spec + grid)
            g = min(255, base_g + spec + grid)
            b = min(255, base_b + spec + grid + 10)

            # Circulo central
            if 0.08 < dist_center < 0.11:
                r, g, b = min(255, r+40), min(255, g+60), min(255, b+90)

            # Linha central vertical (nx perto de 0)
            if abs(nx) < 0.008:
                r, g, b = min(255, r+30), min(255, g+50), min(255, b+80)

            pixels += [r, g, b, 255]
    return pixels, w, h


def make_ball_texture(size=64):
    pixels = []
    for y in range(size):
        for x in range(size):
            nx = (x / size) * 2 - 1
            ny = (y / size) * 2 - 1
            v  = 200 + math.sin(nx * 6) * 25 + math.cos(ny * 6) * 25
            v  = v + random.randint(-8, 8)
            r  = clamp_byte(v)
            g  = clamp_byte(v)
            b  = clamp_byte(v + 10)
            pixels += [r, g, b, 255]
    return pixels, size, size


def init_textures():
    global TEX_BALL, TEX_PADDLE, TEX_FIELD
    mp, mw, mh = make_metal_texture(128)
    TEX_PADDLE = upload_texture(mp, mw, mh)
    fp, fw, fh = make_air_hockey_field(256, 256)
    TEX_FIELD  = upload_texture(fp, fw, fh)
    bp, bw, bh = make_ball_texture(64)
    TEX_BALL   = upload_texture(bp, bw, bh)


def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 14.0, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [0.22, 0.22, 0.26, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [0.95, 0.95, 1.00, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.00, 1.00, 1.00, 1.0])

    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 10.0, 8.0, 1.0])
    glLightfv(GL_LIGHT1, GL_AMBIENT,  [0.04, 0.04, 0.06, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  [0.28, 0.30, 0.38, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.40, 0.40, 0.50, 1.0])

    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR,  [0.90, 0.92, 0.95, 1.0])
    glMaterialf (GL_FRONT_AND_BACK, GL_SHININESS, 80.0)


def draw_capsule_paddle(radius, half_h, segs=24):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, TEX_PADDLE)

    body_h = half_h - radius
    body_h = max(body_h, 0.0)

    glBegin(GL_QUAD_STRIP)
    for i in range(segs + 1):
        a   = 2 * math.pi * i / segs
        nx  = math.cos(a)
        nz  = math.sin(a)
        tx  = i / segs
        glNormal3f(nx, 0, nz)
        glTexCoord2f(tx, 0.25); glVertex3f(nx * radius,  body_h, nz * radius)
        glTexCoord2f(tx, 0.75); glVertex3f(nx * radius, -body_h, nz * radius)
    glEnd()

    for cap_sign in (+1, -1):
        cap_cy = cap_sign * body_h
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, cap_sign, 0)
        glTexCoord2f(0.5, 0.5)
        glVertex3f(0, cap_cy + cap_sign * radius, 0)
        ring_range = range(segs + 1) if cap_sign == 1 else range(segs, -1, -1)
        for i in ring_range:
            a  = 2 * math.pi * i / segs
            nx = math.cos(a)
            nz = math.sin(a)
            for phi_i in range(9):
                phi = (math.pi / 2) * phi_i / 8
                sy  = cap_sign * math.sin(phi)
                sr  = math.cos(phi)
                glNormal3f(nx * sr, cap_sign * math.sin(phi), nz * sr)
            glTexCoord2f(0.5 + nx * 0.5, 0.5 + nz * 0.5)
            glVertex3f(nx * radius, cap_cy + cap_sign * radius * 0, nz * radius)
        glEnd()

    for cap_sign in (+1, -1):
        cap_cy  = cap_sign * body_h
        hsegs   = 10
        rng_phi = range(hsegs + 1)
        for pi in range(hsegs):
            phi0 = (math.pi / 2) * pi       / hsegs
            phi1 = (math.pi / 2) * (pi + 1) / hsegs
            r0   = math.cos(phi0) * radius
            r1   = math.cos(phi1) * radius
            y0   = cap_cy + cap_sign * math.sin(phi0) * radius
            y1   = cap_cy + cap_sign * math.sin(phi1) * radius
            glBegin(GL_QUAD_STRIP)
            for i in range(segs + 1):
                a  = 2 * math.pi * i / segs
                nx = math.cos(a)
                nz = math.sin(a)
                tx = i / segs
                n0x = nx * math.cos(phi0); n0y = cap_sign * math.sin(phi0); n0z = nz * math.cos(phi0)
                n1x = nx * math.cos(phi1); n1y = cap_sign * math.sin(phi1); n1z = nz * math.cos(phi1)
                glNormal3f(n0x, n0y, n0z)
                glTexCoord2f(tx, (pi    ) / hsegs * 0.25 + (0.75 if cap_sign < 0 else 0.0))
                glVertex3f(nx * r0, y0, nz * r0)
                glNormal3f(n1x, n1y, n1z)
                glTexCoord2f(tx, (pi + 1) / hsegs * 0.25 + (0.75 if cap_sign < 0 else 0.0))
                glVertex3f(nx * r1, y1, nz * r1)
            glEnd()

    glDisable(GL_TEXTURE_2D)


def draw_sphere():
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, TEX_BALL)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)
    gluSphere(quad, BALL_RADIUS, 32, 32)
    gluDeleteQuadric(quad)
    glDisable(GL_TEXTURE_2D)


def draw_field():
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, TEX_FIELD)
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-LIMIT_X, -LIMIT_Y, -0.55)
    glTexCoord2f(1, 0); glVertex3f( LIMIT_X, -LIMIT_Y, -0.55)
    glTexCoord2f(1, 1); glVertex3f( LIMIT_X,  LIMIT_Y, -0.55)
    glTexCoord2f(0, 1); glVertex3f(-LIMIT_X,  LIMIT_Y, -0.55)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glColor3f(0.35, 0.55, 0.90)
    glLineWidth(2.5)
    glBegin(GL_LINE_LOOP)
    glVertex3f(-LIMIT_X, -LIMIT_Y, -0.50)
    glVertex3f( LIMIT_X, -LIMIT_Y, -0.50)
    glVertex3f( LIMIT_X,  LIMIT_Y, -0.50)
    glVertex3f(-LIMIT_X,  LIMIT_Y, -0.50)
    glEnd()

    glColor3f(0.30, 0.48, 0.80)
    glLineWidth(1.5)
    glBegin(GL_LINES)
    y, seg = -LIMIT_Y, 0.55
    while y < LIMIT_Y:
        glVertex3f(0, y, -0.50)
        glVertex3f(0, min(y + seg, LIMIT_Y), -0.50)
        y += seg * 2
    glEnd()

    cr, csegs = 1.8, 48
    glBegin(GL_LINE_LOOP)
    for i in range(csegs):
        a = 2 * math.pi * i / csegs
        glVertex3f(math.cos(a) * cr, math.sin(a) * cr, -0.50)
    glEnd()

    glEnable(GL_LIGHTING)


def render_surface_2d(surface, x, y):
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
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


def life_color(ratio):
    if ratio > 0.6:
        r = int(30  + (1 - ratio) / 0.4 * 225)
        g = 210
        b = 30
    elif ratio > 0.25:
        t = (ratio - 0.25) / 0.35
        r = 230
        g = int(60 + t * 150)
        b = 20
    else:
        r = 220
        g = int(30 + ratio / 0.25 * 40)
        b = 20
    return (min(255,r), min(255,g), min(255,b))


def draw_healthbar_hud(paddle_h_l, paddle_h_r):
    total_range = PADDLE_H_DEFAULT - PADDLE_H_MIN
    ratio_l = max(0.0, (paddle_h_l - PADDLE_H_MIN) / total_range)
    ratio_r = max(0.0, (paddle_h_r - PADDLE_H_MIN) / total_range)

    bar_w    = 160
    bar_h    = 16
    pad_x    = 20
    pad_y    = 16
    radius   = 7

    font_lbl = pygame.font.SysFont("monospace", 11, bold=True)

    def draw_bar(ratio, bx, label, color_tint):
        s = pygame.Surface((bar_w + 4, bar_h + 28), pygame.SRCALPHA)

        lbl = font_lbl.render(label, True, color_tint)
        s.blit(lbl, ((bar_w + 4 - lbl.get_width()) // 2, 0))

        bg_rect = pygame.Rect(2, 14, bar_w, bar_h)
        pygame.draw.rect(s, (20, 20, 35, 210), bg_rect, border_radius=radius)
        pygame.draw.rect(s, (55, 55, 80, 180), bg_rect, 1, border_radius=radius)

        fill_w = max(4, int(bar_w * ratio))
        col    = life_color(ratio)

        fill_surf = pygame.Surface((fill_w, bar_h), pygame.SRCALPHA)
        for px in range(fill_w):
            t = px / max(1, fill_w - 1)
            r = min(255, int(col[0] * (0.6 + 0.4 * t)))
            g = min(255, int(col[1] * (0.6 + 0.4 * t)))
            b = min(255, int(col[2] * (0.6 + 0.4 * t)))
            pygame.draw.line(fill_surf, (r, g, b, 230), (px, 0), (px, bar_h - 1))

        fill_mask = pygame.Surface((fill_w, bar_h), pygame.SRCALPHA)
        pygame.draw.rect(fill_mask, (255,255,255,255), (0,0,fill_w,bar_h), border_radius=radius)
        fill_surf.blit(fill_mask, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

        highlight = pygame.Surface((fill_w, bar_h // 2), pygame.SRCALPHA)
        for px in range(fill_w):
            pygame.draw.line(highlight, (255,255,255,55), (px,0),(px, bar_h//2 -1))
        fill_surf.blit(highlight, (0, 0))

        s.blit(fill_surf, (2, 14))

        pct = font_lbl.render(f"{int(ratio*100)}%", True, (200,200,215))
        s.blit(pct, ((bar_w + 4 - pct.get_width()) // 2, 14 + bar_h + 2))

        render_surface_2d(s, bx, pad_y)

    draw_bar(ratio_l, pad_x,                   "P1",  (100, 190, 255))
    draw_bar(ratio_r, WIDTH - bar_w - pad_x - 4, "P2", (255, 140,  55))


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def reset_ball():
    angle     = random.uniform(-25, 25)
    direction = random.choice([-1, 1])
    rad = math.radians(angle)
    return [0.0, 0.0, 0.0], [direction * BALL_SPEED_INIT * math.cos(rad),
                               BALL_SPEED_INIT * math.sin(rad), 0.0]


def check_paddle_collision(ball_pos, ball_vel, px, py, ph):
    if (abs(ball_pos[0] - px) < PADDLE_R + BALL_RADIUS and
            abs(ball_pos[1] - py) < ph + BALL_RADIUS):
        hit_offset = (ball_pos[1] - py) / ph
        angle = hit_offset * 65
        speed = min(math.hypot(ball_vel[0], ball_vel[1]) * random.uniform(1.03, 1.07),
                    BALL_SPEED_INIT * 3.2)
        rad    = math.radians(angle)
        new_vx = math.copysign(speed * math.cos(rad), -ball_vel[0])
        new_vy = speed * math.sin(rad)
        return True, [new_vx, new_vy, 0.0]
    return False, ball_vel


def enter_2d_overlay():
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix(); glLoadIdentity()
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix(); glLoadIdentity()
    glDisable(GL_DEPTH_TEST)


def exit_2d_overlay():
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION); glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING)


def blit_surface_centered(s, cx, cy):
    w, h = s.get_size()
    x = cx - w // 2
    y = cy - h // 2
    data = pygame.image.tostring(s, "RGBA", True)
    glRasterPos2i(x, y)
    glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, data)


def show_menu():
    font_title = pygame.font.SysFont("monospace", 40, bold=True)
    font_sub   = pygame.font.SysFont("monospace", 17)
    font_small = pygame.font.SysFont("monospace", 13)
    clock = pygame.time.Clock()
    t = 0

    enter_2d_overlay()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN: running = False
                if event.key == K_ESCAPE: pygame.quit(); exit()

        t += 1
        pulse = 0.5 + 0.5 * math.sin(t * 0.05)

        glClearColor(0.04, 0.04, 0.10, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        bw, bh = 530, 330
        s = pygame.Surface((bw, bh), pygame.SRCALPHA)
        s.fill((10, 10, 24, 238))
        bc = (int(55+45*pulse), int(55+45*pulse), int(115+65*pulse))
        pygame.draw.rect(s, bc, (0,0,bw,bh), 2, border_radius=12)

        title = font_title.render("PONG  3D", True, (100, 200, 255))
        s.blit(title, ((bw - title.get_width()) // 2, 24))

        sub = font_sub.render("Quiz de Computacao Grafica", True, (160, 160, 205))
        s.blit(sub, ((bw - sub.get_width()) // 2, 76))

        lines = [
            ("P1:  W  /  S          P2:  Seta Cima / Baixo", (145, 145, 185)),
            ("Erre a pergunta e perde vida",                  (200, 120, 120)),
            ("Perca toda a barra de vida = derrota",          (190, 130, 130)),
        ]
        yy = 120
        for txt, col in lines:
            ln = font_small.render(txt, True, col)
            s.blit(ln, ((bw - ln.get_width()) // 2, yy))
            yy += 26

        ec = (int(70+120*pulse), int(195+45*pulse), int(70+120*pulse))
        enter = font_sub.render("Pressione  ENTER  para comecar", True, ec)
        s.blit(enter, ((bw - enter.get_width()) // 2, 248))

        esc = font_small.render("ESC para sair", True, (65, 65, 95))
        s.blit(esc, ((bw - esc.get_width()) // 2, 298))

        data = pygame.image.tostring(s, "RGBA", True)
        glRasterPos2i((WIDTH-bw)//2, (HEIGHT-bh)//2)
        glDrawPixels(bw, bh, GL_RGBA, GL_UNSIGNED_BYTE, data)

        pygame.display.flip()
        clock.tick(60)

    exit_2d_overlay()


def show_question_popup(question_data, scorer_name, loser_name):
    font_title = pygame.font.SysFont("monospace", 18, bold=True)
    font_q     = pygame.font.SysFont("monospace", 15, bold=True)
    font_opt   = pygame.font.SysFont("monospace", 14)

    box_w, box_h = 540, 295
    box_x = (WIDTH  - box_w) // 2
    box_y = (HEIGHT - box_h) // 2

    options  = question_data["options"]
    selected = 0
    answered = False
    correct  = False
    result_timer = 0
    clock = pygame.time.Clock()

    enter_2d_overlay()
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
                    answered = True
                    correct  = (options[selected] == question_data["answer"])
                    result_timer = 100

        if answered:
            result_timer -= 1
            if result_timer <= 0: running = False

        s = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        s.fill((10, 10, 24, 244))
        pygame.draw.rect(s, (68, 68, 128), (0,0,box_w,box_h), 2, border_radius=10)

        tc = (90, 200, 255) if "1" in scorer_name else (255, 135, 55)
        t  = font_title.render(f"{scorer_name} marcou ponto!", True, tc)
        s.blit(t, ((box_w - t.get_width())//2, 11))

        sub = font_opt.render(f"Pergunta para {loser_name} — erre e perde vida:", True, (135,135,175))
        s.blit(sub, ((box_w - sub.get_width())//2, 32))

        words = question_data["q"].split()
        lines, line = [], ""
        for w in words:
            test = (line + " " + w).strip()
            if font_q.size(test)[0] < box_w - 40:
                line = test
            else:
                lines.append(line); line = w
        if line: lines.append(line)
        qy = 56
        for ql in lines:
            qs = font_q.render(ql, True, (224,224,224))
            s.blit(qs, ((box_w - qs.get_width())//2, qy)); qy += 20

        opt_y = qy + 6
        for i, opt in enumerate(options):
            is_sel = (i == selected)
            if answered:
                if opt == question_data["answer"]:
                    col, bgc = (60,220,100),  (18,55,28,215)
                elif is_sel:
                    col, bgc = (220,60,60),   (55,18,18,215)
                else:
                    col, bgc = (108,108,128), (28,28,42,185)
            else:
                col  = (235,225,75) if is_sel else (172,172,198)
                bgc  = (46,46,78,215) if is_sel else (28,28,42,185)

            row = pygame.Surface((box_w-30, 25), pygame.SRCALPHA)
            row.fill(bgc)
            s.blit(row, (15, opt_y-3))
            mk = "> " if is_sel and not answered else "  "
            s.blit(font_opt.render(f"{mk}[{chr(65+i)}] {opt}", True, col), (23, opt_y))
            opt_y += 30

        if answered:
            msg = "Correto! Vida preservada." if correct else "Errado! Vida perdida."
            rs  = font_q.render(msg, True, (70,215,95) if correct else (215,70,70))
            s.blit(rs, ((box_w - rs.get_width())//2, box_h-28))
        else:
            hint = font_opt.render("W / S  para mover   |   ENTER para confirmar", True, (62,62,98))
            s.blit(hint, ((box_w - hint.get_width())//2, box_h-18))

        data = pygame.image.tostring(s, "RGBA", True)
        glRasterPos2i(box_x, HEIGHT - box_y - box_h)
        glDrawPixels(box_w, box_h, GL_RGBA, GL_UNSIGNED_BYTE, data)

        pygame.display.flip()
        clock.tick(60)

    exit_2d_overlay()
    return correct


def show_victory_screen(winner_name):
    font_big = pygame.font.SysFont("monospace", 36, bold=True)
    font_sub = pygame.font.SysFont("monospace", 17)
    clock = pygame.time.Clock()
    t = 0

    enter_2d_overlay()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); exit()
            if event.type == KEYDOWN and event.key in (K_RETURN, K_ESCAPE, K_SPACE):
                running = False

        t += 1
        pulse = 0.5 + 0.5 * math.sin(t * 0.06)

        glClearColor(0.04, 0.04, 0.10, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        bw, bh = 460, 185
        s = pygame.Surface((bw, bh), pygame.SRCALPHA)
        s.fill((10, 10, 26, 250))
        bc = (int(75+55*pulse), int(75+55*pulse), int(150+60*pulse))
        pygame.draw.rect(s, bc, (0,0,bw,bh), 2, border_radius=10)

        col = (90,200,255) if "1" in winner_name else (255,135,55)
        title = font_big.render(f"{winner_name}  VENCEU!", True, col)
        s.blit(title, ((bw - title.get_width())//2, 34))

        sub = font_sub.render("O adversario perdeu toda a barra de vida.", True, (162,162,198))
        s.blit(sub, ((bw - sub.get_width())//2, 88))

        hc = (int(55+85*pulse), int(175+55*pulse), int(55+85*pulse))
        hint = font_sub.render("ENTER para sair", True, hc)
        s.blit(hint, ((bw - hint.get_width())//2, 138))

        data = pygame.image.tostring(s, "RGBA", True)
        glRasterPos2i((WIDTH-bw)//2, (HEIGHT-bh)//2)
        glDrawPixels(bw, bh, GL_RGBA, GL_UNSIGNED_BYTE, data)

        pygame.display.flip()
        clock.tick(60)

    exit_2d_overlay()


def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Pong 3D")

    gluPerspective(45, WIDTH / HEIGHT, 0.1, 80.0)
    glTranslatef(0.0, 0.0, -22)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    setup_lighting()
    init_textures()

    show_menu()

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

    def pick_q():
        pool = [q for q in QUESTIONS if q not in used_qs]
        if not pool:
            used_qs.clear(); pool = QUESTIONS[:]
        q = random.choice(pool); used_qs.append(q); return q

    clock   = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT: running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE: running = False

        keys = pygame.key.get_pressed()
        if keys[K_w]:    paddle_l_y += PADDLE_SPEED
        if keys[K_s]:    paddle_l_y -= PADDLE_SPEED
        if keys[K_UP]:   paddle_r_y += PADDLE_SPEED
        if keys[K_DOWN]: paddle_r_y -= PADDLE_SPEED

        paddle_l_y = clamp(paddle_l_y, -(LIMIT_Y - paddle_h_l), LIMIT_Y - paddle_h_l)
        paddle_r_y = clamp(paddle_r_y, -(LIMIT_Y - paddle_h_r), LIMIT_Y - paddle_h_r)

        ball_pos[0] += ball_vel[0]; ball_pos[1] += ball_vel[1]
        ball_rot[0] += ball_vel[1] * 5; ball_rot[1] += ball_vel[0] * 5

        if ball_pos[1] >  LIMIT_Y - BALL_RADIUS:
            ball_pos[1] =  LIMIT_Y - BALL_RADIUS; ball_vel[1] *= -1
        if ball_pos[1] < -LIMIT_Y + BALL_RADIUS:
            ball_pos[1] = -LIMIT_Y + BALL_RADIUS; ball_vel[1] *= -1

        if ball_vel[0] < 0:
            hit, ball_vel = check_paddle_collision(ball_pos, ball_vel, PADDLE_X_L, paddle_l_y, paddle_h_l)
            if hit: ball_pos[0] = PADDLE_X_L + PADDLE_R + BALL_RADIUS + 0.01

        if ball_vel[0] > 0:
            hit, ball_vel = check_paddle_collision(ball_pos, ball_vel, PADDLE_X_R, paddle_r_y, paddle_h_r)
            if hit: ball_pos[0] = PADDLE_X_R - PADDLE_R - BALL_RADIUS - 0.01

        if ball_pos[0] > LIMIT_X:
            goal_flash = 20
            if not show_question_popup(pick_q(), "Jogador 1", "Jogador 2"):
                paddle_h_r = max(PADDLE_H_MIN, paddle_h_r - PADDLE_H_PENALTY)
                if paddle_h_r <= PADDLE_H_MIN:
                    show_victory_screen("Jogador 1"); running = False
            ball_pos, ball_vel = reset_ball()
            paddle_l_y = 0.0
            paddle_r_y = 0.0

        if ball_pos[0] < -LIMIT_X:
            goal_flash = 20
            if not show_question_popup(pick_q(), "Jogador 2", "Jogador 1"):
                paddle_h_l = max(PADDLE_H_MIN, paddle_h_l - PADDLE_H_PENALTY)
                if paddle_h_l <= PADDLE_H_MIN:
                    show_victory_screen("Jogador 2"); running = False
            ball_pos, ball_vel = reset_ball()
            paddle_l_y = 0.0
            paddle_r_y = 0.0

        if goal_flash > 0: goal_flash -= 1

        glClearColor(*(0.05, 0.05, 0.11, 1.0) if goal_flash == 0 else (0.15, 0.04, 0.04, 1.0))
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_field()

        glPushMatrix()
        glTranslatef(PADDLE_X_L, paddle_l_y, 0)
        glColor3f(0.55, 0.75, 0.95)
        draw_capsule_paddle(PADDLE_R, paddle_h_l)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(PADDLE_X_R, paddle_r_y, 0)
        glColor3f(1.00, 0.70, 0.40)
        draw_capsule_paddle(PADDLE_R, paddle_h_r)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(ball_pos[0], ball_pos[1], 0)
        glRotatef(ball_rot[0], 1, 0, 0)
        glRotatef(ball_rot[1], 0, 1, 0)
        glColor3f(0.95, 0.95, 0.98)
        draw_sphere()
        glPopMatrix()

        draw_healthbar_hud(paddle_h_l, paddle_h_r)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()