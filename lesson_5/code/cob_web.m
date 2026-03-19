clear, close 

r = 1.75;    % growth rate
x0 = 0.25;   % initial population size
n_total = 30;   % number of generations to simulate

x = zeros(n_total+1, 1);
x(1) = x0;

for i = 1:n_total
    x(i+1) =r*(1 - x(i))*x(i);
end


x_n = x(1:end-1);
x_n_plus_1 = x(2:end);
x_plot = 0:0.01:1;
y_plot = r.*x_plot.*(1-x_plot);

for  i = 1:n_total
    figure(1)
    tiledlayout(2,1);
    nexttile
        hold on
            plot(x_plot,y_plot, Color="blue" , LineWidth=2)     % "parabola"
            plot([0 1],[0 1], Color="black" , LineWidth=2);     % "the line"
            stairs(x_n(1:i),x_n_plus_1(1:i), Color="red" , LineWidth=1)
            plot([x_n(1) x_n(1)],[0 x_n_plus_1(1)], Color="red" , LineWidth=1);
            axis square
        hold off
    
    nexttile
        plot(x_n(1:i), LineWidth=1, Color="red");
        ylim([0,1])
        xlim([0,n_total])
    pause(0.1);
end