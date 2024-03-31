Concurrency and parallelism in Java
===================================

Why we should know concurrency and parallelism? These concepts are very important and complex with every developer. They don’t depend on any languages such as Java, C, PHP, Swift, and so on.

After reading this article, you will understand things:

*   What are concurrency and parallelism? Why we should use them? How to use them in your project?
*   Unit of concurrency: Multiprocessing, Multitasking, Multithreading
*   The limitations of concurrency
*   Common problems of concurrency
*   Benefits/problems of Multithreading
*   Thread in Java: Executor framework and Thread Pool, Thread Synchronization, Locks and Atomic Variables
*   How to use CompletableFuture in Java?
*   How to use Parallelism in Java? Give you some case studies
*   Some notes when we use concurrency and parallelism

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

Thread in Java
==============

**Creating and Managing Thread**

There are two options for creating a Thread in Java. Each thread is created in Java 8 will consume about 1MB as default on OS 64 bit. You can check via command line: _java -XX:+PrintFlagsFinal -version | grep ThreadStackSize._

*   **Option 1**: You can create a class that inherits the Thread.java class.
*   **Option 2**: You can use a Runnable object.

In my option, you should use a Runnable object to creating a Thread. It’s very flexible. We also can _pause_ a Thread via _sleep() method_ and _waiting_ for the completion of another thread via the _join() method_. Thread has three priorities: Thread._MIN\_PRIORITY (1),_ Thread._NORM\_PRIORITY(5),_ Thread._MAX\_PRIORITY(10)._ The default thread has priority: Thread.NORM\_PRIORITY.

To create and manage Thread in Java you can use the Executors framework. Java Concurrency API defines three executor interfaces that cover everything that is needed for creating and managing threads:

*   **Executor**: launch a task specified by a `Runnable` object.
*   **ExecutorService**: a sub-interface of `Executor` that adds functionality to manage the lifecycle of the tasks.
*   **ScheduledExecutor**: a sub-interface of `ExecutorService` that adds functionality to schedule the execution of the tasks.

Most of the executor implementations use _thread pools_ to execute tasks.

![](https://miro.medium.com/v2/resize:fit:1260/1*NfpH4OUeD49DExLryK0aRQ.png)

Executor Service. Source: baeldung.com

**Synchronization & Locks:** In a multiple-thread program, access to shared variables must be synchronized in order to prevent race conditions. We can use the `synchronized` keyword for method or block. Besides, you can use the `volatile` keyword to avoid memory consistency errors in multi-thread programs. If you mark a variable as `volatile` the compiler won’t optimize or reorder instructions around that variable.

Instead of using an intrinsic lock via the `synchronized` keyword, you can also use various Locking classes provided by Java Concurrency API: ReentrantLock(since java 1.5), ReadWriteLock(since java 1.5), StampedLock(since java 1.8) and Atomic Variables(since java 1.5): _AtomicInteger, AtomicBoolean, AtomicLong, AtomicReference_ and so on. More details: [https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/package-summary.html](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/package-summary.html)

**How to use CompletableFuture in Java?**
=========================================

CompletableFuture is used for asynchronous programming in Java. Asynchronous programming is a means of writing non-blocking code by running a task on a separate thread than the main application thread and notifying the main thread about its progress, completion of failure. This way, the main thread doesn’t block/wait for the completion of the task and it can execute other tasks in concurrent or parallel.

Basically, CompletableFuture is implemented two interfaces: Future(since java 1.5) and CompletationStage. It provides a huge set of convenience methods for creating, chaining, and combining multiple Futures. It also has a very comprehensive exception handling support. Its complements limitations of Future such as: can’t be manually completed, can’t perform further action on a Future’s result without blocking, multiple futures can’t be chained together, you can’t combine multiple Futures together, no exception handling.

*   You can create a Completable simply by using the following no-arg constructor: `new CompletableFuture<String>();` and call `get()` method to receive the result. In this case, the `get()` method will block until the Future is complete.
*   If you want to run some background tasks asynchronously and don’t wanna return anything from the task. You can use `CompletableFuture.runAsync()` method.
*   If you want to run some background tasks asynchronously and wanna return something. You can use `Completable.supplyAsync()` method.
*   Moreover, you can also use the Executors framework(Executor, ServiceExecutor) to run something in the background. I highly recommend you use them in your project:

*   Because the `CompletableFuture.get()` method is blocking. It waits for util the Future is completed and returns the result after its completion. In case, we won’t need to wait for the result and handle logic after completion of the Future. You can use callback methods: `thenApply()`, `thenApplyAsync()`, `thenAccept()` and `thenRun()` methods. To transform the result of CompletableFuture when it arrives you can use `thenApply()` and `thenApplyAsync()` (Run in a different thread with `supplyAsync()` or executor from ForkJoinPool.commonPool()).
*   If you don’t wanna return anything from your callback and just wanna run some codes after the completion of CompletableFuture you can use: `thenAccept()` and `thenRun()`.
*   You can combine two dependent futures using `themCompose()` , and combine two independent futures using `thenCombine()`. In case, you wanna run a list of CompletableFuture and do something after all of them are complete. You can use the `CompletableFuture.allOf(` method.
*   You can handle exceptions via using `exceptionally()` callback and using the generic `handle()` method

More details: [https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/CompletableFuture.html)

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

References
==========

*   [https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/package-summary.html](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/package-summary.html)
*   [https://blog.golang.org/waza-talk#:~:text=In%20programming%2C%20concurrency%20is%20the,lots%20of%20things%20at%20once.](https://blog.golang.org/waza-talk)
*   [https://medium.com/@k.wahome/concurrency-is-not-parallelism-a5451d1cde8d](/@k.wahome/concurrency-is-not-parallelism-a5451d1cde8d)
*   [https://medium.com/educative/java-multithreading-and-concurrency-for-senior-engineering-interviews-9d8c970cd4ce](/educative/java-multithreading-and-concurrency-for-senior-engineering-interviews-9d8c970cd4ce)
*   [https://www.callicoder.com/java-concurrency-multithreading-basics/](https://www.callicoder.com/java-concurrency-multithreading-basics/)
*   [https://dzone.com/articles/how-much-memory-does-a-java-thread-take](https://dzone.com/articles/how-much-memory-does-a-java-thread-take)
*   [https://www.callicoder.com/java-8-completablefuture-tutorial/](https://www.callicoder.com/java-8-completablefuture-tutorial/)
*   [https://www.developer.com/java/data/parallel-programming-basics-with-the-forkjoin-framework-in-java.html](https://www.developer.com/java/data/parallel-programming-basics-with-the-forkjoin-framework-in-java.html)
