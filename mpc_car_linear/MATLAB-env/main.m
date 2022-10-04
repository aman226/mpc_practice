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
    sim_time = 10; % Simulation Time
    time = 0:Ts:sim_time;
%--------------------------------------------------------------------------


%--------------------------------------------------------------------------
%   MODEL/PARAMS Lateral Dynamics for Vehicle
%--------------------------------------------------------------------------
% Get Dynamics Model
[A,B,C,D,X,U,x_dot] = get_lat_dyn_model(); % Edit Params in this function 
% Number of Control Variables and State Variables are
N_controls = size(U,1);
N_states = size(X,1);
N_outputs = 2;


N_horizon = 20; % Horizon for MPC

fprintf("No. of State Variables =  %d \n",N_states)
fprintf("No. of Control Variables =  %d \n",N_controls)
%--------------------------------------------------------------------------

%--------------------------------------------------------------------------
% Get the ref_trajectory and signal
%--------------------------------------------------------------------------
[psi_ref,x_ref,y_ref] = generate_ref_trajectory(time,x_dot);
ref_signal = zeros(size(x_ref,2)*size(C,1),1);
ref_signal(1:N_outputs:end) = psi_ref;
ref_signal(2:N_outputs:end) = y_ref;
%--------------------------------------------------------------------------


%--------------------------------------------------------------------------
% Get Cost Matrix for the Cost Function
%--------------------------------------------------------------------------
[S,Q,R] = get_cost_matrix(N_controls);
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
[A_ag,B_ag,C_ag,D_ag,X_ag,U_ag,N_aug_states,N_aug_controls] = augument_model(A_d,B_d,C_d,D_d,X,N_states,N_controls,U_k1,del_U);

x_aug = A_ag*X_ag + B_ag*U_ag;
y_aug = C_ag*X_ag + D_ag*U_ag;
%--------------------------------------------------------------------------



%--------------------------------------------------------------------------
% Get X for next N Steps - Horizon
%--------------------------------------------------------------------------
[A_horizon, B_horizon] = get_x_horizon(A_ag,B_ag,N_aug_states,N_aug_controls,N_horizon);

U_horizon = MX.sym('d',N_horizon*N_aug_controls,1);
state_horizon = MX.sym('x',N_aug_states,1);

x_horizon = A_horizon*state_horizon + B_horizon*U_horizon;
% state_horizon = x_k
%--------------------------------------------------------------------------


[H_db,F_db_t] = get_optimized_input(C_ag,S,Q,R,N_horizon,N_aug_states,N_aug_controls,A_horizon, B_horizon);

%--------------------------------------------------------------------------
% Initial Conditions
%--------------------------------------------------------------------------
y_dot = 0.5;
psi = 0.2;
psi_dot = 0;
Y = y_ref(1)+2;
current_state = [y_dot;psi;psi_dot;Y];
delta = 0;
%--------------------------------------------------------------------------




y_act = zeros(size(time,2),1);
k = 0;
N_horizon_temp = N_horizon;

for i=1:size(time,2)-1
    

    x_aug_0 = [current_state;delta]; 
   
    
    k = k + N_outputs;
    if k+N_outputs*N_horizon_temp<=(size(ref_signal,1))
        r = ref_signal(k+1:k+N_outputs*N_horizon_temp);
    else
        r = ref_signal(k+1:size(ref_signal,1));
        N_horizon_temp=N_horizon_temp-1;
    end

    if N_horizon_temp<N_horizon
        [A_horizon, B_horizon] = get_x_horizon(A_ag,B_ag,N_aug_states,N_aug_controls,N_horizon_temp);
        [H_db,F_db_t] = get_optimized_input(C_ag,S,Q,R,N_horizon_temp,N_aug_states,N_aug_controls,A_horizon, B_horizon);
    end
    
    control_input = -(inv(H_db)) * F_db_t' * [x_aug_0;r];
    delta = delta + control_input(1);

    if delta < -pi/6
        delta = -pi/6;
    end

    if delta > pi/6
        delta = pi/6;
    end
    y_act(i) = x_aug_0(4);
    current_state = next_state_calculate(current_state,delta,Ts);
end
y_act(size(time,2)) = y_act(size(time,2)-1);


close all
plot(x_ref,y_ref) 
h = animatedline('Color','r','LineWidth',3);

for l=1:size(time,2)
    addpoints(h,x_ref(l),y_act(l))
    pause(0.02)
end
