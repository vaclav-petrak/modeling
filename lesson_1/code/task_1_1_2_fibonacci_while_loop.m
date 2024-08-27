fib_seq = [1,1]; 
max_value = 5000;

%set index to 2
i = 2;

while (fib_seq(i) + fib_seq(i-1)) < max_value
    fib_seq(i+1) = fib_seq(i) + fib_seq(i-1);
    i = i + 1;
end

disp(fib_seq);