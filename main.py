# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import *
from util.common import *

class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)
    def run(self):
        d2 = abs(self.me.location.y - self.foe_goal.location.y)
        d1 = abs(self.ball.location.y - self.foe_goal.location.y)
        is_in_front_of_ball = d1 > d2
        available_boosts = [boost for boost in self.boosts if boost.large and boost.active]
        closest_boost = None
        closest_distance = 10000
        ball_to_me_x = abs(self.ball.location.x-self.me.location.x)
        ball_to_me_y = abs(self.ball.location.y-self.me.location.y)
        ball_distance_squared = ball_to_me_y*ball_to_me_y + ball_to_me_x*ball_to_me_x
        ball_distance = math.sqrt(ball_distance_squared)

        for boost in available_boosts:
            distance = (self.me.location - boost.location).magnitude()
            if closest_boost is None or distance < closest_distance:
                closest_boost = boost
                closest_distance = distance

        if self.get_intent() is not None:
            return
        if self.kickoff_flag:
            self.set_intent(kickoff())
            return
        targets = {
            'at_opponent_goal': ((self.foe_goal.left_post), (self.foe_goal.right_post)),
            'away_from_our_net': ((self.friend_goal.right_post), (self.friend_goal.left_post))
        }

        hits = find_hits(self, targets)
        if len(hits['at_opponent_goal']) > 0:
            self.set_intent(hits['at_opponent_goal'][0])
            return             
         
        if len(hits['away_from_our_net']) > 0:
            self.set_intent(hits['away_from_our_net'][0])
            return   

        if closest_boost is not None and self.me.boost < 33:
            self.set_intent(goto(closest_boost.location))
            return            

