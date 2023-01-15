def rungeKutta4_Order(A, B, C, X, U, dt):
    k1 = dt * (A @ X + B @ U + C)
    k2 = dt * (A @ X + A @ (0.5 * k1) + B @ U + C)
    k3 = dt * (A @ X + A @ (0.5 * k2) + B @ U + C)
    k4 = dt * (A @ X + A @ (k3) + B @ U + C)
    return X + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
