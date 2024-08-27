% MODELING PARAMETERS
    P0 = 2.50;                  % Intial popoulation in milions
    r = 0.027;                  % Population Growth rate 2.7%
    start_year = 1950;          % For plotting
    t_start = 0;  t_end = 70;   % Start and end years
    t_diff = 1;                 % Step (1/12 is one month, 1/365 is one day) 

% EXPLICIT SOLUTION
    t_expl= t_start:t_diff:t_end;
    P_expl= P0*exp(r*t_expl);

% NUMERICAL SOLUTION   
   t_num = t_start;  P_num = P0; 
    for i = 1:t_end/t_diff    
           P_num = [P_num, P_num(i) + r*P_num(i)*t_diff;];   
           t_num = [t_num, t_num(i) + t_diff];
    end

% PLOTTING
tiledlayout (1, 2)
nexttile       % Tile with explicit and numerical solution
    hold on
    plot(t_expl + start_year, P_expl , Color = "red")
    plot(t_num + start_year, P_num , Color = " blue")
    title("Explicit and numerical solution")
    ylim([0,20]); xlim([1950,2020])
    hold off
nexttile       % Tile with the difference
    plot(t_expl + start_year, P_expl - P_num, Color =" black")
    title ("The difference")
    ylim([0,0.5]); xlim([1950,2020])