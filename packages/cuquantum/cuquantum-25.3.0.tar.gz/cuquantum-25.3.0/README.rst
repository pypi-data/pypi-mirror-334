****************************************************************************************
cuQuantum SDK: A High-Performance Library for Accelerating Quantum Computing Simulations
****************************************************************************************

`NVIDIA cuQuantum SDK <https://developer.nvidia.com/cuquantum-sdk>`_ is a set of high-performance libraries and tools for accelerating 
quantum computing simulations at both the circuit and device level by orders of magnitude. It consists of three major components:

* cuDensityMat: a high-performance library for quantum dynamics equation solvers
* cuStateVec: a high-performance library for state vector quantum simulators
* cuTensorNet: a high-performance library for tensor network computations

In addition to C APIs, cuQuantum also provides Python APIs via `cuQuantum Python`_.

.. _cuQuantum Python: https://pypi.org/project/cuquantum-python/

Documentation
=============

Please refer to https://docs.nvidia.com/cuda/cuquantum/index.html for the cuQuantum documentation.

Installation
============

.. code-block:: bash

   pip install -v --no-cache-dir cuquantum

.. note::

   Starting cuQuantum 22.11, this package is a meta package pointing to ``cuquantum-cuXX``,
   where XX is the CUDA major version (currently CUDA 11 & 12 are supported).
   The meta package will attempt to infer and install the correct ``-cuXX`` wheel. However,
   in situations where the auto-detection fails, this package currently points to ``cuquantum-cu11``
   with a warning raised (if the verbosity flag ``-v`` is set, as shown above). This behavior
   will change in the next release, moving from cu11 to cu12, and users are encouraged to install the new wheels that
   come *with* the ``-cuXX`` suffix.

   The argument ``--no-cache-dir`` is required for pip 23.1+. It forces pip to execute the
   auto-detection logic.

.. note::

   Future support for CUDA 11 will be deprecated in the next release when support for CUDA 13 is added.

   To use cuQuantum's Python APIs, please directly install `cuQuantum Python`_.

Citing cuQuantum
================

`H. Bayraktar et al., "cuQuantum SDK: A High-Performance Library for Accelerating Quantum Science," 2023 IEEE International Conference on Quantum Computing and Engineering (QCE), Bellevue, WA, USA, 2023, pp. 1050-1061, doi: 10.1109/QCE57702.2023.00119 <https://doi.org/10.1109/QCE57702.2023.00119>`_
