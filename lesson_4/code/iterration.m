% This script initializes a forest matrix and iteratively displays elements within a defined area.
% It shows how to access individual elements

clear, clc

% --- Initiate ---
area = 2;
iterations = 2;

forrest = [
0 2 1
1 1 0
0 0 1
];

% --- Iterate ---
for i = 1:iterations
   for row = 1:area
      for col = 1:area  
          display(forrest(row,col)));   
      end
   end
end