#!/usr/bin/python -i

# "Copyright (c) 2000-2003 The Regents of the University of California.  
# All rights reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose, without fee, and without written agreement
# is hereby granted, provided that the above copyright notice, the following
# two paragraphs and the author appear in all copies of this software.
# 
# IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT
# OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY
# OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE.  THE SOFTWARE PROVIDED HEREUNDER IS
# ON AN "AS IS" BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATION TO
# PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS."
#
# @author Kamin Whitehouse 
# @author Michael Okola
#

# The server must be run in the application directory or told where it is,
# and must be told which platform to import (first parameter).  It will then import all
# nesc types, enums, and messages defined in the application.
#
# If the user has a node running this application and indicates how to connect to
# that node (second parameter), the script will also load any rpc functions and ram symbols
# in the application and present them to the user.
#
# In lieu of the first and second parameters, the TINYOS_DEFAULT_PLATFORM and MOTECOM
# environment variables can be used.
#
# usage:
# $     Pytos.py [buildDir] [motecom]
#
# Where "buildDir" is
# 1.  only a platform name, eg "pc" or "telosb"
# 2.  a path to the build dir, eg. "../../TestRpc/build/telosb"
#
# And where motecom is the standard comm port definition, eg "sf@localhost:9001"
#
# Once the application is loaded, the "app" variable will be available, from which you
# can access all imported enums, types, messages, rpc functions or ram symbols.
#
# Be sure to set the tosbase variable below if you are using a TosBase

import pdb
import re
from SimpleXMLRPCServer import *
import sys
import pytos.util.NescApp as NescApp
import pytos.util.ParseArgs as ParseArgs

class MarionetteServer:
    def __init__(self, app):
        self.app = app

    def _dispatch(self, method, params):
        #First check to see if this is the str method
        if method == "str":
            #Make sure that the app object is the parent
            match = re.match("^app", params[0])
            if match is None:
                raise Exception('The object passed must be part of the app object')
            try:
                obj = eval(params[0])
            except:
                raise Exception('Object %s is does not exist' % params[0])
            return str(obj).replace('\x08', '')

        #Make sure that the app object is the parent
        match = re.match("^app\.",method)
        if match is None:
            raise Exception('The function called must be part of the app object')

        try:
            func = eval(method)
        except:
            raise Exception('Method %s is does not exist' % method)

        #call the function if it is exposed
        if func is not None:
            result = func(*params)
            if result[0].value.has_key('value'):
                return result[0].value['value'].value
            else:
                raise Exception('Return type is not currently supported by Marionette Server')

if __name__ == '__main__':
    server = SimpleXMLRPCServer(("localhost", 21777), requestHandler=SimpleXMLRPCRequestHandler, allow_none = True)
    server.register_introspection_functions()

    args = ParseArgs.ParseArgs(sys.argv)
    app = NescApp.NescApp(args.buildDir, args.motecom, tosbase=False, localCommOnly=True)
    myFunctions = MarionetteServer(app)
    
    server.register_instance(myFunctions, allow_dotted_names = True)

    try:
        server.serve_forever()
    finally:
        server.server_close()
