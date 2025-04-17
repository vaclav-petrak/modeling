    % Parameters
    points = 2000;
    i = 100;  
    
    % Create a grid of complex numbers
    x = linspace(-2, 1, points);
    y = linspace(-1.5, 1.5, points);
    [X, Y] = meshgrid(x, y);
    C = X + 1i * Y;
    Z = zeros(size(C));
    divergence = zeros(size(C));


    % Set up the figure
    figure('Position', [100, 100, 1000, 1000]); 
    colormap("gray")
    axis equal;
    
    % Mandelbrot calculation
    for n = 1:i
        Z = Z.^2 + C;
        divergence(abs(Z) > 2) = 1;

        figure(1)
        imagesc(x, y, divergence);
    end
    

