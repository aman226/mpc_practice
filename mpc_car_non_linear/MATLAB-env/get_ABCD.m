function [A,B,C,D,x_dot] = get_ABCD(x_dot,y_dot,psi, delta)

    % State Space = [x_dot y_dot phi phi_dot X Y]
    
    %-----------------SET PARAMS-----------
    m = 1500;
    Iz = 3000;
    Caf = 19000;
    Car = 33000;
    lf = 2;
    lr = 3;
    mu = 0.1;
    g = 9.81;
    %---------------------------------------

    A11 = -  mu*g/x_dot;
    A12 =  ( Caf*sin(delta) )/( m*x_dot );
    A14 =  ( Caf*sin(delta)*lf )/( m*x_dot ) + y_dot;
    B11 = -( Caf*sin(delta) )/m;

    A22 = -( Car+Caf*cos(delta) )/( m*x_dot );
    A24 = -( Caf*cos(delta)*lf - Car*lr )/( m*x_dot ) - x_dot;
    B21 =  ( Caf*cos(delta) )/m;
    
    A34 =  1;

    A42 = -( Caf*lf*cos(delta)-lr*Car)/(Iz*x_dot);
    A44 = -( Caf*(lf^2)*cos(delta)+(lr^2)*Car)/(Iz*x_dot);
    A51 =    cos(psi);
    A52 = -  sin(psi);
    A61 =    sin(psi);
    A62 =    cos(psi);

    B41 =  ( Caf*cos(delta)*lf )/Iz;

    
    

    %---------------MODEL---------------
    A=[A11  A12 0   A14 0   0;... 
       0    A22 0   A24 0   0;...
       0    0   0   A34 0   0;...
       0    A42 0   A44 0   0;...
       A51  A52 0   0   0   0;...
       A61  A62 0   0   0   0];

    B=[B11  1;...
       B21  0;...
       0    0;...
       B41  0;...
       0    0;...
       0    0];

    C = [1 0 0 0 0 0 ; 0 0 1 0 0 0 ; 0 0 0 0 1 0 ; 0 0 0 0 0 1];
    D = [0  0; 0 0 ; 0 0; 0 0];
    
    
end