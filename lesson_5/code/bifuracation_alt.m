% Calculate bifurcation plot

clear, close , clc
r = linspace(0, 4, 20000); 
n_total = 2000; 

% Initial condition
x = 0.5*ones(1, length(r)); 

% Iterate the logistic map, until we get into stable tate
for i = 1:n_total
    x = r.*x.*(1-x); 
end


figure(1)
for i = 1:50 % Iterate to create bifurcation diagram
    x = r.*x.*(1-x);
    hold on; 
        plot(r, x, '.', Color = 'Black', MarkerSize=0.01)
    hold off
    pause(0.1)
    xlim([2.8, 4])
    xlabel("r")
    ylabel("x")
end

saveas(gcf,'Bifurcation.png')

