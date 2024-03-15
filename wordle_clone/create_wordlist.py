import pathlib
import sys
from string import ascii_letters

if len(sys.argv) == 4:
  try:
    word_length = int(sys.argv[1])

    if word_length == 0:
      raise Exception("You entered 0, should be an integer greater than 0.")
  except ValueError:
    print("You didn't enter an integer, default to 5.")
    word_length = 5
  except Exception:
    print("You entered 0, default to 5.")
    word_length = 5

  in_path = pathlib.Path(sys.argv[2])
  out_path = pathlib.Path(sys.argv[3])

  words = sorted(
    {
      word.lower()
      for word in in_path.read_text(encoding="utf-8").split()
      if len(word) == word_length and all(letter in ascii_letters for letter in word)
    },
    key=lambda word: (len(word), word),
  )
elif len(sys.argv) == 3:

  in_path = pathlib.Path(sys.argv[1])
  out_path = pathlib.Path(sys.argv[2])

  words = sorted(
    {
      word.lower()
      for word in in_path.read_text(encoding="utf-8").split()
      if all(letter in ascii_letters for letter in word)
    },
    key=lambda word: (len(word), word),
  )
else:
  raise Exception("You didn't pass the correct number of arguments.")


out_path.write_text("\n".join(words))