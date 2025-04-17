% The first task is to prepare a grid containing random numbers
clear, clc

% --- Initiate ---
area = 100;
intial_coverage = 0;
iterations = 200;
step_time = 0.05;

% colors
dead = [ 238 243 106] / 255;
live = [  63  48  71] / 255;

pattern = [
1 1 1   
1 0 1 
1 0 1 
];

% intial states
grid = rand(area) < intial_coverage;

grid = place_pattern(grid, pattern, [50, 50]);

% --- Iterate ---
for i = 1:iterations
    
    % --- Update status ---
    % prepare empty grid
    new_grid = zeros(area);   
 
    % iterate throuhg every cell
    for row = 1:area
        for col = 1:area
            % get information cell and about surroundings
            neighbors_alive = get_neighbors_alive(row, col, grid);
            is_alive = grid(row, col);
            % update states
            new_grid(row,col) = update_cell_state(is_alive, neighbors_alive);
        end
    end

    grid = new_grid;
    
     % --- Plot ---
    figure(1)
      colormap([live;dead]);
      imagesc(grid)
      axis square; axis off;
      title(['Iteration ', num2str(i)]);
   
    % --- Pause ---
    pause(step_time)
end

% checking how many neighnors live
function neighbors_alive = get_neighbors_alive(row, col, grid)
    % get grid dimensions
    [width, height] = size(grid);

    % gets neighborhood with the cell by indexing
    cell_with_neighborhood = grid(max(1,row-1):min(width,row+1),max(1,col-1):min(height,col+1));

    % substract cell
    neighbors_alive  = sum(sum(cell_with_neighborhood)) - grid(row, col);
end

%  asigning new state
function new_state = update_cell_state(is_alive, neighbors_alive)
     % live cell with fewer than 2 live neighbors dies
    if is_alive && neighbors_alive < 2        
        new_state = 0;  

     % live cell with 2 or 3 live neighbors lives
    elseif is_alive && (neighbors_alive == 2 || neighbors_alive == 3)
        new_state = 1;  

    % live cell with more than 3 live neighbors dies
    elseif is_alive && neighbors_alive > 3
        new_state = 0;  

    % dead cell with 3 live neighbors becomes alive
    elseif ~is_alive && neighbors_alive == 3
        new_state = 1;  
        
    % otherwise dead cells remain dead
    else
        new_state = 0;  
    end
end

%  place patten
function grid = place_pattern(grid, pattern, position)
    w = width(pattern)-1;
    h = height(pattern) - 1;
    grid(position(1):position(1)+h, position(2):position(2) + w) = pattern;
end
