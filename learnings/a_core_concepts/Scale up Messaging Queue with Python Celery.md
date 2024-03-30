
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

====================

Handling I/O Bound Tasks with Python Celery using Processes vs Threads Pool — Part 2
====================================================================================

We are going to scrape hundreds to thousands of web pages using Celery with Threads Pool and Processes Pool to compare which pool works best for I/O bound tasks.

Every time we get data through scraping, we save the response to AWS S3 and Meta data to Mongo which makes the total number of I/O calls within a single task to 3 times.

1.  Get data from data source (scrape web page)
2.  Save meta data to Mongo
3.  Save response data to AWS S3

We don’t do anything else other than get data, create meta and save data and meta to mongo and S3. No computation at all. No data processing or transformation. Which makes it completely I/O intensive tasks.

If we handle all these tasks through a prefork process pool with default concurrency, it is just a waste of CPU time because most of the time, the task will be doing I/O work and the CPU will be idle waiting for I/O.

```python
@shared_task  
def scrape():  
  
    # I/O Call  
    base_page = requests.get("http://www.my-scraping-page.com/list")  
    child_urls = soup.find_all('a', href=True)  
  
    for i, child_url in enumerate(child_urls\[:100\]):  
        # I/O Call   
        child_page = requests.get(child_url)  
          
        # I/O Call  
        save_meta_to_mongo(child_page)  
          
        # I/O Call  
        save_response_to_s3(child_page)
```

This is the process pool running for our current web scraping with a default concurrency of 8.

```
celery -A project worker --concurrency=8
```

![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/40313ec4-5ee3-4fce-bc40-8f2c379e3bb9)

You can see, most of the processes are sleeping except the master worker process and 1 child process handling all of the load for scraping. There is just 1 process doing all stuff as we are getting all web pages using a loop inside a single task. So single task will be handled by a single process if we trigger that task just once.

Getting the base page and then getting child pages and saving to mongo and to s3 all handled by a single process. This one child process is going to a sleeping/running cycle because of I/O calls. So this is completely sequential to scrape and waste of resources to keep these processes up while doing nothing.

**Scraping 100 pages took 6.4 minutes. \[Internet speed matters\]**

Instead of prefork process pool, we can use gevent threads pool to spin up thousands of threads and then threads will be doing context switching as it gets an I/O.

We’ll need to convert our tasks to micro tasks, doing an I/O call and then closing. So instead of going through web pages to scrape and then go against all following URLs to scrape those nested pages and so on, all in one thread, we can create a task such that we pass a URL to the task, it gets the data, save meta to Mongo and response data to S3.

So one thread goes through the main page, getting URLs for nested pages and then passes that URL of the nested page to the task handling actual scraping through another thread.

If we optimize our code to like below code, we can make all of our processes busy which makes it faster to process the same stuff.

```python
@shared_task  
def scrape():  
    # I/O Call  
    base_page = requests.get("http://www.my-scraping-page.com/list")  
    child_urls = soup.find_all('a', href=True)  
  
    for i, child_url in enumerate(child_urls\[:100\]):  
          
        # I/O Call  
        child_page = requests.get(child_url)  
          
        # Spin up new process  
        save_meta_to_mongo.delay(child_page)  
          
        # Spin up new process  
        save_response_to_s3.delay(child_page)  
  
@shared_task  
def save_meta_to_mongo(child_page):  
    # save meta data to mongo.  
    ...  
  
@shared_task  
def save_response_to_s3(child_page):  
    # save response to s3  
    ...

```

```
celery -A project worker --concurrency=8
```

After code refactoring and creating micro task for S3 I/O and Mongo I/O,

**this took just 3 minutes**

because more processes were handling more tasks at the same time instead of 1 process doing everything i.e pull, save meta and save to S3.

Each time a parent task def scrape() calls another task save_meta_to_mongo or save_response_to_s3, it starts that sub task in a new process and moves on to the next page to pull.

same code took 3 minutes when running on concurrent threads using below celery config

```
celery -A project worker --concurrency=100 --pool=gevent
```

Because we are spending more time on

```python
# I/O call  
requests.get("http://www.my-scraping-page.com/list")  
  
# and  
# I/O Call  
requests.get(child_url)

in parent task and inside for loop before we start a new task and then assign rest of the stuff to child tasks save_meta_to_mongo and save_response_to_s3 so we are not utilizing all of the 100 threads

We need to refactor more so each sub task gets its own html page from the provided URL and then does the rest of the stuff. So we can spin up 100 threads, each with its own URL to get html page and save data. Move I/O call to its relevant task (Process/Thread).

@shared_task  
def scrape():  
      
    # I/O Call  
    base_page = requests.get("http://www.my-scraping-page.com/list")  
    child_urls = soup.find_all('a', href=True)  
  
    for i, child_url in enumerate(child_urls\[:100\]):  
        # Spin up new process  
        save_meta_to_mongo.delay(child_url)  
          
        # Spin up new process  
        save_response_to_s3.delay(child_url)  
  
  
@shared_task  
def save_meta_to_mongo(child_url):  
    # I/O call  
    child_page = requests.get(child_url)  
      
    # I/O call  
    # save meta data to mongo.  
  
  
@shared_task  
def save_response_to_s3(child_url):  
    # I/O call  
    child_page = requests.get(child_url)  
      
    # I/O call  
    # save response to s3
```

This more refactored code took

*   **just 7~8 seconds to scrape 100 web pages**
*   **2 minutes to scrape 2100 web pages while celery was up with 1000 threads pool.**

Here the worker master process just get the list of URLs and trigger a task for saving meta and saving to S3 with desired URL. Each task is responsible for getting its web page data from its provided web page url
