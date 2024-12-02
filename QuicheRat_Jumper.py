#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 18:31:26 2024

@author: amelie
"""

import pygame
import sys
import random as rd

class Player:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load('Rat_assis.png'), (135, 105))
        self.x = 170
        self.y = 650
        self.y_change = 0
        self.x_change = 0
        self.jump = False
        self.speed = 3

    def update_position(self, gravity=0.4, jump_height=10):
        if self.jump:
            self.y_change = -jump_height
            self.jump = False
        self.y += self.y_change
        self.y_change += gravity

    def move(self, direction):
        self.x_change = direction * self.speed

    def stop(self):
        self.x_change = 0

    def update_image(self):
        """Update the player's image based on movement direction."""
        if self.x_change < 0:  # Moving left
            self.image = pygame.transform.scale(pygame.image.load('Rat_assis.png'), (135, 105))
        elif self.x_change > 0:  # Moving right
            self.image = pygame.transform.flip(
                pygame.transform.scale(pygame.image.load('Rat_assis.png'), (135, 105)), True, False
            )

class Quiche:
    def __init__(self):
        try:
            self.image = pygame.transform.scale(pygame.image.load('Quiche.png'), (70, 70))
        except pygame.error as e:
            print(f"Erreur de chargement de l'image : {e}")
            self.image = None  # Pour éviter une erreur fatale si l'image manque
        self.x = None
        self.y = None
        self.active = False

    def spawn(self, platform):
        """Fait apparaître la quiche sur une plateforme."""
        self.x = platform[0] + (platform[2] // 2) - 35  # Centrer sur la plateforme
        self.y = platform[1] - 70  # Placer au-dessus de la plateforme
        self.active = True

    def draw(self, screen):
        """Dessine la quiche s'il est actif."""
        if self.active:
            if self.image:
                screen.blit(self.image, (self.x, self.y))
            else:
                print("L'image de la quiche est introuvable ou non chargée.")

    def check_collision(self, player):
        """Vérifie si le joueur attrape la quiche."""
        if self.active and player.x + 40 < self.x + 70 and player.x + 95 > self.x and player.y + 60 < self.y + 70 and player.y + 105 > self.y:
            self.active = False  # Désactive la quiche
            return True
        return False
        if self.active and self.y > 750:
            self.active = False

class Booster:
    def __init__(self):
        try:
            self.image = pygame.transform.scale(pygame.image.load('Caron.png'), (70, 70))
        except pygame.error as e:
            print(f"Erreur de chargement de l'image : {e}")
            self.image = None  # Pour éviter une erreur fatale si l'image manque
        self.x = None
        self.y = None
        self.active = False

    def spawn(self, platform):
        """Fait apparaître le booster sur une plateforme."""
        self.x = platform[0] + (platform[2] // 2) - 35  # Centrer sur la plateforme
        self.y = platform[1] - 70  # Placer au-dessus de la plateforme
        self.active = True

    def draw(self, screen):
        """Dessine le booster s'il est actif."""
        if self.active:
            if self.image:
                screen.blit(self.image, (self.x, self.y))
            else:
                print("L'image du booster est introuvable ou non chargée.")

    def check_collision(self, player):
        """Vérifie si le joueur attrape le booster."""
        if self.active and player.x + 40 < self.x + 70 and player.x + 95 > self.x and player.y + 60 < self.y + 70 and player.y + 105 > self.y:
            self.active = False  # Désactive le booster
            print("Collision avec le booster détectée !")
            return True
        return False
        if self.active and self.y > 750:
            self.active = False

class Enemy:
    def __init__(self):
        try:
            self.image = pygame.transform.scale(pygame.image.load('Chartes.png'), (70, 70))
        except pygame.error as e:
            print(f"Erreur de chargement de l'image : {e}")
            self.image = None  # Prévenir une erreur si l'image manque
        self.x = None
        self.y = None
        self.active = False
        self.speed = 2  # Vitesse de déplacement latéral
        self.direction = 1  # 1 pour droite, -1 pour gauche

    def spawn(self):
        """Créer un ennemi à une position aléatoire."""
        self.x = rd.randint(10, 320)
        self.y = rd.randint(-70, -10)
        self.active = True
        print(f"Ennemi apparu à ({self.x}, {self.y})")

    def move(self):
        """Déplacer l'ennemi latéralement."""
        if not self.active:
            return

        # Mouvement d'aller-retour
        self.x += self.direction * self.speed
        if self.x <= 10 or self.x >= 320:
            self.direction *= -1  # Inverse la direction

    def draw(self, screen):
        """Dessiner l'ennemi s'il est actif."""
        if self.active:
            if self.image:
                screen.blit(self.image, (self.x, self.y))
            else:
                pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 70, 70))  # Rectangle rouge temporaire

    def check_collision(self, player):
        """Vérifie si le joueur entre en collision avec l'ennemi."""
        if self.active and player.x + 40 < self.x + 70 and player.x + 95 > self.x and player.y + 60 < self.y + 70 and player.y + 105 > self.y:
            return True
        return False


