import pygame, sys, random
from pygame import Vector2

pygame.init()
pygame.mixer.init()

width = 640
height = 400

class Bird:
    def __init__(self):
        self.x = width / 4
        self.y = height / 4
        self.width = 40
        self.height = 40

        self.pos = Vector2(self.x, self.y)
        self.velocity = Vector2(300, 0)
        self.flap = 240

    def draw_bird(self):
        bird = pygame.image.load("assets/cheek2.png")
        bird_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        window.blit(bird, bird_rect)

    def move_bird(self):
        self.pos.y += self.velocity.y * dt
        self.velocity.y += game.g * dt

class Pipe:
    def __init__(self):
        self.gap = bird.height * 3.5
        self.distance = width / 2

        self.width = bird.width * 1.5
        self.height = height

        self.pos = []
        self.pos.append(Vector2(width, random.randint(int(height / 2.5), height - 100)))

    def spawn_pipes(self):
        if self.pos[len(self.pos) - 1].x + self.width + self.distance <= width:
            pipe_pos = Vector2(width, random.randint(int(height / 2.5), height - 100))
            self.pos.append(pipe_pos)

    def draw_pipes(self):
        for pos in self.pos:
            pipe1 = pygame.image.load("assets/pipe_up.png")
            pipe2 = pygame.image.load("assets/pipe_down.png")

            pipe_rect1 = pygame.Rect(pos.x, pos.y, self.width, self.height)
            pipe_rect2 = pygame.Rect(pos.x, pos.y - self.height - self.gap, self.width, self.height)

            window.blit(pipe1, pipe_rect1)
            window.blit(pipe2, pipe_rect2)

    def move_pipes(self):
        for pos in self.pos:
            if pos.x + self.width < 0:
                self.pos.remove(pos)
                game.scored = False

            pos.x -= bird.velocity.x * dt

class Scene:
    def __init__(self):
        self.grass_height = 70
        self.grass_pos = []
        self.grass_pos.append(Vector2(0, height - self.grass_height))

        self.back_paralax_factor = 0.2
        self.back_pos = []
        self.back_pos.append(Vector2(0, 0))

    def spawn_grass(self):
        if self.grass_pos[len(self.grass_pos) - 1].x + width <= width:
            self.grass_pos.append(Vector2(width, height - self.grass_height))

    def draw_grass(self):
        for pos in self.grass_pos:
            grass = pygame.image.load("assets/grass2.png")
            grass_rect = pygame.Rect(pos.x, pos.y, width, self.grass_height)
            window.blit(grass, grass_rect)

    def move_grass(self):
        for pos in self.grass_pos:
            if pos.x + width < 0:
                self.grass_pos.remove(pos)

            pos.x -= bird.velocity.x * dt

    def spawn_background(self):
        if self.back_pos[len(self.back_pos) - 1].x + width <= width:
            self.back_pos.append(Vector2(width, 0))

    def draw_background(self):
        for pos in self.back_pos:
            background = pygame.image.load("assets/background.png")
            back_rect = pygame.Rect(pos.x, pos.y, width, height)
            window.blit(background, back_rect)

    def move_background(self):
        for pos in self.back_pos:
            if pos.x + width < 0:
                self.back_pos.remove(pos)

            pos.x -= bird.velocity.x * self.back_paralax_factor * dt

