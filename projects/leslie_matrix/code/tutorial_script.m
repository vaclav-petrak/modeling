% Leslie Matrix Population Model Implementation

% Step 1: Define Parameters
% Fecundity rates (average offspring per individual in each age class)
f = [0, 1.6, 0.8]; % f1=0, f2=2, f3=1

% Survival rates (probability of surviving to the next age class)
s = [0.5, 0.7]; % s1=0.5 (age 1->2), s2=0.7 (age 2->3)
num_age_classes = length(f); % Number of age classes (k=3)

% Step 2: Construct the Leslie Matrix (L)
L = zeros(num_age_classes, num_age_classes);

% Fill the first row with fecundity rates
L(1, :) = f;

% Fill the sub-diagonal with survival rates
for i = 1:(num_age_classes - 1)
    L(i+1, i) = s(i);
end

disp('Leslie Matrix (L):');
disp(L);

% Step 3: Define the Initial Population Vector (N0)
N0 = [10; 8; 5]; % Column vector: [n1; n2; n3] at time t=0
disp('Initial Population Vector (N0):');
disp(N0);

% Step 4: Project the Population for One Time Step
N1 = L * N0; % Calculate population at time t=1
disp('Population Vector at t=1 (N1):');
disp(N1);

% Step 5: Simulate Population Growth Over Multiple Time Steps
num_time_steps = 20; % Number of years to simulate
population_history = zeros(num_age_classes, num_time_steps + 1); % To store N vectors
population_history(:, 1) = N0; % Store initial population

Nt = N0; % Current population vector starts at N0
for t = 1:num_time_steps
    Nt_plus_1 = L * Nt;             % Project to next step (N_{t+1} = L N_t)
    population_history(:, t+1) = Nt_plus_1; % Store result
    Nt = Nt_plus_1;                 % Update current population for next iteration
end

% Step 6: Analyze and Visualize Results
% Calculate total population size at each time step
total_population = sum(population_history, 1);

% Calculate age structure (proportions) over time
age_structure = zeros(size(population_history));
for t = 1:size(population_history, 2)
    if total_population(t) > 0 % Avoid division by zero
        age_structure(:, t) = population_history(:, t) / total_population(t);
    end
end

% Plot total population size
figure(1);
plot(0:num_time_steps, total_population, 'b-o', 'LineWidth', 1.5);
xlabel('Time Step (Years)'); ylabel('Total Population Size');
title('Total Population Growth Over Time'); grid on;

% Plot age structure over time
figure(2);
area(0:num_time_steps, age_structure', 'FaceColor','flat');
xlabel('Time Step (Years)'); ylabel('Proportion of Population');
title('Population Age Structure Over Time');
legend('Age Class 1', 'Age Class 2', 'Age Class 3'); ylim([0 1]);

% Step 7: Eigenvalue Analysis
[eigenvectors, eigenvalues_diag] = eig(L);
eigenvalues = diag(eigenvalues_diag); % Get eigenvalues as a vector

% Find the dominant eigenvalue (largest positive real part)
[dominant_eigenvalue, idx] = max(real(eigenvalues));
dominant_eigenvector = eigenvectors(:, idx);

% Normalize the stable age distribution eigenvector so elements sum to 1
stable_age_distribution = real(dominant_eigenvector) / sum(real(dominant_eigenvector));

disp(' '); % Blank line for spacing
fprintf('Dominant Eigenvalue (lambda): %.4f\n', dominant_eigenvalue);
disp('Stable Age Distribution (Proportions):');
disp(stable_age_distribution);

% Compare final simulated age structure to the calculated stable age distribution
disp('Simulated Age Structure at final time step:');
disp(age_structure(:, end));

% Animated Age Pyramid (Population Age Tree)
figure(3);
for t = 1:(num_time_steps + 1)
    clf;
    % Plot horizontal bar chart for current population vector
    barh(1:num_age_classes, population_history(:, t), 0.5, 'FaceColor', [0.2 0.4 0.6]);
    set(gca, 'YDir', 'reverse'); % Reverse Y-axis so youngest at top
    xlim([0, max(population_history(:)) * 1.1]);
    yticks(1:num_age_classes);
    yticklabels({'Age Class 1', 'Age Class 2', 'Age Class 3'});
    xlabel('Number of Individuals');
    title(sprintf('Population Age Tree - Year %d', t-1));
    grid on;
    drawnow;
    pause(0.2); % Delay to control animation speed
end



