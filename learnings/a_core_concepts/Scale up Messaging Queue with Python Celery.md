
Scale up Messaging Queue with Python Celery (Processes vs Threads) — Part 1
===========================================================================


![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/c6b8ec01-d72e-404e-8eef-3d6740a79d6d)

Image Source: [https://sixfeetup.com/blog/high-availability-scaling-with-celery](https://sixfeetup.com/blog/high-availability-scaling-with-celery)

![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/bb55c2fa-ca7f-4758-a898-82c656cb3e40)



### Queue

This is the basic architecture of how a message queue system works.

⇒ There is some **Producer**, could be a REST API endpoint hit by some externa entity, a scheduler scheduling jobs at a regular intervals or an external entity directly pushing tasks to Broker Queue through Broker API.

⇒ Then there is a **Broker** i.e tasks queue holding N number of tasks pushed by any producer. Could be a single queue or N number of queues.

⇒ And then lastly we have a **Consumer**, polling tasks from Broker queues at regular intervals to process accordingly. Consumer could be another process, some AWS service or a database handler which process and push data to database

### Celery
Celery consumer is just a process (worker process) which continuously looks for tasks in the broker queue, picks a task and spin up a child process to process that task.

So if we are adding 1 task to the queue at a regular interval, celery picks that task and assigns it to the child process to be processed.

NOW, what if we have hundreds of tasks pushed to the broker queue at a time. Does the celery worker spin up hundreds of processes?

Celery worker is a master process which only picks tasks from the queue and distributes them to the child processes.

How many child processes a worker process is allowed to spin up, depends on the number of CPU cores. If a celery worker is running in a machine with 8 CPU cores, the worker process will spin up 8 processes by default even if the worker has no tasks to process.

```
celery -A project worker
```
![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/68cb582d-2903-457c-adb5-79f2e4b3d978)

This is the default. You can see the list of processes ran by celery

If you want to keep 4 processes open any time. You can try this
```
celery -A project worker –concurrency=4
```
![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/9ae53f92-3b6d-47b6-94f7-ece033948632)

Or if you want 20 or 2000
```
celery -A project worker –concurrency=20
```
![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/02173819-29ba-442a-8e9e-bfab4869578a)

**Isn’t it resource wasting? Or useless to keep up 4 or 8 or 2000 processes even not needed at all?**  
Yes. You can configure celery worker to auto scale based on the number of tasks the worker should pick from the broker.
```
celery -A project worker –autoscale=8,1
```
![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/7285ebc3-0cb8-4a89-ab08-0e76abf2da4a)

Now celery worker will just keep one process alive (other than worker master process) and then as the worker gets more tasks from the queue, it will spin up more processes until the limit 8 is reached.

So 8,1 means, by default 1 process running but can go up to 8 processes concurrently

**What if the queue has 50 tasks but worker can spin up max 8 processes at a time? What happens to other tasks in the queue.**

The other tasks will wait in the queue until the worker sees that a child process has finished processing a task and is free to pick up another task. Worker will pick another task from the queue and assign it to the child process. This cycle goes on until all of the 50 tasks are processed by the worker

**So it means more CPU cores, more tasks handling concurrently?**

YES. 16 cores, 16 tasks processing concurrently. 32 cores, 32 tasks processing concurrently

**Isn’t it expensive to increase the number of CPU cores based on how many tasks we are going to handle? Handling hundreds or maybe thousands of tasks. I want to stick to 16 cores of CPU.**

Yes. you can increase number of concurrent tasks processing like this
```
celery -A project worker –autoscale=100,1
```
BUT, the recommended way is, to run 1 process per CPU core and this is how Python does it as well.

**Then How can we run 100 processes on a 16 cores CPU concurrently?**

The worker will still spin up 100 processes concurrently but at a time only 1 process will use 1 CPU core and as soon as one process (core) gets busy on I/O bound stuff, another process will start using that same CPU core and this cycle goes on.

Ahhh.. you kidding me? It’s just illusion-ed like we are handling 100 processes at one time but in reality it’s just 16 processes running at a time.

**YES. Bruh**

![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/da69f5d3-d516-4219-988c-68ded446b4c5)

**NO man. What if I have CPU intensive tasks, continuously using a core of CPU?**

That means your tasks will take longer as CPU cores will be busy most of the time with 1 task and you don’t take advantage of running more tasks concurrently.

**What is the solution?**

Either increase number of cores OR increase number of workers, all running on different machines consuming tasks from the same broker queue or even you can split queues and assign different queue to different worker.

Celery recommends 1 worker per machine to get max use of 1 process per CPU core. so if you have 100% CPU intensive tasks. Then Don’t go for more concurrency than that number of CPU cores.

**8 cores**
```
celery -A project worker –autoscale=8,1
```
**16 cores**
```
celery -A project worker –autoscale=16,1
```
**32 cores**
```
celery -A project worker –autoscale=32,1
```

_BUT this is only True for CPU intensive tasks._


**What if I have I/O intensive tasks? Mostly going over the internet, getting some data, a bit of processing and then putting data back to some database, some hard drive and a chunk of data to some AWS service?**

In this case, the CPU will be idle most of the time, waiting for the I/O as there is nothing to process but just to get or put data on the network or some other I/O

Here you can take full advantage of concurrency even if you have less CPU cores. as the CPU core gets idle while waiting for the I/O, another process can use the same CPU core.

Most of your tasks will not be waiting for a CPU core to get free, because at any time there will be an I/O from any core, and another process can take advantage of this idle time of that idle core.

Interesting……

**BUT processes are heavy, consuming more resources even if idle, it’s still there UP…**

**So spinning up thousands of processes for I/O tasks makes sense as it can take advantage of idle CPU cores and we can continue with max concurrency. But it will consume a lot of memory and CPU as well.**

YES. And here comes Threads…

Celery supports green threads.

Wait? Green?.. Yeah.. green threads which work on the application level NOT on the OS level.

The same LOGIC described above. Switching and checking idle CPU core and taking full use of that core till some I/O stuff is going…

So instead of spinning up thousands of processes which will take more resources, you can spin up that number of threads or even more threads taking much less resources but doing exactly the same stuff. as threads are lightweight.

**REMEMBER…** this is true only if you have I/O bound tasks NOT CPU bound tasks.

**Spin up celery worker with threads pool instead of processes**
```
celery -A project worker –pool gevent –autoscale=1000,10
```
By default keep 10 threads and can go up to 1000 threads or even more if you set here.

By default celery use prefork processes

**Spin up celery worker with processes pool instead of threads**
```
celery -A project worker –pool prefork –autoscale=16,1
```
Prefork is based on python [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) package while gevent is based on [eventlet](https://eventlet.net/) package

So the bigger picture is…
=========================

**CPU intensive tasks ⇒**

Increase number of cores OR number of workers with default concurrency using prefork processes pool

**I/O Intensive tasks ⇒**

Switch to threads pool using eventlet and scale to max threads

**Mix of CPU intensive tasks and I/O intensive tasks ⇒**

Separate queues and workers for CPU intensive tasks and I/O intensive tasks.

1 worker with more cores and default concurrency (1 process per core) while other worker with reasonable cores, use threads pool and max concurrency

[**Handling I/O Bound Tasks with Python Celery using Processes vs Threads Pool**](/@iamlal/handling-i-o-bound-tasks-with-python-celery-using-processes-vs-threads-pool-126a4875600d)
