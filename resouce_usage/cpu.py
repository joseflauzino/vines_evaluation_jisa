import psutil
print(psutil.cpu_percent(interval=0.2,percpu=True))

sw_usage = psutil.swap_memory()
print float(sw_usage.percent)
#swap_usage.append(float(sw_usage.percent))