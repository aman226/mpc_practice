function next_state = next_state_calculate(current_state,delta,Ts)
    m=1500;    
    Iz = 3000;
    Caf = 19000;
    Car = 33000;
    lf = 2;
    lr = 3;
    x_dot = 25;

    y_dot=current_state(1);
    psi=current_state(2);
    psi_dot=current_state(3);
    Y=current_state(4);
    sub_loop=30;
    
    for i=1:sub_loop
        

        y_dot_dot=-(2*Caf+2*Car)/(m*x_dot)*y_dot+(-x_dot-(2*Caf*lf-2*Car*lr)/(m*x_dot))*psi_dot+2*Caf/m*delta;
        psi_dot_dot=-(2*lf*Caf-2*lr*Car)/(Iz*x_dot)*y_dot-(2*(lf^2)*Caf+2*(lr^2)*Car)/(Iz*x_dot)*psi_dot+2*lf*Caf/Iz*delta;
        Y_dot=sin(psi)*x_dot+cos(psi)*y_dot;

        y_dot=y_dot+y_dot_dot*Ts/sub_loop;
        psi=psi+psi_dot*Ts/sub_loop;
        psi_dot=psi_dot+psi_dot_dot*Ts/sub_loop;
        Y=Y+Y_dot*Ts/sub_loop;

        next_state = [y_dot;psi;psi_dot;Y];
    end

end