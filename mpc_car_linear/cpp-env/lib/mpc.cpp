#include "\user\local\include"
void get_lat_dyn_model(){
    
    double m,Iz,Caf,Car,lf,lr,x_dot,A1,A2,A3,A4;
    m = 1500;
    Iz = 3000;
    Caf = 19000;
    Car = 33000;
    lf = 2;
    lr = 3;
    x_dot = 25;
    
    A1 = -(2*Caf+2*Car)/(m*x_dot);
    A2 = -x_dot-(2*Caf*lf-2*Car*lr)/(m*x_dot);
    A3 = -(2*lf*Caf-2*lr*Car)/(Iz*x_dot);
    A4 = -(2*(lf*lf)*Caf+2*(lr*lr)*Car)/(Iz*x_dot);
    
    
    A=[A1 0 A2 0 ; 0  0  1  0 ; A3  0  A4  0 ; 1 x_dot 0 0];
    B=[2*Caf/m ;0 ;2*lf*Caf/Iz;0];
    C=[0 1 0  0 ; 0  0  0  1];
    D=0;
    
}