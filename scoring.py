import pygame

font_name = "./Game_Files/UI/Carnevalee Freakshow.ttf"

class ScoringSystem:
    def __init__(self):
        self.score = 0
        self.scroll_speed = 7
        self.timer = 0
        self.score_font = pygame.font.Font(font_name, 50)

    def update(self, clock):
        self.timer += clock.tick(60) / 1000
        self.scroll_speed += 0.003
        self.score += self.scroll_speed

    def draw(self, screen):
        score_text = self.score_font.render(f"score: {int(self.score)}", True, (255, 255, 255))
        screen.blit(score_text, (13, 13))