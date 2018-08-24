OpenRAVE = RobotRaconteur.Connect('tcp://localhost:1234/OpenRAVE_rr/OpenRAVEObject');

% Compute the closest point on robot and environment
Closest_info = OpenRAVE.CollisionReport(0, 0, 0, 0, pi/2, 0);
Closest_Pt = Closest_info(1:3)
Closest_env = Closest_info(4:6)