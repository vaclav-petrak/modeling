% --- Simulation Parameters ---
L = 160;             % Grid dimension (L x L)
num_steps = 500;     % Number of simulation iterations
f = 0.00002;         % Probability of spontaneous ignition (lightning strike)
p = 0.004;           % Probability of tree growth (planting/regrowth)

% --- State Constants ---
EMPTY = 0;           % Numerical value for empty/ground state
TREE = 1;            % Numerical value for tree state
BURNING = 2;         % Numerical value for burning state

% --- Initialization ---
grid = zeros(L, L);  % Initialize the grid as empty (all cells = EMPTY)
                     % Alternative: Start with trees: grid = ones(L, L) * TREE;

% --- Visualization Setup ---
figure(1);           % Create figure window
% Define colors for visualization
color_ground = [ 76  66  70] / 255; % Ash/Ground color
color_trees  = [118 176  65] / 255; % Tree color
color_fire   = [228  87  46] / 255; % Fire color
colormap([color_ground; color_trees; color_fire]); % Apply the colormap

h_img = imagesc(grid); % Display initial grid and keep handle for updates
title(sprintf('Forest Fire Model - Step 0 / %d', num_steps));
axis equal off;      % Use square pixels and turn off axes
clim([EMPTY BURNING]); % Set color limits consistent with states

% --- Main Simulation Loop ---
for step = 1:num_steps
    % --- State Update ---
    next_grid = zeros(L, L); % Create an empty grid for the next state

    % Iterate through every cell in the current grid
    for r = 1:L % Iterate over rows
        for c = 1:L % Iterate over columns
            % Check if any *neighbor* is burning (Moore neighborhood)
            neighbor_is_burning = isNeighborBurning(r, c, grid, L, BURNING);

            % Get the current state of the cell
            current_state = grid(r, c);

            % Calculate the next state based on rules and neighbor status
            next_grid(r, c) = calculateNextState(current_state, neighbor_is_burning, p, f, EMPTY, TREE, BURNING);
        end
    end

    grid = next_grid; % Update the main grid with the calculated next states

    % --- Plotting ---
    set(h_img, 'CData', grid); % Update the displayed grid data
    title(sprintf('Forest Fire Model - Step %d / %d', step, num_steps)); % Update title
    drawnow; % Force MATLAB to redraw the figure window
    % pause(0.01); % Uncomment to slow down the visualization
end

% --- Helper Functions ---

function is_burning = isNeighborBurning(r, c, grid, L, BURNING)
% Checks the 8 Moore neighbors of cell (r,c) for fire.
% Handles boundary conditions (no wrap-around, edge cells have fewer neighbors).
    is_burning = false; % Assume no neighbor is burning initially
    % Iterate through the 3x3 neighborhood
    for dr = -1:1
        for dc = -1:1
            % Skip the center cell itself
            if dr == 0 && dc == 0
                continue;
            end

            % Calculate neighbor coordinates
            nr = r + dr;
            nc = c + dc;

            % Check if neighbor is within grid boundaries
            if nr >= 1 && nr <= L && nc >= 1 && nc <= L
                % If a neighbor is burning, set flag and exit loops
                if grid(nr, nc) == BURNING
                    is_burning = true;
                    return; % Exit function early once fire is found
                end
            end
        end
    end
end

function next_state = calculateNextState(current_state, neighbor_is_burning, p_growth, f_ignition, EMPTY, TREE, BURNING)
% Calculates the next state of a cell based on its current state,
% whether a neighbor is burning, and the growth/ignition probabilities.

    switch current_state
        case EMPTY   % If cell is currently empty (ground)
            % It becomes a tree with probability p_growth
            if rand() < p_growth
                next_state = TREE;
            else
                next_state = EMPTY; % Stays empty otherwise
            end

        case TREE   % If cell is currently a tree
            % It catches fire if a neighbor is burning OR
            % it ignites spontaneously (lightning) with probability f_ignition
            random_ignition = rand() < f_ignition;
            if (neighbor_is_burning || random_ignition)
                next_state = BURNING; % Tree starts burning
            else
                next_state = TREE; % Stays a tree otherwise
            end

        case BURNING % If cell is currently burning
            % It becomes empty in the next step (burns out)
            next_state = EMPTY;

        otherwise % Should not happen with defined states
            next_state = current_state; % Default to no change
    end
end