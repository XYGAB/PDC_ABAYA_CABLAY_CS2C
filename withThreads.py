'''
Explanation

Imports: 
The necessary modules are imported for threading and time management.
Event Creation: An Event object is created to signal when the threads should stop running.

Thread Function (modify_variable):

This function increments each element of a shared list indefinitely until signaled to stop.
Shared Variable: A list (my_var) is initialized with three integers, which will be modified by both threads.

Thread Creation and Starting:

Two threads are created and started, both executing the modify_variable function with my_var as an argument.

Main Loop:

The main thread continuously prints the current state of my_var every second.

Graceful Shutdown:

If a keyboard interrupt occurs, it sets the event to signal both threads to stop processing.

Joining Threads:

The main thread waits for both worker threads to complete before proceeding.

Final Output:

Finally, it prints the final state of my_var, showing how it has been modified by both threads.
These comments should help clarify each section's purpose and functionality within the code.
'''


from threading import Thread, Event
from time import sleep

# Create an event to signal when to stop the thread
event = Event()

def modify_variable(var):
    """Function to increment each element in the shared variable."""
    while True:
        for i in range(len(var)):
            var[i] += 1  # Increment each element by 1
        if event.is_set():  # Check if the event is set to stop
            break
        sleep(0.5)  # Sleep for a short duration to simulate work

# Shared variable (list) that will be modified by threads
my_var = [1, 2, 3]

# Create and start two threads that modify the same shared variable
t1 = Thread(target=modify_variable, args=(my_var,))  # Thread 1
t2 = Thread(target=modify_variable, args=(my_var,))  # Thread 2
t1.start()  # Start Thread 1
t2.start()  # Start Thread 2

try:
    while True:
        print(my_var)  # Print the current state of the shared variable
        sleep(1)  # Sleep for a second before printing again
except KeyboardInterrupt:
    event.set()  # Signal threads to stop on keyboard interrupt

# Wait for both threads to finish execution
t1.join()  # Wait for Thread 1 to finish
t2.join()  # Wait for Thread 2 to finish

print("Final value of my_var:", my_var)  # Print the final state of the shared variable
