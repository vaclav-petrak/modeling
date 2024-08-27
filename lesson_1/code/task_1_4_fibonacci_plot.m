% require element count
n = 20;
% 1 st and 2 nd elements are 0 and 1
fib_seq = [1 ,1];
for i = 3: n
fib_seq ( i ) = fib_seq (i -1) + fib_seq (i -2) ;
end

fib_seq_15 = fib_seq(1:15)
plot(fib_seq_15)

ratio = fib_seq_15(2:end)./fib_seq_15(1:end-1);
display(ratio)
plot(ratio, '-s')