% Parameters
numGenerations = 10;  % Number of generations to simulate
R0 = 1.5;             % Basic reproduction number
initialInfections = 1; % Number of initial infections

% Initialize arrays
numInfections = zeros(1, numGenerations);
numInfections(1) = initialInfections;

% Run the branching process
for gen = 2:numGenerations
    % Calculate the number of infections in the current generation
    currentInfections = 0;
    for i = 1:numInfections(gen-1)
        % Generate a Poisson-distributed number of new infections
        newInfections = poissrnd(R0);
        currentInfections = currentInfections + newInfections;
    end
    numInfections(gen) = currentInfections;
end

% Display the results
disp('Generation  Infections');
disp([(1:numGenerations)' numInfections']);

% Plot the results
figure;
bar(1:numGenerations, numInfections);
xlabel('Generation');
ylabel('Number of Infections');
title('Disease Spread using Branching Process');
