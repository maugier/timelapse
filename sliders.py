import datetime
import random
import transform
import timelapse

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
        

def sliding_stream(delay=20):
    ts = datetime.datetime.now()
    while True:
        yield(now, random.choice(transform.all_transforms))

class Sliders(timelapse.TimeLapse):
   pass 
