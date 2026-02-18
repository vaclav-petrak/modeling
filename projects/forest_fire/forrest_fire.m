% --- Parameters ---
L = 100;         % Grid size (L x L)
p = 0.01;       % Growth probability
f = 0.0001;      % Lightning probability (f << p)
num_steps = 500;

% --- State Constants ---
EMPTY = 0;
TREE = 1;
BURNING = 2;

% --- Initialize Grid ---
% Start with an empty grid
grid = zeros(L, L) * EMPTY; % Initialize grid as empty

% --- Visualization Setup ---
figure;
h = imagesc(grid); % Handle for image object
colormap([0.8 0.8 0.8; 0 0.6 0; 1 0 0]); % Colors: Ash(0), Green(1), Red(2)
clim([EMPTY, BURNING]); % Set explicit color limits for states 0, 1, 2
axis equal off;
title('Forest Fire Simulation');
% colorbar; % Removed as requested

% --- Simulation Loop ---
for step = 1:num_steps
    next_grid = grid; % Copy current state to initialize next state

    for r = 1:L
        for c = 1:L
            % --- Apply Rules based on current 'grid' state ---

            if grid(r, c) == BURNING
                next_grid(r, c) = EMPTY; % Burning tree becomes empty

            elseif grid(r, c) == TREE
                % Check neighbors for fire (Periodic boundary conditions)
                burning_neighbor = false;
                % Check 4 direct neighbors (von Neumann)
                neighbors = [-1 0; 1 0; 0 -1; 0 1]; % N, S, W, E offsets
                for i = 1:size(neighbors, 1)
                    dr = neighbors(i, 1);
                    dc = neighbors(i, 2);
                    % Wrap around using modulo arithmetic
                    nr = mod(r + dr - 1, L) + 1; 
                    nc = mod(c + dc - 1, L) + 1;
                    if grid(nr, nc) == BURNING
                        burning_neighbor = true;
                        break; % Found one burning neighbor, no need to check more
                    end
                end % End neighbor check loop
                
                % Optional: Check 8 neighbors (Moore) - uncomment below & comment above
                % for dr = -1:1 
                %     for dc = -1:1
                %         if dr == 0 && dc == 0 
                %             continue; % Skip self
                %         end
                %         % Wrap around using modulo arithmetic
                %         nr = mod(r + dr - 1, L) + 1; 
                %         nc = mod(c + dc - 1, L) + 1;
                %         if grid(nr, nc) == BURNING
                %             burning_neighbor = true;
                %             break; % Found one burning neighbor
                %         end
                %     end
                %     if burning_neighbor
                %         break;
                %     end
                % end % End Moore neighbor check

                if burning_neighbor
                    next_grid(r, c) = BURNING; % Catches fire from neighbor
                else
                    % Check for lightning strike
                    if rand < f
                        next_grid(r, c) = BURNING; % Spontaneous ignition
                    end
                    % Otherwise, remains a tree (already set in next_grid copy)
                end

            elseif grid(r, c) == EMPTY
                % Check for tree growth
                if rand < p
                    next_grid(r, c) = TREE; % New tree grows
                end
                % Otherwise, remains empty (already set in next_grid copy)
            end
        end % End column loop
    end % End row loop

    grid = next_grid; % Update the grid for the next step

    % --- Update Visualization ---
    set(h, 'CData', grid); % Update image data
    title(sprintf('Forest Fire Simulation - Step %d', step));
    drawnow limitrate; % Force display update, limitrate helps performance

    % pause(0.01); % Slow down visualization if needed

end % End simulation loop