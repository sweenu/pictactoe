from sense_hat import SenseHat

s = SenseHat()

green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
nothing = (0, 0, 0)
pink = (255, 105, 180)


def grid():
    W = white
    N = nothing
    grid = [
    N, N, W, N, N, W, N, N,
    N, N, W, N, N, W, N, N,
    W, W, W, W, W, W, W, W,
    N, N, W, N, N, W, N, N,
    N, N, W, N, N, W, N, N,
    W, W, W, W, W, W, W, W,
    N, N, W, N, N, W, N, N,
    N, N, W, N, N, W, N, N,
    ]
    return grid


s.set_pixels()
