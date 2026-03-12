# google-smi

TPU counterpart of `nvidia-smi`. Real-time HBM usage, duty cycle, and process attribution for Google Cloud TPUs.

```
Tue Mar 04 14:23:07 2025
+---------------------------------------------------------------------------------------+
| Google-SMI 0.1.0        Driver: vfio-pci libtpu Version: 0.1.dev20250304+nightly      |
|-------------------------------------+--------------------------+----------------------|
| TPU  Name               NUMA Node   | Bus-Id            IOMMU  |          PCIe        |
|                                     |       Memory-Usage       |      TPU-Util        |
|=====================================+==========================+======================|
|   0  TPU v6e                    0   | 0000:00:04.0          4  |      Gen5 x16        |
|                                     |    5120MiB /   32768MiB  |         23.4%        |
+-------------------------------------+--------------------------+----------------------+
|   1  TPU v6e                    0   | 0000:00:05.0          5  |      Gen5 x16        |
|                                     |   12048MiB /   32768MiB  |         78.2%        |
+-------------------------------------+--------------------------+----------------------+
|   2  TPU v6e                    0   | 0000:00:06.0          6  |      Gen5 x16        |
|                                     |   12048MiB /   32768MiB  |         65.7%        |
+-------------------------------------+--------------------------+----------------------+
|   3  TPU v6e                    0   | 0000:00:07.0          7  |      Gen5 x16        |
|                                     |       0MiB /   32768MiB  |          0.0%        |
+-------------------------------------+--------------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
| TPU         PID    Type      Process Name                         Memory Usage        |
|=======================================================================================|
|   0       12345       C      python3                                    5120MiB       |
|   1       12345       C      python3                                   12048MiB       |
|   2       67890       C      jax_worker                                12048MiB       |
+---------------------------------------------------------------------------------------+
```

## Features

- **nvidia-smi-like output** — familiar table layout for TPU monitoring
- **HBM memory tracking** — per-device used/total high-bandwidth memory
- **TPU utilization** — tensor core utilization percentage
- **Process attribution** — maps PIDs to TPU devices with memory usage
- **JSON output** — machine-readable format for scripting
- **Zero config** — auto-detects TPU devices via PCI bus scanning

## Installation

```bash
pip install git+https://github.com/bzantium/google-smi.git
```

## Usage

```bash
google-smi

# Continuous monitoring
google-smi -i
google-smi -i 0.5

# JSON output
google-smi --json
```

Options:

- `-i`, `--interval`, `--watch`: refresh continuously with an in-place redraw
- `--json`: emit machine-readable JSON output
