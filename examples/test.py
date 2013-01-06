#!/usr/bin/env python
import socket
import sys
import os
import timeit
import py9p

try:
    assert py9p.version > "1.0.6"
    from py9p import py9p
    assert hasattr(py9p, "Credentials")
    ng = True
except:
    ng = False

class CmdClient(py9p.Client):

    def cat(self, name, out=None):
        self.open(name)
        self.read(self.msize)
        self.close()

if __name__ == "__main__":

    if os.environ.has_key('USER'):
        user = os.environ['USER']

    sock = socket.socket(socket.AF_INET)
    try:
        sock.connect(('localhost', 10001),)
    except socket.error,e:
        print "%s" % ( e.args[1])
        sys.exit(255)

    if ng:
        cl = CmdClient(sock, py9p.Credentials(user), None)
    else:
        cl = CmdClient(py9p.Sock(sock, 0, 0), 'none', user, None, None, 0)

    t = timeit.Timer('cl.cat("sample1")','from __main__ import cl')
    print "1000 cats (walk/open/read/clunk) in", t.timeit(1000), "seconds"
