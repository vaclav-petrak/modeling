% Population parameters
    P0 = 2.50; % Intial popoulation 
    r = 0.027; % Growt rate 2.7%

% Timescale
    t_start = 0;  t_end = 70;  t_diff = 1; 

% Years of interest
    t_expl= t_start:t_diff:t_end;

 % Results
    P_expl= P0*exp(r*t_expl);

% Plot
    plot(t_expl, P_expl, LineWidth=2)
    xlabel("Time (years)");  
    ylabel("Population (millions)"), 
    ylim([0, 20])