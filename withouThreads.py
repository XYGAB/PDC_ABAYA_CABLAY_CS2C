'''
Importing Modules: 

The code imports necessary modules from multiprocessing and numpy.

Writer Function:

Attaches to a named shared memory block.
Creates a NumPy array that uses this shared memory.
Fills the array with even numbers.
Closes the shared memory after writing.

Reader Function:

Also attaches to the same named shared memory block.
Creates a NumPy array to access the same data.
Prints out the contents of the array.
Closes the shared memory after reading.

Main Block:

Defines the shape and data type of the array.
Creates a new shared memory block large enough to hold the specified array.
Starts both writer and reader processes.
Cleans up by closing and unlinking (removing) the shared memory after use.

This example illustrates how two separate processes can communicate
through a shared memory space efficiently without needing to write to or read from files.'''

import multiprocessing
from multiprocessing import shared_memory
import numpy as np

def writer(shm_name, shape, dtype):
    # Attach to the existing shared memory block using its name
    shm = shared_memory.SharedMemory(name=shm_name)
    
    # Create a NumPy array backed by the shared memory block
    shared_array = np.ndarray(shape, dtype=dtype, buffer=shm.buf)
    
    # Write data to the shared array
    for i in range(shape[0]):
        shared_array[i] = i * 2  # Fill the array with even numbers (0, 2, 4, ...)
    
    print("Writer process finished writing data.")  # Indicate that writing is complete
    shm.close()  # Close the shared memory block for this process

def reader(shm_name, shape, dtype):
    # Attach to the existing shared memory block using its name
    shm = shared_memory.SharedMemory(name=shm_name)
    
    # Create a NumPy array backed by the shared memory block
    shared_array = np.ndarray(shape, dtype=dtype, buffer=shm.buf)
    
    # Read data from the shared array and print it
    print("Reader process read data:", shared_array[:])  # Output the contents of the array
    
    shm.close()  # Close the shared memory block for this process

if __name__ == "__main__":
    # Define the shape and data type of the NumPy array
    shape = (10,)  # Array will have 10 elements
    dtype = np.int64  # Data type of each element in the array
    
    # Create a new shared memory block with enough size to hold the array
    shm = shared_memory.SharedMemory(create=True, size=np.prod(shape) * np.dtype(dtype).itemsize)
    
    # Start writer and reader processes
    p1 = multiprocessing.Process(target=writer, args=(shm.name, shape, dtype))  # Process for writing data
    p2 = multiprocessing.Process(target=reader, args=(shm.name, shape, dtype))  # Process for reading data
    
    p1.start()  # Start the writer process
    p1.join()   # Wait for the writer process to finish before proceeding
    
    p2.start()  # Start the reader process
    p2.join()   # Wait for the reader process to finish before cleaning up
    
    # Clean up: close and unlink (free) the shared memory block
    shm.close()   # Close the shared memory in this process
    shm.unlink()  # Remove the shared memory block from the system
