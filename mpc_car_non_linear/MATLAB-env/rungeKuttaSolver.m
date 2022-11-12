function nextState = rungeKuttaSolver(A,B,curr_state,inp,h)
    temp1 = A*curr_state;
    temp = B*inp;
    
    k1 = h*(temp + temp1);
    
    temp = temp + B*h/2;
    k2 = h*(temp + temp1 + A*k1/2);
    k3 = h*(temp + temp1 + A*k2/2);

    temp = temp + B*h/2;
    k4 = h*(temp + temp1 + A*k3);

    nextState = curr_state + (k1 + 2*k2 + 2*k3 + k4)/6;
end