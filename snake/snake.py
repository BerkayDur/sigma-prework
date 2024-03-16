from rich.console import Console
import random
from time import sleep, time
import msvcrt
import math
from collections import namedtuple

## ToDo:
## Make it so the food doesn't spawn under the snake (Thinking about using set for SnakeParts)
## Maybe add a score
## Refactor code
## Optimise as much as possible
## Maybe convert to a linked list??




SnakePart=namedtuple("SnakePart", "x y type")
console = Console()




x_grid_size, y_grid_size = 15, 15


snake = [SnakePart(5, 5, "h"), SnakePart(5, 6, "t")]
y_food, x_food = random.randint(0, y_grid_size-1), random.randint(0, x_grid_size-1)

inertia = 0

def generate_coordinates(x_grid_size, y_grid_size):
  return random.randint(0, x_grid_size-1), random.randint(0, y_grid_size-1)

def verify_bound(val, lower_bound, upper_bound):
  return val >= lower_bound and val <= upper_bound

def verify_boundary(snake):
  return verify_bound(snake[0].x, 0, x_grid_size-1) and verify_bound(snake[0].y, 0, y_grid_size-1)

def generate_grid(snake):
  grid = [["." for i in range(y_grid_size)] for i in range(x_grid_size)]
  grid[y_food][x_food] = "f"
  for part in snake:
    grid[part.y][part.x] = part.type
  return grid

def move_snake(snake, inertia, grow_snake):
  x, y = inertia_map(inertia)
  prev = SnakePart(snake[0].x+x, snake[0].y+y, None)
  
  for i, part in enumerate(snake):
    snake[i] = SnakePart(prev.x, prev.y, part.type)
    prev = part
  if grow_snake:
    snake[-1] = SnakePart(snake[-1].x, snake[-1].y, "b")
    snake.append(prev)
  return snake
    

def should_grow_snake(snake, x_food, y_food):
  if snake[0].x == x_food and snake[0].y == y_food:
    return True, *generate_coordinates(x_grid_size, y_grid_size)
  return False, x_food, y_food
  

def inertia_map(inertia):
  match inertia:
    case 0:
      return 0, -1
    case 1:
      return 1, 0
    case 2:
      return 0, 1
    case 3:
      return -1, 0

def map_grid_to_output(grid):
  maps = {
    "." : "[on white]⠀⠀[/]",
    "h" : "[on #276221]⠀⠀[/]",
    "b" : "[on green]⠀⠀[/]",
    "t" : "[on #acd8a7]⠀⠀[/]",
    "f" : "[on yellow]⠀⠀[/]"
  }
  layers = [[maps[i] for i in g] for g in grid]
  layers = ["".join(i) for i in layers]
  return "\n".join(layers)

def calculate_direction_from_input(char):
  match char:
    case "w" : return 0
    case "d" : return 1
    case "s" : return 2
    case "a" : return 3


def get_input(duration, inertia):
  start = time()
  direction = -1
  while True:
    if time() - start > duration:
      return direction
    elif msvcrt.kbhit():
      char = msvcrt.getwch()
      direction = calculate_direction_from_input(char)
      if abs(direction - inertia) == 2:
        direction = -1
      if char == "q":
        raise KeyboardInterrupt

while True:
  grid = generate_grid(snake)
  console.clear()
  console.print(map_grid_to_output(grid))

  direction = get_input(0.3, inertia)
  if direction != -1:
    inertia = direction

  grow_snake, x_food, y_food = should_grow_snake(snake, x_food, y_food)
  snake = move_snake(snake, inertia, grow_snake)

  if not verify_boundary(snake):
    print("Out of Bounds!")
    break