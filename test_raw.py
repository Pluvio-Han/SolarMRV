from solar_monitor import SolarMonitor
m = SolarMonitor('/dev/null')
print(m.read_realtime_data())
