from Object3D import Object3D
from ColorPointDF import ColorPointDF
import numpy as np
import os
import pandas as pd
from PIL import ImageColor, Image
import cv2


class Print(Object3D):
    def __init__(self):
        pass

    def x_high(self, object3D:Object3D, dir="slice_img", filename="slice.png", color_scheme="threshold", connect_lines=None, hide_points=False):
        self.obj3D_to_png(object3D, 0, -1, dir, filename, color_scheme, connect_lines=connect_lines, hide_points=hide_points)

    def x_low(self, object3D:Object3D, dir="slice_img", filename="slice.png", color_scheme="threshold", connect_lines=None, hide_points=False):
        self.obj3D_to_png(object3D, 0, 1, dir, filename, color_scheme, connect_lines=connect_lines, hide_points=hide_points)

    def y_high(self, object3D:Object3D, dir="slice_img", filename="slice.png", color_scheme="threshold", connect_lines=None, hide_points=False):
        self.obj3D_to_png(object3D, 1, -1, dir, filename, color_scheme, connect_lines=connect_lines, hide_points=hide_points)

    def y_low(self, object3D:Object3D, dir="slice_img", filename="slice.png", color_scheme="threshold", connect_lines=None, hide_points=False):
        self.obj3D_to_png(object3D, 1, 1, dir, filename, color_scheme, connect_lines=connect_lines, hide_points=hide_points)

    def z_high(self, object3D:Object3D, dir="slice_img", filename="slice.png", color_scheme="threshold", connect_lines=None, hide_points=False):
        self.obj3D_to_png(object3D, 2, -1, dir, filename, color_scheme, connect_lines=connect_lines, hide_points=hide_points)

    def z_low(self, object3D:Object3D, dir="slice_img", filename="slice.png", color_scheme="threshold", connect_lines=None, hide_points=False):
        self.obj3D_to_png(object3D, 2, 1, dir, filename, color_scheme, connect_lines=connect_lines, hide_points=hide_points)

    def arr2D_to_img_old(self, arr2D):
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
    

    def arr2D_to_img(self, arr2D, color_scheme="threshold"):
        colorPointDF = ColorPointDF()
        df = colorPointDF.from_arr2d(arr2D, color_scheme=color_scheme, drop_values=[0])
        # New array with rgb values
        new_arr2D = np.zeros((arr2D.shape[0], arr2D.shape[1], 3))
        # put default background color
        default_color = ImageColor.getrgb("black")
        new_arr2D[:,:,0] = default_color[0]
        new_arr2D[:,:,1] = default_color[1]
        new_arr2D[:,:,2] = default_color[2]
        # set arr2d
        new_arr2D[df["x_idx"].to_numpy(), df["y_idx"].to_numpy(), :] = df[["R", "G", "B"]].to_numpy()
        # Make PIL Image
        PIL_image = Image.fromarray(np.uint8(new_arr2D)).convert('RGB')
        return PIL_image


    def img2png(self, img, dir="slice_img", filename="slice.png"):
        p = os.path.join(dir, filename)
        img.save(p)

    def arr2D_to_png(self, arr2D, dir="slice_img", filename="slice.png"):
        img = self.arr2D_to_img(arr2D)
        self.img2png(img, dir, filename)

    def obj3D_to_png(self, object3D:Object3D, axis, xray, dir="slice_img", filename="slice.png", color_scheme="threshold", connect_lines=None, hide_points=False):
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
        photons_img = self.arr2D_to_img(img_arr, color_scheme)
        img = self.blend_with_connect_lines(photons_img, connect_lines=connect_lines, hide_points=hide_points)
        self.img2png(img, dir, filename)

    def projectionResultRecordsDF_to_png(self, resultRecordsDF, image_shape, dir="photonwise_projection_img", filename="projection_df.png", connect_lines=None, hide_points=False):
        photons_img = self.projectionResultRecordsDF_to_img(resultRecordsDF, image_shape)
        img = self.blend_with_connect_lines(photons_img, connect_lines=connect_lines, hide_points=hide_points)
        self.img2png(img, dir, filename)

    def projectionResultRecordsDF_to_img(self, resultRecordsDF, image_shape):
        # New array with rgb values
        new_arr2D = np.zeros((image_shape[0], image_shape[1], 3))
        # put default background color
        default_color = ImageColor.getrgb("black")
        new_arr2D[:,:,0] = default_color[0]
        new_arr2D[:,:,1] = default_color[1]
        new_arr2D[:,:,2] = default_color[2]
        # set arr2d
        new_arr2D[resultRecordsDF["x_idx"].to_numpy(), resultRecordsDF["y_idx"].to_numpy(), :] = resultRecordsDF[["R", "G", "B"]].to_numpy()
        # Make PIL Image
        PIL_image = Image.fromarray(np.uint8(new_arr2D)).convert('RGB')
        return PIL_image
    
    def background_img(self, image_shape):
        # New array with rgb values
        new_arr2D = np.zeros((image_shape[0], image_shape[1], 3))
        # put default background color
        default_color = ImageColor.getrgb("black")
        new_arr2D[:,:,0] = default_color[0]
        new_arr2D[:,:,1] = default_color[1]
        new_arr2D[:,:,2] = default_color[2]
        # Make PIL Image
        PIL_image = Image.fromarray(np.uint8(new_arr2D)).convert('RGB')
        return PIL_image
    
    def rgb_to_rgba(self, img):
        img = img.copy()
        if img.mode == "RGB":
            a_channel = Image.new('L', img.size, 255)   # 'L' 8-bit pixels, black and white
            img.putalpha(a_channel)
        return img
    
    def blend_with_connect_lines(self, photons_img: Image.Image, connect_lines=None, hide_points=False):
        if connect_lines is None:
            img = photons_img.copy()
        else:
            image_shape = photons_img.size
            if hide_points:
                background = self.background_img(image_shape)
            else:
                background = photons_img
            arrows = self.connect_lines_img(connect_lines, image_shape)
            arrows_rgba = self.rgb_to_rgba(arrows)
            background_rgba = self.rgb_to_rgba(background)
            #create a mask using RGBA to define an alpha channel to make the overlay transparent
            alpha = 123
            mask = Image.new('RGBA', arrows_rgba.size, (0,0,0,alpha))
            img = Image.composite(background_rgba, arrows_rgba, mask).convert('RGB')
        return img
    
    def connect_lines_img(self, connect_lines: pd.DataFrame, image_shape):
        # Create an empty transparent image
        im = Image.new('RGBA', image_shape, (0,0,0,0))
        # Make into Numpy array so we can use OpenCV drawing functions
        na = np.array(im)
        # Draw arrowed lines
        for i in range(len(connect_lines)):
            x = connect_lines["x_idx"].iloc[i]
            y = connect_lines["y_idx"].iloc[i]
            x2 = connect_lines["x_idx_2"].iloc[i]
            y2 = connect_lines["y_idx_2"].iloc[i]
            r = connect_lines["R"].iloc[i]
            g = connect_lines["G"].iloc[i]
            b = connect_lines["B"].iloc[i]
            a = connect_lines["A"].iloc[i]
            # openCV uses top left corner as (0,0) point
            y = image_shape[1] - y
            y2 = image_shape[1] - y2
            # OpenCV uses BGR rather than RGB
            width = 1
            na = cv2.arrowedLine(na, (x,y), (x2,y2), (b,g,r,a), width)
        # Revert back to PIL Image and save
        img = Image.fromarray(na)
        return img
