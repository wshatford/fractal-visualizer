import math
import random
import pygame

# Screen setup
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
FPS = 60

CENTER = (WIDTH // 2, HEIGHT // 2)
SCENE_DURATION = FPS * 10
FADE_DURATION = FPS * 2

class Pattern:
    def update(self):
        pass
    def draw(self, surface):
        pass




class PainterlyMandalaField(Pattern):
    class Ring:
        def __init__(self, center, layers=4):
            self.center = center
            self.layers = layers
            self.hue_base = random.randint(0, 360)
            self.rotation = 0
            self.rotation_speed = random.uniform(-0.01, 0.01)
            self.scale = 0.1
            self.growth_rate = random.uniform(0.002, 0.006)
            self.max_scale = random.uniform(0.9, 1.5)
            self.angle_offsets = [random.uniform(0, 2 * math.pi) for _ in range(layers)]

        def hsv_to_rgb(self, h, s, v):
            h, s, v = float(h), float(s)/100, float(v)/100
            hi = int(h / 60) % 6
            f = h / 60 - hi
            p, q, t = v * (1 - s), v * (1 - f * s), v * (1 - (1 - f) * s)
            return [(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)][hi]

        def draw_petal(self, surface, x, y, angle, hue):
            size = 60
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            r1, g1, b1 = self.hsv_to_rgb(hue, 80, 100)
            r2, g2, b2 = self.hsv_to_rgb((hue + 40) % 360, 70, 60)
            for i in range(12):
                t = i / 12
                r = int(max(0, min(255, (1 - t) * r1 * 255 + t * r2 * 255)))
                g = int(max(0, min(255, (1 - t) * g1 * 255 + t * g2 * 255)))
                b = int(max(0, min(255, (1 - t) * b1 * 255 + t * b2 * 255)))
                a = int(255 * (1 - t))
                col = (r, g, b, a)
                pygame.draw.ellipse(
                    surf, col,
                    (size - size * 0.5 * (1 - t), size - size * (1 - t), size * (1 - t), size * 2 * (1 - t))
                )
            rotated = pygame.transform.rotozoom(surf, -math.degrees(angle), self.scale)
            rect = rotated.get_rect(center=(int(x), int(y)))
            surface.blit(rotated, rect)

        def update(self):
            self.rotation += self.rotation_speed
            if self.scale < self.max_scale:
                self.scale += self.growth_rate

        def draw(self, surface):
            for layer in range(self.layers):
                petals = 6 + layer * 2
                radius = 40 + 25 * layer
                hue = (self.hue_base + layer * 20) % 360
                for i in range(petals):
                    angle = 2 * math.pi * i / petals + self.rotation + self.angle_offsets[layer]
                    x = self.center[0] + math.cos(angle) * radius
                    y = self.center[1] + math.sin(angle) * radius
                    self.draw_petal(surface, x, y, angle, hue)

    def __init__(self):
        self.rings = [self.Ring(
            (random.randint(150, WIDTH - 150), random.randint(150, HEIGHT - 150)),
            layers=random.randint(3, 5)
        ) for _ in range(8)]

    def update(self):
        for r in self.rings:
            r.update()

    def draw(self, surface):
        for r in self.rings:
            r.draw(surface)



class BrushStreakBurst(Pattern):
    class Streak:
        def __init__(self):
            self.center = (random.randint(150, WIDTH - 150), random.randint(150, HEIGHT - 150))
            self.angle = random.uniform(0, 2 * math.pi)
            self.length = random.randint(80, 160)
            self.width = random.randint(6, 12)
            self.hue = random.randint(0, 360)
            self.alpha = 255
            self.fade_speed = random.uniform(0.3, 1.0)

        def update(self):
            self.alpha = max(0, self.alpha - self.fade_speed)

        def draw(self, surface):
            if self.alpha <= 0:
                return
            color = pygame.Color(0)
            color.hsva = (self.hue, 70, 100, self.alpha / 2.55)
            end_x = self.center[0] + math.cos(self.angle) * self.length
            end_y = self.center[1] + math.sin(self.angle) * self.length
            pygame.draw.line(surface, color, self.center, (end_x, end_y), self.width)

    def __init__(self):
        self.streaks = []

    def update(self):
        if len(self.streaks) < 200:
            for _ in range(3):
                self.streaks.append(self.Streak())
        for s in self.streaks:
            s.update()
        self.streaks = [s for s in self.streaks if s.alpha > 0]

    def draw(self, surface):
        for s in self.streaks:
            s.draw(surface)


class SoftLayeredBloom(Pattern):
    class Bloom:
        def __init__(self):
            self.center = (random.randint(150, WIDTH - 150), random.randint(150, HEIGHT - 150))
            self.layers = random.randint(3, 6)
            self.rotation = random.uniform(0, 2 * math.pi)
            self.scale = 0.1
            self.max_scale = random.uniform(0.8, 1.6)
            self.growth_rate = random.uniform(0.003, 0.008)
            self.hue = random.randint(0, 360)

        def update(self):
            if self.scale < self.max_scale:
                self.scale += self.growth_rate

        def draw(self, surface):
            for i in range(self.layers):
                petals = 6 + i * 2
                radius = 40 + i * 25
                for j in range(petals):
                    angle = 2 * math.pi * j / petals + self.rotation
                    x = self.center[0] + math.cos(angle) * radius
                    y = self.center[1] + math.sin(angle) * radius
                    color = pygame.Color(0)
                    color.hsva = ((self.hue + i * 15 + j * 5) % 360, 50, 100 - i * 10, 100)
                    alpha = int(255 * (1 - i / self.layers))
                    surf = pygame.Surface((30, 60), pygame.SRCALPHA)
                    pygame.draw.ellipse(surf, color, (0, 0, 30, 60))
                    surf.set_alpha(alpha)
                    rotated = pygame.transform.rotozoom(surf, -math.degrees(angle), self.scale)
                    rect = rotated.get_rect(center=(int(x), int(y)))
                    surface.blit(rotated, rect)

    def __init__(self):
        self.blooms = [self.Bloom() for _ in range(10)]

    def update(self):
        for b in self.blooms:
            b.update()

    def draw(self, surface):
        for b in self.blooms:
            b.draw(surface)



class ExpressiveSwirlBloom(Pattern):
    def __init__(self):
        self.swirls = [self.create_swirl() for _ in range(6)]

    def create_swirl(self):
        return {
            'center': (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100)),
            'angle': random.uniform(0, 2 * math.pi),
            'hue': random.randint(0, 360),
            'radius': 5,
            'growth': random.uniform(1.2, 2.0),
            'arms': random.randint(3, 7),
            'rotation_speed': random.uniform(-0.02, 0.02),
            'age': 0,
            'max_age': random.randint(120, 240)
        }

    def update(self):
        for swirl in self.swirls:
            swirl['radius'] += swirl['growth']
            swirl['angle'] += swirl['rotation_speed']
            swirl['hue'] = (swirl['hue'] + 0.5) % 360
            swirl['age'] += 1
        self.swirls = [s if s['age'] < s['max_age'] else self.create_swirl() for s in self.swirls]

    def draw(self, surface):
        for swirl in self.swirls:
            for i in range(100):
                t = i / 100 * 4 * math.pi
                r = swirl['radius'] * t / (4 * math.pi)
                x = r * math.cos(t * swirl['arms'] + swirl['angle'])
                y = r * math.sin(t * swirl['arms'] + swirl['angle'])
                sx = int(swirl['center'][0] + x)
                sy = int(swirl['center'][1] + y)
                if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                    color = pygame.Color(0)
                    color.hsva = ((swirl['hue'] + i * 2) % 360, 80, 100, 100)
                    size = max(1, int(r / 20))
                    pygame.draw.circle(surface, color, (sx, sy), size)

