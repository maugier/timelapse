
import re
import datetime

# --- Log opened Fri May 25 12:56:23 2012
header_line = re.compile(r'--- Log opened (.*)')
header_date_format = "%a %b %d %H:%M:%S %Y"
# 12:56 <%Gael> haha sympa comme vhost
message_line = re.compile(r'(\d\d:\d\d) (<.[^>+]> .*)')
message_date_format = "%H:%M"


def read_log(file): 
    """From a log file, generate an alternating stream of known timestamps and log messages.
       This is because, in the log file, we only know the timestamp of each sentence up to the minute,
       and we do not want to output all lines with the same known time every minute.
       Instead, we interleave a stream of messages and timestamps, and let an intermediary consumer spread
       the messages along each interval"""
    
    current_date = None

    with open(file, 'r') as f:
        for line in f:
           m = header_line.match(line)
           if m:
             current_date = datetime.datetime.strptime(m.group(1), header_date_format)
             yield (True, current_date)
            
           m = message_line.match(line)
           if m:
             message_hour = datetime.datetime.strptime(m.group(1), message_date_format)
             message_line = m.group(2)

             if message_hour > current_date:
                current_date = message_hour
                yield (True, current_date)


             yield (False, message_line)
             
            

def interpolate(stream):
    """ Takes an interleaved stream of tuples containing either (True, index) or (False, value).
        Outputs a stream of tuples (index, value) where index will be a linear interpolation
        of the known preceding and following values in the stream. For instance, inputting

          (True, 1)
          (False, a)
          (False, b)
          (False, c)
          (True, 4)
          (False, d)
          (False, e)
          (True, 8)
          (False, f)

       Will generate

          (1,a),(2,b),(3,c),(4,d),(6,e),(8,f) """

    current_index = None
    values_buffer = []

    for (t,v) in stream:
        if t:
            if current_index is not None:
                delta = (v - current_index) / len(values_buffer)
                for v2 in values_buffer:
                    yield (current_index, v2)
                    current_index += delta
                values_buffer = []
            current_index = v

        else:
            values_buffer += v
