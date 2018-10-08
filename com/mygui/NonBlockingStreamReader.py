'''
Created on Jul 30, 2018

@author: yiz
'''

from threading import Thread
from queue import Queue, Empty

class NonBlockingStreamReader:

    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''
        self._s = stream
        self._q = Queue()

        def _populateQueue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'quque'.
            '''
            while True:
                line = stream.readline()
                #print("thread: " + line.decode("utf-8"))
                if line:
                    queue.put(line)
                else:
                    queue.put("&*#@!~%+-END(|".encode(encoding='utf_8'))
                    break;
                    #raise UnexpectedEndOfStream
            print("thread _populateQueue over!")

        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        self._t.start() #start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            line = self._q.get(block = timeout is None,
                    timeout = timeout)
            if line.decode('utf-8').find("&*#@!~%+-END(|") != -1:
                return None
            return line
        except Empty:
            return None

class UnexpectedEndOfStream(Exception): pass