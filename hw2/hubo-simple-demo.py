#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*
# Copyright (c) 2013, Daniel M. Lofaro
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the names of its contributors may
#       be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# */



import hubo_ach as ha
import ach
import sys
import time
from ctypes import *

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
#s.flush()
#r.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()

# Get the current feed-forward (state) 
[statuss, framesizes] = s.get(state, wait=False, last=False)

#Set Left arm in wave position
ref.ref[ha.LEB] = -2.0
ref.ref[ha.LSP] = -0.5
ref.ref[ha.LWR] = 1.5
ref.ref[ha.LWP] = -0.5
ref.ref[ha.LSY] = 0.0

# Print out the actual position of the LEB
print "Joint = ", state.joint[ha.LEB].pos

# Print out the Left foot torque in X
print "Mx = ", state.ft[ha.HUBO_FT_L_FOOT].m_x

# Write to the feed-forward channel
r.put(ref)

time.sleep(2)

i = 0
while i < 30:
	ref.ref[ha.LSY] = 0.0
	r.put(ref)
	time.sleep(.25)
	ref.ref[ha.LSY] = 0.4
	r.put(ref)
	time.sleep(.25)
	ref.ref[ha.LSY] = 0.0
	r.put(ref)
	time.sleep(.25)
	ref.ref[ha.LSY] = -0.4
	r.put(ref)
	time.sleep(.25)
	i = i + 1
	print "Wave ", i

# return to base position 
ref.ref[ha.LEB] = 0.0
ref.ref[ha.LSP] = 0.0
ref.ref[ha.LWR] = 0.0
ref.ref[ha.LWP] = 0.0
ref.ref[ha.LSY] = 0.0
r.put(ref)

# Close the connection to the channels
r.close()
s.close()

