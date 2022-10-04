function [A_horizon,B_horizon] = get_x_horizon_func(A,B,N_states,N_controls,N_horizon)
    addpath('/casadi')
    import casadi.*
    B_horizon = zeros(N_states*N_horizon,N_horizon*N_controls);
    A_horizon = zeros(N_states*N_horizon,N_states);
    
    for i=1:N_horizon
        A_horizon(1+(i-1)*N_states:N_states*i,:) = A^i;
        for j=1:i 
            B_horizon(1+(i-1)*N_states:N_states*i,1+(j-1)*N_controls:N_controls*j) = A^(i-j)*B;
        end
    end
end