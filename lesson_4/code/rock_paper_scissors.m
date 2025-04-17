%Create grid
size = 200;
grid = randi(3,size);


%Find neighbourhoods
newgrid = grid;
for gen = 1:300
    for r = 2:size-1
        for c = 2:size -1
            neighbourhood = grid(r-1:r+1,c-1:c+1);
            %Create rules
            switch grid(r,c)
                case 1 %Cell: ROCK
                    if sum(neighbourhood(:) == 2) > 2 %Paper is winning
                        newgrid(r,c) = 2;
                    end
                case 2 %Cell: PAPER
                    if sum(neighbourhood(:) == 3) > 2 %Scissors are winning
                        newgrid(r,c) = 3;
                    end
                case 3 %Cell: SCISSORS
                    if sum(neighbourhood(:) == 1) > 2 %Rock is winning
                        newgrid(r,c) = 1;
                    end
            end            
        end
    end
    grid = newgrid;
    pause(0.01)
    imagesc(grid)
    colormap([1 0 0; 0 1 0; 0 0 1])
    axis square
end