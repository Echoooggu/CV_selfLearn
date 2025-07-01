# 1st project: poisson image editing

## Descriptions
Ten cases, each with a provided source image, a target image, and potentially a mask image. If there is no mask, then draw a mask by mouse through a popped-out window.  
Cannot manipulate where to blend the image in the target.

## Basic knowledge required
numpy, opencv  

## Algorithms

## Potential problems
### 1. The source is black when blending into the target
A: uint8 should be float64
### 2. The source is blurred within the mask region in the result.
A: Should probably use MIXED gradient for poisson blending.

## Acknowledgements
https://github.com/willemmanuel/poisson-image-editing.git  
[2003 poisson image editing paper](https://github.com/Echoooggu/CV_selfLearn/blob/main/poisson_image_editing/2003%20poisson%20image%20editing.pdf)
