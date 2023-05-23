from Object3D import Object3D
import numpy as np
import os
from PIL import ImageColor, Image

class Print(Object3D):
    def __init__(self):
        pass

    def x_high(self, object3D:Object3D, dir="slice_img", filename="slice.png"):
        self.obj3D_to_png(object3D, 0, -1, dir, filename)

    def x_low(self, object3D:Object3D, dir="slice_img", filename="slice.png"):
        self.obj3D_to_png(object3D, 0, 1, dir, filename)

    def y_high(self, object3D:Object3D, dir="slice_img", filename="slice.png"):
        self.obj3D_to_png(object3D, 1, -1, dir, filename)

    def y_low(self, object3D:Object3D, dir="slice_img", filename="slice.png"):
        self.obj3D_to_png(object3D, 1, 1, dir, filename)

    def z_high(self, object3D:Object3D, dir="slice_img", filename="slice.png"):
        self.obj3D_to_png(object3D, 2, -1, dir, filename)

    def z_low(self, object3D:Object3D, dir="slice_img", filename="slice.png"):
        self.obj3D_to_png(object3D, 2, 1, dir, filename)

    def arr2D_to_img(self, arr2D):
        color_names = ['green', 'yellow', 'orange', 'red', 'purple', 'blue', 'pink', '#339933',
                    '#FF3366', '#CC0066', '#99FFCC', '#3366FF', '#0000CC']
        # 1. Preparing dict for translating vals in arr2D into rgb color
        uniq_vals = np.unique(arr2D)
        colors_len = len(color_names)
        uniq_len = len(uniq_vals)
        if colors_len > uniq_len:
            color_names = color_names[0:uniq_len]
        else:
            # repeat colors
            for i in range(uniq_len - colors_len):
                color_names.append(color_names[i % colors_len])
        colors_rgb = [ImageColor.getrgb(c) for c in color_names]
        trans_color = dict(zip(uniq_vals, colors_rgb))
        # 2. New array with rgb values
        new_arr2D = np.zeros((arr2D.shape[0], arr2D.shape[1], 3))
        for i in range(new_arr2D.shape[0]):
            for j in range(new_arr2D.shape[1]):
                rgb = trans_color[arr2D[i,j]]
                new_arr2D[i,j,0] = rgb[0]
                new_arr2D[i,j,1] = rgb[1]
                new_arr2D[i,j,2] = rgb[2]
        # 3. Make PIL Image
        PIL_image = Image.fromarray(np.uint8(new_arr2D)).convert('RGB')
        return PIL_image

    def img2png(self, img, dir="slice_img", filename="slice.png"):
        p = os.path.join(dir, filename)
        img.save(p)

    def arr2D_to_png(self, arr2D, dir="slice_img", filename="slice.png"):
        img = self.arr2D_to_img(arr2D)
        self.img2png(img, dir, filename)

    def obj3D_to_png(self, object3D:Object3D, axis, xray, dir="slice_img", filename="slice.png"):
        if xray == 1:
            ax = 0
        elif xray == -1:
            ax = -1
        else:
            ax = None
            ValueError("xray must be in {-1,1}")
        b = object3D.body
        if axis == 0:
            img_arr = b[ax,:,:]
        elif axis == 1:
            img_arr = b[:,ax,:]
        elif axis == 2:
            img_arr = b[:,:,ax]
        else:
            img_arr = None
            ValueError("axis must be in {0,1,2}")
        img = self.arr2D_to_img(img_arr)
        self.img2png(img, dir, filename)
        