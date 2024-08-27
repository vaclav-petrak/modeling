function fib_seq = generate_fibonacci(n)
fib_seq = [1, 1]; 
    
for i = 3:n
    fib_seq(i) = fib_seq(i-1) + fib_seq(i-2);
end
  
fib_seq = fib_seq(1:n); %subset the result
end