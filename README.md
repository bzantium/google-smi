# google-smi

`google-smi` is a TPU-oriented status CLI in the style of `nvidia-smi`. It shows per-device HBM usage, TPU utilization, PCIe / NUMA / IOMMU context, and process attribution for local TPU VMs.

```text
Thu Mar 12 01:58:21 2026
+---------------------------------------------------------------------------------------+
| Google-SMI 0.1.0        Driver: vfio-pci libtpu Version: 0.0.17                       |
|-------------------------------------+--------------------------+----------------------|
| TPU  Name               NUMA Node   | Bus-Id            IOMMU  |          PCIe        |
|                                     |       Memory-Usage       |      TPU-Util        |
|=====================================+==========================+======================|
|   0  TPU v6e                    0   | 0000:00:04.0          0  |            x0        |
|                                     |     406MiB /   31995MiB  |          0.0%        |
+-------------------------------------+--------------------------+----------------------+
|   1  TPU v6e                    0   | 0000:00:05.0          1  |            x0        |
|                                     |     406MiB /   31995MiB  |          0.0%        |
+-------------------------------------+--------------------------+----------------------+
...
| Processes:                                                                            |
| TPU         PID    Type      Process Name                         Memory Usage        |
|=======================================================================================|
|   0     2955029       C      python                                     406MiB        |
+---------------------------------------------------------------------------------------+
```

## Install

```bash
pip install git+https://github.com/bzantium/google-smi.git
```

## Quick Start

```bash
# default table view
google-smi

# show Bus-Id / IOMMU detail columns
google-smi -d

# refresh in place every second
google-smi -i

# refresh every 0.5 seconds
google-smi -i 0.5

# machine-readable output
google-smi --json
```
