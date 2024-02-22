import matplotlib.pyplot as plt

center = -0.05 - 0.66j
range_ = 0.9 + abs(center)
max_iterations = 100

x1, y1 = -1.5, -1
x2, y2 = 1.5, 1
linearResolution = 500

M, N = int((y2 - y1) * linearResolution), int((x2 - x1) * linearResolution)

xcoordinates = [(x1 + ((x2 - x1) / N) * i) for i in range(N)]
ycoordinates = [(y1 + ((y2 - y1) / M) * i) for i in range(M)]

juliaSet = [[None for i in xcoordinates] for j in ycoordinates]

for y in range(len(ycoordinates)):
    for x in range(len(xcoordinates)):
        z = complex(xcoordinates[x], ycoordinates[y])
        iteration = 0
        while (abs(z) < range_ and iteration < max_iterations):
            iteration += 1
            z = z ** 2 + center

        if (iteration == max_iterations):
            juliaSet[y][x] = 0
        else:
            juliaSet[y][x] = iteration

ax = plt.axes()
ax.set_aspect('equal')
plot = ax.pcolormesh(xcoordinates, ycoordinates, juliaSet, cmap='magma')
plt.colorbar(plot)
plt.title('Julia-set \ncenter = {}, range = {:.3f}, max-iterations = {}'.format(center, range_, max_iterations))  # setting title
plt.show()