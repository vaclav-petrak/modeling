clear, close , clc

% Calculate bifurcation plot
r = linspace(2.9, 4, 80000); 
n_initial = 2000; 
n_plotting = 100;
% Initial condition
x = 0.5*ones(1, length(r)); 

% Iterate the logistic map, until we get into stable tate
for i = 1:n_initial
    x = r.*x.*(1-x); 
end

% Plot
figure(1)
    hold on; 

   % Repeat and plot multiple dots into one image
for i = 1:n_plotting
    x = r.*x.*(1-x);
    plot(r, x, '.', Color = 'Black', MarkerSize=0.01)
end
 hold off

 xlim([2.9, 4])
 xlabel("r")
 ylabel("x")
