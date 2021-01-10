import pygame

class Ship:##宇宙船を管理するクラス(p11)
    

    def __init__(self, ai_game):
        
        self.screen = ai_game.screen#宇宙船を初期化し、開始時の位置を設定する(p11)
        self.screen_rect = ai_game.screen.get_rect()#p11

        self.settings = ai_game.settings#p21で追加

        self.image = pygame.image.load('images/ship.bmp')#宇宙船の画像を読み込み、サイズを取得する(p11)
        self.rect = self.image.get_rect()#p11
        self.rect.midbottom = self.screen_rect.midbottom#新しい宇宙船を画面下部の中央に配置する(p12)

        #宇宙船の水平位置の浮動小数点数を格納する(p21)
        self.x = float(self.rect.x)#p21で追加

        #左右の移動フラグ(初期値としてFalseを設定)(p18)
        self.moving_right = False#p18
        self.moving_left = False#p19
    
    def update(self):
        #移動フラグによって宇宙船の位置を更新する(p18)
       
        if self.moving_right and self.rect.right < self.screen_rect.right:#p18とp22
            # self.rect.x += 1#p18
            self.x += self.settings.ship_speed #宇宙船のxの値を更新する（rectではない)(p21)
        if self.moving_left and self.rect.left > 0:#p19とp22
            # self.rect.x -= 1#p19
            self.x -= self.settings.ship_speed#宇宙船のxの値を更新する（rectではない)(p21)

        
        self.rect.x = self.x#self.xからrectオブジェクトの位置を更新する(p21)


    def center_ship(self):
        #宇宙船を画面の中央に配置する(p59)
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)


    def blitme(self):
        self.screen.blit(self.image, self.rect)#宇宙船を現在位置に描画する(p12)
