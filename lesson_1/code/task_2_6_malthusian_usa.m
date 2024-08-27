% Growth rate
   r = 0.0275;   

% Start year
   start_year = 1790; 

% Time axis
    t_usa = 0:10:230;

% US population
   P_usa = [  3.9,   5.3,   7.2,   9.6,  12.9,  17.1,  23.2,  31.4, ...
             38.6,  50.2,  63.0,  76.2,  92.2, 106.0, 123.2, 132.2, ... 
            151.3, 179.3, 203.3, 226.5, 248.7, 281.4, 308.7, 331.4];

% EXPLICIT SOLUTION
    P_expl= P_usa(1)*exp(r*(t_usa)); %initial populatin is the first value

% PLOTTING
    tiledlayout(1, 2)
    nexttile       
        hold on
        plot(t_usa + start_year, P_expl, Color = "red")
        plot(t_usa + start_year, P_usa,  Color = " black")
        title("Real data and model")
        ylim([0,350]); 
        hold off
    nexttile       % Tile with the difference
        plot(t_usa + start_year, P_expl - P_usa, '-o', Color =" black ")
        title ("The difference")