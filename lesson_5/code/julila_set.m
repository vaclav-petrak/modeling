   
    % Parameters
    points = 1000;
    i = 10; 

    % figure settings
    figure('Position', [100, 100, 1000, 1000]); 
    colormap([flipud(jet); 0 0 0]);  
    axis equal;

    % grid of complex numbers
    x = linspace(-2, 2, points);
    y = linspace(-2, 2, points);
    [real, complex] = meshgrid(x, y);
    C = real + complex * 1i;
    
    Z = C ;
    escape_time = zeros(size(C));
      
 
    % Mandelbrot calculation
    for n = 1:i
         % checks which points remain bounded 
        bounded = abs(Z) <= 2;
       
        % iterates bounded points
        Z(bounded) = Z(bounded).^2;

        % add time to bounded points
        escape_time(bounded) = escape_time(bounded) + 1;
        figure(1)
        imagesc(x, y, escape_time);

        pause(0.5)

    end
    