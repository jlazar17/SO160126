# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# set params
stride = 16384
stride_start = -2
stride_end = 6
print u'loading the array (get some coffee, this could take a while☕️ ☕️ 😐 )'

# function for loading the array
def load_time_slice(fname, stride, stride_start, stride_end):
    i = 0
    a = []
    with open(fname) as f:
        # handle negative start differently; will either be at end or at beginning
        if stride_start < 0:
            for line in f:
                stride_start_mod = stride_start + stride
                if i % stride >= stride_start_mod or i % stride < stride_end:
                    a.append(float(line))
                i += 1
        else:
            for line in f:
                if i % stride >= stride_start and i % stride < stride_end:
                    a.append(float(line))
                i += 1
    print u'done loading 😂 😂 🙌 🙌 🙏 '
    l = len(a)
    n = l/(stride_end - stride_start)
    if l % (stride_end - stride_start) != 0:
        print 'the loaded array:'
        print a
        raise ValueError('length of array ' + str(l) + ' must be divisible by subsample length ' + str(stride_end-stride_start) + '.')
    print 'reshaping... '
    if stride_start < 0:
        print 'stride start is negative, removing one of the lines...'
        n -= 1
        b = np.array( a[stride_end:l+stride_start] ).reshape(n, stride_end - stride_start)
    else:
        b = np.array( a ).reshape(n, stride_end - stride_start)
    print 'done. ✂️ 📐 🚬 ☕️ 🚿 '
    return b

b = load_time_slice('l-dtone.dat', stride, stride_start, stride_end)

# find the t-axis in microseconds.
# TODO: Make methods for finding the t-axis for these repeated graphs
t = 1e6 * np.arange( stride_start, stride_end ) / float(stride)


print 'calculating mean, standard dev, mins and maxes...'
m = np.mean(b, 0)
s = np.std(b, 0)
d = m - np.min(b, 0)
u = np.max(b, 0) - m

print 'done.\n'
print 'mean:'
print m
print 'standard deviation:'
print s
print 'error, lower:'
print d
print 'error, upper:'
print u
print '\n'

def t_axis():
    t = np.arange( stride_start, stride_end ) / float(stride)
    return t

print 'almost finished, making some plots: 📈 📉 📊 🔭 '
def plot(ax):
    ax.close()
    title = 'Mean DuoTone Signal, Livingston EX, near Zero Crossing\nwith Max/Min Values and Std. Dev.'
    fname = 'l-ex-dtone'
    print 'plotting ' + fname + ' and saving...'
    # first figure
    ax.figure(1)
    ax.plot(t, m, 'k')
    # ax.plot(t, np.zeros(len(t)), 'k')
    ax.errorbar(t, m, yerr=[d, u], fmt='k')
    ax.errorbar(t, m, yerr=s, fmt='go', linewidth=4)
    ax.title(title)
    ax.xlabel(r'Time since start of second ($\mu s$)')
    ax.ylabel('Signal Voltage')
    ax.grid(b=True, which='major', color='#262626', linestyle='--')
    ax.savefig(fname + '.png')
    # second, zoomed figure
    ax.figure(2)
    ax.plot(t, m, 'k')
    # ax.plot(t, np.zeros(len(t)), 'k')
    ax.errorbar(t, m, yerr=[d, u], fmt='k')
    ax.errorbar(t, m, yerr=s, fmt='go', linewidth=4)
    ax.title(title)
    ax.xlabel(r'Time since start of second ($\mu s$)')
    ax.ylabel('Signal Voltage')
    ax.xlim(61, 63.5)
    ax.ylim(-70, 30)
    ax.grid(b=True, which='major', color='#262626', linestyle='--')
    ax.savefig(fname + '-zoom.png')
    # third, very zoomed figure
    ax.figure(3)
    ax.plot(t, m, 'k')
    # ax.plot(t, np.zeros(len(t)), 'k')
    ax.errorbar(t, m, yerr=[d, u], fmt='k')
    ax.errorbar(t, m, yerr=s, fmt='go', linewidth=4)
    ax.title(title)
    ax.xlabel(r'Time since start of second ($\mu s$)')
    ax.ylabel('Signal Voltage')
    ax.xlim(61, 61.1)
    ax.ylim(-64, -54)
    ax.grid(b=True, which='major', color='#262626', linestyle='--')
    ax.savefig(fname + '-super-zoom.png')

plot(plt)
print 'done! 🎉 🎊 🎈 '
