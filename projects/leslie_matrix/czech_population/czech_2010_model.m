%% Lesle matrxi model
%% --- Model Parameters ---
% Group size
group_interval = 5;  

% Simulation values 
simulation_years = 100;

intitial_year = 2010;

% Initial population vector
population_initial = [275413, 228558, 223394, 300086, 339507, 365668, ...
    450984, 410637, 341023, 333977, 351237, 390758, ...
    380115, 293910, 212293, 196457, 149630, 84217, ...
    16110, 5079];

% Annual survival rates per year
survival_annual = [0.999354, 0.999891, 0.999888, 0.999783, 0.999747, 0.999751, ...
    0.999643, 0.999437, 0.998944, 0.998111, 0.996996, 0.995222, ...
    0.992205, 0.987149, 0.978713, 0.962139, 0.925109, 0.857950, ...
    0.743265];

% Fertility rates per year
fertility_annual = [0.000000, 0.000000, 0.000027, 0.005455, 0.022008, 0.048309, ...
    0.047481, 0.019136, 0.002915, 0.000117, 0.000006, 0.000000, ...
    0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, ...
    0.000000, 0.000000];


%% --- Initation ---
% Number of simulation steps
simulation_steps = floor(simulation_years / group_interval);

% Adjust annual survival and fertility rates to match group interval
survival_group = survival_annual .^ group_interval;
fertility_group = fertility_annual * group_interval;

%%  --- Build Leslie matrix ---
n = length(population_initial);
leslie_matrix = zeros(n);
leslie_matrix(1, :) = fertility_group;
for i = 2:n
    leslie_matrix(i, i-1) = survival_group(i-1);
end

% Initialize population matrix for saving data
population_by_step = zeros(n, simulation_steps + 1);
population_by_step(:, 1) = population_initial;
disp(population_by_step)

%% --- Run simulation ---
for t = 2:(simulation_steps + 1)
    population_by_step(:, t) = leslie_matrix * population_by_step(:, t - 1);
end

%% --- Analysis ---
% Compute total population at each time step
total_population = sum(population_by_step, 1);

%% --- Plotting ---
year_axis = intitial_year:group_interval:start_year + simulation_steps*group_interval;

subplot(1,2,1);
plot(year_axis, total_population, '-o', 'LineWidth', 2);
xlabel('Year');
ylabel('Total Population');
title(['Population Development (' num2str(group_interval) '-Year Leslie Model)']);
grid on;


ylim([0, max(total_population)*1.1]); 

% Generate age group labels
age_labels = strings(n,1);
for i = 1:n-1
    age_labels(i) = sprintf('%d-%d', (i-1)*group_interval, i*group_interval - 1);
end
age_labels(n) = sprintf('%d+', (n-1)*group_interval);


subplot(1,2,2);
% Combine initial and final population vectors
population_compare = [population_by_step(:,1), population_by_step(:,end)];

% Create side-by-side bar plot
barh(population_compare, 'grouped');
set(gca, 'YTick', 1:n, 'YTickLabel', age_labels, 'YDir', 'reverse');
xlabel('Population');
legend({'Initial year)', ['Final year']}, 'Location', 'best');
title('Initial vs Final Population by Age Group');
grid on;

