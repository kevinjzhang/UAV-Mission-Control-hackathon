import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D

import parse

# colours
colours = ['xkcd:purple', 'xkcd:green', 'xkcd:blue', 'xkcd:pink',
           'xkcd:brown', 'xkcd:red', 'xkcd:light blue', 'xkcd:teal',
           'xkcd:orange', 'xkcd:light green', 'xkcd:magenta',
           'xkcd:yellow', 'xkcd:grey', 'xkcd:light purple',
           'xkcd:dark green', 'xkcd:tan', 'xkcd:cyan', 'xkcd:beige',
           'xkcd:hot pink', 'xkcd:pumpkin']

# plot points coloured by field
def show_plot(fields, plot_3d, dot_size):
    colour = 0

    if plot_3d:
        f_3d = Axes3D(plot.figure())

    for field, rows in fields.items():
        lats = [row[0] for row in rows]
        longs = [row[1] for row in rows]
        alts = [row[2] for row in rows]
        
        if not plot_3d:
            plot.scatter(longs, lats, s=dot_size,
                         c=colours[colour], label=field)
            # plot.legend()
        else:
            f_3d.scatter(longs, lats, alts, s=dot_size,
                         c=colours[colour], label=field)
            # f_3d.legend()
        colour += 1

    plot.show()

# run module
def run(file, plot_3d, dot_size):
    _, fields = parse.run(file)
    show_plot(fields, plot_3d, dot_size)

if __name__ == "__main__":
    run("poi.csv", True, 10)
