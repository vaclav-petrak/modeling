% Parameters
grid_size = 100;
grain_count = 0;

% Initialize grid
grid = zeros(grid_size);

% Visualization setup
figure(1);
axis off;
drawnow;

% Simulation loop
while grain_count < round(grid_size^2/4)  % Fill up to 25%
    new_grid = grid;  % Copy for updating

    for row = grid_size-1:-1:1  % bottom-up to prevent overwrite
        for col = 2:grid_size-1  % avoid borders
            if grid(row, col) == 1
                new_grid = update_grain_position(grid, new_grid, row, col);
            end
        end
    end

    grid = new_grid;

    % Generate new grain
    grid = generate_new_grain(grid, grid_size);

    % Grain count 
    grain_count = sum(grid(:));

    % Display
    imagesc(grid);
    drawnow;
end


function new_grid = update_grain_position(grid, new_grid, row, col)
% UPDATE_GRAIN_POSITION Moves a single sand grain based on gravity rules.

    % Try to fall straight down
    if grid(row+1, col) == 0
        new_grid(row, col) = 0;
        new_grid(row+1, col) = 1;

    % Try to fall down-left
    elseif grid(row+1, col-1) == 0
        new_grid(row, col) = 0;
        new_grid(row+1, col-1) = 1;

    % Try to fall down-right
    elseif grid(row+1, col+1) == 0
        new_grid(row, col) = 0;
        new_grid(row+1, col+1) = 1;
    end
end

function grid = generate_new_grain(grid, grid_size)
% GENERATE_NEW_GRAIN Adds a new grain to the top row of the grid
% Grains are added in two streams

    % Define the horizontal center of the grid
    plot_center = round(grid_size / 2);

    % Introduce randomness in position
    random_variation = randi([-5, 5]);

    % Stream variation: randomly generate stream
    stream_distance = round(grid_size / 5);
    stream_position_start = [2, 1, 1, 1, -1, -1];
    idx = randi(numel(stream_position_start));
    stream = stream_distance * stream_position_start(idx);

    % Compute final column index for new grain
    grain_start = plot_center + stream + random_variation;

     % Ensure grain starts within grid bounds
    grain_start = max(1, min(grid_size, grain_start));

    % Place the grain in the top row
    grid(1, grain_start) = 1;
end

