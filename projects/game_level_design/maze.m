% Example 1: Basic network
gridSize = 100;
numSegments = 200;
segmentLength = 7;
turnProbability = 0.25;
corridorMap = createRandomCorridorNetwork(gridSize, numSegments, segmentLength, turnProbability);
figure;
imshow(corridorMap);
title('Random Corridor Network');


function corridorNetwork = createRandomCorridorNetwork(gridSize, numSegments, segmentLength, turnProbability)
% createRandomCorridorNetwork creates a random corridor network in a grid.
%
%   corridorNetwork = createRandomCorridorNetwork(gridSize, numSegments, segmentLength, turnProbability)
%
%   Inputs:
%     gridSize        - Size of the square grid (e.g., 100 for 100x100).
%     numSegments     - Total number of corridor segments to generate.
%     segmentLength   - Length of each corridor segment (number of steps).
%     turnProbability - Probability (0-1) of changing direction after a segment.
%                       A lower value means straighter corridors.
%
%   Output:
%     corridorNetwork - A gridSize x gridSize matrix where 1s represent
%                       corridors and 0s represent walls.

    if nargin < 4
        turnProbability = 0.3; % Default turn probability
    end
    if nargin < 3
        segmentLength = 5; % Default segment length
    end
    if nargin < 2
        numSegments = 200; % Default number of segments
    end
    if nargin < 1
        gridSize = 100; % Default grid size
    end

    % Initialize the grid with walls (0s)
    corridorNetwork = zeros(gridSize, gridSize);

    % Choose a random starting point
    currentX = randi(gridSize);
    currentY = randi(gridSize);
    corridorNetwork(currentY, currentX) = 1; % Mark as corridor

    % Define possible directions: [dy, dx]
    % N: [-1, 0], S: [1, 0], E: [0, 1], W: [0, -1]
    directions = [-1, 0;    % North
                   1, 0;     % South
                   0, 1;     % East
                   0, -1];   % West

    currentDirectionIdx = randi(4); % Start with a random direction

    for i = 1:numSegments
        % Decide whether to turn or continue in the same direction
        if rand() < turnProbability
            currentDirectionIdx = randi(4); % Choose a new random direction
        end
        currentDirection = directions(currentDirectionIdx, :);

        % Walk for segmentLength
        for j = 1:segmentLength
            newX = currentX + currentDirection(2);
            newY = currentY + currentDirection(1);

            % Check boundaries
            if newX >= 1 && newX <= gridSize && newY >= 1 && newY <= gridSize
                currentX = newX;
                currentY = newY;
                corridorNetwork(currentY, currentX) = 1; % Mark as corridor
            else
                % If we hit a boundary, choose a new direction immediately
                % and break from this segment walk.
                currentDirectionIdx = randi(4);
                break;
            end
        end
    end
end