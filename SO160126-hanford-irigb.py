# timing data quality verification for event SO162601.
# the event took place on Tue 26 Jan 00:21:00 UTC 2016

# run ligo.py script to add a bunch of useful stuff; use connh() and connl() for
# connections to Hanford and Livingston NDS servers, respectively.
from ligo import *

# parameters for plots of the IRIGB and DuoTone signals
starts = ['Jan 25 2016 23:51:00', 'Jan 26, 2016 00:21:00']
ends = ['Jan 26, 2016 00:20:59', 'Jan 26, 2016 00:51:00']
start = 'Jan 26, 2016 00:21:00'
end = 'Jan 26, 2016 00:22:00'
stride = 16384

# want more temporal subdivisions for DuoTone, fewer for IRIG-B
irigb_stride_div = [0, stride]
irigb_stride_div.extend( start_stop_list(stride, 4) )
duotone_stride_div = [0, stride]
duotone_stride_div.extend( start_stop_list(stride, 10) )

for i in xrange(len(starts)):
    if len(starts) != len(ends):
        raise ValueError('gotta have same number of start and end times!')

    # run for IRIG-B, Hanford EX
    channels = [ch.hanford_irigb_ex]
    titles = ['Overlay of IRIG-B, Hanford EX']
    iterative_fetch_save_and_plot(starts[i], ends[i], connh(), channels, stride, irigb_stride_div, titles)
