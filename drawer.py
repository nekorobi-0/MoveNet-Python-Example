import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
def draw(x,y,z):
    ax.clear()
    ax.set_xlabel("x")
    ax.set_ylabel("z")
    ax.set_zlabel("y")
    ax.scatter(x,z,y)
    plt.pause(0.001)
if __name__ == "__main__":
    import random
    while True:
        x = [random.randint(0,100) for i in range(100)]
        y = [random.randint(0,100) for i in range(100)]
        z = [random.randint(0,100) for i in range(100)]
        draw(x,y,z)
    plt.show()