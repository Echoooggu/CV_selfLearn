# 1st project: poisson image editing

## Descriptions
Ten cases, each with a provided source image, a target image, and potentially a mask image. If there is no mask, then draw a mask by mouse through a popped-out window.  
Cannot manipulate where to blend the image in the target.

## Basic knowledge required
numpy, opencv  

## Algorithms（*mixed* poisson blending)
### Seamless image fusion with mixed gradients (preserving dominant structures from either source or target).  
For each pixel, select the gradient with the larger magnitude:  
     \[
     \nabla f_{\text{mixed}} = \arg\max_{\nabla f \in \{\nabla f_{\text{source}}, \nabla f_{\text{target}}\}} \|\nabla f\|
     \]  

## Potential problems
### 1. The mask region is mostly black in the result, with blurred edges.
A: uint8 should be float64
### 2. The source is blurred within the mask region in the result.
A: Should probably use MIXED gradient for poisson blending.
### 3. The mask region seems to be in the middle (or any other position) of the source, but it turns out that the ultimate position of processed source image is not and even seems arbitrary.
A: The source image and the target image should be processed to align with each other.

## Acknowledgements
https://github.com/willemmanuel/poisson-image-editing.git  
[2003 poisson image editing paper](https://github.com/Echoooggu/CV_selfLearn/blob/main/poisson_image_editing/2003%20poisson%20image%20editing.pdf)
