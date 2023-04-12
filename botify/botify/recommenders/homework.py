from .toppop import TopPop
from .recommender import Recommender
import random


class Homework(Recommender):
    def __init__(self, tracks_redis, catalog, history):
        self.tracks_redis = tracks_redis
        self.fallback = TopPop(tracks_redis, catalog.top_tracks[:100])
        self.catalog = catalog
        self.history = history

    def get_shuffle(self, track, user: int, prev_track: int, prev_track_time: float):
        tracks = self.tracks_redis.get(track)
        if tracks is None:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)
        tracks = self.catalog.from_bytes(tracks)
        recommendations = tracks.recommendations

        if recommendations is None:
            return self.fallback.recommend_next(user, prev_track, prev_track_time)

        shuffled = list(recommendations)
        random.shuffle(shuffled)
        for i in shuffled:
            if not self.history.check_bad(user, i):
                return i
        return self.fallback.recommend_next(user, prev_track, prev_track_time)

    def recommend_next(self, user: int, prev_track: int, prev_track_time: float) -> int:
        self.history += (user, prev_track, prev_track_time)

        if prev_track_time < 0.4:
            top = self.history.get_top(user)
            if top is None:
                return self.fallback.recommend_next(user, prev_track, prev_track_time)

            return self.get_shuffle(top, user, prev_track, prev_track_time)

        return self.get_shuffle(prev_track, user, prev_track, prev_track_time)
