function [A_ag,B_ag,C_ag,D_ag,X_ag,U_ag,N_states,N_controls] = augument_model(A_d,B_d,C_d,D_d,X,U,N_s,N_c,U_k1,del_U)
    addpath('/casadi')
    import casadi.*
    
    A_ag = [A_d B_d;zeros(N_c,N_s) eye(N_c) ];
    B_ag = [B_d;eye(N_c) ];
    
    C_ag = [C_d zeros(size(C_d,1),size(U_k1,1))];
    D_ag = D_d;

    X_ag = [X;U_k1];
    U_ag = [del_U];
    
    N_controls = size(U_ag,1);
    N_states = size(X_ag,1);


end
