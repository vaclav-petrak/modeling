% Population parametees
    r = 0.0237; P0 = 5.2; K = 460;
% Start year
    start_year = 1790; 
% Time axis
    t_usa = 0:10:230;
% US population
    P_usa = [  3.9,   5.3,   7.2,   9.6,  12.9,  17.1,  23.2,  31.4, ...
              38.6,  50.2,  63.0,  76.2,  92.2, 106.0, 123.2, 132.2, ... 
             151.3, 179.3, 203.3, 226.5, 248.7, 281.4, 308.7, 331.4];
 % Timescale for numerical modelling
    t_start = 0;  t_end = 230; t_diff = 1/12; 
 % Initial time and population
    t_num = t_start; P_num = P0; P_diff = NaN;

% Calculation loop with Logistic Model
    for i = 1:t_end/t_diff  
        P_diff_step =  r*P_num(end)*(1 - P_num(end)/K)*t_diff;
        P_num =  [P_num,  P_num(end) + P_diff_step];   
        t_num =  [t_num,  t_num(end) + t_diff];
    end

% Plotting
   hold on
        plot(t_num + start_year, P_num, Color = "red")
        plot(t_usa + start_year, P_usa, 'o', Color = " black")
        ylim([0,350]);   xlim([1790,2020]); 
   hold off
