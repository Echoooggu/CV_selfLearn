# 1st project: poisson image editing, with ten cases testing
## Basic knowledge required: 
numpy, opencv

## Potential problems:
### 1. The source is black when blending into the target
A: uint8 should be float64
### 2. The source is blurred within the mask region in the result.
A: Should probably use MIXED gradient for poisson blending.
