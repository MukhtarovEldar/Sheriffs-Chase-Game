import pygame
from math import sqrt

font_name = "./Game_Files/UI/Carnevalee Freakshow.ttf"

best_score = 0


class ScoringSystem:
    def __init__(self):
        self.score = 0
        # self.best_score = 0
        self.scroll_speed = 7
        self.timer = 0
        self.score_font = pygame.font.Font(font_name, 50)
        self.calculated_score = 0

    def update(self, clock, speed=0.003):
        global best_score
        self.timer += clock.tick(60) / 1000
        self.scroll_speed += speed
        self.score += self.scroll_speed
        self.calculated_score = int(sqrt(self.score))
        best_score = max(best_score, self.calculated_score)

    def draw(self, screen):
        score_text = self.score_font.render(
            f"score: {self.calculated_score}", True, (255, 255, 255))
        screen.blit(score_text, (13, 13))

    def calculate_score(self):
        return self.calculated_score, best_score
