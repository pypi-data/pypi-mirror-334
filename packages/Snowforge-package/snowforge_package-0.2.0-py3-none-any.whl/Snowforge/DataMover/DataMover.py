import os
import multiprocessing as mp


from .Extractors.ExtractorStrategy import ExtractorStrategy
from ..Logging import Debug

class DataMover():
    
    def __init__(self, strategy: ExtractorStrategy):
        """Initialize the DatMover engine. Takes the ExtractStrategy as input (i.e NetezzaExtractor, OracleExtractor etc.)"""
        self.extractor = strategy()
    
    @staticmethod
    def parallel_process(worker_func: object, args_list: list[tuple], num_workers: int = None, use_shared_queue: bool = False, queue = None):
        """
        Executes a worker function 'worker_func' in parallel using a number multiple processes defined by the 'num_workers' variable.

        Args:
            worker_func (function): The function that each worker process should execute.
            args_list (list): A list of tuples, where each tuple contains arguments for worker_func.
            num_workers (int, optional): Number of parallel workers. Defaults to max(4, CPU count - 2).
            use_shared_queue (bool, optional): If True, a multiprocessing queue will be created and passed to workers.
            queue (mp.Queue, optional): If provided, it will be used instead of creating a new queue.

        Returns:
            list: List of results from worker processes if applicable.
        """

        # Determine the number of CPU cores to use
        if num_workers is None:
            num_workers = max(4, os.cpu_count() - 2) #failsafe slik at noen kjerner er tilgjengelig for systemet

        num_processes = min(num_workers, len(args_list))

        process_list = []
        if use_shared_queue and queue is None:
            Debug.log("You HAVE to supply a queue as input to this function if you set 'use_shared_queue = True', otherwise the queue will not be reachable to produces/consumer processes on the other side!", 'WARNING')
            raise SyntaxError

        # Create and start all worker processes
        for i in range(num_processes):

            if use_shared_queue:
                process = mp.Process(target=worker_func, args=(*args_list[i], queue))
            else:
                process = mp.Process(target=worker_func, args=args_list[i])

            process.daemon = True  # Ensure processes exit when main program exits. This ensures no orphans or zombies
            process_list.append(process)
            process.start()

        return process_list  # Return the list of running processes

    
    @staticmethod
    def determine_file_offsets(file_name: str, num_chunks: int):
        """Determine file offsets for parallel reading based on line breaks."""
        file_size = os.path.getsize(file_name)
        chunk_size = max(1, file_size // num_chunks)

        offsets = [0]
        with open(file_name, 'rb') as f:
            for _ in range(num_chunks - 1):
                f.seek(offsets[-1] + chunk_size)
                f.readline()
                offsets.append(f.tell())
        print(f"DEBUG: File offsets computed: {offsets}")
        return offsets