Concurrency and parallelism 
=============================

Why we should know concurrency and parallelism? These concepts are very important and complex with every developer. They don’t depend on any languages such as Java, C, PHP, Swift, and so on.

After reading this article, you will understand things:

*   What are concurrency and parallelism? Why we should use them? How to use them in your project?
*   Unit of concurrency: Multiprocessing, Multitasking, Multithreading
*   The limitations of concurrency
*   Common problems of concurrency
*   Benefits/problems of Multithreading

What are concurrency and parallelism?
=====================================

With a laptop/pc, you can listen to some favorite songs, download English videos, and write some codes at the same time. Currently, I’m developing enterprise web applications that use the Spring Boot project. The spring boot project uses the Tomcat embed server which is default and helps us handling concurrent requests from the client by multi-threading. There are lots of examples in the real about concurrency.

**“In programming, concurrency is the _composition_ of independently executing processes, while parallelism is the simultaneous _execution_ of (possibly related) computations. Concurrency is about _dealing with_ lots of things at once. Parallelism is about _doing_ lots of things at once.” Source: blog.golang.org**

![](https://miro.medium.com/v2/resize:fit:1080/1*c9hJciosear4PTicZp0ukA.jpeg)

**Concurrent**: Two queues to one coffee machine, **Parallel**: Two queues to two coffee machines.

**_“Concurrency is about structure, parallelism is about execution.”_**

Why we use concurrency and parallelism? The answer is very simple: It’ll improve throughput and the interactivity of the program.

Unit of Concurrency
===================

As far as I know, concurrency has three levels:

*   **Multiprocessing**: Multiple Processors/CPUs executing concurrently. This unit here is a CPU.
*   **Multitasking:** Multiple tasks/processes running concurrently on a single CPU. The OS executes these tasks by switching between them very frequently. This unit here is a Process.
*   **Multithreading**: Multiple parts of the same program running concurrently. In this case, we go a step further and divide the same program into multiple parts/threads and run those threads concurrently.

In this article, we will only discuss the Multithreading level.

Process vs Thread
=================

**A process** is a program in execution. It has its own address space, a call stack, and link to any resources such as open files. A computer system normally has multiple processes running at a time. The OS keeps track of all these processes and facilitates their execution by sharing the processing time of the CPU among them.

**A thread** is a path of execution within a process. Every process has at least one thread called the main thread. The main thread can create additional threads within the process. Threads within a process share the process’s resources including memory and open files. Besides, every thread has its own call stack which will be created at runtime. For every method call, one entry will be added in the stack called a stack frame. Each stack frame has the reference for the local variable array, operand stack, and runtime constant pool of a class where the method being executed belongs.

The limitations of concurrency
==============================

Within a Java application, you work with several threads to achieve parallel processing or asynchronous behavior. Concurrency promises to perform certain tasks faster as these tasks can be divided into subtasks and these subtasks can be executed in parallel. Of course, the runtime is limited by parts of the task which can be performed in parallel.

The theoretical possible performance gain can be calculated by following the rule which is referred to as **_Amdahl’s Law_**. This law stipulates that there will always be a maximum speedup that can be achieved when the execution of a program is split into parallel threads.

Amdahl's law describes the theoretical limit at best a program can achieve by using additional computing resources: `S(n) = 1 / (1 - P) + P/n`

*   **S(n)** is the speedup achieved by using n cores or threads.
*   **P** is the fraction of the program that is parallelizable.
*   **(1-P)** is the fraction of the program that must be executed serially.

Common Problems of concurrency
==============================

Besides, improve significantly the throughput by increasing CPU utilization. The concurrency still has some problems:

*   **Thread interference errors (Race condition)**: It occurs when the multiple threads try to read or write a shared variable concurrently, and these read and write operations overlap in execution. The solution here, we only allow one thread to access a shared resource at a time. This is usually done by acquiring a mutually exclusive lock before accessing any shared resource. The concept of acquiring a lock before accessing any shared resource can lead to other problems like _deadlock_ and _starvation_.

![](https://miro.medium.com/v2/resize:fit:1260/1*E0NLljJ7s4CP84nbUj6bpw.png)

A simple example of a race condition.

![](https://miro.medium.com/v2/resize:fit:1260/1*k5zto3oNHn4B8b_-xDA2qA.png)

A simple example of a mutually exclusive lock.

*   **Memory consistency errors**: It occurs when different threads have inconsistent views of the same data. This happens when one thread updates some shared data, but this update is not propagated to other threads, and they end up using the old data. In Java, we can use `violate` keyword to solve this.

Benefits of Multithreading
==========================

*   **Higher throughput**: the ability to process more units of information in a given amount of time.
*   **More responsive applications** that provide user seamless experiences and the illusion of multitasking.
*   **More efficient utilization of resources:** Generally speaking, thread creation is less _costly_ compared to creating a brand new process. Web servers that use threads instead of creating a new process when fielding web requests consume far fewer resources.

Problems of Multithreading
==========================

*   **More difficult to find bugs:** The execution order and prioritization of threads can’t always be predicted and is up to the operating system itself.
*   **The higher cost of code maintenance**: Since the code has now had multiple levels of complexity added to it.
*   **More demand on the system:** The creation of each thread consumes additional memory, CPU cycles for book-keeping, and time spent on witching contexts. Additionally, keep in mind if a processor is going to run 5 threads simultaneously it will also need to keep information about each of those processes around and accessible while other ones execute, requiring more registers.

How to use Parallelism in Java?
===============================

Unlike multithreading, where each task is a discrete logical unit of a larger task, parallel programming tasks are independent and their execution order doesn’t matter. The tasks are defined according to the function they perform or data used in processing; this is called functional parallelism or data parallelism, respectively. Parallel programming is suitable for a larger problem base that doesn’t fit into a single CPU architecture, or it may be the problem is so large that is can’t be solved in a reasonable estimate of time. As a result, tasks, when distributed among processors, can obtain the result relatively fast.

In other words, Parallel computing involves dividing a problem into subproblems, solving those problems simultaneously(in parallel, with each subproblem running in a separate thread), and then combining the results of the solutions to the subproblems. Java SE provides the Fork/Join Framework which helps you to more easily implement parallel computing in your applications.

One difficulty in implementing parallelism in applications that use collections is that collections aren’t thread-safe, which means that multiple threads can’t manipulate a collection without introducing thread interference or memory consistency errors. Not that parallelism isn’t automatically faster than performing operations serially, although it can be if you have enough data and processor cores.

In Java, You can run streams in serial or in parallel. When a stream executes in parallel, the Java runtime partitions the stream into multiple substreams.

More details: [Parallelism](https://docs.oracle.com/javase/tutorial/collections/streams/parallelism.html) and [Fork/Join Framework](https://docs.oracle.com/javase/tutorial/essential/concurrency/forkjoin.html)

Some notes when we use concurrency and parallelism in Java
==========================================================

*   An application can be concurrent, but not parallel. It means that it can process more than one task at the same time, but no two tasks are executing at the exact same time. A thread is only executing one task at a time. There is no parallel execution of tasks going in parallel threads/CPUs.
*   An application can also be parallel but not concurrent. It means that the application only works on one task at a time, and this task is broken down into subtasks which can be processed in parallel. However, each task (includes subtasks) is completed before the next task is split up and executed in parallel.
*   Additionally, an application can be neither concurrent nor parallel. Is means that it works on only one task at a time, and the task is never broken down into subtasks for parallel execution.
*   Finally, an application can also be both concurrent and parallel. It means that it works on multiple tasks at the same time, and also breaks each task down into subtasks for parallel execution. However, some benefits of concurrency and parallelism may be lost in this case, as the CPUs are already kept reasonably busy with either concurrency or parallelism alone. Combining it may lead to only a small performance gain or even performance loss. Make sure you analyze and measure before you adopt a concurrent parallel model blindly.

**Summary**
===========

*   As far as I know about synchronous and asynchronous programming. They are programming models. We can apply concurrency and parallelism in asynchronous programming. Concurrency and parallelism are the ways that executed tasks. Single-thread and Multi-thread are the environments of task execution.
*   Finally, you should use concurrency and parallelism wisely. Happy coding !!!

If you have any doubts/questions, please comment here !!!. Thank you for your reading !!!.


