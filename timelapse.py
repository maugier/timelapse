#!/usr/bin/env python3

import datetime
import logging
import re
import sys
from irc.bot import SingleServerIRCBot

# --- Log opened Fri May 25 12:56:23 2012
header_open_line = re.compile(r'--- Log opened (.*)')
header_open_format = "%a %b %d %H:%M:%S %Y"
# --- Day changed Sat Jun 02 2012
header_change_line = re.compile(r'--- Day changed (.*)')
header_change_format = "%a %b %d %Y"
# 12:56 <%Gael> haha sympa comme vhost
message_line = re.compile(r'(\d\d:\d\d) (<.[^>]+> .*)')
message_date_format = "%H:%M"


def read_log(file): 
    """From a log file, generate an alternating stream of known timestamps and log messages.
       This is because, in the log file, we only know the timestamp of each sentence up to the minute,
       and we do not want to output all lines with the same known time every minute.
       Instead, we interleave a stream of messages and timestamps, and let an intermediary consumer spread
       the messages along each interval"""
    
    current_date = None

    with open(file, 'rb') as f:
        for buf in f:
           try: 
             line = buf.decode('utf-8')
           except UnicodeDecodeError:
             line = buf.decode('latin1')

           m = header_open_line.match(line)
           if m:
             current_date = datetime.datetime.strptime(m.group(1), header_open_format)
             yield (True, current_date)

           m = header_change_line.match(line)
           if m:
             current_date = datetime.datetime.strptime(m.group(1), header_change_format)
             yield (True, current_date)
            
           m = message_line.match(line)
           if m:
             message_hour = datetime.datetime.combine(current_date.date(), 
                datetime.datetime.strptime(m.group(1), message_date_format).time())

             if message_hour > current_date:
                current_date = message_hour
                yield (True, current_date)


             yield (False, m.group(2))
             
            

def interpolate(stream):
    """ Takes an interleaved stream of tuples containing either (True, index) or (False, value).
        Outputs a stream of tuples (index, value) where index will be a linear interpolation
        of the known preceding and following values in the stream. For instance, inputting

          (True, 1),(False, a),(False, b),(False, c),
          (True, 4),(False, d),(False, e),
          (True, 8),(False, f)

       Will generate

          (1,a),(2,b),(3,c),(4,d),(6,e),(8,f) """

    current_index = None
    values_buffer = []

    for (t,v) in stream:
        if t:
            if current_index is not None and values_buffer:
                delta = (v - current_index) / len(values_buffer)
                for v2 in values_buffer:
                    yield (current_index, v2)
                    current_index += delta
                values_buffer = []
            current_index = v

        else:
            values_buffer.append(v)

def adjust(f, g):
    for (i,v) in g:
        yield (f(i), v)

def send_timed_stream(stream, client, handler):
    
    # Find next event
    while True:
        (ts, msg) = next(stream)
        if ts > datetime.datetime.now():
            break

    logging.debug("Next timelapse stamp at {0}".format(ts))

    # Build the event function
    def next_tick():
        handler(msg)
        send_timed_stream(stream, client, handler)
        
    # Schedule it
    client.execute_at(ts, next_tick, [])

class TimeLapse(SingleServerIRCBot):
    def __init__(self, server_list, nick="TimeLapse", channel="#timelapse", replay_log="/dev/null", delay=datetime.timedelta(365), **params):
        self.lapsed_channel = channel
        self.lapsed = adjust(lambda x: x + delay, interpolate(read_log(replay_log)))
        super().__init__(server_list, nick, "TimeLapse", **params)

    def on_welcome(self, c, e):
        c.join(self.lapsed_channel)
        send_timed_stream(self.lapsed, self.connection, self.on_lapsed_message)

    def on_lapsed_message(self, msg):
        logging.info("Lapsed message: {0}".format(msg))
        self.connection.privmsg(self.lapsed_channel, msg)


if __name__ == "__main__":
    for i in interpolate(read_log(sys.argv[1])):
        print(i)
