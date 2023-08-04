import numpy
from PIL import Image, ImageOps
from scipy.ndimage import label, grey_dilation


def boxes(orig):
    img = ImageOps.grayscale(orig)
    im = numpy.array(img)

    # Inner morphological gradient.
    im = grey_dilation(im, (3, 3)) - im

    # Binarize.
    mean, std = im.mean(), im.std()
    t = mean + std
    im[im < t] = 0
    im[im >= t] = 1

    # Connected components.
    lbl, numcc = label(im)
    # Size threshold.
    min_size = 1400 # pixels
    box = []
    for i in range(1, numcc + 1):
        py, px = numpy.nonzero(lbl == i)

        if len(py) < min_size:

            im[lbl == i] = 0
            continue
        xmin, xmax, ymin, ymax = px.min(), px.max(), py.min(), py.max()
        # Four corners and centroid.
        box.append([
            [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)],
            (numpy.mean(px), numpy.mean(py))])

    return im.astype(numpy.uint8) * 255, box

def boxCardNameSplit(filePath):
    global areas
    orig = Image.open(filePath)
    im, box = boxes(orig)

    images = []
    for b, centroid in box:
        # draw.line(b + [b[0]], fill='yellow')
        #print(b)
        area = (b[0][0], b[0][1], b[2][0], b[2][1])
        cropped_img = orig.crop(area)

        width = cropped_img.width
        if width < 400:
            images.append(cropped_img)
        else:
            if width < 800:
                areas = [(0, 0, width // 2, cropped_img.height), (width // 2, 0, width, cropped_img.height)]
                imgs = [cropped_img.crop(area) for area in areas]
                for img in imgs:
                    images.append(img)
            elif width < 1200:
                oneThird = width // 3
                areas = [(0, 0, oneThird, cropped_img.height), (oneThird, 0, oneThird * 2, cropped_img.height),
                         (oneThird * 2, 0, width, cropped_img.height)]

            imgs = [cropped_img.crop(area) for area in areas]
            for img in imgs:
                if img.height < 200:
                    images.append(img)
                else:
                    print("FIX height card name")
                    nImg = int(img.height/145)
                    print(nImg)
                    for n in range(nImg):
                        print("n step :", str(n))
                        area = (0, int(img.height/nImg)*n, img.width, int(img.height/nImg)*(n+1))
                        images.append(img.crop(area))
    return images