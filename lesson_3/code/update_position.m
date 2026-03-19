function [x, y] = update_position(x, y, area)
    
direction = randi([1 4]);  
    switch direction    
        case 1  % go up
            if y < area; y = y + 1; 
            end

        case 2  % go down
            if y > 0; y = y - 1;
            end
            
        case 3  % go left
            if x > 0; x = x - 1;
            end
             
        case 4  % go right
            if x < area; x = x + 1;
            end
    end
end