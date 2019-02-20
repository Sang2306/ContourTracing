import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

image = cv.imread('leaf.jpg', 0)


def thresholdImage():
    global image
    _, image = cv.threshold(image, 250, 255, cv.THRESH_BINARY)


def matrixOfBinaryImage():
    global image_bin_matrix
    image_bin_matrix = np.array(image)  # chuyen anh binary ve dang ma tran
    p = 0
    for i in range(0, image_bin_matrix.shape[0]):
        for j in range(0, image_bin_matrix.shape[1]):
            if image_bin_matrix[i][j] == 255:
                p = 1
            else:
                p = image_bin_matrix[i][j]
        #     print(p, end=' ')
        # print('\n')


class Point:
    def __init__(self, i, j):
        self.i = i
        self.j = j


def findFirstContourPixel():
    """
    P(i):
    P(j) mo ta cho P(j+1)
    :return:
    """
    for i in range(0, image_bin_matrix.shape[0]):
        for j in range(0, image_bin_matrix.shape[1] - 1):
            Pi, Pj = image_bin_matrix[i][j], image_bin_matrix[i][j + 1]
            if Pi == 255 and Pj == 0:
                print('Cap diem nen-vung xuat phat la {0} va {1}'.format((i-1, j), (i, j + 1)))
                return Point(i, j + 1)


orient = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
ERR = -1


def getNextDirection(pt: Point, dir):
    """
    Tim huong tiep theo cho diem anh
    :param pt: point diem nen_vunf xuat phat
    :param dir: huong kim dong ho
    :return: point direction hoac ERR
    """
    global flag
    pdir = (dir + 7) % 8
    while pdir != dir:
        if pt.i - 1 < 0 or pt.i + 1 > image_bin_matrix.shape[0]:
            break
        if pt.j - 1 < 0 or pt.j + 1 > image_bin_matrix.shape[1]:
            break
        if image_bin_matrix[pt.i + orient[pdir][0]][pt.j + orient[pdir][1]] == 0:
            return pdir
        pdir = (pdir + 7) % 8
    return ERR


def fullContour(pt: Point, dir):
    while True:
        image_bin_matrix[pt.i][pt.j] = 127
        pdir = getNextDirection(pt, dir)
        dir = (pdir + 3) % 8
        if pdir == ERR:
            return ERR
        pt.i += orient[pdir][0]
        pt.j += orient[pdir][1]


def showImage():
    plt.subplot(121), plt.imshow(np.array(image), 'gray'), plt.title('Ảnh gốc')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(image_bin_matrix, 'gray'), plt.title('Ảnh có biên(màu xám)')
    plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == '__main__':
    thresholdImage()
    matrixOfBinaryImage()
    pt = findFirstContourPixel()  # lay cap diem nv xuat phat
    fullContour(pt, 1)
    showImage()
