-----------------------------------------------------------------------

 ### global interpreter lock
The mechanism used by the CPython interpreter to assure that only one thread executes Python bytecode at a time. This simplifies the CPython implementation by making the object model (including critical built-in types such as dict) implicitly safe against concurrent access. Locking the entire interpreter makes it easier for the interpreter to be multi-threaded, at the expense of much of the parallelism afforded by multi-processor machines.

However, some extension modules, either standard or third-party, are designed so as to release the GIL when doing computationally intensive tasks such as compression or hashing. Also, the GIL is always released when doing I/O.

Past efforts to create a “free-threaded” interpreter (one which locks shared data at a much finer granularity) have not been successful because performance suffered in the common single-processor case. It is believed that overcoming this performance issue would make the implementation much more complicated and therefore costlier to maintain.

![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/0c1e8230-bab0-4b39-9f3b-24c91f44024e)

![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/8f561587-194d-4f8e-a7eb-ee918446335f)

### Understanding Concurrency in Python

Concurrency refers to the execution of multiple tasks simultaneously in a program. There are primarily three ways to introduce concurrency in Python - Multithreading, Multiprocessing and Asyncio. Each approach has its own advantages and disadvantages.

Choosing the right concurrency model for your Python program depends on the specific requirements and use-cases. This comprehensive guide will provide an overview of all three approaches with code examples to help you decide when to use Multithreading, Multiprocessing or Asyncio in Python.

