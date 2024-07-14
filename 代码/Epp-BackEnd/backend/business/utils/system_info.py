import psutil
import GPUtil


def get_cpu_info():
    # 获取 CPU 使用情况
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    cpu_count = psutil.cpu_count(logical=False)
    cpu_count_logical = psutil.cpu_count(logical=True)
    return {
        'cpu_usage': cpu_usage,
        'cpu_count': cpu_count,
        'cpu_count_logical': cpu_count_logical
    }


def get_memory_info():
    # 获取内存使用情况
    virtual_mem = psutil.virtual_memory()
    swap_mem = psutil.swap_memory()
    return {
        'total_memory': virtual_mem.total,
        'used_memory': virtual_mem.used,
        'available_memory': virtual_mem.available,
        'total_swap': swap_mem.total,
        'used_swap': swap_mem.used,
        'free_swap': swap_mem.free
    }


def get_gpu_info():
    # 获取 GPU 使用情况
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            'id': gpu.id,
            'name': gpu.name,
            'load': gpu.load,
            'memory_total': gpu.memoryTotal,
            'memory_used': gpu.memoryUsed,
            'memory_free': gpu.memoryFree,
            'temperature': gpu.temperature
        })
    return gpu_info


def get_system_info():
    cpu_info = get_cpu_info()
    memory_info = get_memory_info()
    gpu_info = get_gpu_info()

    return {
        'cpu_info': cpu_info,
        'memory_info': memory_info,
        'gpu_info': gpu_info
    }


if __name__ == "__main__":
    system_info = get_system_info()
    print(system_info)
