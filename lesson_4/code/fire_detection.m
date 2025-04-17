% This script initializes a forest matrix and checks for the presence of fire (number '2') 
% in the neighborhood of specified grid positions using the detect_fire function.

forrest = [
0 1 1 0 2
0 1 1 1 1
0 2 0 1 1
1 1 0 0 0
];

detect_fire(2,2, forrest)
detect_fire(4,5, forrest)
detect_fire(1,5, forrest)
detect_fire(1,5, forrest)

function fire_in_neighborhood = detect_fire(row, col, grid)
    % Get grid dimensions
    [width, height] = size(grid);

    % Get neighborhood with the specified cell by indexing
    neighborhood = grid(max(1,row-1):min(width,row+1),max(1,col-1):min(height,col+1));

    % Determine if fire (represented as '2') is present in the neighborhood
    fire_in_neighborhood = max(max(neighborhood)) == 2;
end
