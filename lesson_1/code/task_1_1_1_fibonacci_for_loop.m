% require element count
n = 20;    

% 1st and 2nd elements are 0 and 1
fib_seq = [1,1]; 

for i = 3:n
    fib_seq(i) = fib_seq(i-1) + fib_seq(i-2);
end

disp(fib_seq)