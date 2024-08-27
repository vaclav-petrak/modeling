% Growth rate
   r = 0.027;   

% Start year
   start_year = 1950; 

% Time axis
    t_sen   = [0,  5, 10, 15, 20, 25, 30, 35, 40,  ...
              45, 50, 55, 60, 65, 70, 72, 73, 74];

% Senegalese population
    P_sen = [ 2.5,  2.8,  3.3,  3.8,  4.4,  5.0, 5.7,  ...
              6.5,  7.5,  8.6,  9.7, 11.0, 12.5,14.4,  ...
             16.4, 17.3, 17.8, 18.2];
             
% EXPLICIT SOLUTION
    P_expl= P_sen(1)*exp(r*(t_sen)); %initial populatin is the first value

% PLOTTING
    tiledlayout(1, 2)
    nexttile       
        hold on
        plot(t_sen + start_year, P_expl, Color = "red")
        plot(t_sen + start_year, P_sen,  Color = " blue")
        title("Reald data and model")
        ylim([0,20]); 
        hold off
    nexttile
        plot(t_sen + start_year, P_expl - P_sen, '-o', Color =" black ")
        title ("The difference")