class PlatformManager:
    def __init__(self):
        self.platforms = [[175, 730, 70, 10],
                          [85, 620, 70, 10],
                          [265, 620, 70, 10],
                          [175, 510, 70, 10],
                          [85, 400, 70, 10],
                          [265, 400, 70, 10],
                          [175, 290, 70, 10],
                          [85, 180, 70, 10],
                          [265, 180, 70, 10],
                          [175, 70, 70, 10]]
        self.score = 0
        self.next_booster_score = rd.randint(30, 60)       
        self.next_quiche_score = rd.randint(20, 40)
        if self.next_booster_score == self.next_quiche_score:
            self.next_booster_score += 5

    def update_platforms(self, player_y, y_change, booster, quiche):
        if player_y < 375 and y_change < 0:
            for platform in self.platforms:
                platform[1] -= y_change
            # Déplace également le booster si actif
            if booster.active:
                booster.y -= y_change
            # Déplace également la quiche si active
            if quiche.active:
                quiche.y -= y_change

        for platform in self.platforms:
            if platform[1] > 750:
                self.platforms.remove(platform)
                new_platform = [rd.randint(10, 320), rd.randint(-50, -10), 70, 10]
                self.platforms.append(new_platform)
                self.score += 1

                # Vérifie si le score atteint le seuil pour un booster
                if self.score >= self.next_booster_score and not booster.active:
                    booster.spawn(new_platform)  # Associe le booster à la nouvelle plateforme
                    self.next_booster_score += rd.randint(30, 60)
                    if self.next_booster_score == self.next_quiche_score:
                        self.next_booster_score += 5
                    print(f"Prochain booster à {self.next_booster_score} points.")
                
                # Vérifie si le score atteint le seuil pour une quiche
                if self.score >= self.next_quiche_score and not quiche.active:
                    quiche.spawn(new_platform)  # Associe le booster à la nouvelle plateforme
                    self.next_quiche_score += rd.randint(20, 40)
                    if self.next_booster_score == self.next_quiche_score:
                        self.next_quiche_score += 5
                    print(f"Prochaine quiche à {self.next_booster_score} points.")

    def draw(self, screen):
        blocks = []
        for platform in self.platforms:
            block = pygame.draw.rect(screen, (0, 0, 0), platform, 0, 3)
            blocks.append(block)
        return blocks

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 400, 750
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption('QuicheRat Jumper')

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.font = pygame.font.Font('OldeEnglish.ttf', 21)
        self.font_game_over = pygame.font.Font('OldeEnglish.ttf', 40)

        self.player = Player()
        self.quiche = Quiche()
        self.booster = Booster()
        self.platform_manager = PlatformManager()

        self.super_jump = 1
        self.nb_quiche = 0
        self.high_score = 0
        
        self.enemies = []  # Liste d'ennemis
        self.next_enemy_score = rd.randint(50, 70)  # Score pour le prochain ennemi
        
        self.game_over = False
        self.background_color = (180, 180, 180)

    def check_collisions(self, blocks):
        for block in blocks:
            if block.colliderect([self.player.x + 40, self.player.y + 60, 55, 5]) and not self.player.jump and self.player.y_change > 0:
                self.player.jump = True

    def reset_game(self):
        self.player = Player()
        self.platform_manager = PlatformManager()
        self.quiche = Quiche()
        self.booster = Booster()
        self.enemies = []
        self.next_enemy_score = rd.randint(50, 70)
        self.super_jump = 1
        self.game_over = False


    def render_texts(self):
        super_jump_text = self.font.render(f"Doubles sauts (Espace) : {self.super_jump}", True, (0, 0, 0), self.background_color)
        self.screen.blit(super_jump_text, (5, 0))
        
        nb_quiche_text = self.font.render(f"Quiches mangées : {self.nb_quiche}", True, (0, 0, 0), self.background_color)
        self.screen.blit(nb_quiche_text, (5, 30))

        high_score_text = self.font.render(f"Meilleur score : {self.high_score}", True, (0, 0, 0), self.background_color)
        self.screen.blit(high_score_text, (285, 0))

        score_text = self.font.render(f"Score : {self.platform_manager.score}", True, (0, 0, 0), self.background_color)
        self.screen.blit(score_text, (325, 30))

        if self.game_over:
            game_over_text = self.font_game_over.render("Perdu", True, (0, 0, 0), self.background_color)
            self.screen.blit(game_over_text, (150, 180))
            game_over_text = self.font_game_over.render("Espace pour jouer !", True, (0, 0, 0), self.background_color)
            self.screen.blit(game_over_text, (80, 260))

    def run(self):
        while True:
            self.clock.tick(self.fps)
            self.screen.fill(self.background_color)
            self.screen.blit(self.player.image, (self.player.x, self.player.y))
    
            blocks = self.platform_manager.draw(self.screen)
            self.render_texts()
            
            # Gestion des ennemis
            for enemy in self.enemies:
                enemy.move()
                enemy.draw(self.screen)
                if enemy.check_collision(self.player):
                    print("Collision avec un ennemi ! Partie perdue.")
                    self.game_over = True
        
            # Vérifie si un nouvel ennemi doit apparaître
            if self.platform_manager.score >= self.next_enemy_score:
                new_enemy = Enemy()
                new_enemy.spawn()
                self.enemies.append(new_enemy)
                self.next_enemy_score += rd.randint(50, 70)
                print(f"Prochain ennemi à {self.next_enemy_score} points.")
    
            # Dessine le booster et gère les collisions
            self.booster.draw(self.screen)
            if self.booster.check_collision(self.player):
                self.super_jump += 1
                
            # Dessine la quiche et gère les collisions
            self.quiche.draw(self.screen)
            if self.quiche.check_collision(self.player):
                self.nb_quiche += 1
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_over:
                            self.reset_game()
                        elif self.super_jump > 0:
                            self.super_jump -= 1
                            self.player.y_change = -15
                    if event.key == pygame.K_LEFT:
                        self.player.move(-1)
                    if event.key == pygame.K_RIGHT:
                        self.player.move(1)
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self.player.stop()
    
            if self.player.y < 675:
                self.player.update_position()
            else:
                self.game_over = True
    
            self.player.x += self.player.x_change
            self.player.update_image()
            if not self.game_over :
                self.check_collisions(blocks)
            self.platform_manager.update_platforms(self.player.y, self.player.y_change, self.booster, self.quiche)
            
            # Synchronisation des ennemis avec le mouvement global
            if self.player.y < 375 and self.player.y_change < 0:
               for enemy in self.enemies:
                   enemy.y -= self.player.y_change
    
            if self.player.x < -30:
                self.player.x = -30
            elif self.player.x > 295:
                self.player.x = 295
    
            if self.platform_manager.score > self.high_score:
                self.high_score = self.platform_manager.score
    
            pygame.display.flip()



if __name__ == "__main__":
    Game().run()