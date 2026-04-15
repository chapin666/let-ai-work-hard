# Source: chapter-35-ai-batch-processing.md
# Lines: 1033-1054
# Language: python

# 并行处理优化
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

# CPU密集型任务：使用进程池
def cpu_intensive_transform(files):
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(transform_file, files)
    return results

# IO密集型任务：使用线程池
def io_intensive_api_calls(files):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(call_api, files)
    return results

# 异步IO：最高效
async def async_api_calls(files):
    tasks = [async_convert(f) for f in files]
    results = await asyncio.gather(*tasks)
    return results
