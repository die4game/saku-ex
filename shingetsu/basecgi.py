'''Base CGI module.
'''
#
# Copyright (c) 2005,2006 shinGETsu Project.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHORS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHORS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#
# $Id$
#

import os
import sys

__version__ = "$Revision$"
__all__ = ['CGI']


class BodyFilter:
    '''Filtered output stream.

    When HEAD method is used, output HTTP header only.
    '''
    mode = 'wb'     # Writable stream

    def __init__(self, env, output):
        self.output = output
        self.ishead = (env['REQUEST_METHOD'] == 'HEAD')
        self.flag_body = False
        self.buf = ''

    def write(self, msg):
        if not self.ishead:
            self.output.write(msg)
        elif self.ishead and self.flag_body:
            pass
        else:
            self.buf += msg.replace('\r\n', '\n')
            i = self.buf.find('\n\n')
            if i >= 0:
                self.output.write(self.buf[:i+2].replace('\n', '\r\n'))
                self.buf = ''
                self.flag_body = True

    def flush(self):
        return self.output.flush()

    def close(self):
        if self.buf:
            self.output.write(self.buf.replace('\n', '\r\n'))
        return self.output.close()

    def __del__(self):
        self.close()

# End of BodyFilter


class CGI:

    """Base CGI class.

    start(): start the CGI.
    run(): main routine for CGI.

    """

    def __init__(self,
                 stdin=sys.stdin,
                 stdout=sys.stdout,
                 stderr=sys.stderr,
                 environ=os.environ):
        self.stdin = stdin
        self.stdout = BodyFilter(environ, stdout)
        self.stderr = stderr
        self.environ = environ

    def start(self):
        """Start the CGI."""
        import socket
        try:
            self.run()
        except (IOError, socket.error, socket.timeout), strerror:
            self.stderr.write("%s: %s\n" %
                              (self.environ['REMOTE_ADDR'], strerror))

    def run(self):
        """Main routine for CGI."""
        pass

# End of CGI
