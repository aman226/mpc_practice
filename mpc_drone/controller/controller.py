class PID:
    def __init__(self, k_p, k_i, k_d, max = float("inf"), min = - float("inf")) -> None:
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self.prevError = 0
        self.integral = 0
        self.der = 0
        self.max = max
        self.min = min
    
    def update(self,error,dt):

        self.integral += (error - self.prevError)*dt
        
        self.der = (error - self.prevError)/dt
        self.prevError = error 

        control_out = self.k_p * error + self.k_i * self.integral + self.k_d * self.der

        if max != float("inf"):
            if control_out > self.max:
                control_out = self.max
        
        if min != -float("inf"):
            if control_out < self.min:
                control_out = self.min
        
        return control_out
    
    def reset(self):
        self.prevError = 0
        self.integral = 0
        self.der = 0
