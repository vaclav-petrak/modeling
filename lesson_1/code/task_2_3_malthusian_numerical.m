% Population parameters
    P0 = 2.50; r = 0.027; 
% Timescale
    t_start = 0;  t_end = 70;  t_diff = 1; 
% Initial time and population
    t_num = t_start;  P_num = P0; 
% Numerical caclulation loop
    for i = 1:t_end/t_diff    
       % Calulate new step
           P_new = P_num(i) + r*P_num(i)*t_diff;
           t_new = t_num(i) + t_diff;
       % Append to existing vector
           P_num = [P_num, P_new];   
           t_num = [t_num, t_new];
    end
 % Plot
    plot(t_num, P_num, Color="red")
    xlabel("Time (years)");  
    ylabel("Population (millions)"), 
    ylim([0, 20])
