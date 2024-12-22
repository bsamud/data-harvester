from multiprocessing import Pool, cpu_count
from common.logger import log

class ParallelProcessor:
    def __init__(self, num_workers=None):
        self.num_workers = num_workers or cpu_count()

    def process_batch(self, func, items):
        with Pool(self.num_workers) as pool:
            results = pool.map(func, items)
        log.info(f"Processed {len(items)} items with {self.num_workers} workers")
        return results
