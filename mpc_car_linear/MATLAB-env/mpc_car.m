    addpath('/casadi')
    import casadi.*
%----------------------------------------------
%   Sim Parameters
    Ts = 0.02;
    N_horizon = 4;
%----------------------------------------------
%   MODEL/PARAMS Lateral Dynamics for Vehicle
%----------------------------------------------

% Edit Dynamics Model in this function 
[A,B,C,D,X,U] = get_lat_dyn_model();


% Number of Control Variables and State Variables are
N_controls = size(U,1);
N_states = size(X,1);
fprintf("No. of State Variables =  %d \n",N_states)
fprintf("No. of Control Variables =  %d \n",N_controls)

% State and Output Function
state_dot = A*X + B*U;
output = C*X + D*U;

%------------------------------------
% Get the discretized State Function (Euler Forward)
[A_d,B_d,C_d,D_d] = euler_discretize(A,B,C,D,Ts);
x_discrete = A_d*X + B_d*U;

% Get the Augumented Matrix
[A_ag,B_ag,C_ag,D_ag,X_ag,U_ag,N_aug_states,N_aug_controls] = augument_model(A_d,B_d,C_d,D_d,X,U,N_states,N_controls);
x_aug = A_ag*X_ag + B_ag*U_ag;
y_aug = C_ag*X_ag + D_ag*U_ag;

x_aug_function = Function('AugumentedX',{X_ag,U_ag},{x_aug});
y_aug_function = Function('AugumentedY',{X_ag,U_ag},{y_aug});

y_aug_function(x_aug_function([0,0,0,0,0],1),0)

%-------------------------------------
% Initial Conditions
y_dot = 0;
psi = 0;
psi_dot = 0;
Y = 0;
delta = 0;
%-------------------------------------


