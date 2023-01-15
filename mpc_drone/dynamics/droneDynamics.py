import numpy as np

class droneDynamics:
    def __init__(self, mass = 1, g = 9.81 , I_x = 0.1 , I_y = 0.1 , I_z = 0.1 ):
        self.mass = mass
        self.I_x = I_x
        self.I_y = I_y
        self.I_z = I_z
        self.g = g
    
    def getA(self,states):
        """
        state - List of States

        States
        [ phi theta psi p q r u v w x y z ]
        """

        [phi,theta,psi,p,q,r,u,v,w,x,y,z] = states
        
        _a =  np.sin(phi) * np.tan(theta)
        _b =  np.cos(phi) * np.tan(theta)
        _c =  np.cos(phi)
        _d = -np.sin(phi)
        _e =  np.sin(phi)/np.cos(theta)
        _f =  np.cos(phi)/np.cos(theta)
        _g =  ( (self.I_y - self.I_z) * q )/(self.I_x) 
        _h =  ( (self.I_z - self.I_x) * p )/(self.I_y) 
        _i =  ( (self.I_x - self.I_y) * q )/(self.I_z) 
        _j =  -( self.g*np.sin(theta) ) 
        _k = -w
        _l =  v
        _m =  w
        _n =  ( self.g * np.sin(phi) * np.cos(theta) )
        _o = -u
        _p = -v
        _q =  u
        _r =  ( self.g * np.cos(phi) * np.cos(theta) )
        _s =  np.cos(psi) * np.cos(theta)
        _t = -np.cos(phi) * np.sin(psi) + np.cos(psi) * np.sin(phi) * np.sin(theta)
        _u =  np.sin(phi) * np.sin(psi) + np.cos(phi) * np.cos(psi) * np.sin(theta)
        _v =  np.sin(psi) * np.cos(theta)
        _w =  np.cos(phi) * np.cos(psi) + np.sin(phi) * np.sin(psi) * np.sin(theta)
        _x = -np.cos(psi) * np.sin(phi) + np.cos(phi) * np.sin(psi) * np.sin(theta)
        _y = -np.sin(theta)
        _z =  np.cos(theta) * np.sin(phi)
        _a1 = np.cos(phi) * np.cos(theta)

        A = np.array([ [ 0.0, 0.0, 0.0, 1.0,  _a,  _b, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],           # = phi_dot
                       [ 0.0, 0.0, 0.0, 0.0,  _c,  _d, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],           # = theta_dot
                       [ 0.0, 0.0, 0.0, 0.0,  _e,  _f, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],           # = psi_dot
                       [ 0.0, 0.0, 0.0, 0.0, 0.0,  _g, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],           # = p_dot
                       [ 0.0, 0.0, 0.0, 0.0, 0.0,  _h, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],           # = q_dot
                       [ 0.0, 0.0, 0.0,  _i, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],           # = r_dot
                       [ 0.0, 0.0, 0.0, 0.0,  _k,  _l, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],           # = u_dot
                       [ 0.0, 0.0, 0.0,  _m, 0.0,  _o, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],           # = v_dot
                       [ 0.0, 0.0, 0.0,  _p,  _q, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],           # = w_dot
                       [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  _s,  _t,  _u, 0.0, 0.0, 0.0],           # = x_dot
                       [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  _v,  _w,  _x, 0.0, 0.0, 0.0],           # = y_dot
                       [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  _y,  _z, _a1, 0.0, 0.0, 0.0]])          # = z_dot
        return A

    def getB(self):
        """
        state - List of States

        States
        [ phi theta psi p q r u v w x y z ]

        Control Inputs
        [ Roll Pitch Yaw Thrust]
        """

        B = np.array([ [ 0.0, 0.0, 0.0, 0.0],
                       [ 0.0, 0.0, 0.0, 0.0],
                       [ 0.0, 0.0, 0.0, 0.0],

                       [ 1/self.I_x, 0.0, 0.0, 0.0],
                       [ 0.0, 1/self.I_y, 0.0, 0.0],
                       [ 0.0, 0.0, 1/self.I_z, 0.0],

                       [ 0.0, 0.0, 0.0, 0.0],
                       [ 0.0, 0.0, 0.0, 0.0],
                       [ 0.0, 0.0, 0.0, -1/self.mass],
                       
                       [ 0.0, 0.0, 0.0, 0.0],
                       [ 0.0, 0.0, 0.0, 0.0],
                       [ 0.0, 0.0, 0.0, 0.0]])
        
        return B

    def getC(self,states):
        [phi,theta,psi,p,q,r,u,v,w,x,y,z] = states
        _a =  -( self.g*np.sin(theta) ) 
        _b =  -( self.g * np.sin(phi) * np.cos(theta) )
        _c =  ( self.g * np.cos(phi) * np.cos(theta) )
        C =np.array([ 0.0, 0.0, 0.0, 0.0,  0.0,  0.0, _a, _b, _c, 0.0, 0.0, 0.0])
        return C
