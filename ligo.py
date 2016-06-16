# you can run this file by starting up python and typing `run ligo.py`
# (assuming you are in the same folder as this file)
print('Setting up ligo convenience functions...')
print('\n    (This script assumes you have GWpy and NDS2 installed)\n')

# import my human-readable channel names
import channels as ch

# import nds2 for fetching data
import nds2

# import numerical and plotting tools
import matplotlib.pyplot as plt
import numpy as np

### FOR GWPY EQUIPPED COMPUTERS ONLY
# import GWpy stuff
import gwpy as g
from gwpy.time import tconvert as tcon
from gwpy.timeseries import TimeSeries as TS
from gwpy.plotter import TimeSeriesPlot as TSPlot
from gwpy.detector import Channel as Ch

### FOR CLUSTER ONLY
# Force matplotlib to not use any Xwindows backend. NECESSARY ON CLUSTER.
# import matplotlib
# matplotlib.use('Agg')
import os

# functions for connecting
def connl():
    return nds2.connection('nds.ligo-la.caltech.edu', 31200)

def connh():
    return nds2.connection('nds.ligo-wa.caltech.edu', 31200)

# THIS TIME CONVERTER USES GWPY (HENCE ASTROPY)
# def tcons(str=""):
    # return tcon(str).gpsSeconds

# THIS TIME CONVERTER USES LALAPPS_TCONVERT, IS BETTER FOR PCDEV1
def tcons(str=""):
    return int(os.popen("lalapps_tconvert " + str).read())

# THIS CODE DOESN'T WORK AND IS BASED ON MY PAST IGNORANCE OF FRAME FILE STRUCTURE
# def tcons60(str):
#     t = tcons(str)
#     return t - t % 60

# a function for just plotting to a subplot
def plot_to_subplot(t, x, n_subplots, buffer_index=1, options={'plot_style': 'k'}):
    # merge user options
    default_options = {'plot_style': 'k'}
    default_options.update(options)
    options = default_options
    plt.subplot(n_subplots, 1, buffer_index+1)
    plt.plot(t, x, options['plot_style'])

# wrapper for maintaining compatibility with old scripts
def plot_overlay(data, stride, stride_time, fig_num, stride_intervals=None, options=None):
    handle_segment(data, stride, plot_to_subplot, {'fig_num': fig_num, 'stride_time': stride_time, 'stride_intervals': stride_intervals})

# define a function for overlaying repetitive functions
def handle_segment(data, stride, segment_handler, options={}):
    # Provide data (array-like), stride (int), segment_handler (function), and options.

    # define options; can, of course, specify extra ones
    default_options = {
        'fig_num': 1,
        'stride_intervals': [0, stride],
        'stride_time': 1
    }
    default_options.update(options)
    options = default_options

    # extract variables from the options
    fig_num = options['fig_num']
    stride_intervals = options['stride_intervals']
    stride_time = options['stride_time']

    # make sure we're getting an even number of segments
    if np.size(data) % stride != 0:
        raise ValueError('data.length % stride != 0; non-integer number of overlays!')
    if len(stride_intervals) % 2 !=0:
        raise ValueError('you have to provide pairs of stride start and end values!')

    # number of repeating time intervals considered
    n_subplots = len(stride_intervals) / 2
    # number of segments to overlay
    data_length = np.size(data)
    n = data_length / stride
    plt.figure(fig_num)
    # add each of them to the plot
    for i in xrange(n):
        for j in xrange(n_subplots):

            # find start and end of each stride
            stride_start = stride_intervals[2*j]
            stride_end = stride_intervals[2*j+1]
            if stride_start > stride_end:
                raise ValueError('your stride_end has to be after your stride_start!')
            if stride_start <= -stride:
                raise ValueError("you can't peer THAT far back; stride_start must be greater than negative stride")

            # find the start and end indices for each stride
            start = i * stride + stride_start
            end = i * stride + stride_end

            # find the t-axis
            t = np.arange( stride_start, stride_end ) * float(stride_time) / float(stride)

            # if the start and the end are within the overall window, plot away
            if start >= 0 and end <= data_length:
                segment = data[start:end]
                # PLOT-RELATED: t, n_subplots, buffer_index, segment, options
                segment_handler(t, segment, n_subplots, j, options)

# iteratively fetch channels and plot/save them
def iterative_fetch_save_and_plot(start, end, conn, channels, stride, stride_intervals=None, titles=None, generatePlots=True, saveData=True, error_bars=False, width=24, height_per_plot=4, plot_style="k", dpi=100):

    # check for bad input
    if stride_intervals is None:
        stride_intervals = [0, stride]
    if len(stride_intervals) % 2 !=0:
        raise ValueError('you have to provide pairs of stride start and end values!')
    if titles is None:
        titles = channels
    if len(channels) != len(titles):
        raise ValueError('must have same number of channels and titles!')

    # generate full titles for the filenames and super titles
    full_titles = []
    for i in xrange(len(titles)):
        full_titles.append(titles[i] + ' from ' + start + ' to ' + end)
    s = tcons(start)
    e = tcons(end)

    # clear the plot variable
    plt.close('all')

    # make the figures the correct size
    n_subplots = len(stride_intervals) / 2
    title_height = 2.4
    height = n_subplots * height_per_plot + title_height
    for i in range(len(channels)):
        plt.figure(num=i, figsize=(width, height))

    # iteratively fetch and plot the data
    print 'fetching buffers...'
    seconds_per_query = 60
    num_queries = int( np.ceil( float(e-s) / seconds_per_query ) )
    current_step = 1
    for bufs in conn.iterate(s, e, seconds_per_query, channels):
        print 'retrieved buffer ' + str(current_step) + ' of ' + str(num_queries) + ':'
        current_step += 1
        print bufs
        # if there are multiple channels, plot each
        for i in range(len(channels)):
            # plot the data
            if generatePlots:
                print 'generating plots...'
                plot_overlay(bufs[i].data, stride, 1, i, stride_intervals)
            # save this data to a file
            if saveData:
                print 'saving data...'
                with open(full_titles[i] + '.dat', 'a') as file:
                    np.savetxt(file, bufs[i].data)
            print 'done with this buffer.'

    # when finished, check if we need to add error bars...
    print "done fetching."
    # ...and then save the figures.
    print "saving figures..."
    for i in range(len(channels)):
        plt.figure(num=i, dpi=dpi)
        plt.suptitle(titles[i] + '\n' + start + ' to ' + end, fontsize=40)
        plt.tight_layout()
        plt.subplots_adjust(top=(1. - title_height/height))
        plt.savefig(full_titles[i] + '.png')
        print 'saved ' + full_titles[i] + '.png'
    print "done."

    # then, finally, close the connection
    conn.close()
    print 'connection closed. done.'

# create a start/stop index list based on desired number of subdivisions
def start_stop_list(stride, divisions):
    a = np.linspace(0, stride, divisions + 1).tolist()
    b = []
    for i in a:
        b.append(int(np.floor(i)))
        b.append(int(np.ceil(i)))
    b.pop()
    b.pop(0)
    return b

print('...done.\n')
print('If you get "Request SASL authentication protocol", run kinit.')
