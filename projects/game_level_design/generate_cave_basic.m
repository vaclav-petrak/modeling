%% --- Cave Generation using Cellular Automata in MATLAB ---
% version 1: basic version that works

% Clean up
clear;
clc;
close all;

%% --- Parameters --- 
grid_width = 100;        
grid_height = grid_width;        
initial_wall_chance = 0.54; 
simulation_steps = 5;     
seed = 1; % Set a seed for reproducibility

%% -- The CA rule ---
% If a wall has less than this many neighbors, it becomes a floor
wall_death_limit = 4;
% If a floor has more than this many neighbors becomes a wall
wall_birth_limit = 5;


%% --- Create a Random Grid --
% rng function is a seed. It allows you to make reproducible results
rng(seed)
random_grid = rand(grid_height, grid_width);
map = zeros(grid_height, grid_width);
map(random_grid < initial_wall_chance) = 1;


%% --- Simulation ---
for step = 1:simulation_steps
    % We create a new map to store the changes for this step.
    new_map = map;

    % We loop over every except for the bordets
    for y = 2:grid_height-1
        for x = 2:grid_width-1
            neighbors = map(y-1:y+1, x-1:x+1);

            % Count the number of wall neighbors
            wall_count = sum(neighbors(:)) - map(y, x);

            % --- Apply the Automata Rules ---
            if map(y, x) == 1 
                if wall_count < wall_death_limit
                    new_map(y, x) = 0; % It becomes a floor.
                end
            else % If the cell is currently a FLOOR
                if wall_count > wall_birth_limit
                    new_map(y, x) = 1; % It becomes a wall.
                end
            end
        end
    end

    % Update the main map 
    map = new_map;
    fprintf('Step %d complete.\n', step);
end

%% --- Post-Processing Enforce Border Walls ---
map(1, :) = 1;        % Top row
map(end, :) = 1;      % Bottom row
map(:, 1) = 1;        % Left column
map(:, end) = 1;      % Right column

%% --- Visualization ---
figure;
imagesc(map);
colormap(flipud(gray));
title('Generated Cave Map');
axis off;
axis equal;