![](https://media.licdn.com/dms/image/D4D12AQFzK8L4_D3kRA/article-inline_image-shrink_1500_2232/0/1700323413686?e=1717027200&v=beta&t=9dwKGZS0e7gxSH-BIofkyXL3w82FWUBZguEKGSEFtc8)

![](https://media.licdn.com/dms/image/D5612AQF1n2qpbZ689Q/article-inline_image-shrink_1500_2232/0/1700327813543?e=1717027200&v=beta&t=aWhr0bl4RqxT9wpTa7riG-DC_U_N3L1HROzPteXm3jM)

### Multithreading in Python

**Multithreading** refers to concurrently executing multiple threads within a single process. The Python thread module allows you to spawn multiple threads in your program.

![](https://media.licdn.com/dms/image/D5612AQHeVZXfNQYWfw/article-inline_image-shrink_1500_2232/0/1700328043488?e=1717027200&v=beta&t=dx9nE5rn3PnAlHi2xY_NC-PqUE4VlSkVk-ZtcOOPq1U)

Here is an example code to understand multithreading in Python:

```python
import threading 

def print_cube(num):
  """
  Function to print cube of given num
  """
  print("Cube: {}".format(num * num * num))

def print_square(num):
  """
  Function to print square of given num
  """
  print("Square: {}".format(num * num))

if __name__ == "__main__":
    # creating thread
    t1 = threading.Thread(target=print_square, args=(10,))  
    t2 = threading.Thread(target=print_cube, args=(10,))

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()

    print("Done!") 
```
In the above code, we create two threads t1 and t2. t1 calls print_square() function while t2 calls print_cube().

We start both the threads using start() method. join() ensures that the main thread waits for these threads to complete before terminating.

The key advantage of multithreading is that it allows maximum utilization of a single CPU core by executing threads concurrently. All threads share same process resources like memory. Context switching between threads is lightweight.

However, multithreading also comes with challenges like race conditions, deadlocks etc. when multiple threads try to access shared resources. Careful synchronization is needed to avoid these issues.

[Download Images using Multithreading](https://gist.github.com/IamAkshayKaushik/2544a941d28692ee5982d35ea5403596)

### Multiprocessing in Python

**Multiprocessing** refers to executing multiple processes concurrently. The multiprocessing module in Python allows spawning processes using an API similar to threading.

![](https://media.licdn.com/dms/image/D5612AQFkBulX7E_DSg/article-inline_image-shrink_1500_2232/0/1700328329265?e=1717027200&v=beta&t=phK2rmdbpM51588-seg3l4aYEP_cZGUgf-Slf4zGT9U)

Here is an example:
```python
import multiprocessing 

def print_cube(num):
  """
  Function to print cube of given num
  """
  print("Cube: {}".format(num * num * num))

def print_square(num):
  """
  Function to print square of given num
  """
  print("Square: {}".format(num * num))

if __name__ == "__main__":
    # creating process
    p1 = multiprocessing.Process(target=print_square, args=(10,))
    p2 = multiprocessing.Process(target=print_cube, args=(10,))

    # starting process 1
    p1.start()
    # starting process 2
    p2.start()

    # wait until process 1 is finished
    p1.join()
    # wait until process 2 is finished
    p2.join()

    print("Done!") 
```
Here, we create two processes p1 and p2 to execute the print_square() and print_cube() functions concurrently.

The main difference between multithreading and multiprocessing is that threads run within a single process while processes run independently in separate memory spaces.

Multiprocessing avoids GIL limitations and allows full utilization of multicore CPUs. But processes have higher memory overhead compared to threads. Interprocess communication is more complicated compared to thread synchronization primitives.

[Process Images using Multiprocessing](https://gist.github.com/IamAkshayKaushik/8d458337358968a7cde5a1683443da87)

### Asyncio in Python

Asyncio provides a single-threaded, non-blocking concurrency model in Python. It uses cooperative multitasking and an event loop to execute coroutines concurrently.

Here is a simple asyncio example:
```python
import asyncio

async def print_square(num):
  print("Square: {}".format(num * num))

async def print_cube(num):
  print("Cube: {}".format(num * num * num))

async def main():
  # Schedule coroutines to run concurrently
  await asyncio.gather(
    print_square(10),
    print_cube(10)
  )

asyncio.run(main()) 
```
We define coroutines using async/await syntax. The event loop schedules execution of coroutines and runs them consecutively.

Asyncio is best suited for IO-bound tasks and use cases where execution consists of waiting on network responses, database queries etc. It provides high throughput and minimizes blocking.

However, asyncio doesn't allow true parallellism on multicore systems. CPU-bound processing may suffer performance issues. It has a steep learning curve compared to threads and processes.

[**Threading is about workers; asynchrony is about tasks.**](https://stackoverflow.com/a/34681101)

### Key Differences

Here is a quick comparison of the three concurrency models:

![Multithreading VS Multiprocessing VS Asyncio in Python](https://media.licdn.com/dms/image/D4D12AQGZvMj5soZR6w/article-inline_image-shrink_1500_2232/0/1700323093034?e=1717027200&v=beta&t=rUxVsdZJkWssHJXoWJ2l8HCiglH1MY-AzA-7nXASREg)

### Use Cases

*   Use **multithreading** when you need to run I/O bound or CPU bound jobs concurrently in a single process. Examples - serving concurrent requests in a web server, parallel processing in data science apps etc.
*   Leverage **multiprocessing** for CPU bound jobs that require truly parallel execution across multiple cores. Examples - multimedia processing, scientific computations etc.
*   **Asyncio** suits network applications like web servers, databases etc. where blocking I/O operations limit performance. Asyncio minimizes blocking for high throughput.

**So in summary:**

*   Multithreading provides concurrent execution in a single process, limited by GIL
*   Multiprocessing provides full parallelism by executing separate processes
*   Asyncio uses an event loop for cooperative multitasking and minimized blocking

Choose the right concurrency model based on your application requirements and use cases.

### Conclusion

*   Multithreading, multiprocessing and asyncio provide different approaches to concurrency and parallelism in Python.
*   Multithreading uses threads in a single process, multiprocessing spawns separate processes while asyncio leverages an event loop and coroutines for cooperative multitasking.
*   Each model has its own strengths and limitations. Understanding the key differences is important to make an informed decision based on the specific problem you are trying to solve.
*   The code examples and comparisons highlighted in this guide should help you pick the appropriate concurrency framework for your Python programs.

### FAQs

**Q: What is the Global Interpreter Lock (GIL) in Python?**

A: The GIL is a mutex that allows only one thread to execute Python bytecodes at a time even in multi-threaded programs. This prevents multiple threads from running simultaneously on multiple CPU cores.

**Q: How can I achieve true parallelism in Python?**

A: The multiprocessing module allows spawning multiple processes which can leverage multiple CPUs and cores for parallel execution. It avoids GIL limitations.

**Q: When should I use multithreading vs multiprocessing?**

A: Use multithreading for I/O bound tasks. Multiprocessing is best for CPU intensive work that needs parallel speedup across multiple CPU cores.

**Q: What are the differences between multiprocessing and multithreading?**

A: Key differences are separate vs shared memory, different synchronization primitives, parallelism capabilities etc. Multiprocessing provides full parallelism while multithreading is limited by GIL.

**Q: How does asyncio work and when should it be used?**

A: Asyncio uses an event loop and coroutines for cooperative multitasking model suited for I/O bound apps. It minimizes blocking and provides high throughput.
