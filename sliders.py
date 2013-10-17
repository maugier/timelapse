import datetime
import random
import transform
import timelapse

def merge(s1, s2):
    while True:
        try:
            x1 = next(s1)
        except StopIteration:
            yield from s2

        try:
            x2 = next(s2)
        except StopIteration:
            yield from s1

        if x2 > x1:
            yield x1
            try:
                x1 = next(s1)
            except StopIteration:
                yield from s2
        else:
            yield x2
            try:
                x2 = next(s2)
            except StopIteration:
                yield from s1
        

def sliding_stream(delay=20):
    ts = datetime.datetime.now()
    while True:
        yield(now, random.choice(transform.all_transforms))

class Sliders(timelapse.TimeLapse):
    
