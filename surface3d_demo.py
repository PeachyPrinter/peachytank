from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from math import tan, atan, pi


def get_rps(height_of_laser, edge_from_center_of_base, speed_mm_per_s):
    radians_from_center = atan(edge_from_center_of_base / height_of_laser)
    time_to_center = edge_from_center_of_base / speed_mm_per_s
    rad_per_sec = radians_from_center / time_to_center
    rps = rad_per_sec * 2.0 * pi
    return rps


def base_at_height(height, radian):
    return tan(radian) * height


@np.vectorize
def glue(height, speed_mm_per_s):
    base = base_at_height(height, pi / 8)
    rps = get_rps(height, base, speed_mm_per_s)
    return rps

fig = plt.figure()
ax = fig.gca(projection='3d')
Height = np.linspace(50.0, 2500.0)
Speed = np.linspace(200.0, 600.0, num=2)
Height, Speed = np.meshgrid(Height, Speed)
RPM = glue(Height, Speed)
surf = ax.plot_surface(Speed, RPM, Height, rstride=1, cstride=1, cmap=cm.PRGn, linewidth=0, antialiased=False)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.set_xlabel('Speed')
ax.set_ylabel('RPS')
ax.set_zlabel('Height')

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

