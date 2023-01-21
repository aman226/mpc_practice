from numpy import sqrt,cos,pi
class PID:
    def __init__(self, k_p, k_i, k_d, max = float("inf"), min = - float("inf"), fc = 0) -> None:
        self.k_p = k_p 
        self.k_i = k_i
        self.k_d = k_d

        self.prevError = 0
        self.integral = 0
        self.derivative = 0

        self.max = max
        self.min = min

        self.fc = fc # derivative filter frequency cutoff
        self.alpha = 1
    
    def update(self,error,dt):
        self.alpha = self.alphaExpMA(self.fc * dt)
        self.integral += (error - self.prevError)*dt
        
        error_filtered = self.alpha * error  + (1 - self.alpha) * self.prevError
        self.derivative = (error_filtered - self.prevError)/dt

        control_out = self.k_p * error + self.k_i * self.integral + self.k_d * self.derivative

        if max != float("inf"):
            if control_out > self.max:
                control_out = self.max
        
        if min != -float("inf"):
            if control_out < self.min:
                control_out = self.min
        
        self.prevError = error 
        
        return control_out

    
    def alphaExpMA(self, fn): # fn = fc * dt
        if fn <= 0:
            return 1
        # α(fₙ) = cos(2πfₙ) - 1 + √( cos(2πfₙ)² - 4 cos(2πfₙ) + 3 )
        c = cos(2 * pi * fn)
        return c - 1 + sqrt(c * c - 4 * c + 3)
    
    def reset(self):
        self.prevError = 0
        self.integral = 0
        self.derivative = 0
