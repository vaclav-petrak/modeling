import random


def update_position(x: int, y: int, area: int) -> tuple[int, int]:
    direction = random.randint(1, 4)
    if direction == 1:
        if y < area:
            y += 1
    elif direction == 2:
        if y > 0:
            y -= 1
    elif direction == 3:
        if x > 0:
            x -= 1
    else:
        if x < area:
            x += 1
    return x, y
