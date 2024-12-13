class MemoryManager:
    def __init__(self, block_sizes, total_memory):
        """
        Initialize memory blocks and free lists.
        """
        self.free_lists = {size: [size] * (total_memory // size) for size in block_sizes}
        self.general_pool = []  # To store blocks not fitting predefined sizes
        self.allocations = {}  # Track process allocations (process_id -> block size)

    def allocate_memory(self, process_id, process_size):
        """
        Allocate memory for a process using Quick Fit algorithm.
        """
        # Check for predefined size
        for size in self.free_lists:
            if size >= process_size and self.free_lists[size]:
                block = self.free_lists[size].pop(0)
                self.allocations[process_id] = block
                print(f"Process {process_id} allocated {block} units.")
                return

        # Allocate from general pool if no matching predefined block
        for block in self.general_pool:
            if block >= process_size:
                self.general_pool.remove(block)
                self.allocations[process_id] = process_size
                print(f"Process {process_id} allocated {process_size} units from general pool.")
                return

        print(f"Process {process_id} cannot be allocated. Insufficient memory.")

    def deallocate_memory(self, process_id):
        """
        Deallocate memory for a process.
        """
        if process_id in self.allocations:
            block = self.allocations.pop(process_id)
            for size in self.free_lists:
                if block == size:
                    self.free_lists[size].append(block)
                    print(f"Process {process_id} deallocated and returned to block size {size}.")
                    return

            self.general_pool.append(block)
            print(f"Process {process_id} deallocated and returned to general pool.")
        else:
            print(f"Process {process_id} is not allocated.")

    def display_memory(self):
        """
        Display the current state of memory.
        """
        print("Free Lists:")
        for size, blocks in self.free_lists.items():
            print(f"  Size {size}: {blocks}")
        print(f"General Pool: {self.general_pool}")
        print(f"Allocations: {self.allocations}")


# Example Usage
block_sizes = [16, 32, 64]
total_memory = 256  # Total memory in units
manager = MemoryManager(block_sizes, total_memory)

manager.allocate_memory("P1", 16)
manager.allocate_memory("P2", 32)
manager.allocate_memory("P3", 48)  # Goes to general pool
manager.deallocate_memory("P1")
manager.display_memory()
