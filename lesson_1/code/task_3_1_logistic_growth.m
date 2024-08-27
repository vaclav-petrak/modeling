% Population parameters
    P0 = 3.9;     % Initial population 
    r = 0.0255;     % Intrinsic growth rate
    K = 430;      % Carrying capacity
% Timescale
    t_start = 0;  t_end = 400; t_diff = 1/12; 
% Initial time and population
    t_num = t_start; P_num = P0; P_diff = NaN;

% Calculation loop with Logistic Model
    for i = 1:t_end/t_diff  
        P_diff_step =  r*P_num(end)*(1 - P_num(end)/K)*t_diff;
        P_diff = [P_diff, P_diff_step];
        P_num =  [P_num,  P_num(end) + P_diff_step]; 
        t_num =  [t_num,  t_num(end) + t_diff];
    end

 % Plot
figure(1); tiledlayout(2, 2)
nexttile
   plot(t_num, P_num)
nexttile 
    plot(t_num, P_diff)
nexttile 
    plot(P_num, P_diff./P_num)
nexttile 
    plot(P_num, P_diff)