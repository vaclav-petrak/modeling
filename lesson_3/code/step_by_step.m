% ----- Initiate -----
clear, close 
% Constants
    area = 100;
    population = 1000;
    infected = 10;
    iterations = 1500;
    infection_probability = 0.80;
    cure_constant = 0.01;

% Position of a person
    position = randi(area, population, 2);  

% Status - susceptible: 1, infeced 2: recovered: 3
    status = ones(population, 1); % set 1 as default
    status(1:infected)= 2;        % first are infected

    
for i = 1:iterations

    for p = 1:population
        [position(p,1),position(p,2)] = update_position(position(p,1),position(p,2), area);
    end

figure(1)
clf
hold on;
    plot(position(status == 1, 1), position(status == 1, 2),'o', 'MarkerFaceColor', 'green');
    plot(position(status == 2, 1), position(status == 2,2), 'o', 'MarkerFaceColor', 'red')
    plot(position(status == 3, 1), position(status == 3,2), 'o', 'MarkerFaceColor', 'blue')
hold off;
axis square;
end