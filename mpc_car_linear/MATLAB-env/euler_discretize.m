function [A_d,B_d,C_d,D_d] = euler_discretize(A,B,C,D,Ts)
    A_d = eye(size(A,1)) + A*Ts;
    B_d = B*Ts;
    C_d = C;
    D_d = D; 
end