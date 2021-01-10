class Settings:
    #エイリアン侵略の全設定を格納するクラス

    def __init__(self):
        #ゲームの初期設定
        #画面に関数設定(p9)
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        
        self.ship_limit = 3#使用できる宇宙船の数(p57)

        #弾の設定(p27)
        self.bullet_width = 3
        # self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3#p32(弾の制限)

        self.fleet_drop_speed = 10#エイリアンの設定(p46)

        #ゲームのスピードアップする速さ(p72)
        self.speedup_scale = 1.1#p72
        #エイリアンの点数が増加する量(p81)
        self.score_scale = 1.5

        self.initialize_dynamic_settings()#関数実行追加(p72)

    def initialize_dynamic_settings(self):
        #ゲーム中に変更される設定値を初期化する

        self.ship_speed = 1.5#宇宙船の設定(p21、p73でスピードアップ用に移動)
        self.alien_speed = 1.0##エイリアンの設定(p46、p73でスピードアップ用に移動)
        self.bullet_speed = 1.0#弾の設定(p27)、弾のスペード調整の記述p54)、p73でスピードアップ用に移動

        #艦隊の移動方向を表し、1は右、-1は左、に移動することを表す(p48)
        self.fleet_direction = 1

        #点数(p78)
        self.alien_points = 50

    def increase_speed(self):
        #速度の設定値を増やす(p73)
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)#レベルアップで得点アップ(p81)
        # print(self.alien_points)#得点アップの確認(p81)










