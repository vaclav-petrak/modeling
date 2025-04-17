% ----- Initiate -----
clear, close 
% Constants
    area = 100;
    population = 1000;
    infected = 10;
    iterations = 1500;
    infection_probability = 2;
    cure_constant = 0.03;

% Position of a person
    position = randi(area, population, 2);  

% Status - susceptible: 1, infeced 2: recovered: 3
    status = ones(population, 1); % set 1 as default
    status(1:infected)= 2;        % first are infected

% Pre-assigned vectors for sumary
    infected_count    = zeros(iterations, 1);
    susceptible_count = zeros(iterations, 1);
    recovered_count   = zeros(iterations, 1);

% ----- Run simulation -----
for i = 1:iterations   
    % --- Update status ---
    for person = 1:population
        if status(person) == 1  % Susceptible
            % Check if any individual is in the same grid cell as the current person and is infected
            
            %  array for individuals with the same X coordinate
            same_x = position(:,1) == position(person,1);
            same_y = position(:,2) == position(person,2);
            
            %  array for individuals that are infected (status == 2)
            is_infected = (status == 2);
            
            same_square_and_infected = same_x & same_y & is_infected;
                if any(same_square_and_infected) && rand < infection_probability
                    status(person) = 2;
                end

        elseif status(person) == 2  % Infected
            % Infected person has chance to be cured
            if rand < cure_constant
                status(person) = 3;
            end
        end
    end
    
    % ----- Summarize results  -----
    infected_count(i) = length(status(status == 2));
    susceptible_count(i) = length(status(status == 1));
    recovered_count(i) = length(status(status == 3));
    
    % ----- Plot -----
    % Set the figure size and position
    figure(1);
    set(gcf, 'Position', [100, 100, 1200, 600]); % [left, bottom, width, height]
    
    % Create 
    tiledlayout(1, 2);
    
    % First subplot
    nexttile;
    hold on;
        plot(position(status == 1, 1), position(status == 1, 2),'o','MarkerFaceColor', 'green');
        plot(position(status == 2, 1), position(status == 2,2), 'o', 'MarkerFaceColor', 'red')
        plot(position(status == 3, 1), position(status == 3,2), 'o', 'MarkerFaceColor', 'blue')
        hold off;
    axis square;
    
    % Second subplot
    nexttile;
    hold on;
        plot(1:i, susceptible_count(1:i), Color= 'green', LineWidth=2);
        plot(1:i, infected_count(1:i),    Color= 'red',   LineWidth=2);
        plot(1:i, recovered_count(1:i),   Color= 'blue',  LineWidth=2);
        xlim([1, iterations]);
    hold off;
    
        % ----- Update positions -----
        for person = 1:population
            [position(person,1), position(person,2)] = update_position(position(person,1), position(person,2), area);
        end
end

function [x, y] = update_position(x, y, area)
    
direction = randi([1 4]);  
    switch direction    
        case 1  % go up
            if y < area; y = y + 1; 
            end

        case 2  % go down
            if y > 0; y = y - 1;
            end
            
        case 3  % go left
            if x > 0; x = x - 1;
            end
             
        case 4  % go right
            if x < area; x = x + 1;
            end
    end
end