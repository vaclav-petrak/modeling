forest = [
    [0, 2, 1],
    [1, 1, 0],
    [0, 0, 1],
]

area = 2
iterations = 2

for _ in range(iterations):
    for row in range(area):
        for col in range(area):
            print(forest[row][col])
