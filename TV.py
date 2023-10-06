import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

# Define parameters
Lx = 1.0  # Length of the room in the x-direction (meters)
Ly = 1.0   # Length of the room in the y-direction (meters)
Nx = 50   # Number of grid points in the x-direction
Ny = 50    # Number of grid points in the y-direction
D = 10e-5   # Diffusion coefficient (m^2/s)

# # Zero Velocity Field
# u, v = 0, 0

# # Constant Velocity Field
# u, v = 0.001, 0.001

# Constant Tilted Velocity Field
u = 0.001 * np.cos(np.pi/4)    # Horizontal airflow velocity (m/s)
v = 0.001 * np.sin(np.pi/4)  # Vertical airflow velocity (m/s)


x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x, y)

delta_x = Lx / Nx
delta_y = Ly / Ny
delta_t = 0.1 
t_simulation = 100.0
num_time_steps = int(t_simulation / delta_t)

C = np.zeros((Nx, Ny))

# Initial condition (a point source at the center)
C[Nx//4, Ny//4] = 100.0
C[3*Nx//4, 3*Ny//4] = 75.0
C[2*Nx//3, Ny//3] = 150.0


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

Concentration_snapshots = []

for step in range(num_time_steps):
    C_new = C.copy()
    # Finite difference calculations for interior grid points
    for i in range(1, Nx - 1):
        for j in range(1, Ny - 1):
            C_new[i, j] = C[i, j] + D * delta_t * (
                (C[i+1, j] - 2 * C[i, j] + C[i-1, j]) / delta_x**2 +
                (C[i, j+1] - 2 * C[i, j] + C[i, j-1]) / delta_y**2) - u * delta_t * (C[i + 1, j] - C[i, j])/delta_x
            - v * delta_t * (C[i, j + 1] - C[i, j])/delta_y
    C = C_new
    Concentration_snapshots.append(C.copy())

## Velocity Field
plt.figure()
plt.quiver(X, Y, u* np.ones_like(X), v* np.ones_like(Y), scale=20, color = 'b', width=0.005)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Tilted Velocity Field')
plt.axis((0, Lx, 0, Ly))
# plt.savefig("0TV.png")
plt.grid()
plt.show()

# # Visualization of concentration evolution over time with constant concentration axis scaling
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

trail = np.zeros((num_time_steps//10, 3))
for i, conc_snapshot in enumerate(Concentration_snapshots):
    if i % 10 == 0:
        ax.clear()
        surf = ax.plot_surface(X, Y, conc_snapshot.T, cmap='inferno')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Concentration')
        ax.set_title(f'Concentration Distribution at Time Step {i} -> Convection-Diffusion')
        ax.set_xlim(0, Lx)
        ax.set_ylim(0, Ly)
        ax.set_zlim(0, 1.0)
        arr = conc_snapshot
        rows, cols = np.unravel_index(np.argmax(arr), arr.shape)
        trail[i//10, 0], trail[i//10, 1], trail[i//10, 2] = rows * Lx/Nx, cols * Ly/Ny, np.max(conc_snapshot)
        ax.scatter(trail[:, 0][:i//10], trail[:, 1][:i//10], trail[:, 2][:i//10], color = "green", marker = ".", linestyle = "--")
        plt.pause(0.000001) 
        # if i % 100 == 0:
        #     filename = os.path.join("/Users/guntas13/Desktop/JetBrains Projects/MA203_Project", f'concentration_step_T_{i//100:04d}.png')
        #     plt.savefig(filename, dpi=300)
        
# plt.savefig("1TV.png")
plt.show()


plt.figure(figsize = (8, 6))
plt.contourf(X, Y, Concentration_snapshots[0].T, cmap = "inferno")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Intial Condition of Spillage")
plt.colorbar()
# plt.savefig("2ZV.png")
plt.show()

arr = Concentration_snapshots[num_time_steps//2]
rows, cols = np.unravel_index(np.argmax(arr), arr.shape)
tx, ty = rows * Lx/Nx, cols * Ly/Ny
plt.figure(figsize = (8, 6))
plt.contourf(X, Y, Concentration_snapshots[num_time_steps//2].T, cmap = "inferno")
eq = rf"({tx}, {ty})"
plt.text(tx+0.001, ty+0.001, eq, {'color': 'black', 'fontsize': 12})
plt.plot(tx, ty, color = "black", marker = "o")
plt.plot(tx, ty)
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Intermediate Situation in Tilted Velocity Field")
plt.colorbar()
# plt.savefig("3TV.png")
plt.show()

arr = Concentration_snapshots[-1]
rows, cols = np.unravel_index(np.argmax(arr), arr.shape)
tx, ty = rows * Lx/Nx, cols * Ly/Ny
plt.figure(figsize = (8, 6))
plt.contourf(X, Y, Concentration_snapshots[-1].T, cmap = "inferno")
eq = rf"({tx}, {ty})"
plt.text(tx+0.001, ty+0.001, eq, {'color': 'black', 'fontsize': 12})
plt.plot(tx, ty, color = "black", marker = "o")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Final Concentration in Tilted Velocity Field")
plt.colorbar()
# plt.savefig("4TV.png")
plt.show()