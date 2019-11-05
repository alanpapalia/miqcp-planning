import numpy as np
import random
import vtolParam as P

class vtolDynamics:
    def __init__(self):
        self.state = np.matrix([[P.zc0],
                                [P.h0],
                                [P.theta0],
                                [P.zcdot0],
                                [P.hdot0],
                                [P.thetadot0]])
        alpha = 0.0  # Uncertainty parameter
        self.mu = P.mu * (1+2*alpha*np.random.rand()-alpha)
        self.mc = P.mc * (1+2*alpha*np.random.rand()-alpha)
        self.Jc = P.Jc * (1+2*alpha*np.random.rand()-alpha)
        self.d = P.d * (1+2*alpha*np.random.rand()-alpha)
        self.g = P.g
        self.mr = P.mr
        self.ml = P.ml

        self.a1 = (2*P.beta-P.Ts)/(2*P.beta+P.Ts)
        self.a2 = 2/(2*P.beta+P.Ts)
        self.zcdot_e = P.zcdot0
        self.zc_km1 = P.zc0
        self.hdot_e = P.hdot0
        self.h_km1 = P.h0
        self.thetadot_e = P.thetadot0
        self.theta_km1 = P.theta0

    def propagateDynamics(self, u):
        # extract fl and fr from [F, T]
        F = u[0]
        T = u[1]
        fr = 0.5*F + 1/(2*P.d)*T
        fl = 0.5*F - 1/(2*P.d)*T

        k1 = self.derivatives(self.state, fl, fr)
        k2 = self.derivatives(self.state + P.Ts/2*k1, fl, fr)
        k3 = self.derivatives(self.state + P.Ts/2*k2, fl, fr)
        k4 = self.derivatives(self.state + P.Ts*k3, fl, fr)
        self.state += P.Ts/6 * (k1 + 2*k2 + 2*k3 + k4)

    def derivatives(self, state, fl, fr):
        zv = state.item(0)
        h = state.item(1)
        theta = state.item(2)
        zvdot = state.item(3)
        hdot = state.item(4)
        thetadot = state.item(5)
        fl = fl
        fr = fr
        ctheta = np.cos(theta)
        stheta = np.sin(theta)

        # equations of motion
        F1 = -(fl+fr)*stheta - self.mu*zvdot #+ P.F_wind
        F2 = (fl+fr)*ctheta - self.g*(self.mc+self.mr+self.ml)
        F3 = (fr-fl)*self.d - (self.mr-self.ml)*self.g*self.d*ctheta
        M1 = self.mc + self.mr + self.ml
        M2 = self.ml*self.d*self.d + self.mr*self.d*self.d + self.Jc

        zvddot = F1/M1
        hddot = F2/M1
        thetaddot = F3/M2

        # build xdot and return
        xdot = np.matrix([[zvdot], [hdot], [thetadot], [zvddot], [hddot], [thetaddot]])
        return xdot

    def outputs(self):
        return np.array(self.state.transpose())[0][0:3]

    def states(self):
        return self.state
