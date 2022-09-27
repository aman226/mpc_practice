function [S,Q,R] = generate_cost_function()
    
    CQC = C'*Q*C;
    CSC = C'*S*C;
    QC = Q*C;
    SC = S*C;
end