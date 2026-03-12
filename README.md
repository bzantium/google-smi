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

# refresh in place every second
google-smi -i

# refresh every 0.5 seconds
google-smi -i 0.5

# machine-readable output
google-smi --json
```

## What It Shows

- TPU device index, name, NUMA node, PCI bus ID, IOMMU group, and PCIe link information
- HBM usage per TPU device
- TPU duty cycle / utilization
- Process attribution with PID, process name, and device memory usage

## Notes

- `-i`, `--interval`, and `--watch` refresh continuously with an in-place redraw rather than shelling out to `watch`.
- `--json` is intended for scripting and integrations.
- Output depends on local TPU discovery and available runtime metrics.
