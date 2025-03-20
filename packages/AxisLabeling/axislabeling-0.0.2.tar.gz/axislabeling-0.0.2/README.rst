What is it?
===========

AxisLabeling is a Python package that implements several axis-labeling algorithms. The package is ideal for generating aesthetically pleasing axis tick locations for data visualizations. It includes implementations of:

  - **Heckbert’s algorithm**
  - **Wilkinson’s algorithm**
  - **Extended Wilkinson’s algorithm**
  - **Nelder’s algorithm**
  - **R’s pretty algorithm**
  - **Matplotlib’s algorithm**
  - **Gnuplot’s algorithm**
  - **Sparks’ algorithm**
  - **Thayer & Storer’s algorithm**

Input parameters
================

  - **dmin**: Minimum value of the data range.
  - **dmax**: Maximum value of the data range.
  - **m**: Desired (or target) number of labels.


How to use is it?
=================

```python

from AxisLabeling import Labeler

# Define data range and desired number of labels
dmin, dmax, m = 7.1, 14.1, 4
labeler = Labeler(dmin, dmax, m)

print("Heckbert labels:", labeler.heckbert())
print("Wilkinson labels:", labeler.wilkinson())
print("Extended labels:", labeler.extended())
print("Nelder labels:", labeler.nelder())
print("R pretty labels:", labeler.rpretty())
print("Matplotlib labels:", labeler.matplotlib_labeling())
print("Gnuplot labels:", labeler.gnuplot_labeling())
print("Sparks labels:", labeler.sparks())
print("Thayer labels:", labeler.thayer())

```

Where to get it?
================

`pip install AxisLabeling`


References
============

1. Heckbert, P. S. (1990) Nice numbers for graph labels, Graphics Gems I.
2. Wilkinson, L. (2005) The Grammar of Graphics.
3. Talbot, J., Lin, S., Hanrahan, P. (2010) An Extension of Wilkinson’s Algorithm for Positioning Tick Labels on Axes, InfoVis 2010.
