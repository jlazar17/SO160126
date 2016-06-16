# timing data quality verification for event SO160126.
# the event took place on Tue Jan 26, 2016 UTC 00:21:00

# run ligo.py script to add a bunch of useful stuff; use connh() and connl() for
# connections to Hanford and Livingston NDS servers, respectively.
from ligo import *

# parameters for plots of the IRIGB and DuoTone signals
start = 'Jan 25, 2016 18:21:00'
end = 'Jan 26, 2016 06:21:00'
stride = 16
s = tcon(start)
e = tcon(end)

# run for ex GPS, ey GPS, msr GPS, Livingston
# fetch Livingston GPS data
print 'fetching livingston GPS data...'
print 'fetching EX GPS Clock data...'
ex_gps = TS.fetch(ch.livingston_cnsii_ex, s, e)
print 'fetching EY GPS Clock data...'
ey_gps = TS.fetch(ch.livingston_cnsii_ey, s, e)
print 'fetching MSR NTS data...'
msr_gps = TS.fetch(ch.livingston_nts_msr, s, e)
print 'done fetching.'

print 'plotting...'
plot_gps = TSPlot()
ax_gps = plot_gps.gca()
ex_gps_line, = ax_gps.plot(ex_gps, color='#6c71c4', label='EX CNSII GPS Clock')
ey_gps_line, = ax_gps.plot(ey_gps, color='#d33682', label='EY CNSII GPS Clock')
msr_gps_line, = ax_gps.plot(msr_gps, color='#2aa198', label='MSR Network Time Server')
plot_gps.set_title("1PPS Offset, GPS Clocks vs. aLIGO TDS, Livingston")
plot_gps.set_ylabel("Offset [s]")
plot_gps.set_ylim(min_gps, max_gps)
plot_gps.add_legend(
    [ex_gps_line, ey_gps_line, msr_gps_line],
    ['EX CNSII GPS Clock', 'EY CNSII GPS Clock', 'MSR Network Time Server']
)
plot_gps.savefig("l-gps-timediff-longer.png")
plot_gps.close()
plot_cs.show()
print 'done plotting.'

# run for ex TCT, ey TCT, msr TCG, Hanford
# fetch Hanford TCT data
print 'fetching livingston Cesium Clock data...'
print 'fetching EX TCT data...'
ex_cesium = TS.fetch(ch.livingston_cesium_ex, s, e)
print 'fetching EY TCT data...'
ey_cesium = TS.fetch(ch.livingston_cesium_ey, s, e)
print 'fetching MSR TCG data...'
msr_cesium = TS.fetch(ch.livingston_cesium_msr, s, e)
print 'done fetching.'

plot_cs = TSPlot()
ax_cs = plot_cs.gca()
# plot curves
ex_cesium_line, = ax_cs.plot(ex_cesium, color='#6c71c4', label='EX TCT')
ey_cesium_line, = ax_cs.plot(ey_cesium, color='#d33682', label='EY TCT')
msr_cesium_line, = ax_cs.plot(msr_cesium, color='#2aa198', label='MSR TCG')
# set titles and legends
plot_cs.set_title("1PPS Offset, Cesium Clock vs. aLIGO TDS, Livingston")
plot_cs.set_ylabel("Offset [s]")
plot_cs.add_legend(
        [ex_cesium_line, ey_cesium_line, msr_cesium_line],
        ['EX TCT', 'EY TCT', 'MSR TCG']
)
# save figure
plot_cs.savefig("l-cesium-timediff-longer.png")
plot_gps.close()
print 'done.'
