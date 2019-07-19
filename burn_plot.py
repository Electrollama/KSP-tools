from matplotlib import pyplot as plt
from matplotlib import rcParams, rc
import matplotlib.ticker
from numpy import linspace
hf = 0
vf = 0
v_td = 10 #max touch-down velocity to prevent crashing, micro legs = 10 m/s
prevent_crash = True

x_maxpow = 5
y_maxpow = 3
y_minpow = 1

vel_basic = lambda a, d: (2*a*d + v_td**2)**0.5
if prevent_crash:
    vel = lambda a, d: min((2*a*(d-hf) + vf**2)**0.5, vel_basic(a, d))
else:
    vel = lambda a, d: (2 * a * (d - hf) + vf ** 2) ** 0.5
dist = lambda a, v: (v**2 - vf**2)/(2*a) + hf

def_size = rcParams['font.size']
fig_size = 5
fig = plt.figure(figsize=(fig_size*11/8.5, fig_size))
ax = plt.axes(xscale='log', yscale='log')
colors_bw = ['#000000', '#555555', '#AAAAAA']
colors_cb = ['#008a8a', '#621aab', '#c27b0a']
colors_rgb = ['b', 'g', 'r']
colors = colors_cb

def main():
    d_list = [10**m for m in linspace(1, x_maxpow, 100)]
    a_list = [0.5, 1, 2, 5, 10, 20, 50]

    rc('font', size=def_size*1.2)
    for i, acc in enumerate(a_list):
        vel_list = [vel(acc, d) for d in d_list]
        ax.plot(d_list, vel_list,
                color=colors[i%3], linestyle='-', lw=2.5, marker='', zorder=2)
        # write on border
        text_x = min(10 ** x_maxpow, dist(acc, 10 ** y_maxpow))
        text_y = min(10 ** y_maxpow, vel(acc, 10 ** x_maxpow))
        if acc >= 10:
            a_str = str(acc)
        else:
            a_str = '{} m/s\u00b2'.format(acc)
        plt.text(text_x, text_y, a_str, color=colors[i%3])
    rc('font', size=def_size)

    actual_d = []
    actual_v = []
    ax.plot(actual_d, actual_v, color='k', linestyle='-', lw=3.5,
            marker='o', ms=5, zorder=3)


    ax.set_xticks([10**m for m in range(1, 5)], minor=True)
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_yticks([10**m for m in range(y_minpow, 4)], minor=False)

    for power in range(1,x_maxpow+1):
        numbers = [1, 2, 5]
        widths = [2.0, 1.5, 1.5]
        styles = ['-', '--', '--']
        for i in range(3):
            plt.axvline(numbers[i]*10**power,
                        color=colors_bw[i], lw=widths[i], ls=styles[i], zorder=1)
            plt.axhline(numbers[i] * 10 ** power,
                        color=colors_bw[i], lw=widths[i], ls=styles[i], zorder=1)

    # time markers
    #t_mark = 3 #seconds
    #h_mark = [0.5 * a * t_mark**2 for a in a_list]
    #v_mark = [a * t_mark for a in a_list]
    #plt.plot(h_mark, v_mark, 'k*')

    # time labels
    for t in [1, 3, 5, 10, 30, 60, 2*60, 5*60, 10*60]:
        for i in range(len(a_list)):
            a = a_list[i]
            color = colors[i%3]
            if t >= 60:
                t_str = '{}m'.format(t//60)
            else:
                t_str = '{}s'.format(t)
            text_x, text_y = 0.5 * a * t ** 2, a * t
            if (text_x > 10 and text_x*1.5 < 10**x_maxpow
                and text_y > 10*1.2 and text_y < 10**y_maxpow):
                ax.text(text_x, text_y, t_str,
                        color=color, ha='left', va='top')

    # compensation compass


    ax.grid(False)
    ax.minorticks_on()
    ax.set_xlim(xmin=10, xmax=10**x_maxpow)
    ax.set_ylim(ymin=10, ymax=10**y_maxpow)
    title_str = 'Suicide Burn Descent Profile \n'#[h={} m, v{}{} m/s]'
    ax.set_title(title_str.format(round(hf),
                                  {0: '=', 1: '<'}[prevent_crash],
                                  round(vf)))
    ax.set_xlabel('Altitude [m]')
    ax.set_ylabel('Vertical speed [m/s]')


def compass():
    """
    Draw a "compass" to show slopes related to under-thrust or over-thrust while
    on a line.
    """
    x0, y0 = 50, 500
    comp_list = [-1, 0, 1, 2]
    x_lim_list = [2/3, 1/2, 7/12, 2/3] #where they intersect neighboring curves
    for i,comp in enumerate(comp_list):
        x_ratios = linspace(1, x_lim_list[i], 20)
        x_vals = [x0 * r for r in x_ratios]
        if comp < 1:
            color = colors[0]
        elif comp > 1:
            color = colors[1]
        else: # 1
            color=colors[2]
        y_vals = [(comp*(y0**2/x0)*(x-x0) + y0**2)**0.5 for x in x_vals]
        ax.plot(x_vals, y_vals, ls='-', marker='', color=color)
        ax.text(x_vals[-1], y_vals[-1], '{}x'.format(comp),
                va='center', ha='right', color=color)

main()
compass()
plt.show()