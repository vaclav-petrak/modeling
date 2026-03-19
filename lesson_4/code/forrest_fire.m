 
forrest_color_map = [ 
    % R,   G,  B
     76,  66, 70         % dark for ground
    118, 176, 65         % green for trees
    228,  87, 46]/ 255;  % red for fire


forrest =[
    1 1 1 0 0
    1 1 1 1 0
    1 1 2 1 0
    1 1 2 0 0
    1 0 0 0 0];

colormap(forrest_color_map);
imagesc(forrest) 
