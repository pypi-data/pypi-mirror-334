import psutil
import time
import numpy as np
import os
import multiprocessing
import cpuinfo


def cpu_info():
    info = {}
    cpu_name = cpuinfo.get_cpu_info()
    info['cpu_name'] = cpu_name['brand_raw']
    info["physical_cores"] = psutil.cpu_count(logical=False)
    info["logical_cores"] = psutil.cpu_count(logical=True)
    freq = psutil.cpu_freq()
    info["max_frequency"] = freq.max
    info["min_frequency"] = freq.min
    info["current_frequency"] = freq.current
    info["cpu_percent"] = psutil.cpu_percent(interval=1, percpu=True)

    return info


def memory_info():
    info = {'Total_GB': psutil.virtual_memory().total / (1024 ** 3),
            'Used_GB': psutil.virtual_memory().used / (1024 ** 3),
            'Free_GB': psutil.virtual_memory().free / (1024 ** 3), 'Percent': psutil.virtual_memory().percent}
    return info


def disk_info():
    disk_info_dict = {}
    disk_partitions = psutil.disk_partitions()
    for partition in disk_partitions:
        partition_info = {}
        usage = psutil.disk_usage(partition.mountpoint)
        partition_info['mountpoint'] = partition.mountpoint
        partition_info['total_size_GB'] = round(usage.total / (1024 ** 3), 2)
        partition_info['used_size_GB'] = round(usage.used / (1024 ** 3), 2)
        partition_info['free_size_GB'] = round(usage.free / (1024 ** 3), 2)
        partition_info['usage_percent'] = usage.percent
        disk_info_dict[partition.device] = partition_info
    return disk_info_dict


def cpu_calculation(number_a, i, size=10000000):
    start_time = time.time()
    number_a ** size
    elapsed_time = round(time.time() - start_time, 2)
    cpu_load = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq().current
    return i, elapsed_time, cpu_load, cpu_freq


class StressTest:
    def __init__(self, debug=False):
        self.debug = debug

    def ram_test(self):
        num_elements = 8 * 1024 * 1024 // 4  # 8 MB
        elements = []
        start_time = time.time()
        ram_used = {}
        while True:
            try:
                memory = np.ones(num_elements, dtype=np.float32)
                elements.append(memory)

                if self.debug:
                    used_percent = psutil.virtual_memory().percent
                    ram_used[round(time.time() - start_time, 2)] = f'{used_percent:.2f}%'
            except MemoryError:
                elements.clear()
                break

        if self.debug:
            elapsed_time = round(time.time() - start_time)
            full_dict = {'elapsed_time': elapsed_time,
                         'ram_used': ram_used}
            return full_dict

    def memory_test(self):
        filename = 'testfile.bin'
        file_size = 1 * 1024 * 1024 * 1024
        data = os.urandom(file_size)  # 1 GB
        time_dict = {}
        speed_dict = {}
        for i in range(1, 11):
            start_time = time.time()
            with open(filename, 'wb') as file:
                file.write(data)
            os.remove(filename)
            elapsed_time = round(time.time() - start_time, 2)
            write_speed = (file_size / (1024 * 1024)) / elapsed_time
            if self.debug:
                time_dict[i] = elapsed_time
                speed_dict[i] = round(write_speed, 2)
            else:
                return round(write_speed, 2), elapsed_time
        if self.debug:
            average_speed = round(sum(speed_dict.values()) / len(speed_dict), 2)
            average_time = round(sum(time_dict.values()) / len(time_dict), 2)
            full_dict = {'average_speed': average_speed, 'average_time': average_time}
            return full_dict

    def cpu_test(self, size=10000000):
        number_a = 2 ** 256

        start_cpu_load = psutil.cpu_percent(interval=1)
        start_cpu_freq = psutil.cpu_freq().current

        cpu_load_dict = {'start': start_cpu_load}
        cpu_freq_dict = {'start': start_cpu_freq}
        time_dict = {}

        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            results = pool.starmap(cpu_calculation, [(number_a, i, size) for i in range(1, 11)])

        if self.debug:
            for i, elapsed_time, cpu_load, cpu_freq in results:
                cpu_load_dict[i] = cpu_load
                cpu_freq_dict[i] = cpu_freq
                time_dict[i] = elapsed_time

            average_cpu_load = round(sum(cpu_load_dict.values()) / len(cpu_load_dict), 2)
            average_cpu_freq = round(sum(cpu_freq_dict.values()) / len(cpu_freq_dict), 2)
            average_time = round(sum(time_dict.values()) / len(time_dict), 2)

            cpu_full_dict = {
                'average_cpu_load': average_cpu_load,
                'average_cpu_freq': average_cpu_freq,
                'average_time': average_time,
                'cpu_load_dict': cpu_load_dict,
                'cpu_freq_dict': cpu_freq_dict,
                'time_dict': time_dict
            }

            return cpu_full_dict
        else:
            return results[0][1]


root = disk_info()
print(root)