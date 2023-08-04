import cv2
import numpy as np

img_rgb = cv2.imread('cardimage/4.pdf_page_15.png')
template = cv2.imread('delete.png')
w, h = template.shape[:-1]

res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
threshold = .7
loc = np.where(res >= threshold)
print(len(loc))
for pt in zip(*loc[::-1]):  # Switch columns and rows
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

cv2.imwrite('result.png', img_rgb)