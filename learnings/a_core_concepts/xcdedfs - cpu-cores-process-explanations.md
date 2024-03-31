Differences Between Core and CPU
================================

1\. Introduction[](#introduction)
---------------------------------

When we host a big party, we typically have several tasks to accomplish. Besides actually doing the work in the party location, we also have to organize all the work, talk with suppliers for food, drinks, and decoration, and deal with the guest list.

Hosting a big party involves a lot of work. So, it would be nice having many people working on it. But, of course, we still need the figure of the party host to make decisions and manage the other people working. But, with multiple people, it’s possible to divide all the required tasks and do them in parallel.

Hosting a party is an analogy to *how a modern computer CPU works*. The **CPU** is our **party host**. It deals with several requests and messages and divides the processing work among the available cores. The **cores**, in turn, are the **people working at the party**. They listen to the host (CPU) instructions and execute the required tasks.

### With this example, we can already note that cores and CPUs are not synonyms.

Thus, in this tutorial, we’ll study the main differences and similarities between them. Initially, we’ll have a brief historical context of processing units. So, we’ll investigate the concepts of cores and CPU. Finally, we’ll compare them in a systematic summary.

> CPU -> Party Host.
> Core -> Workers at the party

2\. The Context of Processing Units[](#the-context-of-processing-units)
-----------------------------------------------------------------------

Early computer systems, before the 70s, used limited processing units due to the complex integration of transistors and logical gates on a large scale in a single chip. Thus, CPUs required connected chips to work together to process a single task.

After, in the 70s, the Large-Scale Integration (LSI) enabled the creation of microprocessors with data processing and control logic in the same chip. LSI allowed the coexistence of tens of thousands of transistors and up to ten thousand logical ports in the same chip for the same CPU.

The number of transistors and logical ports in the same chip kept increasing in the following decades. So, in the early 2000s, it becomes viable to have [multiple processing cores working together in the same die](/cs/advanced-cpu-designs#superscalar-processors-and-multi-core-processors). It means, in practice, a CPU working with several processing cores and executing parallel tasks.

After that, other technologies, such as multithreading, make the parallelism in the CPUs even better. However, in the following sections, we’ll focus on multicore and understand the relationship between a CPU and its processing cores.

3\. Processing Core[](#processing-core)
---------------------------------------

**A core is a processing unit of the CPU.** It is responsible for executing programs and multiple other actions on a computer.

In general, we can divide a core into three main parts: control unit, arithmetic-logic unit, and memory. Each part of the core is responsible for particular tasks:

*   **Control Unit (CU)**: This unit enables the communication of the core with other components of a computer system. So, for example, it requires instructions processing, sends signals for the computer system hardware, and manages the computer system data. In this way, the control unit communicates with both the arithmetic-logic unit and the memory
*   **Arithmetic-Logic Unit (ALU)**: This unit consists of electronic circuits that execute arithmetic and logical operations. Usually, the ALU executes four arithmetic operations – addition, subtraction, multiplication, and division. Furthermore, it typically executes three logical operations – equal-to, less-than, and greater-than
*   **Memory**: The memory built within the core consists of registers and cache. [Registers](/cs/registers-and-ram#registers) are portions of memory used to, for example, keep addresses, instructions, and results of calculations for the core processing. [Cache](/cs/cache-memory), in turn, is a high-speed random access memory that holds data that the core probably will (re)use

Other relevant particular elements of a core are [the clock and the buses](/cs/cache-memory). The following image shows an abstract core architecture:

![Core 2](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/7a7c6118-e5ee-42e9-b859-794e7e488d86)

4\. Central Processing Unit[(CPU)](#central-processing-unit) or Processor
-------------------------------------------------------

**The CPU consists of the component that coordinates cores for executing tasks in a computer system.** In this way, a computer with a single CPU can simultaneously execute  **n** tasks, where **n** is the number of cores. As a note,  **n** is the total number of available threads if the CPU cores employ multithreading.

A processor (CPU) is the logic circuitry that responds to and processes the basic instructions that drive a computer. The CPU is seen as the main and most crucial integrated circuitry (IC) chip in a computer, as it is responsible for interpreting most of computers commands. CPUs will perform most basic arithmetic, logic and I/O operations, as well as allocate commands for other chips and components running in a computer.

The term processor is used interchangeably with the term central processing unit (CPU), although strictly speaking, the CPU is not the only processor in a computer. The GPU (graphics processing unit) is the most notable example, but the hard drive and other devices within a computer also perform some processing independently. Nevertheless, the term processor is generally understood to mean the CPU.

In addition to hosting and coordinating the processing cores, the CPU establishes the communication between other components of a computer system and processing cores (through their control unit). To do that, a CPU generally has controllers for memory accessing and data I/O.

The CPU commonly contains an extra level of cache shared within all the processing cores (typically a layer two or a layer three cache). Furthermore, it is possible to integrate a GPU into the CPU. Actually, the CPU can host multiple different components, benefiting them by being close to the processing cores.


In this way, it is relevant to highlight that CPUs vary according to the adopted design. Early CPUs, for example, have many of their controllers implemented in a complementary chipset. Most of the modern CPUs, however, have all the controllers implemented inside them.

The following image shows an abstract CPU design:

![CPU](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/5f0d30c1-283e-4557-852e-bc6b805f2442)


5\. Systematic Summary[](#systematic-summary)
---------------------------------------------

**We studied the concepts of processing core and CPU.** Both concepts are related to the execution of tasks in a computer system. However, they aren’t synonyms.

> A CPU is a component of computer systems that manages and executes tasks. Thus, controllers, cache memory, and, most important, processing cores compose a CPU.

> Processing cores, as previously stated, are part of the CPU. They actually process tasks on a computer. Typically, they have some standard elements. The most prominent of them are CU, ALU, and memory.

The following table compares and summarizes information of processing cores and CPUs:

![Differences Between Core and CPU](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/d0d1171f-ec1a-4e97-9195-26c906c234a1)


6\. Conclusion[](#conclusion)
-----------------------------

**In this article, we learned about the differences between a processing core and a CPU.** First, we had a brief review of the evolution of processing units. So, we studied the concept of a processing core, thus understanding their main elements. Similarly, we analyzed the concept and main elements of a CPU. Finally, we had a summary on processing cores and CPU and compared their relations and differences.

We can conclude that, in fact, processing cores and CPUs are not the same things. While cores actually process tasks, a CPU is responsible for controlling the cores, as well as interfacing data from other computer system components to them. So, a processing core works within the CPU, and one depends on another to accomplish the computer tasks.

--------------------------------

# PROCESS 


![image](https://github.com/vijayanandrp/blog/assets/3804538/45d6be94-c40f-4b29-b28d-4b6f83a3c589)

### Process states

![image](https://github.com/vijayanandrp/blog/assets/3804538/2657b2b2-7e5d-4b2e-819e-120d9feb0874)

An operating system kernel that allows multitasking needs processes to have certain states. Names for these states are not standardised, but they have similar functionality.

  - First, the process is **"created"** by being loaded from a secondary storage device (hard disk drive, CD-ROM, etc.) into main memory. After that the process scheduler assigns it the **"waiting"** state.
  - While the process is **"waiting"**, it waits for the scheduler to do a so-called *context switch*. The *context switch* loads the process into the processor and changes the state to **"running"** while the previously **"running"** process is stored in a **"waiting"** state.
  - If a process in the **"running"** state needs to wait for a resource (wait for user input or file to open, for example), it is assigned the **"blocked"** state. The process state is changed back to **"waiting"** when the process no longer needs to wait (in a blocked state).
  - Once the process finishes execution, or is terminated by the operating system, it is no longer needed. The process is removed instantly or is moved to the **"terminated"** state. When removed, it just waits to be removed from main memory.

![image](https://github.com/vijayanandrp/vijayanandrp/assets/3804538/ba55cb2e-1835-4b3c-a5ee-109df92b55e0)


# Credits:

1. [https://www.baeldung.com/cs/core-vs-cpu](https://www.baeldung.com/cs/core-vs-cpu)
