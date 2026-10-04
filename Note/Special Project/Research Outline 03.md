# Research Outline: Hybrid Vision-CNN Pipelines on FPGA SoC

## Part 01: Observation & Objective
- **Observation:** Hybrid datapath (FDM + CNN) is highly accurate for edge object detection. Pure NPUs (like Hailo-8) cannot run FDM, causing heavy off-chip DDR data transfers, leading to Memory Wall and Latency Wall.
- **Objective:** Design an FPGA Domain-Specific Architecture (DSA) with a custom hardware pipeline to achieve "Zero-Copy" execution, eliminating off-chip memory bottlenecks.
- **Model Selection (Symmetric):** ResNet50 (Compute-bound) vs. MobileNet (Memory-bound) as two extreme hardware stress tests.

## Part 02 & 03: Challenge & Method
- **Insight:** "Data movement costs more power than computation." Fusing FDM and CNN MAC into a single PL pipeline saves immense energy.
- **Method:** 3 Hardware platforms (FPGA SoC, Nvidia Jetson, Hailo 8) x 2 Models (ResNet50 vs. MobileNet).
- **Latency Wall (ResNet50):** ASIC relies on Host CPU & PCIe for pre-processing. FPGA DSA uses a Zero-Copy Pipeline (PL handles FDM and streams directly to MAC array) to win on System-Level Latency.
- **Memory Wall (MobileNet):** Depthwise convolution has low Arithmetic Intensity. FPGA DSA uses Custom On-Chip Buffering (Line Buffer & Ping-Pong Buffer in BRAM) to drastically reduce DDR access, winning on FPS/Watt (Energy Efficiency).

## Part 04: Roofline Model Analysis
- **Compute-bound (ResNet50):** High Arithmetic Intensity. Bottleneck is the computation unit (MAC/DSP).
- **Memory-bound (MobileNet):** Low Arithmetic Intensity (DW convolutions). Bottleneck is the external DDR memory bandwidth (Pipeline Stalls).
- **Kitchen Analogy:**
  - Compute-bound: Assistant (Memory) delivers a big piece of meat, Chef (ALU) spends 30 mins carving it. Chef is always busy.
  - Memory-bound: Assistant fetches onions one by one from the basement. Chef chops them in 2 seconds and waits. Chef is idle, Assistant is exhausted.
