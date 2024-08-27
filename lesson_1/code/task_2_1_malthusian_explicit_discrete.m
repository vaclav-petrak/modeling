% Clean up
    clear, clc

% Population parameters
    P0 = 2.5;   % Intial popoulation 
    r = 0.027;  % Growt rate 2.7%

% Years of interest
    t_task1 = [1, 5, 7.5, 25.78];

% Results
    disp("Years of interest:")
    disp(t_task1)
    disp("Caclulated population size:")
    disp(P0*exp(r*t_task1))