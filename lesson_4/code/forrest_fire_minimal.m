% Simple, functional version of forrest fire cellular automata

clear, clc

% --- Initiate ---
area = 160;
iterations = 500;
P_ignition = 0.00002;
P_planting = 0.004;
grid = zeros(area);

% --- Iterate ---
for i = 1:iterations
   % --- Update status ---
   % prepare empty grid
   new_grid = zeros(area);  

   % iterate throuhg every cell
   for row = 1:area
      for col = 1:area  
         fire_in_neighborhood = detect_fire(row, col, grid);
         cell_state = grid(row,col);
         new_grid(row,col) = update_cell_state(cell_state, fire_in_neighborhood, P_planting, P_ignition);
      end
   end

   grid = new_grid; 

   % --- Plot ---
figure(1)
imagesc(grid);
clim([0 2]);
end

function fire_in_neighborhood = detect_fire(row, col, grid)
    % get grid dimensions
    [width, height] = size(grid);

    % gets neighborhood with the cell by indexing
    neighborhood = grid(max(1,row-1):min(width,row+1),max(1,col-1):min(height,col+1));

    % substract cell
    fire_in_neighborhood = max(max(neighborhood)) == 2;
end

function new_state = update_cell_state(cell_state, fire_in_neighborhood, P_planting, P_ignition)
         switch cell_state
         case 0   % ground
           new_state = rand() < P_planting;
         case 1   % tree
           random_ignition = rand() < P_ignition;

           if (fire_in_neighborhood || random_ignition)
              new_state = 2;
           else
               new_state = 1;
           end
         case 2   % fire
           new_state = 0;
         end
end