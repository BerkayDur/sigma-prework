from rich.console import Console
import random
from time import sleep, time
import msvcrt
import math
from collections import namedtuple

## ToDo:
## Fix error when non square map
## Maybe add a score
## Optimise as much as possible
## Maybe convert to a linked list??
## Randomly initialise inertia and snake spawn and tail

console = Console()

grid_size_def = 5
min_grid_size = 3
refresh_rate = 0.3

def main(x_grid_size=grid_size_def, y_grid_size=grid_size_def):
  if x_grid_size <=min_grid_size and y_grid_size <= min_grid_size:
    x_grid_size = grid_size_def
    y_grid_size = grid_size_def
    print(f"Grid size too small, defaulting to {x_grid_size}x{y_grid_size}")
  SnakePart = namedtuple("SnakePart", "x y type")

  snake, inertia, x_food, y_food = initialise_game(SnakePart, x_grid_size, y_grid_size)

  while True:
    # Output current game state
    gen_and_output_grid(snake, x_grid_size, y_grid_size, x_food, y_food)

    # Get direction
    inertia = get_input(refresh_rate, inertia)

    # Update Grid
    grow_snake = should_snake_grow(snake, x_food, y_food)
    snake = move_snake(snake, inertia, grow_snake, SnakePart)
    if grow_snake:
      x_food, y_food = generate_food(snake, x_grid_size, y_grid_size)
    
    # Verify game state
    game_state = verify_game_state(snake, x_grid_size, y_grid_size)
    match game_state:
      case 0:
        gen_and_output_grid(snake, x_grid_size, y_grid_size, x_food, y_food)
        print("You win!")
        break
      case 1:
        print("Game Over! Snake overlap!")
        break
      case 2:
        print("Game Over! Out of bounds!")
        break

def initialise_game(SnakePart, x_grid_size, y_grid_size):
  snake = [
    SnakePart(x_grid_size//2, y_grid_size//2, "h"),
    SnakePart(x_grid_size//2, y_grid_size//2 + 1, "t")
  ]
  x_food, y_food = generate_food(snake, x_grid_size, y_grid_size)
  inertia = 0
  return snake, inertia, x_food, y_food


def create_snake_set(snake):
  snake_set = set()
  for part in snake:
    snake_set.add((part.x, part.y))
  return snake_set


def generate_coordinates(x_grid_size, y_grid_size):
  return random.randint(0, x_grid_size-1), random.randint(0, y_grid_size-1)

def generate_food(snake, x_grid_size, y_grid_size):
  snake_set = create_snake_set(snake)
  while True:
    x_food, y_food = generate_coordinates(x_grid_size, y_grid_size)
    if (x_food, y_food) not in snake_set:
      return x_food, y_food
    elif verify_no_food_spawn(snake, x_grid_size, y_grid_size):
      return -1, -1

def verify_bound(val, lower_bound, upper_bound):
  return val >= lower_bound and val <= upper_bound

def verify_boundary_cross(snake, x_grid_size, y_grid_size):
  return not(verify_bound(snake[0].x, 0, x_grid_size-1) and verify_bound(snake[0].y, 0, y_grid_size-1))

def verify_snake_overlap(snake):
  snake_set = create_snake_set(snake)
  return len(snake_set) != len(snake)

def verify_no_food_spawn(snake, x_grid_size, y_grid_size):
  return len(snake) == x_grid_size * y_grid_size

def verify_game_state(snake, x_grid_size, y_grid_size):
  no_food_spawn = verify_no_food_spawn(snake, x_grid_size, y_grid_size)
  snake_overlap = verify_snake_overlap(snake)
  boundary_cross = verify_boundary_cross(snake, x_grid_size, y_grid_size)

  if no_food_spawn:
    return 0
  elif snake_overlap:
    return 1
  elif boundary_cross:
    return 2


def generate_grid(snake, x_grid_size, y_grid_size, x_food, y_food):
  grid = [["." for i in range(y_grid_size)] for i in range(x_grid_size)]
  grid[y_food][x_food] = "f"
  for part in snake:
    grid[part.y][part.x] = part.type
  return grid

def move_snake(snake, inertia, grow_snake, SnakePart):
  x, y = inertia_map(inertia)
  prev = SnakePart(snake[0].x+x, snake[0].y+y, None)
  
  for i, part in enumerate(snake):
    snake[i] = SnakePart(prev.x, prev.y, part.type)
    prev = part
  if grow_snake:
    snake[-1] = SnakePart(snake[-1].x, snake[-1].y, "b")
    snake.append(prev)
  return snake
    
def should_snake_grow(snake, x_food, y_food):
  return snake[0].x == x_food and snake[0].y == y_food


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

def gen_and_output_grid(snake, x_grid_size, y_grid_size, x_food, y_food):
  grid = generate_grid(snake, x_grid_size, y_grid_size, x_food, y_food)
  console.clear()
  console.print(map_grid_to_output(grid))

def calculate_direction_from_input(char):
  match char:
    case "w" : return 0
    case "d" : return 1
    case "s" : return 2
    case "a" : return 3
    case _: return -1


def get_input(duration, inertia):
  start = time()
  direction = -1
  while True:
    if time() - start > duration:
      if direction == -1:
        return inertia
      return direction
    elif msvcrt.kbhit():
      char = msvcrt.getwch()
      direction = calculate_direction_from_input(char)
      if char == "q":
        raise KeyboardInterrupt
      elif direction == -1:
        continue
      elif abs(direction - inertia) == 2:
        direction = -1
      

if __name__ == "__main__":
  main(8, 8)