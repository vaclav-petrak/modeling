% --- Cave Generation using Cellular Automata in MATLAB ---
% version 4: Keep only the largest cave.

% --- Main Execution ---
% Clean up the environment
clear;
clc;
close all;

% --- Parameters --- 
grid_width = 100;        
grid_height = grid_width;        
initial_wall_chance = 0.535; 
simulation_steps = 15;    
seed = 3; % Set a seed for reproducibility

% The CA rule
wall_death_limit = 4; % If a wall has less than this many neighbors, it becomes a floor
wall_birth_limit = 5; % If a floor has more than this many neighbors, it becomes a wall

% Post-processing parameters
room_size_threshold = 100; % Any room with fewer cells than this will be filled in.

% --- Generation ---
rng(seed); 
%% --- Create a Random Grid --
% 1 represents a wall, 0 represents a floor.
random_grid = rand(grid_height, grid_width);
map = zeros(grid_height, grid_width);
map(random_grid < initial_wall_chance) = 1;

%% --- Simulation ---
% This loop iterates the cellular automata rules to form cave structures.
for step = 1:simulation_steps
    map = run_simulation_step(map, wall_death_limit, wall_birth_limit);
end

%% --- Post-Processing ---
% 1. Remove small, isolated rooms.
map = keep_largest_floor_area(map); 

% 2. Enforce a solid border around the map.
map = enforce_border_walls(map);

%% --- Visualization ---
figure;
imagesc(map);
colormap(flipud(gray))
axis off;
axis equal;

% --- Function Definitions ---
function new_map = run_simulation_step(map, death_limit, birth_limit)
    % Applies one step of the cellular automata rules to the map.
    [grid_height, grid_width] = size(map);
    new_map = map;
    
    % Loop over every cell except for the borders
    for y = 2:grid_height-1
        for x = 2:grid_width-1
            % Get the 3x3 neighborhood
            neighbors = map(y-1:y+1, x-1:x+1);
            % Count the number of wall neighbors (sum of the 3x3 grid minus the center cell)
            wall_count = sum(neighbors(:)) - map(y, x);
            
            % --- Apply the Automata Rules ---
            if map(y, x) == 1 % If the cell is currently a WALL
                if wall_count < death_limit
                    new_map(y, x) = 0; % It becomes a floor (dies).
                end
            else % If the cell is currently a FLOOR
                if wall_count > birth_limit
                    new_map(y, x) = 1; % It becomes a wall (is born).
                end
            end
        end
    end
end

function map_with_border = enforce_border_walls(map)    
    % Ensures the entire border of the map is made of wall cells.
    map_with_border = map;
    map_with_border(1, :) = 1;        % Top row
    map_with_border(end, :) = 1;      % Bottom row
    map_with_border(:, 1) = 1;        % Left column
    map_with_border(:, end) = 1;      % Right column
end


function modified_map = keep_largest_floor_area(map)
% keep_largest_floor_area processes a binary map (0=floor, 1=wall) and
% retains only the largest connected component of floor cells, turning
    [grid_height, grid_width] = size(map);
    
    visited = false(grid_height, grid_width);
    
    % Variables to store the largest component found so far
    largest_component_cells = [];
    max_area = 0;
    
    % Iterate through each cell in the map
    for r = 1:grid_height
        for c = 1:grid_width
            % If the cell is a floor (0) and has not been visited yet
            if map(r, c) == 0 && ~visited(r, c)
                % Start a Breadth-First Search (BFS) to find the connected component
                current_component_cells = []; % Stores [row, col] pairs for the current component
                component_area = 0;
                
                % Initialize a queue for BFS with the current cell
                q = java.util.LinkedList(); % Using Java LinkedList as a queue for efficiency
                q.add([r, c]);
                visited(r, c) = true; % Mark the starting cell as visited
                
                % Define possible directions for neighbors (up, down, left, right)
                dr = [-1, 1, 0, 0]; % 
                dc = [0, 0, -1, 1]; % 
                
                while ~q.isEmpty()
                    % Dequeue a cell
                    current_cell = q.remove();
                    curr_r = current_cell(1);
                    curr_c = current_cell(2);
                    
                    % Add the current cell to the component list and increment area
                    current_component_cells = [current_component_cells; curr_r, curr_c];
                    component_area = component_area + 1;
                    
                    % Explore neighbors
                    for i = 1:4 % Loop through the 4 directions
                        next_r = curr_r + dr(i);
                        next_c = curr_c + dc(i);
                        
                        % Check if the neighbor is within bounds
                        if next_r >= 1 && next_r <= grid_height && ...
                           next_c >= 1 && next_c <= grid_width
                            % If the neighbor is a floor and has not been visited
                            if map(next_r, next_c) == 0 && ~visited(next_r, next_c)
                                visited(next_r, next_c) = true; 
                                q.add([next_r, next_c]); 
                            end
                        end
                    end
                end
                
                % After BFS for one component, check if it's the largest found so far
                if component_area > max_area
                    max_area = component_area;
                    largest_component_cells = current_component_cells;
                end
            end
        end
    end
    
    % Create the new map, initially all walls
    modified_map = ones(grid_height, grid_width);
    
    % Set cells belonging to the largest floor area back to floor (0)
    for i = 1:size(largest_component_cells, 1)
        row = largest_component_cells(i, 1);
        col = largest_component_cells(i, 2);
        modified_map(row, col) = 0;
    end
end
