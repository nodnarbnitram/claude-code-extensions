# Frigate Object Detector Comparison

## Detector Types Overview

| Detector | Hardware | Performance | Power | Cost | Best For |
|----------|----------|-------------|-------|------|----------|
| USB Coral | Coral TPU | Excellent | ~2W | $60 | Most users |
| PCIe Coral | Coral TPU | Excellent | ~2W | $40 | Servers with PCIe |
| OpenVINO GPU | Intel iGPU | Very Good | Varies | Free | Intel systems |
| OpenVINO CPU | Any CPU | Poor | High | Free | Testing only |
| ONNX | Multi-GPU | Very Good | Varies | Free | Multi-vendor |
| TensorRT | NVIDIA Jetson | Excellent | Low | $200+ | Jetson devices |
| Hailo-8L | Hailo NPU | Excellent | ~1.5W | $70 | RPi 5 AI Kit |
| RKNN | Rockchip SoC | Good | Low | Varies | ARM SBCs |
| CPU | Any CPU | Poor | High | Free | Not recommended |

## Detailed Comparison

### USB Coral TPU

**Pros:**
- Best performance per watt
- Simple USB connection
- Works on any system with USB
- Handles 10+ cameras easily

**Cons:**
- Can be hard to find in stock
- USB bandwidth can be limiting with many cameras
- Generates some heat

**Configuration:**
```yaml
detectors:
  coral:
    type: edgetpu
    device: usb
```

### PCIe/M.2 Coral TPU

**Pros:**
- Same performance as USB
- No USB bandwidth limitations
- Lower latency
- Dual-edge TPU available for double throughput

**Cons:**
- Requires PCIe slot or M.2 slot
- Harder to install
- Limited to desktop/server systems

**Configuration:**
```yaml
detectors:
  coral:
    type: edgetpu
    device: pci
```

### OpenVINO (Intel)

**Pros:**
- Uses existing Intel GPU (free)
- Good performance on modern Intel CPUs
- Supports multiple model architectures

**Cons:**
- Requires Intel 6th Gen (Skylake) or newer
- GPU mode requires compatible integrated graphics
- CPU mode is inefficient

**Configuration:**
```yaml
detectors:
  ov:
    type: openvino
    device: GPU  # or CPU for testing
```

### ONNX Runtime

**Pros:**
- Automatically uses available GPU acceleration
- Works with AMD ROCm, Intel OpenVINO, NVIDIA TensorRT
- Flexible model support (YOLO variants)

**Cons:**
- Requires compatible GPU drivers
- Performance varies by hardware

**Configuration:**
```yaml
detectors:
  onnx:
    type: onnx
    device: auto  # Automatically selects best available
```

### TensorRT (NVIDIA Jetson)

**Pros:**
- Optimized for Jetson hardware
- Low power consumption
- Good for edge deployments

**Cons:**
- Only works on Jetson devices
- Requires model preprocessing on target hardware
- Limited to NVIDIA ecosystem

**Configuration:**
```yaml
detectors:
  tensorrt:
    type: tensorrt
    device: 0
```

### Hailo-8L (Raspberry Pi 5 AI Kit)

**Pros:**
- Designed for Raspberry Pi 5
- Low power consumption
- Good performance for edge

**Cons:**
- Limited to specific hardware
- Newer, less tested

**Configuration:**
```yaml
detectors:
  hailo:
    type: hailo8l
```

### CPU Detector

**Pros:**
- Works on any hardware
- No additional hardware needed

**Cons:**
- Very high CPU usage
- Not suitable for production
- Slow inference times

**Configuration:**
```yaml
detectors:
  cpu:
    type: cpu
    num_threads: 3
```

## Capacity Guidelines

| Detector | Cameras @ 5fps | Cameras @ 10fps |
|----------|---------------|-----------------|
| Single USB Coral | 10-15 | 5-8 |
| Dual USB Coral | 20-30 | 10-15 |
| PCIe Coral (single) | 10-15 | 5-8 |
| PCIe Coral (dual) | 20-30 | 10-15 |
| OpenVINO GPU | 5-10 | 3-5 |
| OpenVINO CPU | 2-3 | 1-2 |

## Important Notes

1. **Cannot mix detector types for object detection** - You can't use Coral for some cameras and OpenVINO for others. Pick one detector type for all object detection.

2. **Other tasks can use different hardware** - Semantic search, face recognition, and other features can use different hardware than the main object detector.

3. **USB bandwidth matters** - If using multiple USB Coral TPUs, ensure they're on different USB controllers.

4. **Temperature affects performance** - Coral TPUs throttle at high temperatures. Consider cooling for sustained workloads.

## Recommendations

| Scenario | Recommended Detector |
|----------|---------------------|
| Home user, 1-4 cameras | USB Coral TPU |
| Home user, Intel system | OpenVINO GPU |
| Power user, 5-15 cameras | USB Coral TPU |
| Server, 10+ cameras | Dual PCIe Coral |
| Raspberry Pi 5 | Hailo-8L |
| NVIDIA Jetson | TensorRT |
| Budget/Testing | OpenVINO CPU (temporary only) |
