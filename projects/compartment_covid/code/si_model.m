% Parameters
beta = 0.3;       % infection rate
N = 1000;         % total population
I0 = 1;           % initial number of infected individuals
S0 = N - I0;      % initial number of susceptible individuals
t_max = 60;      % duration of simulation (days)
dt = 0.1;         % time step

% Time vector
t = 0:dt:t_max;
num_steps = length(t);

% Initialize S and I arrays
S = zeros(1, num_steps);
I = zeros(1, num_steps);

% Set initial values
S(1) = S0;
I(1) = I0;

% Simulation loop 
for i = 2:num_steps
    dS = -beta * S(i-1) * I(i-1) / N;
    dI = -dS;  % because S + I = N

    S(i) = S(i-1) + dS * dt;
    I(i) = I(i-1) + dI * dt;
end

% Plot results
plot(t, S, 'b', 'LineWidth', 2);
hold on;
plot(t, I, 'r', 'LineWidth', 2);
xlabel('Time (days)'); ylabel('Number of individuals');
legend('Susceptible', 'Infected');
title('SI Model Simulation');
