import pygame
from math import sqrt

font_name = "./Game_Files/UI/Carnevalee Freakshow.ttf"

best_score = 0


class ScoringSystem:
    """
    A class representing the scoring system.
    """

    def __init__(self):
        """
        Initialize the Scoring object.
        
        Attributes:
        - score: The current score of the player.
        - scroll_speed: The speed at which the game scrolls.
        - timer: The timer used to track the game time.
        - score_font: The font used to render the score text.
        - calculated_score: The calculated score based on the current score.
    """
        self.score = 0
        self.scroll_speed = 7
        self.timer = 0
        self.score_font = pygame.font.Font(font_name, 50)
        self.calculated_score = 0

    def update(self, clock, speed=0.003):
        """
        Update the scoring system.

        Parameters:
        - clock: The clock object used to measure time.
        - speed: The speed at which the game scrolls.

        Returns: None
        """
        global best_score
        self.timer += clock.tick(60) / 1000
        self.scroll_speed += speed
        self.score += self.scroll_speed
        self.calculated_score = int(sqrt(self.score))
        best_score = max(best_score, self.calculated_score)

    def draw(self, screen):
        """
        Draw the score on the screen.

        Parameters:
        - screen: The screen object to draw on.

        Returns: None
        """
        score_text = self.score_font.render(
            f"score: {self.calculated_score}", True, (255, 255, 255))
        screen.blit(score_text, (13, 13))

    def calculate_score(self):
        """
        Calculate the current score and the best score.

        Returns:
        - A tuple containing the current score and the best score.
        """
        return self.calculated_score, best_score
