import pygame.font


class Button:#playボタンを作成するためのclassを作成(p65)

    def __init__(self, ai_game, msg):
        #ボタンの属性を初期化する(p65)
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #ボタンの大きさと属性を設定する(p65)
        self.width, self.height = 200, 50
        self.button_color =(0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #ボタンのrectオブジェクトを生成し画面の中央に配置する(p65)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #ボタンのメッセージは一度だけ準備する必要がある(p65)
        self._prep_msg(msg)

    def _prep_msg(self, msg):#p65で追加
        #msgを画像に変換しボタンの中央に配置する(p65)
        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #空白のボタンを描画し、メッセージを描画する(p66)
        self.screen.fill(self.button_color, self.rect)#p8の画面描画と同じ表現
        self.screen.blit(self.msg_image, self.msg_image_rect)#p12のshipのbiltと同じ表現

