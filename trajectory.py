import math
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation as Animation
from functools import partial

# constants
GRAVITY = 9.81           # m/s^2
AIR_DENSITY = 1.2        # kg/m^3
TIME_STEP = 0.01         # s

# ball parameters
MASS = 0.43              # kg
RADIUS = 0.11            # m
LINEAR_RESISTANCE_COEFFICIENT = 0.5 
QUADRATIC_RESISTANCE_COEFFICIENT = 0.25 

# speed and angle of the kick
speed = 40.0      # m/s
angle = 20.0      # degrees

# trajectory without resistance
def no_resistance(vx, vy):
    x = 0.0 
    y = 0.0       
    time = 0.0

    x_values = [x]
    y_values = [y]

    while y >= 0:
        x = x + vx * TIME_STEP
        y = y + vy * TIME_STEP

        vy = vy - GRAVITY * TIME_STEP

        time = time + TIME_STEP

        x_values.append(x)
        y_values.append(y)

    return x_values, y_values

# trajectory with linear resistance
def linear_resistance(vx, vy):
    x = 0.0
    y = 0.0
    time = 0.0

    x_values = [x]
    y_values = [y]

    while y >= 0:
        ax = -(LINEAR_RESISTANCE_COEFFICIENT / MASS) * vx
        ay = -GRAVITY - (LINEAR_RESISTANCE_COEFFICIENT / MASS) * vy

        vx = vx + ax * TIME_STEP
        vy = vy + ay * TIME_STEP

        x = x + vx * TIME_STEP
        y = y + vy * TIME_STEP

        time = time + TIME_STEP

        x_values.append(x)
        y_values.append(y)

    return x_values, y_values

# trajectory with quadratic resistance
def quadratic_resistance(vx, vy):
    area = math.pi * RADIUS**2

    x = 0.0
    y = 0.0
    time = 0.0

    x_values = [x]
    y_values = [y]

    while y >= 0:

        v = math.sqrt(vx**2 + vy**2)

        ax = -((AIR_DENSITY * QUADRATIC_RESISTANCE_COEFFICIENT * area) / (2 * MASS)) * v * vx
        ay = -GRAVITY - ((AIR_DENSITY * QUADRATIC_RESISTANCE_COEFFICIENT * area) / (2 * MASS)) * v * vy

        vx = vx + ax * TIME_STEP
        vy = vy + ay * TIME_STEP

        x = x + vx * TIME_STEP
        y = y + vy * TIME_STEP

        time = time + TIME_STEP

        x_values.append(x)
        y_values.append(y)

    return x_values, y_values

# compute velocities
angle_in_radians = math.radians(angle)

vx = speed * math.cos(angle_in_radians)
vy = speed * math.sin(angle_in_radians)

# compute trajectories
x_values_no_resistance, y_values_no_resistance = no_resistance(vx, vy)
x_values_linear_resistance, y_values_linear_resistance = linear_resistance(vx, vy)
x_values_quadratic_resistance, y_values_quadratic_resistance = quadratic_resistance(vx, vy)

x_max = max(max(x_values_no_resistance), max(x_values_linear_resistance), max(x_values_quadratic_resistance))
y_max = max(max(y_values_no_resistance), max(y_values_linear_resistance), max(y_values_quadratic_resistance))
max_length = max(len(x_values_no_resistance), len(x_values_linear_resistance), len(x_values_quadratic_resistance))

# create animation
fig, ax = plot.subplots()

ax.set_title("Soccer ball trajectories")
ax.set_xlabel("Distance (m)")
ax.set_ylabel("HEIGHT (m)")

ax.set_xlim(0, x_max * 1.1)
ax.set_ylim(0, y_max * 1.1)

traj_no, = ax.plot([], [], 'b-', lw=2, label='No resistance')
traj_lin, = ax.plot([], [], 'g-', lw=2, label='Linear resistance')
traj_quad, = ax.plot([], [], 'r-', lw=2, label='Quadratic resistance')

ball_no, = ax.plot([], [], 'bo', markersize=8)
ball_lin, = ax.plot([], [], 'go', markersize=8)
ball_quad, = ax.plot([], [], 'ro', markersize=8)

ax.legend()

def update(frame):
    # no resistance
    last_no = min(frame, len(x_values_no_resistance) - 1)

    traj_no.set_data(
        x_values_no_resistance[:last_no + 1],
        y_values_no_resistance[:last_no + 1]
    )

    ball_no.set_data(
        [x_values_no_resistance[last_no]],
        [y_values_no_resistance[last_no]]
    )

    # linear resistance
    last_lin = min(frame, len(x_values_linear_resistance) - 1)

    traj_lin.set_data(
        x_values_linear_resistance[:last_lin + 1],
        y_values_linear_resistance[:last_lin + 1]
    )

    ball_lin.set_data(
        [x_values_linear_resistance[last_lin]],
        [y_values_linear_resistance[last_lin]]
    )

    # quadratic resistance
    last_quad = min(frame, len(x_values_quadratic_resistance) - 1)

    traj_quad.set_data(
        x_values_quadratic_resistance[:last_quad + 1],
        y_values_quadratic_resistance[:last_quad + 1]
    )

    ball_quad.set_data(
        [x_values_quadratic_resistance[last_quad]],
        [y_values_quadratic_resistance[last_quad]]
    )

    return (
        traj_no, ball_no,
        traj_lin, ball_lin,
        traj_quad, ball_quad
    )

animation = Animation(
    fig,
    update,
    frames=max_length,
    interval=20,
    blit=True
)

plot.grid(True)
plot.show()
