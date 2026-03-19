clear, close

% ----- Parameters -----
area = 100;
population = 1000;
initial_infected = 1;
iterations = 1500;
infection_probability = 0.5;

% ----- Initialization -----
position = randi(area, population, 2);      % Random positions
status = ones(population, 1);               % 1 = Susceptible, 2 = Infected
status(1:initial_infected) = 2;

infected_count    = zeros(iterations,1);
susceptible_count = zeros(iterations,1);

% ----- Prepare figure once -----
figure(1); set(gcf, 'Position', [100, 100, 1200, 500]);
tiledlayout(1, 2);

% ----- Simulation loop -----
for i = 1:iterations
    % Infection logic
    for person = 1:population
        if status(person) == 1
            same_x = position(:,1) == position(person,1);
            same_y = position(:,2) == position(person,2);
            nearby_infected = same_x & same_y & (status == 2);
            if any(nearby_infected) && rand < infection_probability
                status(person) = 2;
            end
        end
    end

    % Record counts
    susceptible_count(i) = sum(status == 1);
    infected_count(i)    = sum(status == 2);

    % ----- Plot  -----
    nexttile(1);
    cla;
    hold on;
    plot(position(status==1,1), position(status==1,2), 'go', 'MarkerFaceColor','g');
    plot(position(status==2,1), position(status==2,2), 'ro', 'MarkerFaceColor','r');
    axis square; xlim([0 area]); ylim([0 area]);

    nexttile(2);
    cla;
    plot(1:i, susceptible_count(1:i), 'g', 'LineWidth', 2); hold on;
    plot(1:i, infected_count(1:i), 'r', 'LineWidth', 2);
    title('S vs. I over time'); xlim([1 iterations]); ylim([0 population]);
    drawnow;

    % Move agents
    for p = 1:population
        [x, y] = move(position(p,1), position(p,2), area);
        position(p,:) = [x, y];
    end
end

function [x, y] = move(x, y, area)
    switch randi(4)
        case 1, if y < area, y = y + 1; end  % up
        case 2, if y > 1,    y = y - 1; end  % down
        case 3, if x > 1,    x = x - 1; end  % left
        case 4, if x < area, x = x + 1; end  % right
    end
end