class GalaxySwirlBloom(Pattern):
    class Particle:
        def __init__(self, center):
            self.center = center
            self.angle = random.uniform(0, 2 * math.pi)
            self.radius = 0
            self.speed = random.uniform(0.5, 1.5)
            self.angle_speed = random.uniform(0.01, 0.03)
            self.hue = random.randint(180, 300)  # Bluish-purple range
            self.alpha = 255
            self.size = random.uniform(2, 4)

        def update(self):
            self.radius += self.speed
            self.angle += self.angle_speed
            self.alpha = max(0, self.alpha - 0.8)

        def draw(self, surface):
            x = self.center[0] + math.cos(self.angle) * self.radius
            y = self.center[1] + math.sin(self.angle) * self.radius
            glow = pygame.Surface((20, 20), pygame.SRCALPHA)
            color = pygame.Color(0)
            color.hsva = (self.hue, 80, 100, min(100, self.alpha / 2.55))  # Pygame expects alpha 0–100
            pygame.draw.circle(glow, color, (10, 10), int(self.size))
            surface.blit(glow, (x - 10, y - 10), special_flags=pygame.BLEND_ADD)

    def __init__(self):
        self.center = CENTER
        self.particles = []

    def update(self):
        for _ in range(5):
            self.particles.append(self.Particle(self.center))
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.alpha > 0]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)



