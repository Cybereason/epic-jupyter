# Epic jupyter &mdash; Conveniences for working in Jupyter Notebook or Ipython
[![Epic-jupyter CI](https://github.com/Cybereason/epic-jupyter/actions/workflows/ci.yml/badge.svg)](https://github.com/Cybereason/epic-jupyter/actions/workflows/ci.yml)


## What is it?
The **epic-jupyter** Python library provides several utilities tailored to run under Jupyter
environments, and to help in writing libraries that adapt nicely to the environment they run in and
its capabilities.


## Main modules

### epic.jupyter.ipython

Allows safe discovery of the current environment.
* `get_ipython()` gets the IPython manager if it is available
* `is_ipython()` tells you whether you're in an IPython-based environment
* `is_jupyter_notebook()` tells you specifically whether you're running in a Jupyter kernel

### epic.jupyter.display

Provides functions related to displaying content.
* `display_if_ipython(...)` allows for safe displaying of objects, with optional graceful degradation to printing
* `markdown("# hey!")` displays preformatted markdown content
* `side_by_side(...)` displays arbitrary objects in a side-by-side table (and also in one-after-the-other columns)

### epic.jupyter.initialization

Provides the function `event_register_once(event, callback, ...)` which registers an IPython event and removes it after
it has triggered for the first time.
This is intended to trigger initialization of internal structures upon some first time event. 

### epic.jupyter.interpolate

Provides the IPython magic `%interpolate` line and cell magic.
This magic is a debug helper: use it to simulate IPython's variable interpolation mechanism and review the results.

Load this extension by calling `%loadext epic.jupyter.interpolate`.

You can also load this and all future extenstions by calling `%loadext epic.jupyter`.