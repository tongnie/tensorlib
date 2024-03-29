# Low-rank tensor completion algorithm for spatiotemporal traffic data imputation 
--------------
![Python 3.8](https://img.shields.io/badge/Python-3.8-blue.svg)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)

**L**ow-**r**ank **t**ensor **c**ompletion using **T**runcated tensor **S**chatten **p**-**N**orm, LRTC-TSpN.


> This is the code repository for paper 'Truncated tensor Schatten p-norm based approach for spatiotemporal traffic data
imputation with complicated missing patterns' which is published on Transportation Research Part C: Emerging Technologies

## Overview
This project provides some examples about how to use LRTC-TSpN to achieve efficient and accurate missing data imputation for transportation time series data. We aim at performing off-line data imputation tasks, with several realistic structural missing patterns. Missing data imputation problem is modelled as a low-rank tensor completion problem (low-rank tensor learning). The objective is to obtain a fully recovered tensor by minimizing a predefined tensor rank function, given the observations. We define a new **truncated tensor Schatten p-norm** to substitute for the traditional tensor nuclear norm. We recommend ones to refer to Kolda and Bader’s review [Tensor Decompositions and Applications](https://epubs.siam.org/doi/abs/10.1137/07070111x) for more basics about tensor algebra.

## Model description
We organise the multiple input time series data into a third-order tensor structure of (time intervals × locations × days). Traditional methods resort to tensor nuclear norm (or sum of nuclear norm) to substitute for the tensor rank, however, these convex surrogates are not powerful in practice. Therefore, we use the newly emerging Schatten p-norm and its truncated version to approximate tensor rank in order to achieve more accurate traffic data imputation.


<p align="center">
<img align="middle" src="https://github.com/tongnie/tensorlib/blob/main/Figures/norm_compare.png" width="650" />
</p>

> Schatten p-norm always serves as a better rank surrogate (closer to the true rank) than nuclaer norm, and we can use its nonconvex properity to better approximate tensor rank.

The objective function of Schatten p-norm minimization is formulated as:

<p align="center">
<img align="middle" src="https://github.com/tongnie/tensorlib/blob/main/Figures/objective.png" width="320" height="100"/>
</p>

This is a typical noncnovex optimization problem. Previous works aiming at solving tensor completion problem always conduct a singular value thresholding (SVT) algorithm. While existing SVT could not be applied to our problem directly. So the main challenge is to develop a new generalized SVT algorithm for this new definition of norm. 

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

Despite of nonconvexity, ADMM framework still ensures the convergence of our model. With proper updating scheme, our algorithm can converge with fewer iterations. More algorithmic details can be found in our paper. The preprint version is available at [arXiv](https://arxiv.org/abs/2205.09390), and the published version can be found at the [Elsevier publisher](https://doi.org/10.1016/j.trc.2022.103737).


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

## Implementation
The Python implementation of LRTC-TSpN is given in [../Imputer/](https://github.com/tongnie/tensorlib/blob/main/Imputer.py). The core of the algorithm is the GST and ADMM iteration module. We organize this implementation in a tensor-only way to make it more efficient. Some utils and basic tensor operation functions are provided in [../Helper/](https://github.com/tongnie/tensorlib/blob/main/Helper.py).


## Toy Examples
We give some examples written in Jupyter notebook [../Examples/](https://github.com/tongnie/tensorlib/blob/main/Examples).  

## References

  >Please cite our paper if this repo helps your research.

#### Cited as:
bibtex:

```
@article{nie2022truncated,
  title={Truncated tensor Schatten p-norm based approach for spatiotemporal traffic data imputation with complicated missing patterns},
  author={Nie, Tong and Qin, Guoyang and Sun, Jian},
  journal={Transportation Research Part C: Emerging Technologies},
  volume={141},
  pages={103737},
  year={2022},
  publisher={Elsevier}
}
```

### Our Publications
--------------
- Tong Nie, Guoyang Qin, Yunpeng Wang, and Jian Sun (2023). **Towards better traffic volume estimation: Tackling both underdetermined and non-equilibrium problems via a correlation-adaptive graph convolution network**. arXiv preprint arXiv:2303.05660. [[Preprint](https://doi.org/10.48550/arXiv.2303.05660)] [[Code](https://github.com/tongnie/GNN4Flow)]

- Tong Nie, Guoyang Qin, Yunpeng Wang, and Jian Sun (2023). **Correlating sparse sensing for large-scale traffic speed estimation:
A Laplacian-enhanced low-rank tensor kriging approach**. Transportation Research Part C: Emerging Technologies, 152, 104190, [[Preprint](https://doi.org/10.48550/arXiv.2210.11780)] [[DOI](https://doi.org/10.1016/j.trc.2023.104190)] [[Code](https://github.com/tongnie/tensor4kriging)]

- Tong Nie, Guoyang Qin, and Jian Sun (2022). **Truncated tensor Schatten p-norm based approach for spatiotemporal traffic data imputation with complicated missing patterns**. Transportation research part C: emerging technologies, 141, 103737, [[Preprint](https://doi.org/10.48550/arXiv.2205.09390)] [[DOI](https://doi.org/10.1016/j.trc.2022.103737)] [[Code](https://github.com/tongnie/tensorlib)]


License
--------------

This work is released under the MIT license.
