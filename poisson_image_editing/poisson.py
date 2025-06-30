import numpy as np
from scipy.sparse import linalg as linalg
from scipy.sparse import lil_matrix as lil_matrix

inside = 0
edge = 1
outside = 2

def get_surrounding_coordinates(index):     #给定index，返回四个邻近索引
    i, j = index
    return [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]

def mask_nonzero_indicies(mask):        #返回给定图像（此处是为了掩码）中非零区域的所有坐标
    nonzero = np.nonzero(mask) #返回一个元组，每个元素是一个数组array，每个array存的是每个维度上的索引
    return list(zip(nonzero[0], nonzero[1])) #把两个维度的数组组合成坐标形式，这里返回的是所有点

def lapl_at_index(source, index):
    i, j = index
    h, w = source.shape
    center = 4 * source[i, j]
    up = source[i - 1, j] if i - 1 >= 0 else 0
    down = source[i + 1, j] if i + 1 < h else 0
    left = source[i, j - 1] if j - 1 >= 0 else 0
    right = source[i, j + 1] if j + 1 < w else 0
    return center - (up + down + left + right)


def process(source, target, mask):
    binary_mask = (mask > 0).astype(np.uint8)
    source = source.astype(np.float64)
    target = target.astype(np.float64)

    h, w = source.shape
    indicies = mask_nonzero_indicies(binary_mask)
    index_map = {pt: i for i, pt in enumerate(indicies)}
    N = len(indicies)

    A = lil_matrix((N, N))
    b = np.zeros(N)

    for i, index in enumerate(indicies):
        A[i, i] = 4
        b_i = 0

        for pt in get_surrounding_coordinates(index):
            si, sj = index
            ti, tj = pt

            if not (0 <= ti < h and 0 <= tj < w):
                continue

            source_grad = source[si, sj] - source[ti, tj]
            target_grad = target[si, sj] - target[ti, tj]

            # Mixed gradient: choose the one with larger magnitude
            v = source_grad if abs(source_grad) > abs(target_grad) else target_grad
            b_i += v

            if pt in index_map:
                j = index_map[pt]
                A[i, j] = -1
            else:
                b_i += target[ti, tj]

        b[i] = b_i

    x = linalg.cg(A.tocsr(), b)[0]
    result = np.copy(target)
    for i, index in enumerate(indicies):
        result[index] = np.clip(x[i], 0, 255)
    return result.astype(np.uint8)

# def process(source, target, mask):
#     binary_mask = (mask > 0).astype(np.uint8) # 二值化的mask
#     source = source.astype(np.float64)
#     target = target.astype(np.float64)
#
#     h, w = source.shape
#     indicies = mask_nonzero_indicies(binary_mask)
#     index_map = {pt: i for i, pt in enumerate(indicies)}
#     N = len(indicies)
#
#     A = lil_matrix((N, N))
#     b = np.zeros(N)
#
#     for i, index in enumerate(indicies):
#         A[i, i] = 4
#         b[i] = lapl_at_index(source, index)
#
#         for pt in get_surrounding_coordinates(index):
#             if pt not in index_map:
#                 if 0 <= pt[0] < h and 0 <= pt[1] < w:
#                     b[i] += target[pt]
#             else:
#                 j = index_map[pt]
#                 A[i, j] = -1
#
#     x = linalg.cg(A.tocsr(), b)[0]
#     result = np.copy(target)
#     for i, index in enumerate(indicies):
#         result[index] = np.clip(x[i], 0, 255)
#     return result.astype(np.uint8)