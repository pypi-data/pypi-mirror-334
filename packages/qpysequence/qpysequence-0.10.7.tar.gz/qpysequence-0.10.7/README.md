# QPySequence

[![Coverage](https://codecov.io/gh/qilimanjaro-tech/qpysequence/branch/main/graph/badge.svg?token=Z2ADH5BS5S)](https://codecov.io/gh/qilimanjaro-tech/qpysequence)
[![Package Version](https://img.shields.io/pypi/v/qpysequence?color=%2334D058&label=pypi%20package)](https://pypi.org/project/qpysequence)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/qpysequence.svg?color=%2334D058)](https://pypi.org/project/qpysequence)

## Introduction

QPySequence, which stands for *Qblox Python Sequence*, is a python library developed by Qilimanjaro Quantum Tech to create the `sequence.json` file that is uploaded to a Qblox sequencer.
The sequences that are uploaded to the Qblox instruments is a dictionary of four components:

- **Waveforms**: dictionary containing an explicit array representation of the pulses to be played, each identified with an index and a name.
- **Acquisitions**: dictionary containing different specifications for the acquisition of data, mainly the number of bins, each identified with an index and a name.
- **Weights**: dictionary containing lists of time-dependent acquisition weights, each associated with an index and a name.
- **Program**: description of the sequence in the Q1ASM language, represented as a plain text. In the program all waveforms, acquisitions and weights are referenced by their indices.

In the [Qblox docs](https://qblox-qblox-instruments.readthedocs-hosted.com/en/master/) there are several examples on how to write a Q1ASM program to perform a certain experiment as well as the necessary waveforms, acquisitions and weights to complete the sequence. This is task usually done by manually writing the waveforms and weights dictionaries with an inline numpy array generating function, the acquisitions are specified also manually, and finally a Q1ASM program is writen as a python formated string, with some variables inside for certain parameters.

This procedure is feasible for small examples and certain simple experiments. However, when integrating this into a larger codebase, for example, inside of a general quantum control library, with a complex class structure, holding many instrument drivers and being developed by several colaborators; the maintenance, quality, readability and debugging of the code can become a cumbersome task.

While certain parts of this procedure could be modularized with some helper functions, the string nature of the Q1ASM program as well with the remaining parts of the sequence it is connected to, indirectly via integers (the indices) that have to be handled separately, still leaves a lot of room for improvement with the implementation of a higher abstraction layer that would handle the creation of the sequence in an easier and more robust manner.

QPySequence is a library that handles all the components of a sequence as python objects, from the sequence itself to each instruction of the program, including new abstractions as blocks and loops to structure the program in a more clear and readable way.

## Structure

The main classes of QPySequence imitate the structure of the `sequence.json` itself: `Waveforms`, `Acquisitions`, `Weights` and `Program`, as well as the class `Sequence` which contains them.
The `Program` class is the one with higher complexity of the main four, with several internal classes used to structure all the instructions it holds (instances of classes which inherit from the abstract `Instruction` class). In contrast, the other three main classes (`Acquisitions`, `Weights` and `Waveforms`) share a very similar structure, since their structure is that of their dictionary counterpart in `sequence.json`, with the addition of methods that facilitate their construction.
All the classes that are not internal have an implementation of the `repr()` method, which gives the equivalent string representation of that object that will be actually sent to the sequencer. In this way, when a `Sequence` object is completed with all of its components and its `repr()` method is called, it calls the `repr()` method of its elements, which gets recursively repeated until until reaching the lower layers, obtaining finally the complete string representation of the `sequence.json` file that can be directly uploaded to a Qblox sequencer.
The `repr()` method can be called on any component of QPySequence, which allow to only generate the string representation of a single component, as the `Program` for example, if desired.

## Example

This simple example illustrates how to create a sequence for an averaged readout

```python
import qpysequence as qps
import numpy as np

# Experiment parameters
readout_duration = 1000
play_acq_delay = 120
averaging_repetitions = 1024

# Create waveforms
waveforms = qps.waveforms.Waveforms()
readout_pulse = np.array([1.0 + 0.0j for _ in range(readout_duration)], dtype=np.complex128)
ro_index_i, ro_index_q = waveforms.add_pair_from_complex(readout_pulse)

# Create acquisitions
acquisitions = qps.acquisitions.Acquisitions()
acq_index = acquisitions.add("averaged")

# Create an empty weights object
weights = {}

# Create the program
program = qps.program.Program()
main_loop = qps.program.Loop("main", averaging_repetitions)
play = qps.program.instructions.Play(ro_index_i, ro_index_q, play_acq_delay)
acquire = qps.program.instructions.Acquire(acq_index, bin_index=0, wait_time=readout_duration)
main_loop.append_components([play, acquire])
program.append_block(main_loop)

# Create the sequence with all the components
sequence = qps.Sequence(program, waveforms, acquisitions, weights)

# The sequence can now be converted to a json string and uploaded to a qblox sequencer
sequence_json = repr(sequence)
```

## Development setup

If you want to participate in the project, set up first your local environment, set up the git hooks and install the library.

Read the [development](./doc/DEVELOPMENT.md) documentation.
