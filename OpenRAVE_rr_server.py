# -*- coding: utf-8 -*-
import time
import thread
import threading
import RobotRaconteur as RR
from openravepy import *
import numpy as np
from OpenRAVEfunctions import *

RRN = RR.RobotRaconteurNode.s

class OpenRAVEObject(object):
	def __init__(self):
         print "Create OpenRAVE object"
         self._lock = threading.RLock()
         self.CollisionInit()
			
	def CollisionInit(self):
	     with self._lock:
	         self.cc = CollisionChecker(gui=True)
	         
	         # robot base
	         robot_pose = [0,0,0,1,0,0,0]
             self.T1 = np.dot(translation_matrix(robot_pose[0:3]), quaternion_matrix(robot_pose[3:7]))
             
             # testbed pose
             self.T2 = np.dot(translation_matrix([0,0,0]), quaternion_matrix([1,0,0,0]))
	     
	def CollisionReport(self,q1,q2,q3,q4,q5,q6):        
             tmp_array = (q1,q2,q3,q4,q5,q6)
             
             joints = {'irb6640_185_280_Testbed' : tmp_array}
            
             collision_poi = {'irb6640_185_280_Testbed': self.T1}
             
             collision_env = {'testbed': self.T2}
             
             tmp_result = self.cc.check_safety(collision_poi, collision_env, joints)
             
             print '------------------------------------------'
             print tmp_result[3], tmp_result[4]

             return np.concatenate((tmp_result[3], tmp_result[4]))
     

	
def main():    
    RRN.UseNumPy = True
    
    # Create and Register Local Transport (names the node example.math)
    t1 = RR.LocalTransport()
    t1.StartServerAsNodeName("OpenRAVE_rr")
    RRN.RegisterTransport(t1)
    
    # Create and Register TCP Transport
    t2 = RR.TcpTransport()
    t2.EnableNodeAnnounce()
    t2.StartServer(1234)
    RRN.RegisterTransport(t2)
    
    # read in Service Definition File
    with open('OpenRAVE_rr.robdef','r') as f:
        service_def = f.read()
    
    # Register Service Definition
    RRN.RegisterServiceType(service_def)
    
    # Create instance of OpenRAVEObject object
    OpenRAVE_obj = OpenRAVEObject()
    
    # Register Service 'OpenRAVEObject' of type 'example.math.MathSolver'
    RRN.RegisterService("OpenRAVEObject","OpenRAVE_rr.OpenRAVEObject", OpenRAVE_obj)
       
    print "Connect to OpenRAVEObject at:"
    # address : port / node name / service
    print "tcp://localhost:1234/OpenRAVE_rr/OpenRAVEObject"
    raw_input('press enter to quit')
    
if __name__ == '__main__':
    main()
    
