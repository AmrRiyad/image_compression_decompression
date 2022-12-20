import math
from math import log2

import numpy
from PIL import Image
import numpy as np


def spliter(array, vectorHeight, vectorWidth):
    blocks = []

    for i in range(0, array.shape[0], vectorWidth):
        for j in range(0, array.shape[1], vectorHeight):
            blocks.append(array[i:i + vectorWidth, j:j + vectorHeight])

    return blocks


def calc_mean(blocks, n, m):
    vec = []
    temp = []
    summ = 0
    for i in range(0, n):
        for j in range(0, m):
            for block in blocks:
                summ += block[i][j]
            temp.append(int(summ / len(blocks)))
            summ = 0
        vec.append(temp)
        temp = []
    return vec


def dis(vec1, vec2, n, m):
    summ = 0
    for i in range(0, n):
        for j in range(0, m):
            summ += abs(vec1[i][j] - vec2[i][j])
    return summ


code_book = []
counter = 0


def sol(vec, curr_blocks, n, m, k):
    global code_book
    global counter
    if k == 0:
        code_book.append((counter, vec))
        counter += 1
        return
    curr_vec1 = []
    curr_vec2 = []
    temp = []
    for i in range(n):
        for j in range(m):
            temp.append(vec[i][j] + 1)
        curr_vec1.append(temp)
        temp = []

    for i in range(n):
        for j in range(m):
            temp.append(vec[i][j] - 1)
        curr_vec2.append(temp)
        temp = []

    left_blocks = []
    right_blocks = []

    for i in curr_blocks:
        if dis(i, curr_vec1, n, m) < dis(i, curr_vec2, n, m):
            left_blocks.append(i)
        else:
            right_blocks.append(i)

    new_vec1 = calc_mean(left_blocks, n, m)
    new_vec2 = calc_mean(right_blocks, n, m)

    if len(left_blocks) != 0:
        sol(new_vec1, left_blocks, n, m, k - 1)
    if len(right_blocks) != 0:
        sol(new_vec2, right_blocks, n, m, k - 1)


def encode(data, n, m, k):
    blocks = spliter(data, n, m)

    vec = calc_mean(blocks, n, m)
    sol(vec, blocks, n, m, int(log2(k)))

    compressedImageSize = int(math.ceil(math.sqrt(len(blocks))))
    compressedImage = [[-1 for i in range(compressedImageSize)] for j in range(compressedImageSize)]

    i = 0
    j = 0

    for block in blocks:
        mn = 1000000000000
        for code in code_book:
            if dis(block, code[1], n, m) < mn:
                compressedImage[i][j] = code[0]
        j += 1
        if j == compressedImageSize:
            j = 0
            i += 1

    return code_book, compressedImage


def decoder(codebook, compressedImage, originalSize, vectorWidth, vectorHeight):
    imgArr = []
    orignalImage = [[0 for i in range(originalSize)] for j in range(originalSize)]
    for i in range(0, len(compressedImage)):
        for j in range(0, len(compressedImage)):
            imgArr.append(codebook[compressedImage[i][j]])

    imgArr = np.array(imgArr)
    orignalImage = np.array(orignalImage)
    imgArr = imgArr.astype('uint8')
    orignalImage = orignalImage.astype('uint8')

    blockIndex = 0
    for i in range(0, originalSize, vectorWidth):
        for j in range(0, originalSize, vectorHeight):
            orignalImage[i:i + vectorWidth, j:j + vectorHeight] = imgArr[blockIndex]
            blockIndex += 1

    return orignalImage


imgPath = 'one.jpg'
img = Image.open(imgPath).convert("L")
imgArr = np.asarray(img)

x, y = encode(imgArr, 3, 3, 4)
final = decoder(x, y, 1080, 3, 3)
savePath = 'something.png'
print("hi")
decodedImg = Image.fromarray(final)
decodedImg.save(savePath)  # will save it as gray image
