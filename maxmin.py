def maxmin(iter):
  mx, mn = iter[0], iter[0]
  for v in iter:
    if v > mx:
      mx = v
    elif v < mn:
      mn = v
  return [mn, mx]

if __name__ == "__main__":
	print(maxmin([2, 4, 1, 0, 2, -1]))
	print(maxmin([20, 50, 12, 6, 14, 8]))
	print(maxmin([100, -100]))
