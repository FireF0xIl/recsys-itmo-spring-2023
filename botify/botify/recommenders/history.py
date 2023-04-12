from random import choice


class HistoryManager:
    def __init__(self):
        self.dict = {}

    def __iadd__(self, other):
        user, track, track_time = other
        self.dict[user] = self.dict.get(user, History())
        self.dict[user] += (track, track_time)
        return self

    def check_bad(self, user, track):
        self.dict[user] = self.dict.get(user, History())
        return self.dict[user].check_bad(track)

    def get_top(self, user):
        self.dict[user] = self.dict.get(user, History())
        return self.dict[user].get_top()


class History:
    def __init__(self):
        self.tracks = set()
        self.bad = set()
        self.top = set()
        self.duration = 0

    def __iadd__(self, other):
        previous_track, time = other
        if time < 0.5:
            self.bad.add(previous_track)
        elif time > 0.8:
            self.duration += 1
            self.top.add(previous_track)
        self.tracks.add(previous_track)
        return self

    def check_bad(self, track):
        return track in self.bad

    def get_top(self):
        if len(self.top) > 0:
            return choice(tuple(self.top))
        else:
            return None
