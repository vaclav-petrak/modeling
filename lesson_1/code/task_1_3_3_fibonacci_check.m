function is_fibonacci = check_fibonacci(input)
    % initialize the first two Fibonacci numbers
    a = 1; b = 1;
    
    % keep generating Fibonacci numbers until 
    % we exceed input value
    while b < input
        memomory = b; % memorize b
        b = a + b;    
        a = memomory;  % a is recalled from memory
    end
        
    % true if we found an exact match
    is_fibonacci = (b == input); 
end