class Game:
    def __init__(self):
        self.g = 360
        self.collision_error = 5

        self.game_state = "MENU"
        self.paused = False

        self.score = 0
        self.scored = False

        self.text_alpha = 225
        self.alpha_switch = False

        self.death_message = ""

    def draw_score(self):
        font = pygame.font.SysFont("Comic Sans", 100)
        text = font.render(str(self.score), True, (225, 225, 225))
        text_rect = text.get_rect(center = (width / 2, height / 8))
        text.set_alpha(80)
        window.blit(text, text_rect)

    def check_score(self):
        for pipe_pos in pipe.pos:
            if bird.x > pipe_pos.x + pipe.width and not self.scored:
                self.score += 1
                self.scored = True

    def check_collision(self):
        for pipe_pos in pipe.pos:
            if (bird.pos.x + bird.width > pipe_pos.x + self.collision_error and bird.pos.x < pipe_pos.x + pipe.width - self.collision_error) and (bird.pos.y + bird.height > pipe_pos.y + self.collision_error or bird.pos.y < pipe_pos.y - pipe.gap - self.collision_error):
                hit.play()
                self.game_state = "GAME_OVER"
                self.death_message = "Cheek smashed his head"

            if bird.pos.y + bird.height < 0 - self.collision_error:
                hit.play()
                self.game_state = "GAME_OVER"
                self.death_message = "Cheek ascended to heaven"

            if bird.pos.y + bird.height > height - scene.grass_height + self.collision_error:
                hit.play()
                self.game_state = "GAME_OVER"
                self.death_message = "Cheek hit the ground too hard"

    def check_state(self):
        if self.game_state == "MENU":
            menu = pygame.image.load("assets/menu.png")
            menu_rect = pygame.Rect(0, 0, width, height)
            window.blit(menu, (menu_rect))

            font = pygame.font.SysFont("Comic Sans", 25)
            text = font.render("Press any key to start", True, (0, 0, 0))
            text_rect = text.get_rect(center = (width / 2, height / 2.3))

            if self.text_alpha <= 30 or self.text_alpha > 225:
                self.alpha_switch = not self.alpha_switch

            if self.alpha_switch == True:
                self.text_alpha -= 3
                text.set_alpha(self.text_alpha)

            else:
                self.text_alpha += 3
                text.set_alpha(self.text_alpha)

            window.blit(text, text_rect)

        elif self.game_state == "RUNNING":
            if self.paused == False:
                pipe.spawn_pipes()
                scene.spawn_grass()
                scene.spawn_background()

                scene.draw_background()
                bird.draw_bird()
                pipe.draw_pipes()
                scene.draw_grass()
                game.draw_score()

                bird.move_bird()
                pipe.move_pipes()
                scene.move_grass()
                scene.move_background()

                game.check_collision()
                game.check_score()

            else:
                scene.draw_background()
                bird.draw_bird()
                pipe.draw_pipes()
                scene.draw_grass()

        elif self.game_state == "GAME_OVER":
            scene.draw_background()
            bird.draw_bird()
            pipe.draw_pipes()
            scene.draw_grass()

            overlay = pygame.Surface((640, 400))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(180)
            window.blit(overlay, (0, 0))

            font = pygame.font.SysFont("Comic Sans", 40)
            text = font.render(self.death_message, True, (225, 150, 0))
            text_rect = text.get_rect(center = (width / 2, height / 3))
            window.blit (text, text_rect)

            retry = pygame.image.load("assets/retry2.png")
            retry_rect = retry.get_rect(center = (width / 2, height / 2))
            window.blit(retry, retry_rect)

window = pygame.display.set_mode((width, height))
icon = pygame.image.load("assets/cheek2.png")
pygame.display.set_caption("Cheeky Bird")
pygame.display.set_icon(icon)

bird = Bird()
pipe = Pipe()
scene = Scene()
game = Game()
clock = pygame.time.Clock()

quack = pygame.mixer.Sound("assets/quack.mp3")
hit = pygame.mixer.Sound("assets/hit.mp3")

while True:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.game_state == "MENU":
                game.game_state = "RUNNING"

            if game.game_state == "RUNNING" and event.key == pygame.K_p:
                game.paused = not game.paused

            elif game.game_state == "RUNNING" and not game.paused and event.key == pygame.K_SPACE:
                bird.velocity.y = -1 * bird.flap
                quack.play()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if game.game_state == "GAME_OVER" and (mouse_x >= width / 2 - 25 and mouse_x <= width / 2 + 25) and (mouse_y >= height / 2 - 25 and mouse_y <= height / 2 + 25):
                bird.pos = Vector2(bird.x, bird.y)
                bird.velocity = Vector2(300, 0)
                pipe.pos = []
                pipe.pos.append(Vector2(width, random.randint(int(height / 2), height - 50)))
                game.score = 0
                game.game_state = "RUNNING"

    window.fill((0, 0, 0))
    game.check_state()
    pygame.display.update()