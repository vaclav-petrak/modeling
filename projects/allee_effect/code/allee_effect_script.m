%--- Model parameters and density vector
r = 0.5; % Intrinsic growth rate
K = 200; % Carrying capacity
A_strong = 60; % Strong effect threshold
N = linspace(0, K*1.05, 5000);
%--- Compute growth curves
growth_no = r * N .* (1 - N/K);
growth_weak = (r/K) * N.^2 .* (1 - N/K);
growth_strong = r * N .* (1 - N/K) .* (N/A_strong - 1);
%--- Plot all three curves
figure;
hold on
plot(N, growth_no, 'LineWidth', 2);
plot(N, growth_weak, 'LineWidth', 2);
plot(N, growth_strong, 'LineWidth', 2);
yline(0, 'k-', 'LineWidth', 1.5); 
title('Population Growth Models with Allee Effects');
xlabel('Population Density'); ylabel('dN/dt');
legend('No Allee Effect', 'Weak Allee Effect', 'Strong Allee Effect', 'Location', 'southeast');
xlim([0, K*1.1])
hold off
