# SPDX-License-Identifier: GPL-2.0-only
# Copyright (c) 2019 NITK Surathkal

########################
# SHOULD BE RUN AS ROOT
########################
import sys

sys.path.append('../')

from nest import *

##############################
#
# Topology:
#
# n0 -- r0 -- n1
#
##############################

###### TOPOLOGY CREATION ######

# Create nodes
n0 = Node()
n1 = Node()

# Create routers
r0 = Router()

print('Node and router created')

# Add connections
(n0_r0, r0_n0) = connect(n0, r0)
(n1_r0, r0_n1) = connect(n1, r0)

print('Connections made')

###### ADDRESS ASSIGNMENT; ROUTE ######

Address('10.0.0.4/24')
# Assign address
n0_r0.set_address(Address('10.0.0.1/24'))
r0_n0.set_address(Address('10.0.0.2/24'))
n1_r0.set_address(Address('10.0.1.1/24'))
r0_n1.set_address(Address('10.0.1.2/24'))

print('Addresses are assigned')

# engine.exec_subprocess('ip -all netns del') # TODO: Temporary cleanup routine.
                                            # Replace with more robust stuff

# Add routes
# n0.add_route(Address('DEFAULT'), Address('10.0.0.2'), r0_n0) # ip route add default via 10.0.0.2 dev r0_n0
# r1.add_route(Address('DEFAULT'), Address('10.0.0.1'), n0_r0)
# r1.add_route(Address('10.0.3.2'), Address('10.0.1.2'), r0_r1)
# and other routes...
