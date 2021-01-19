import pygame.font#p75
from pygame.sprite import Group#p88の宇宙船残数表示で追加

from ship import Ship#宇宙船残数表示で追加(p88)

class Scoreboard:
    #得点の情報をレポートするクラス(p75)

    def __init__(self, ai_game):
        #得点を記録するための属性を初期化する(settings,screen,statsオブジェクトにアクセスするため)(p75-76)
        self.ai_game = ai_game#p88で追加def prep_shipsで使用するため(p88)
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        #得点表示用のフォントを設定する(p76)
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)#p76だけどp65参照

        #初期の得点画像を準備する(p76, p83)
        self.prep_score()#p76
        self.prep_high_score()#p83
        self.prep_level()#p85
        self.prep_ships()#p89 

    def prep_score(self):
        #得点を描画用の画像に変換する(p76)
        # score_str = str(self.stats.score)#文字に変換(p76)
        rounded_score = round(self.stats.score, -1)#p82
        score_str = "{:,}".format(rounded_score)#得点をコンマを含んだ数字の文字列に変換(p82)

        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)#画像に変換(p76,p65のbuttonと同じ)

        #画面の右上に得点を表示する(p76)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        #ハイスコアを描画用の画像に変換する(p83)
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)#ハイスコアの画像準備(p65のbuttonと同じ)
        
        #画面上部の中央にハイスコアを表示する(p83)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        #新しいハイスコアかチェックし、必要であれば表示を更新する(p84)
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def show_score(self):
        #画面に得点とレベルを描画する(p76-77, p84, p86, p89)(p66のボタンの長方形と同じ)
        self.screen.blit(self.score_image, self.score_rect)#p76
        self.screen.blit(self.high_score_image, self.high_score_rect)#p84
        self.screen.blit(self.level_image, self.level_rect)#p86
        self.ships.draw(self.screen)#宇宙船残数表示(p89)

    def prep_level(self):
        """レベルを描画用の画像に変換する(p86)"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
            self.text_color, self.settings.bg_color)

        #得点の下にレベルを配置する
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10


    def prep_ships(self):#残数表示のため追加(p89)
        """宇宙船の残数を表示する"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)




