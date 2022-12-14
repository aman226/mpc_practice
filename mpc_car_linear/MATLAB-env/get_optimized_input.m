function [H_db,F_db_t] = get_optimized_input(C_ag,S,Q,R,N_horizon,N_states,N_controls,A_horizon,B_horizon)
    CQC = C_ag' *Q*C_ag;
    CSC = C_ag' *S*C_ag;
    QC = Q*C_ag;
    SC = S*C_ag;
    N_CQC = size(CQC,1);
    N_QC = size(QC,1);

    Q_db = zeros(N_CQC*N_horizon,N_horizon*N_states);
    T_db = zeros(N_QC*N_horizon,N_horizon*N_states);
    
    for i=1:N_horizon
            
            Q_db(1+(i-1)*N_CQC:i*N_CQC,1+(i-1)*N_states:i*N_states) = CQC;
            T_db(1+(i-1)*N_QC:i*N_QC,1+(i-1)*N_states:i*N_states) = QC;
            if i==N_horizon
                Q_db(1+(i-1)*N_CQC:i*N_CQC,1+(i-1)*N_states:i*N_states) = CSC;
                T_db(1+(i-1)*N_QC:i*N_QC,1+(i-1)*N_states:i*N_states) = SC;
            end
    end
    R_db = diag(ones(N_controls*N_horizon,1))*R;
    H_db = B_horizon' * Q_db * B_horizon + R_db;
    F_db_t = [A_horizon' * Q_db * B_horizon; -T_db*B_horizon];
   
    
end