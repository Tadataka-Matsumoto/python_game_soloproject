import sys
from time import sleep# Python標準ライブラリのtimeモジュールからsleep()関数をインポート(p57)

import pygame
from settings import Settings#p9
from game_stats import GameStats#宇宙船が破壊されたときにゲームを一時停止できるように？？？(p57)
from scoreboard import Scoreboard#得点表示できるように追加(p77)
from button import Button#ボタンクラスを呼び出す(p66)
from ship import Ship#p13
from bullet import Bullet#p30弾を発射する
from alien import Alien#p38


class AlienInvasion:
    # ゲームのアセットと動作を管理する全体的なクラス(p6)

    def __init__(self):
        # ゲームを初期化し、ゲームのリソースを作成する(p6)
        pygame.init()
        self.settings = Settings()#p9
        
        # self.bg_color = (230, 230, 230)# 背景色を設定する(p8)


        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))#p10
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)#p24fullscreenにしたけど、画面がすごいことになる
        # self.settings.screen_width = self.screen.get_rect().width#p24
        # self.settings.screen_height = self.screen.get_rect().height#p24

        pygame.display.set_caption("エイリアン侵略")#p6

        #ゲームの統計情報を格納するインスタンスを生成する(p58)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)#スコアボードをインスタンス化(p77)

        self.ship = Ship(self)#宇宙船のインスタンスを作る(p13)
        self.bullets = pygame.sprite.Group()#弾のグループを作る(p29)
        self.aliens = pygame.sprite.Group()#エイリアンのグループを作る(p39)

        self._create_fleet()#_create_fleetメソッド呼び出し(p39)

        #playボタンを作成する(p67)
        self.play_button = Button(self, "Play")


    def run_game(self):
        # ゲームのメインループを開始する(p6)

        while True:
            self._check_events()#p15, p61で移動

            if self.stats.game_active:#self._ship_hit()でstats.game_activeがFalseになるとフリーズする(p61)
                self.ship.update()#p19
                self._update_bullets()#p33
                self._update_aliens()#p47

            self._update_screen()#p15

    def _update_bullets(self):#p33
        #弾の位置を更新し、古い弾を廃棄する
        #弾の位置を更新する
        self.bullets.update()#p29→p33

        #見えなくなった弾を廃棄する(p32)
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            # print(len(self.bullets))
        
        self._check_bullet_alien_collisions()#エイリアンとの衝突と分けるためのリファクタリングとして追加(p54)


    def _check_bullet_alien_collisions(self):#リファクタリング(p54-55)
        #弾とエイリアンの衝突に対応する(p55)
        #弾がエイリアンに当たったかを調べる(p51)
        # その場合は対象の弾とエイリアンを廃棄する
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)#全エイリアンと全弾をを比較し重なっているものを比較(p51に説明)

        if collisions:#弾がエイリアンに当たったら得点を増やす(p79)
            # print(collisions)
            for aliens in collisions.values():#エイリアンの数を得点にする！collisionsは辞書らしい(p80)
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()#p79
            self.sb.check_high_score()#常に得点がハイスコアか確認できる！！(p84)

        if not self.aliens:#(p53)
            #存在する弾を破壊し、新しい艦隊を作成する(p53)
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()#レベルアップ（speedup)用のコード(p73)

            #レベルを増やす(p86)
            self.stats.level += 1
            self.sb.prep_level()

        

    def _check_events(self):#p15
        # キーボードとマウスのイベントに対応する(p7,p17)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#p7
                sys.exit()#p7
            elif event.type == pygame.KEYDOWN:#p17
                self._check_keydown_events(event)#p23
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)#p23
            elif event.type == pygame.MOUSEBUTTONDOWN:#マウスでplayボタンを押すとスタート(P68)
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        #プレイヤーがPlayボタンをクリックしたら新規ゲームを開始する(p68)
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)#ゲーム中にクリックされないように設定(p70)
        if button_clicked and not self.stats.game_active:#(p70で修正)
            #ゲームの設定値（レベルアップしたスピード）をリセット(p74)
            self.settings.initialize_dynamic_settings()#p74
            #ゲームの統計情報をリセットする(p69)
            self.stats.reset_stats()#game_stats.pyの初期化と同じリセット追加、これで宇宙船が3つになる(p69)
            self.stats.game_active = True
            self.sb.prep_score()#得点を0に戻す(p79)
            self.sb.prep_level()#レベルを1から開始する(p87)
            self.sb.prep_ships()#プレイボタン押したときに表示(p90)

            #残ったエイリアンと弾を廃棄する(p69)
            self.aliens.empty()
            self.bullets.empty()

            # 新しい艦隊を生成し、宇宙船を中央に配置する、宇宙船がやられた後(_ship_hit)とかでこの設定(p69)
            self._create_fleet()
            self.ship.center_ship()

            #マウスカーソルを非表示にする(p70)
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):  # p23
        # キーを押すイベントに対応する
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True#p18
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True#p20
        elif event.key == pygame.K_q:#Qを押したら終了(p24)
            sys.exit()
        elif event.key == pygame.K_SPACE:#弾を発射(p30)
            self._fire_bullet()#弾を発射(p30)

    def _check_keyup_events(self, event):#p23
        #キーを離すイベントに対応する
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False#p18
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False#p20

    def _fire_bullet(self):
        #新しい弾を生成し、bulletsグループに追加するp30
        if len(self.bullets) < self.settings.bullets_allowed:#setting.pyで規定した弾数条件追加(p33)
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):#p39
        #エイリアンの艦隊を作成する
        #エイリアンを1匹作成し、1列のエイリアンの数を求める(p41)
        #各エイリアンの間にはエイリアン1匹分のスペースを空ける(p41)
        alien = Alien(self)#エイリアンの幅や高さを算出するために生成(p39)
        alien_width, alien_height = alien.rect.size#p44
        available_space_x = self.settings.screen_width - (2 * alien_width)#1匹(+スペース)のエイリアンの以外のスペース(p41)
        number_aliens_x = available_space_x // (2 * alien_width)#エイリアンの横の数(p41)

        #画面に収まるエイリアンの列数を決定する(p44)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                                (3 * alien_height) - ship_height)#宇宙船1隻とエイリアン3匹分の高さのスペース(p44)
        number_rows = available_space_y // (2 * alien_height)#エイリアンの縦の数(p44)

        #エイリアンの艦隊を作成する
        for row_number in range(number_rows):#列のエイリアンの作成(p)
            for alien_number in range(number_aliens_x):#行（横）のエイリアンを作成(p41)
                self._create_alien(alien_number, row_number)


    def _create_alien(self, alien_number, row_number):#P43でリファクタリング,p44で引数row_numberが追加
        #エイリアンを1匹作成し列の中に配置する #画面に収まるエイリアンの列数を決定する(p41)
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size#sizeにrectオブジェクトの幅と高さがタプルで入っている(p44)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number#リファクタリング(p44)
        self.aliens.add(alien)

    def _update_aliens(self):
        # 艦隊が画面の端にいるか確認してから
        # 艦隊にいる全エイリアンの位置を更新する(p48,p50)
        self._check_fleet_edges()#p50
        self.aliens.update()#p48

        #エイリアンと宇宙船の衝突を探す(p56)
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()#(p59)
            #print('宇宙船にぶつかった!!')

        #画面の一番下に到達したエイリアンを探す(p60)
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        #エイリアンが画面の端に達した場合に適切な処置を行う(p49)
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        #艦隊を下に移動し、横移動の方向を変更する(p49)
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1#右は1,左は-1なので-1を掛けることで方向変換(p50)

    def _check_aliens_bottom(self):#p59で新規追加
        #エイリアンが画面の一番下に到達したかを確認する(p59-60)
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #宇宙船を破壊した時と同じように扱う(p60)
                self._ship_hit()
                break

    def _ship_hit(self):#p58で新規作成
        #エイリアンと宇宙船の衝突に対応する(p58)
        #残りの宇宙船の数を減らす(p58)
        if self.stats.ships_left > 0:#宇宙船の数が残っているか条件分岐(p61)
            self.stats.ships_left -= 1
            self.sb.prep_ships()#1つ宇宙船残数表示を減らす(p90)

            #残ったエイリアンと弾を廃棄する(p58)
            self.aliens.empty()
            self.bullets.empty()

            #新しい艦隊を生成し、宇宙船を中央に配置する(p58)
            self._create_fleet()
            self.ship.center_ship()#center_shipメソッドも後(p59)で作る(p58)

            #一時停止する(p58)
            sleep(0.5)
        else:#宇宙船の数が残っているか条件分岐(p61)
            self.stats.game_active = False#p61
            pygame.mouse.set_visible(True)#p71


    def _update_screen(self):#p15
       
        # (表現変わる) 画面上の画像を更新し、あたらしい画面に切り替える(p15)
        self.screen.fill(self.settings.bg_color) # ループを追加するたびに画面を再描画する(p8,p10)
        self.ship.blitme()#画面上の宇宙船を描画する（p13 ）

        for bullet in self.bullets.sprites():#弾丸を描画(p30)
            bullet.draw_bullet()
        self.aliens.draw(self.screen)#エイリアンを描画(p39)

        #得点の情報を描画する(p77)
        self.sb.show_score()#scoreboard.pyでのメソッドを呼び出す(p77)


        #ゲームが非アクティブ状態のときに「Play」ボタンを描画する(p67)
        if not self.stats.game_active:
            self.play_button.draw_button()

       
        pygame.display.flip() # 最新の状態の画面を表示する(p7)


if __name__ == '__main__': # ゲームのインスタンスを作成し、ゲームを実行する(p7)
    ai = AlienInvasion()
    ai.run_game()

