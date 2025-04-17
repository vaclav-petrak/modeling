% Clear workspace and close all figures
clear;
close;

% Number of steps in the random walk
steps = 100000;

% Maximum boundary for movement in both X and Y directions
boundary = 500;

% Initialize arrays to store coordinates of the two walkers
point = zeros(2, steps); 
point2 = zeros(2, steps);

% Perform the random walk for both points
for i = 1:steps-1
    point(:,i+1) = update_position(point(:,i), boundary);
    point2(:,i+1) = update_position(point2(:,i), boundary);
end

% Plot the paths of both walkers
hold on;
plot(point(1,:), point(2,:)); % First walker (default color)
plot(point2(1,:), point2(2,:), 'Color', [180/255, 70/255, 87/255]); % Second walker (custom color)

% Mark the final positions with red-filled blue circles
plot(point(1,end), point(2,end), 'bo', 'MarkerFaceColor', 'red');
plot(point2(1,end), point2(2,end), 'bo', 'MarkerFaceColor', 'red');

% Label axes
xlabel('X');
ylabel('Y');

% Set axis properties
axis square;
xlim([-boundary, boundary]);
ylim([-boundary, boundary]);
hold off;

% Function to update the position of a walker within the boundary
function pos_next = update_position(pos_current, boundary)
    x = pos_current(1);
    y = pos_current(2);
    
    % Randomly choose direction: 1=up, 2=down, 3=left, 4=right
    direction = randi(4);
    
    switch direction
        case 1 % Move up
            if y < boundary
                y = y + 1;
            end
        case 2 % Move down
            if y > -boundary
                y = y - 1;
            end
        case 3 % Move left
            if x > -boundary
                x = x - 1;
            end
        case 4 % Move right
            if x < boundary
                x = x + 1;
            end
    end
    
    % Return the updated position
    pos_next = [x; y];
end
