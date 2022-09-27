function x_g = get_x_global(x_aug_function,inputs,N_horizon,N_states,current_state)
    state = current_state;
    x_g = zeros(2*N_horizon,N_states);

    for i=1:N_horizon
        x_g(i) = x_aug_function(state,inputs(i))';
        state =  x_g(i);
    end
end