class VortexPetal:
    def __init__(self):
        self.angle = random.uniform(0, 2 * math.pi)
        self.radius = random.uniform(50, min(WIDTH, HEIGHT) // 2)
        self.angular_velocity = random.uniform(0.01, 0.03)
        self.radial_speed = random.uniform(-0.2, 0.2)
        self.size = random.uniform(8, 18)
        self.hue = random.randint(0, 360)
        self.alpha = 255
        self.center = (WIDTH // 2, HEIGHT // 2)

    def update(self):
        self.angle += self.angular_velocity
        self.radius += self.radial_speed
        if self.radius < 10 or self.radius > min(WIDTH, HEIGHT) // 1.5:
            return False
        return True

    def draw(self, surface):
        x = self.center[0] + math.cos(self.angle) * self.radius
        y = self.center[1] + math.sin(self.angle) * self.radius
        petal_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        color = pygame.Color(0)
        color.hsva = (self.hue % 360, 60, 100, 100)
        pygame.draw.ellipse(petal_surface, color, (10, 0, 20, 40))
        rotated = pygame.transform.rotozoom(petal_surface, math.degrees(self.angle), self.size / 20)
        rect = rotated.get_rect(center=(int(x), int(y)))
        surface.blit(rotated, rect)

class PetalDriftVortexScene(Pattern):
    def __init__(self):
        self.petals = [VortexPetal() for _ in range(80)]

    def update(self):
        self.petals = [p for p in self.petals if p.update()]
        while len(self.petals) < 80:
            self.petals.append(VortexPetal())

    def draw(self, surface):
        for petal in self.petals:
            petal.draw(surface)



# --- PainterlyFlowerField (multiple flowers) ---
class PainterlyFlowerField(Pattern):
    class Flower:
        def __init__(self, center, layers=3):
            self.center = center
            self.layers = layers
            self.angle_offsets = [random.uniform(0, 2 * math.pi) for _ in range(layers)]
            self.hue_base = random.randint(0, 360)
            self.rotation = 0
            self.rotation_speed = random.uniform(-0.006, 0.006)
            self.scale = 0.1
            self.growth_rate = 0.01  # Faster growth
            self.max_scale = 1.6

        def hsv_to_rgb(self, h, s, v):
            h, s, v = float(h), float(s)/100, float(v)/100
            hi = int(h/60) % 6
            f = h/60 - hi
            p, q, t = v*(1-s), v*(1-f*s), v*(1-(1-f)*s)
            return [(v,t,p),(q,v,p),(p,v,t),(p,q,v),(t,p,v),(v,p,q)][hi]

        def draw_petal(self, surface, x, y, angle, size, hue):
            surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            r1, g1, b1 = self.hsv_to_rgb(hue, 70, 100)
            r2, g2, b2 = self.hsv_to_rgb((hue+30)%360, 70, 60)
            for i in range(6):  # fewer steps to reduce cost
                t = i / 6
                col = (
                    int((1 - t) * r1 * 255 + t * r2 * 255),
                    int((1 - t) * g1 * 255 + t * g2 * 255),
                    int((1 - t) * b1 * 255 + t * b2 * 255),
                    int(255 * (1 - t))
                )
                pygame.draw.ellipse(
                    surf, col,
                    (size//2 - size*0.5 * (1-t), size//2 - size * (1-t), size * (1 - t), size * 2 * (1 - t))
                )
            rotated = pygame.transform.rotozoom(surf, -math.degrees(angle), self.scale)
            rect = rotated.get_rect(center=(int(x), int(y)))
            surface.blit(rotated, rect)

        def update(self):
            self.rotation += self.rotation_speed
            if self.scale < self.max_scale:
                self.scale += self.growth_rate

        def draw(self, surface):
            for layer in range(self.layers):
                petals = 5 + layer * 2
                radius = 35 + 20 * layer
                hue = (self.hue_base + layer * 30) % 360
                for i in range(petals):
                    angle = 2 * math.pi * i / petals + self.rotation + self.angle_offsets[layer]
                    x = self.center[0] + math.cos(angle) * radius
                    y = self.center[1] + math.sin(angle) * radius
                    self.draw_petal(surface, x, y, angle, 50 + layer * 12, hue)

    def __init__(self):
        self.reset()

    def reset(self):
        self.flowers = [self.Flower((random.randint(150, WIDTH - 150), random.randint(150, HEIGHT - 150)),
                                    layers=random.randint(2, 4)) for _ in range(6)]
        self.age = 0
        self.flash_alpha = 255

    def update(self):
        self.age += 1
        if self.age > FPS * 6:
            self.reset()
        else:
            for flower in self.flowers:
                flower.update()

    def draw(self, surface):
        for flower in self.flowers:
            flower.draw(surface)
        if self.flash_alpha > 0:
            flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            flash.fill((255, 255, 255, int(self.flash_alpha)))
            surface.blit(flash, (0, 0))
            self.flash_alpha -= 20


# --- FractalSpiralBloom pattern ---
class FractalSpiralBloom(Pattern):
    def __init__(self):
        self.flowers = []
        self.max_flowers = 300
        self.angle_offset = 137.5
        self.scale = 3
        self.frame = 0

    def update(self):
        if len(self.flowers) < self.max_flowers:
            i = len(self.flowers)
            theta = math.radians(i * self.angle_offset)
            r = self.scale * math.sqrt(i) * 20
            x = WIDTH // 2 + r * math.cos(theta)
            y = HEIGHT // 2 + r * math.sin(theta)
            hue = (i * 0.01 + self.frame * 0.002) % 1.0
            self.flowers.append((x, y, hue, i * 2))
        self.frame += 1

    def draw(self, surface):
        for x, y, hue, angle in self.flowers:
            draw_recursive_flower(surface, x, y, hue, angle)

def draw_recursive_flower(surface, x, y, hue, angle, depth=3, scale=1.0):
    if depth == 0:
        return
    color = pygame.Color(0)
    color.hsva = (hue * 360 % 360, 70, 100, 100)
    for i in range(6):
        a = math.radians(i * 60 + angle)
        dx = math.cos(a) * 10 * scale
        dy = math.sin(a) * 10 * scale
        pygame.draw.ellipse(surface, color, (x + dx - 5 * scale, y + dy - 5 * scale, 10 * scale, 10 * scale))
        draw_recursive_flower(surface, x + dx, y + dy, hue + 0.02, angle + 10, depth - 1, scale * 0.8)



# --- MultiRosePattern ---
class MultiRosePattern(Pattern):
    def __init__(self):
        self.roses = [self.create_rose() for _ in range(5)]

    def create_rose(self):
        return {
            'k': random.randint(3, 8),
            'size': 10,
            'max_size': random.randint(300, 800),
            'rotation': 0,
            'rotation_speed': random.uniform(-0.02, 0.02),
            'center': (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
            'hue_offset': random.randint(0, 360),
            'color_speed': random.uniform(0.5, 1.5)
        }

    def update(self):
        for rose in self.roses:
            rose['size'] += 1.2
            rose['rotation'] += rose['rotation_speed']
            rose['hue_offset'] += rose['color_speed']
        self.roses = [r if r['size'] < r['max_size'] else self.create_rose() for r in self.roses]

    def draw(self, surface):
        for rose in self.roses:
            for i in range(800):
                theta = (i / 800) * 2 * math.pi
                r = rose['size'] * math.cos(rose['k'] * theta)
                x = r * math.cos(theta + rose['rotation'])
                y = r * math.sin(theta + rose['rotation'])
                sx = int(rose['center'][0] + x)
                sy = int(rose['center'][1] + y)
                if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                    hue = (i * rose['color_speed'] + rose['hue_offset']) % 360
                    color = pygame.Color(0)
                    color.hsva = (hue, 100, 100, 100)
                    radius = max(1, int(abs(r) / 80))
                    pygame.draw.circle(surface, color, (sx, sy), radius)

# --- PhyllotaxisPattern ---
class PhyllotaxisPattern(Pattern):
    def __init__(self):
        self.n = 0
        self.c = random.randint(4, 10)
        self.hue_offset = random.randint(0, 360)

    def update(self):
        self.n += 5
        self.hue_offset += 0.5

    def draw(self, surface):
        for i in range(self.n):
            angle = i * 137.5 * math.pi / 180
            r = self.c * math.sqrt(i)
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            sx = int(CENTER[0] + x)
            sy = int(CENTER[1] + y)
            if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                hue = (i + self.hue_offset) % 360
                color = pygame.Color(0)
                color.hsva = (hue, 100, 100, 100)
                pygame.draw.circle(surface, color, (sx, sy), 3)

# --- MultiLissajousPattern ---
class MultiLissajousPattern(Pattern):
    def __init__(self):
        self.figures = [self.create_fig() for _ in range(5)]

    def create_fig(self):
        return {
            'a': 10,
            'b': 10,
            'max_size': random.uniform(150, 400),
            'growth_rate': random.uniform(1.2, 2.0),
            'freq_x': random.randint(2, 5),
            'freq_y': random.randint(2, 5),
            'delta': random.uniform(0, math.pi),
            'delta_speed': random.uniform(0.005, 0.02),
            'center': (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
            'hue_offset': random.randint(0, 360)
        }

    def update(self):
        for fig in self.figures:
            fig['a'] += fig['growth_rate']
            fig['b'] += fig['growth_rate']
            fig['delta'] += fig['delta_speed']
            fig['hue_offset'] += 0.5
        self.figures = [f if f['a'] < f['max_size'] else self.create_fig() for f in self.figures]

    def draw(self, surface):
        for fig in self.figures:
            for i in range(1000):
                t = i * 2 * math.pi / 1000
                x = fig['a'] * math.sin(fig['freq_x'] * t + fig['delta'])
                y = fig['b'] * math.sin(fig['freq_y'] * t)
                sx = int(fig['center'][0] + x)
                sy = int(fig['center'][1] + y)
                if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
                    hue = (i + fig['hue_offset']) % 360
                    color = pygame.Color(0)
                    color.hsva = (hue, 100, 100, 100)
                    pygame.draw.circle(surface, color, (sx, sy), 2)

# --- MultiLSystemPattern with slow growth and random angles ---
class MultiLSystemPattern(Pattern):
    def __init__(self):
        self.instances = [self.create_instance() for _ in range(4)]
        self.axiom = "F"
        self.rules = {"F": "F[+F]F[-F]F"}

    def create_instance(self):
        return {
            'gen': 0,
            'max_gen': random.randint(5, 7),
            'x': random.randint(100, WIDTH - 100),
            'y': random.randint(100, HEIGHT - 100),
            'hue_offset': random.randint(0, 360),
            'current_string': "F",
            'angle': random.randint(15, 40),
            'growth_timer': 0,
            'growth_delay': random.randint(30, 60)
        }

    def apply_rules(self, s):
        return "".join(self.rules.get(c, c) for c in s)

    def update(self):
        for inst in self.instances:
            inst['growth_timer'] += 1
            if inst['growth_timer'] >= inst['growth_delay'] and inst['gen'] < inst['max_gen']:
                inst['current_string'] = self.apply_rules(inst['current_string'])
                inst['gen'] += 1
                inst['growth_timer'] = 0
            elif inst['gen'] >= inst['max_gen']:
                inst.update(self.create_instance())

    def draw(self, surface):
        for inst in self.instances:
            stack = []
            x, y = inst['x'], inst['y']
            angle = -90
            angle_step = inst['angle']
            hue = inst['hue_offset']
            length = 6
            for cmd in inst['current_string']:
                if cmd == "F":
                    new_x = x + math.cos(math.radians(angle)) * length
                    new_y = y + math.sin(math.radians(angle)) * length
                    color = pygame.Color(0)
                    color.hsva = (hue % 360, 100, 100, 100)
                    pygame.draw.line(surface, color, (x, y), (new_x, new_y), 2)
                    x, y = new_x, new_y
                    hue += 0.5
                elif cmd == "+":
                    angle += angle_step
                elif cmd == "-":
                    angle -= angle_step
                elif cmd == "[":
                    stack.append((x, y, angle))
                elif cmd == "]":
                    x, y, angle = stack.pop()


# --- PetalField overlay ---
class Petal:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-100, -40)
        self.size = random.uniform(10, 20)
        self.growth = random.uniform(0.01, 0.05)
        self.rotation = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-0.01, 0.01)
        self.fall_speed = random.uniform(0.5, 1.5)
        self.hue = random.randint(300, 360)
        self.alpha = 255

    def update(self):
        self.y += self.fall_speed
        self.rotation += self.rotation_speed
        self.size += self.growth
        self.alpha = max(0, self.alpha - 0.3)
        return self.y <= HEIGHT and self.alpha > 0

    def draw(self, surface):
        petal_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        color = pygame.Color(0)
        color.hsva = (self.hue % 360, 60, 100, 100)
        color.a = int(self.alpha)
        pygame.draw.ellipse(petal_surface, color, (10, 0, 20, 40))
        rotated = pygame.transform.rotozoom(petal_surface, math.degrees(self.rotation), self.size / 20)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)

class PetalField:
    def __init__(self):
        self.petals = [Petal() for _ in range(30)]

    def update(self):
        self.petals = [p for p in self.petals if p.update()]
        while len(self.petals) < 30:
            self.petals.append(Petal())

    def draw(self, surface):
        for p in self.petals:
            p.draw(surface)


# PetalField initialization
petal_field = PetalField()


# --- RotatingFlowerField pattern ---
class RotatingFlowerField(Pattern):
    class Flower:
        def __init__(self, center, layers=3, petals_per_layer=6):
            self.center = center
            self.layers = layers
            self.petals_per_layer = petals_per_layer
            self.scale = random.uniform(0.8, 1.4)
            self.hue_base = random.randint(0, 360)
            self.rotation = random.uniform(0, 2 * math.pi)
            self.rotation_speed = random.uniform(-0.002, 0.002)

        def update(self):
            self.rotation += self.rotation_speed

        def draw(self, surface):
            for layer in range(self.layers):
                radius = 20 + layer * 15
                petals = self.petals_per_layer + layer * 2
                angle_step = 2 * math.pi / petals
                color = pygame.Color(0)
                color.hsva = (
                    (self.hue_base + layer * 20) % 360,
                    70,
                    100 - layer * 10,
                    100,
                )
                for i in range(petals):
                    angle = i * angle_step + self.rotation
                    x = self.center[0] + math.cos(angle) * radius
                    y = self.center[1] + math.sin(angle) * radius
                    petal_surf = pygame.Surface((60, 30), pygame.SRCALPHA)
                    pygame.draw.ellipse(petal_surf, color, (0, 0, 60, 30))
                    rotated = pygame.transform.rotozoom(petal_surf, -math.degrees(angle), self.scale)
                    rect = rotated.get_rect(center=(int(x), int(y)))
                    surface.blit(rotated, rect)

    def __init__(self):
        self.flowers = []
        self.spawn_delay = 30
        self.timer = 0
        self.max_flowers = 120

    def update(self):
        self.timer += 1
        for flower in self.flowers:
            flower.update()
        if self.timer >= self.spawn_delay and len(self.flowers) < self.max_flowers:
            self.add_flower()
            self.timer = 0

    def add_flower(self):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 100)
        layers = random.randint(3, 5)
        petals = random.randint(5, 8)
        self.flowers.append(self.Flower((x, y), layers, petals))

    def draw(self, surface):
        for flower in self.flowers:
            flower.draw(surface)


# Scene cycling
patterns = [PainterlyFlowerField,FractalSpiralBloom,RotatingFlowerField,MultiRosePattern, PhyllotaxisPattern, MultiLissajousPattern, MultiLSystemPattern]
scene_index = 0
current_pattern = patterns[scene_index]()
frame_count = 0
fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill((0, 0, 0))

# Scene cycling
patterns = [PainterlyMandalaField, BrushStreakBurst, SoftLayeredBloom, ExpressiveSwirlBloom,
            GalaxySwirlBloom,
            PetalDriftVortexScene,
            PainterlyFlowerField,
            FractalSpiralBloom,
            MultiRosePattern,
            PhyllotaxisPattern,
            RotatingFlowerField,
            MultiLissajousPattern,
            MultiLSystemPattern
            ]
scene_index = 0
current_pattern = patterns[scene_index]()
frame_count = 0
fade_surface = pygame.Surface((WIDTH, HEIGHT))
fade_surface.fill((0, 0, 0))

running = True
while running:
    screen.fill((10, 10, 30))
    petal_field.update()
    current_pattern.update()
    petal_field.draw(screen)
    current_pattern.draw(screen)

    if SCENE_DURATION - FADE_DURATION <= frame_count < SCENE_DURATION:
        alpha = int(255 * (frame_count - (SCENE_DURATION - FADE_DURATION)) / FADE_DURATION)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            running = False

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

    if frame_count >= SCENE_DURATION:
        scene_index = (scene_index + 1) % len(patterns)
        current_pattern = patterns[scene_index]()
        frame_count = 0

pygame.quit()
