# timing data quality verification for event So160126.
# the event took place on Tue Jan 26 2016 00:21:00

# run ligo.py script to add a bunch of useful stuff; use connh() and connl() for
# connections to Hanford and Livingston NDS servers, respectively.
from ligo import *

# parameters for plots of the IRIGB and DuoTone signals
start = 'Jan 26 2016 00:21:00'
end = 'Jan 26 2016 00:21:01'
stride = 16384

# want more temporal subdivisions for DuoTone, fewer for IRIG-B
irigb_stride_div = [0, stride]
irigb_stride_div.extend( start_stop_list(stride, 4) )
duotone_stride_div = [0, stride]
duotone_stride_div.extend( start_stop_list(stride, 10) )

# run for IRIG-B, Hanford EX
channels = [ch.hanford_irigb_ex]
titles = ['One Second of IRIG-B Signal, Hanford EX']
iterative_fetch_save_and_plot(start, end, connh(), channels, stride, irigb_stride_div, titles)
