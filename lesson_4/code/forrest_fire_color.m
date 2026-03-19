% More advanced version of forrest fire cellular automata

clear, clc

% --- Initiate ---
area = 160;
iterations = 1000;
intial_coverage = 0.2;

ignition_chance = 0.00002;
planting_chance = 0.0040;

% colors
ground = [ 76  66 70] / 255;
trees  = [118 176 65] / 255;
fire  =  [228  87 46] / 255;
colormap([ground;trees;fire]);

% intial states
grid = rand(area) < intial_coverage;

% memory allocation
tree_count = NaN(1,iterations);
fire_count = NaN(1,iterations);

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
         new_grid(row,col) = update_cell_state(cell_state, fire_in_neighborhood, planting_chance, ignition_chance);
      end
   end

    grid = new_grid; 

   % --- Summarise ---
   tree_count(i) = sum(sum(grid == 1));
   fire_count(i) = sum(sum(grid == 2));

   % --- Plot ---
figure(1)
set(gcf, 'Position', [100, 100, 1200, 600]); % [left, bottom, width, height]
tiledlayout(1, 2);

nexttile


imagesc(grid);
clim([0 2]);
axis square; axis off;


nexttile
    hold on
    plot(tree_count, LineWidth=2, Color=trees);
    title("Forrest fire simulation")

    plot(fire_count*10, LineWidth=2, Color=fire);
    ylim([0, 12000]);     xlim([0, iterations])
    ylabel("Tree count"); xlabel("Time")
    title("Forrest fire simulation")
    hold off
 
 %  pause(0.05) 
   

end

function fire_in_neighborhood = detect_fire(row, col, grid)
    % get grid dimensions
    [width, height] = size(grid);

    % gets neighborhood with the cell by indexing
    neighborhood = grid(max(1,row-1):min(width,row+1),max(1,col-1):min(height,col+1));

    % substract cell
    fire_in_neighborhood = max(max(neighborhood)) == 2;
end


function new_state = update_cell_state(cell_state, fire_in_neighborhood, planting_chance, ignition_chance)
         switch cell_state
         case 0   % ground
           new_state = rand() < planting_chance;
         case 1   % tree
           random_ignition = rand() < ignition_chance;

           if (fire_in_neighborhood || random_ignition)
              new_state = 2;
           else
               new_state = 1;
           end
         case 2   % fire
           new_state = 0;
         end
end



