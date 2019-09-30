import os
import cv2
import sys

print("Please input the picture directory path.")
directory_path = input("The picture directory path:")
image_dir = sys.argv[1]
save_dir  = "./picture_reduction_directory"
for image_name in os.listdir(image_dir):
    image = cv2.imread(os.path.join(image_dir,image_name))
    w,h,c = image.shape
    print(image.shape,w,h)
    dst = cv2.resize(image,(85*2,122*2),interpolation=cv2.INTER_AREA)
    cv2.imwrite(os.path.join(save_dir,image_name.replace(".JPG",".png")),dst)
