%--------------------------------------------------------------------------
% Importing CaSADi
%--------------------------------------------------------------------------
    addpath('/casadi')
    import casadi.*
%--------------------------------------------------------------------------



%--------------------------------------------------------------------------
%   Simulation Parameters
%--------------------------------------------------------------------------
    Ts = 0.02; % Timestep
    N_horizon = 4; % Horizon for MPC
%--------------------------------------------------------------------------
 


%--------------------------------------------------------------------------
%   MODEL/PARAMS Lateral Dynamics for Vehicle
%--------------------------------------------------------------------------
% Get Dynamics Model
[A,B,C,D,X,U] = get_lat_dyn_model(); % Edit Params in this function 

% Number of Control Variables and State Variables are
N_controls = size(U,1);
N_states = size(X,1);

fprintf("No. of State Variables =  %d \n",N_states)
fprintf("No. of Control Variables =  %d \n",N_controls)
%--------------------------------------------------------------------------



%--------------------------------------------------------------------------
% State and Output Function
%--------------------------------------------------------------------------
state_dot = A*X + B*U;
output = C*X + D*U;
%--------------------------------------------------------------------------



%--------------------------------------------------------------------------
% Get the discretized State Function (Euler Forward)
%--------------------------------------------------------------------------
[A_d,B_d,C_d,D_d] = euler_discretize(A,B,C,D,Ts);
x_discrete = A_d*X + B_d*U;
%--------------------------------------------------------------------------




%--------------------------------------------------------------------------
% Extra state and control variables to be augumented
%--------------------------------------------------------------------------
delta_k1 = MX.sym('delta_k1');   % (For Augumenting in X)
del_delta = MX.sym('del_delta'); % (For Augumenting in U)
U_k1 = [delta_k1]; % For future compatibility, I can add more states here
del_U = [del_delta]; % For future compatibility, I can add more controls here
%--------------------------------------------------------------------------



%--------------------------------------------------------------------------
% Get the Augumented Matrix
%--------------------------------------------------------------------------
[A_ag,B_ag,C_ag,D_ag,X_ag,U_ag,N_aug_states,N_aug_controls] = augument_model(A_d,B_d,C_d,D_d,X,delta_k1,N_states,N_controls,U_k1,del_U);

x_aug = A_ag*X_ag + B_ag*U_ag;
y_aug = C_ag*X_ag + D_ag*U_ag;
%--------------------------------------------------------------------------



%--------------------------------------------------------------------------
% Convert State Space Symbolic Form to Function
%--------------------------------------------------------------------------
x_aug_function = Function('AugumentedX',{X_ag,U_ag},{x_aug});
y_aug_function = Function('AugumentedY',{X_ag,U_ag},{y_aug});
%--------------------------------------------------------------------------


x_g = get_x_horizon(x_aug_function,[-0.01 0.02 -0.02 0.02],N_horizon,N_aug_states,[0 0 0 0 0]);
plot(x_g(:,4),[0.4 0.8 1.2 1.6])


%--------------------------------------------------------------------------
% Initial Conditions
%--------------------------------------------------------------------------
y_dot = 0;
psi = 0;
psi_dot = 0;
Y = 0;
delta = 0;
%--------------------------------------------------------------------------


