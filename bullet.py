import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #宇宙船から発射される弾を管理するクラス(p27)

    def __init__(self, ai_game):
        #宇宙船の現在の位置から弾のオブジェクトを生成する(p27)

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        #弾のrectを(0, 0)の位置に作成してから、正しい位置を設定する(p28)
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        #弾の位置を浮動小数点数で保存する(p28)
        self.y = float(self.rect.y)

    def update(self):
        #画面上の弾を移動する(p28)
        self.y -= self.settings.bullet_speed
        # rectの位置を更新する(p28)
        self.rect.y = self.y

    def draw_bullet(self):
        #画面に弾を描画する(p28)
        pygame.draw.rect(self.screen, self.color, self.rect)

