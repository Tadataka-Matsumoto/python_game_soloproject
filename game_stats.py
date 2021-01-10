

class GameStats:#統計情報としてgame_stats.pyを作成し、クラスを作る(P56)

    #エイリアン侵略ゲームの統計情報を記録する

    def __init__(self, ai_game):
        #統計情報を初期化する(p57)
        self.settings = ai_game.settings
        self.reset_stats()#プレイヤーが新規にゲームを開始するたびにreset_stats()を呼び出す(p57)

        #エイリアン侵略ゲームをアクティブな状態で開始する(p60)
        # self.game_active = True

        #非アクティブな状態でゲームを開始する
        self.game_active = False

        #ハイスコアはリセットしない(p83)
        self.high_score = 0

    def reset_stats(self):
        #ゲーム中に変更される統計情報を初期化する(p57)
        self.ships_left = self.settings.ship_limit
        self.score = 0#スコアを付ける(p75)

