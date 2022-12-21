import math
from math import log2
import numpy
from PIL import Image
import numpy as np


def spliter(array, vectorHeight, vectorWidth):
    blocks = []

    for i in range(0, array.shape[0], vectorHeight):
        for j in range(0, array.shape[1], vectorWidth):
            blocks.append(array[i:i + vectorHeight, j:j + vectorWidth])

    return blocks


def calc_mean(blocks, n, m):
    vec = []
    temp = []
    summ = 0
    for i in range(0, n):
        for j in range(0, m):
            for block in blocks:
                if i >= len(block):
                    break
                if j >= (len(blocks[0])):
                    break
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
            if i >= len(vec1):
                break
            if j >= (len(vec1[i])):
                break
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

    if len(left_blocks) != 0:
        new_vec1 = calc_mean(left_blocks, n, m)
        sol(new_vec1, left_blocks, n, m, k - 1)

    if len(right_blocks) != 0:
        new_vec2 = calc_mean(right_blocks, n, m)
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
        mn = 100000000000000
        for code in code_book:
            if dis(block, code[1], n, m) < mn:
                mn = dis(block, code[1], n, m)
                compressedImage[i][j] = code[0]
        j += 1
        if j == compressedImageSize:
            j = 0
            i += 1

    return code_book, compressedImage


def decoder(codebook, compressedImage, originalHeight, originalWidth, vectorWidth, vectorHeight):
    imgArr = []
    orignalImage = [[0 for i in range(originalHeight)] for j in range(originalWidth)]
    for i in range(0, len(compressedImage)):
        for j in range(0, len(compressedImage)):
            imgArr.append(codebook[compressedImage[i][j]][1])

    imgArr = np.array(imgArr)
    orignalImage = np.array(orignalImage)
    imgArr = imgArr.astype('uint8')
    orignalImage = orignalImage.astype('uint8')

    blockIndex = 0
    for i in range(0, originalHeight, vectorHeight):
        for j in range(0, originalWidth, vectorWidth):
            orignalImage[i:i + vectorHeight, j:j + vectorWidth] = imgArr[blockIndex]
            blockIndex += 1

    return orignalImage


# imgPath = 'two.jpg'
# img = Image.open(imgPath).convert("L")
# original_hight, original_width = img.size
# img = img.resize((1080, 1080))
# imgArr = np.asarray(img)
#
# vector_height = 60
# vector_width = 60
#
# x, y = encode(imgArr, vector_height, vector_width, 16)
# final = decoder(x, y, 1080, 1080, vector_height, vector_width)
# savePath = 'X.jpg'
#
# decodedImg = Image.fromarray(final)
# decodedImg = decodedImg.resize((original_hight, original_width))
# decodedImg.save(savePath)
#
#
#
#
# original_image_size = original_hight * original_width * 8
# number_of_blocks = (original_hight * original_width) / (vector_height * vector_width)
# label_size = number_of_blocks * log2(number_of_blocks)
# codebook_size = number_of_blocks * vector_height * vector_width * 8
# total_compressed_size = codebook_size + label_size
# compression_ratio = original_image_size / total_compressed_size
#
# file1 = open("Calculation.txt", "w")
# p1 = "Original image size: " + str(original_image_size)
# p2 = "Number of blocks: " + str(number_of_blocks)
# p3 = "Label size: " + str(label_size)
# p4 = "Codebook size: " + str(codebook_size)
# p5 = "Total compressed size: " + str(total_compressed_size)
# p6 = "Compression ratio: " + str(compression_ratio)
# file1.write(p1)
# file1.write(p2)
# file1.write(p3)
# file1.write(p4)
# file1.write(p5)
# file1.write(p6)
# file1.close()
#
# file2 = open("CompressedImage.txt", "w")
# file2.write(str(y))
# file2.close()
#
# file3 = open("Table.txt", "w")
# file3.write(str(x))
# file3.close()


