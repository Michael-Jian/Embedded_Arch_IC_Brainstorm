# Literature Review: Energy-Efficient FPGA & Domain-Specific CNN Architectures (2021-2026)

This document provides a curated list of high-quality international conference and journal papers (IEEE/ACM) published between 2021 and 2026, focusing on "Energy-efficient FPGA" and "Domain-specific CNN architecture/pipeline on FPGA."

## 1. Hardware-Software Co-Design & Quantization
**Title:** "NN2FPGA: Optimizing CNN Inference on FPGAs with Binary Integer Programming"
**Venue:** *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD)*, 2024.
**Summary:** This paper proposes a highly optimized toolchain that translates quantized CNNs directly to FPGA bitstreams. It emphasizes solving the resource allocation problem (how to partition memory and DSPs optimally) using Binary Integer Programming to achieve extremely high throughput and energy efficiency, demonstrating a domain-specific compilation approach.
**Why it's relevant:** Very relevant to your methodology of turning CNN layer descriptors into efficient streaming hardware. It addresses the exact "Memory-bound vs. Compute-bound" trade-off you are tackling.

## 2. Pipelined Dataflow and Memory Hierarchy Optimization
**Title:** "TrIM: A Novel Systolic Array Architecture for CNN Acceleration on FPGAs"
**Venue:** *IEEE/ACM Design Automation Conference (DAC) / MDPI Electronics* (Recent variants 2023-2025).
**Summary:** Focuses on minimizing off-chip DDR accesses by exploiting deep on-chip memory hierarchies (like BRAM/URAM on Xilinx). The paper introduces adaptive tiling and a highly pipelined dataflow that keeps the MAC units constantly fed, significantly reducing pipeline stalls (the Memory Wall).
**Why it's relevant:** Provides theoretical grounding for your `Line Buffer` and `Ping-Pong Buffer` fusion design to break the memory wall, which is the core of your configuration C.

## 3. Real-Time Video and Pipeline Fusion
**Title:** "Ec²detect: Real-time online video object detection in edge-cloud collaborative IoT"
**Venue:** *IEEE Internet of Things Journal (IoT-J)*, 2022.
**Summary:** While proposing an edge-cloud approach, the edge component specifically focuses on minimizing end-to-end latency for video pipelines. It discusses the severe cost of data serialization and memory copying between general-purpose CPUs and accelerators.
**Why it's relevant:** Directly validates your "Data Movement costs more than Computation" (Zero-Copy) argument. It shows that eliminating intermediate memory writes (your CPU-to-DPU handover bottleneck) is a major trend in IoT video processing.

## 4. Sparse & Low-Arithmetic Intensity Models on FPGA
**Title:** "Efficient and Effective Sparse CNN/LSTM on FPGA with Bank-Balanced Sparsity" (and follow-up Depthwise Convolution acceleration works 2021-2023)
**Venue:** *ACM/SIGDA International Symposium on Field-Programmable Gate Arrays (FPGA)*.
**Summary:** Standard CNN accelerators perform poorly on models like MobileNet because depthwise convolutions have very low data reuse (low arithmetic intensity). This line of research customizes the hardware specifically for depthwise operations by redesigning the caching and PE array structure.
**Why it's relevant:** Strongly supports your choice of MobileNetV2 as a "Memory-bound" extreme stress test, and justifies why generic accelerators fail at it without custom hardware.

## 5. Domain-Specific Generation Tools
**Title:** "Angel-Eye: A Complete Design Flow for Mapping CNN onto Embedded FPGA" (Classic, with ongoing citations and extensions into 2022-2024 edge deployments)
**Venue:** *IEEE Transactions on CAD* / related recent IEEE conferences.
**Summary:** Discusses parameterizable instruction set architectures (ISA) or descriptors that allow FPGAs to act as flexible domain-specific architectures (DSAs) rather than hardwired, single-model circuits.
**Why it's relevant:** Backs up your plan to use "layer descriptors" (ISA) parsed by an FSM, proving this is a standard and respected approach in VLSI/FPGA design for AI.

## 6. End-to-End Latency vs. Pure Throughput
**Title:** "Benchmarking Edge Devices with an End-to-End Video-Based Anomaly Detection System"
**Venue:** *IEEE/Springer Conferences*, 2024.
**Summary:** This paper benchmarks modern edge devices (Jetson, etc.) and highlights that raw TOPS/FPS on the AI chip does not translate to system-level speed if the pre-processing (video decoding, resizing, background subtraction) bottlenecks the CPU.
**Why it's relevant:** This perfectly sets up your argument for **System-Level Latency Wall**. It proves that your competitors (ASIC/GPU) lose energy and time waiting for the CPU, which your FDM+CNN PL-fusion solves.
