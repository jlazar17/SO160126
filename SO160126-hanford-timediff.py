# timing data quality verification for event GW151226 (GraceDB event G211117).
# the event took place on Sat Dec 26, 2015 03:38:53 UTC 2015

# run ligo.py script to add a bunch of useful stuff; use connh() and connl() for
# connections to Hanford and Livingston NDS servers, respectively.
from ligo import *

# parameters for plots of the IRIGB and DuoTone signals
start = 'Jan 25, 2016 23:51:00'
end = 'Jan 26, 2016 00:51:00'
stride = 16
s = tcon(start)
e = tcon(end)

# TODO: run for ex GPS, ey GPS, msr GPS, Hanford
# fetch Hanford GPS data
print 'fetching hanford GPS data...'
ex_gps = TS.fetch(ch.hanford_cnsii_ex, s, e)
ey_gps = TS.fetch(ch.hanford_cnsii_ey, s, e)
msr_gps = TS.fetch(ch.hanford_nts_msr, s, e)
min_gps = min(
    ex_gps.value.min(),
    ey_gps.value.min(),
    msr_gps.value.min()
)
max_gps = max(
    ex_gps.value.max(),
    ey_gps.value.max(),
    msr_gps.value.max()
)
print 'plotting...'

plot_gps = TSPlot()
ax_gps = plot_gps.gca()
ex_gps_line, = ax_gps.plot(ex_gps, color='#6c71c4', label='EX CNSII GPS Clock')
ey_gps_line, = ax_gps.plot(ey_gps, color='#d33682', label='EY CNSII GPS Clock')
msr_gps_line, = ax_gps.plot(msr_gps, color='#2aa198', label='MSR Network Time Server')
plot_gps.set_title("1PPS Offset, GPS Clocks vs. aLIGO TDS, Hanford")
plot_gps.set_ylabel("Offset [s]")
# plot_gps.set_ylim(min_gps, max_gps)
plot_gps.add_legend(
    [ex_gps_line, ey_gps_line, msr_gps_line],
    ['EX CNSII GPS Clock', 'EY CNSII GPS Clock', 'MSR Network Time Server']
)
plot_gps.savefig("h-gps-timediff.png")
plot_gps.close()
# plot_cs.show()
print 'done.'

# TODO: run for ex TCT, ey TCT, msr TCG, Hanford
# fetch Hanford TCT data
print 'fetching hanford TCT data...'
ex_cesium = TS.fetch(ch.hanford_cesium_ex, s, e)
ey_cesium = TS.fetch(ch.hanford_cesium_ey, s, e)
msr_cesium = TS.fetch(ch.hanford_cesium_msr, s, e)
print 'plotting...'

plot_cs = TSPlot()
ax_cs = plot_cs.gca()
ex_cesium_line, = ax_cs.plot(ex_cesium, color='#6c71c4', label='EX TCT')
ey_cesium_line, = ax_cs.plot(ey_cesium, color='#d33682', label='EY TCT')
msr_cesium_line, = ax_cs.plot(msr_cesium, color='#2aa198', label='MSR TCG')
plot_cs.set_title("1PPS Offset, Cesium Clock vs. aLIGO TDS, Hanford")
plot_cs.set_ylabel("Offset [s]")
plot_cs.add_legend(
        [ex_cesium_line, ey_cesium_line, msr_cesium_line],
        ['EX TCT', 'EY TCT', 'MSR TCG']
)
plot_cs.savefig("h-cesium-timediff.png")
plot_gps.close()
# plot_cs.show()
print 'done.'
