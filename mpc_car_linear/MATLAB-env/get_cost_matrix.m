function [S,Q,R] = get_cost_matrix(N_controls)
    
    S = diag([1 1]);
    Q = diag([1 1]);
    R = diag(ones(1,N_controls));
end