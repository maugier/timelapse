import datetime
import logging
import random
import transform
import timelapse

# merge two iterators producing sorted values
def merge(s1, s2):
    try:
        x1 = next(s1)
    except StopIteration:
        yield from s2
        return

    try:
        x2 = next(s2)
    except StopIteration:
        yield from s1
        return

    while True:
        if x2 > x1:
            yield x1
            try:
                x1 = next(s1)
            except StopIteration:
                yield x2
                yield from s2
                return
        else:
            yield x2
            try:
                x2 = next(s2)
            except StopIteration:
                yield x1
                yield from s1
                return
        

def sliding_stream(delay_secs=20):
    ts = datetime.datetime.now()
    delay = datetime.timedelta(0,delay_secs)
    while True:
        yield(ts, random.choice(transform.all_transforms))
        ts = ts + delay

class Sliders(timelapse.TimeLapse):
    def __init__(self, server_list, nick="Sliders", channel="#sliders", realname="Sliders",
        sliding_window = 60, **params):
        super().__init__(server_list, nick=nick, channel=channel, **params)
        self.lapsed = merge(self.lapsed, sliding_stream(sliding_window))
        self.sliders_transform = random.choice(transform.all_transforms)

    def on_lapsed_message(self, msg):

        if isinstance(msg, transform.Transform):
            self.sliders_transform = msg
            self.connection.privmsg(self.lapsed_channel,
                "\x01ACTION s'ouvre vers un monde parallèle peuplé de jumeaux\x01"
                + msg.name)
        else:
            super().on_lapsed_message(self.sliders_transform(msg))

