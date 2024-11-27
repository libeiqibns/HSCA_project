import numpy as np
import matplotlib.pyplot as plt

# Define the x values from -8 to 0
x_values = np.linspace(-8, 0, 500)  # Fine granularity for smooth curve

# Define the function 2^x
y_values = 2 ** x_values

# Plot the graph
plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values, label=r"$2^x$", linewidth=2)

# # Define the range of x values for shading
# x_shaded0 = np.linspace(-1/8, 0, 200)
# y_shaded0 = 2 ** x_shaded0
# plt.fill_between(x_shaded0, y_shaded0, color="lightskyblue", alpha=0.5, label="$x = -1/8$ to $x = 0$")
# x_shaded1 = np.linspace(-1/4, -1/8, 200)
# y_shaded1 = 2 ** x_shaded1
# plt.fill_between(x_shaded1, y_shaded1, color="skyblue", alpha=0.5, label="$x = -1/4$ to $x = -1/8$")
# x_shaded = np.linspace(-1/2, -1/4, 200)
# y_shaded = 2 ** x_shaded
# plt.fill_between(x_shaded, y_shaded, color="deepskyblue", alpha=0.5, label="$x = -1/2$ to $x = -1/4$")
# x_shaded = np.linspace(-1, -1/2, 200)
# y_shaded = 2 ** x_shaded
# plt.fill_between(x_shaded, y_shaded, color="lightblue", alpha=0.5, label="$x = -1$ to $x = -1/2$")
# x_shaded = np.linspace(-2, -1, 200)
# y_shaded = 2 ** x_shaded
# plt.fill_between(x_shaded, y_shaded, color="powderblue", alpha=0.5, label="$x = -2$ to $x = -1$")
# x_shaded = np.linspace(-4, -2, 200)
# y_shaded = 2 ** x_shaded
# plt.fill_between(x_shaded, y_shaded, color="cadetblue", alpha=0.5, label="$x = -4$ to $x = -2$")
# x_shaded = np.linspace(-8, -4, 200)
# y_shaded = 2 ** x_shaded
# plt.fill_between(x_shaded, y_shaded, color="darkturquoise", alpha=0.5, label="$x = -8$ to $x = -4$")

# Add labels, title, and grid
plt.title("Graph of $2^x$", fontsize=14)
plt.xlabel("x", fontsize=12)
plt.ylabel("$2^x$", fontsize=12)
plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
plt.axvline(0, color="black", linewidth=0.5, linestyle="--")
plt.grid(alpha=0.3)
plt.legend(fontsize=12)
plt.tight_layout()

# Show the plot
plt.show()
