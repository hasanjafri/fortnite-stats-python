from flask import Flask, jsonify
from flask_restful import Resource, Api
from enum import Enum
from fortnite_python import Fortnite

class Platform(Enum):
    PC = 'pc'
    XBOX = 'xbl'
    PSN = 'psn'


class Mode(Enum):
    SOLO = 'p2'
    DUO = 'p10'
    SQUAD = 'p9'

application = Flask(__name__)
api = Api(application)
fortnite_stats_client = Fortnite('023c9de2-7b48-4143-a1c3-707bc5153b92')

class FortnitePlayerStats(Resource):
    def get(self, player_id, platform, mode):
        fortnite_player = fortnite_stats_client.player(player=player_id, platform=self.parse_platform(platform))
        res = fortnite_player.getStats(mode=self.parse_mode(mode))
        return jsonify(self.generate_res_dict(res))

    def generate_res_dict(self, stats_res):
        return {'wins': stats_res.wins, 'total': stats_res.total, 'kd': stats_res.kd, 'win_ratio': stats_res.winratio, 'kills': stats_res.kills,
                'score': stats_res.score, 'score_match': stats_res.score_match, 'kills_match': stats_res.kills_match, 'top3': stats_res.top3, 'top5': stats_res.top5,
                'top6': stats_res.top6, 'top10': stats_res.top10, 'top12': stats_res.top12, 'top25': stats_res.top25}

    def parse_platform(self, platform):
        if platform.lower() == 'pc':
            return(Platform.PC)
        if platform.lower() == 'xbox':
            return(Platform.XBOX)
        if platform.lower() == 'psn':
            return(Platform.PSN)

    def parse_mode(self, mode):
        if mode.lower() == 'solo':
            return(Mode.SOLO)
        if mode.lower() == 'duo':
            return(Mode.DUO)
        if mode.lower() == 'squad':
            return(Mode.SQUAD) 

api.add_resource(FortnitePlayerStats, '/<string:player_id>/<string:platform>/<string:mode>/')

if __name__ == '__main__':
    application.run(debug=True)