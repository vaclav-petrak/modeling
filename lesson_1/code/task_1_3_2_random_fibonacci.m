function random_fib = random_fibonacci(n)
    fib_seq = [1, 1]; 
    for i = 3:n
        fib_seq(i) = fib_seq(i - 1) + fib_seq(i - 2);
    end

    fib_seq = fib_seq(1:n); %subsetting 

    % Choose a random index within the range
    random_index = randi([1, n]);  % For integer index

    % Return the random Fibonacci number
    random_fib = fib_seq(random_index);
end