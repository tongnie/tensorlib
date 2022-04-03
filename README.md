# Tensor operation library
--------------
![Python 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

Low-rank tensor completion using Truncated tensor Schatten p-norm, LRTC-TSpN.

Tutorials and examples are coming soon!

> This is the code repository for paper 'Truncated tensor Schatten p-norm based approach for spatiotemporal traffic data
imputation with complicated missing patterns' which is submitted to Transportation Research Part C: Emerging Technologies

## Overview
This project provides some examples about how to use the proposed LRTC-TSpN to achieve efficient and accurate missing data imputation in time series data. We aim at performing off-line data imputation tasks.

## Model description
We organise the multiple input time series data into a third-order tensor structure of (time interval$\times$)

## Datasets
In this repository, we have used two small-size traffic flow datasets to show how to implement our model, they are:  
- Guangzhou-small: Speed data with the first 50 locations and the first 15 days. The size is (144 × 50 × 15).
- Portland-small: Volume data with the first 80 locations and the first 15 days. The size is (96 × 80 × 15).
some publicly available data sets into our experiments. The original links for these data are given as following.

- [Guangzhou urban traffic speed data set](https://doi.org/10.5281/zenodo.1205228)
- [Portland highway traffic data set](https://portal.its.pdx.edu/home)


License
--------------

This work is released under the MIT license.
