# Tensor operation library
--------------
![Python 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

**L**ow-**r**ank **t**ensor **c**ompletion using **T**runcated tensor **S**chatten p-**n**orm, LRTC-TSpN.

More tutorials and examples are coming soon!

> This is the code repository for paper 'Truncated tensor Schatten p-norm based approach for spatiotemporal traffic data
imputation with complicated missing patterns' which is published on Transportation Research Part C: Emerging Technologies

## Overview
This project provides some examples about how to use LRTC-TSpN to achieve efficient and accurate missing data imputation for transportation time series data. We aim at performing off-line data imputation tasks, with several realistic structural missing patterns. Missing data imputation problem is modelled as a low-rank tensor completion problem (low-rank tensor learning). The objective is to obtain a fully recovered tensor by minimizing a predefined tensor rank function, given the observations. We define a new **truncated tensor Schatten p-norm** to substitute for the traditional tensor nuclear norm.

## Model description
We organise the multiple input time series data into a third-order tensor structure of (time intervals × locations × days). Schatten p-norm always serves as a better rank surrogate than nuclaer norm, and we can use its nonconvex properity to better approximate tensor rank.

<p align="center">
<img align="middle" src="https://github.com/tongnie/tensorlib/blob/main/Figures/norm_compare.png" width="650" />
</p>

The objective function of Schatten p-norm minimization is formulated as:

<p align="center">
<img align="middle" src="https://github.com/tongnie/tensorlib/blob/main/Figures/objective.png" width="300" height="100"/>
</p>

More details can be found in our paper. The preprint version can be found at [arXiv](https://arxiv.org/abs/2205.09390), and the published version can be found at the TRC publisher.

## Solving algorithm
We solve this non-convex problem by using Alternating Direction Method of Multipliers (ADMM) and Generalized Soft Thresholding (GST).

Generalized soft-thresholding algorithm:

<p align="center">
<img align="middle" src="https://github.com/tongnie/tensorlib/blob/main/Figures/algorithm1.png" width="650" />
</p>

ADMM framework:
<p align="center">
<img align="middle" src="https://github.com/tongnie/tensorlib/blob/main/Figures/algorithm2.png" width="650" />
</p>


## Spatial-temporal data missing patterns
Besides the element-wise random missing case, we define three structured fiber mode-n missing scenarios, which are generated through the two-by-two combinations of tensor mode-n fibers. This can be described as: 
- **’Intervals’ mode fiber-like missing (FM-0)**, which illustrates a temporal missing pattern, is caused by adverse weather, breakdown of wireless connections or apparatus maintenance; 
- **’Locations’ mode fiber-like missing (FM-1)**, which denotes a spatial missing pattern, can be explained by lack of electricity for successive sensors or malfunction of Internet Data Center; 
- **’Days’ mode fiber-like missing (FM-2)** illuminates a spatial-temporal mixture missing situation that they are offline (do not operate) at regular time intervals everyday for specific sensors.

## Datasets
In this repository, we have used two small-size traffic flow datasets to show how to implement our model, they are:  
- **Guangzhou-small**: Speed data with the first 50 locations and the first 15 days. The size is (144 × 50 × 15).
- **Portland-small**: Volume data with the first 80 locations and the first 15 days. The size is (96 × 80 × 15).  

We provide the two datasets in [../Datasets/](https://github.com/tongnie/tensorlib/tree/main/Datasets).
The original links for the complete data are given as following.

- [Guangzhou urban traffic speed data set](https://doi.org/10.5281/zenodo.1205228)
- [Portland highway traffic data set](https://portal.its.pdx.edu/home)

## Examples(coming soon)
We give some examples written in Jupyter notebook [../Examples/](https://github.com/tongnie/tensorlib/blob/main/Examples).  
*To be completed!*

## References

  >Please cite our paper if this repo helps your research.

#### Cited as:
bibtex:

```
@article{nie2022truncated,
  title={Truncated tensor Schatten p-norm based approach for spatiotemporal traffic data imputation with complicated missing patterns},
  author={Nie, Tong and Qin, Guoyang and Sun, Jian},
  journal={arXiv preprint arXiv:2205.09390},
  year={2022}
}
```


License
--------------

This work is released under the MIT license.
