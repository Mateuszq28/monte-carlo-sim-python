from Object3D import Object3D
from ColorPointDF import ColorPointDF
from ArrowsDF import ArrowsDF
import numpy as np
import os
import math
import pandas as pd
from PIL import ImageColor, ImageDraw, Image
import cv2
# pip3 install opencv-python


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
        # decide if put empty rows and columns between data points (decide in seperate cases)
        if connect_lines is None:
            do_sparse = False
        else:
            do_sparse = True
        # do sparse data
        if do_sparse:
            put_num = 20
            # sparse background with photons
            photons_img = photons_img.copy()
            photons_img = self.make_img_sparse(photons_img, put_num=put_num)
            # sparse arrows
            if connect_lines is not None:
                connect_lines = connect_lines.copy()
                connect_lines = ArrowsDF.make_sparse(connect_lines, put_num)
        img = self.blend_with_connect_lines(photons_img, connect_lines=connect_lines, hide_points=hide_points)
        self.img2png(img, dir, filename)

    def projectionResultRecordsDF_to_png(self, resultRecordsDF, image_shape, dir="photonwise_projection_img", filename="projection_df.png", connect_lines=None, hide_points=False):
        # decide if put empty rows and columns between data points (decide in seperate cases)
        if connect_lines is None:
            do_sparse = False
        else:
            do_sparse = True
        # do sparse data
        if do_sparse:
            put_num = 20
            image_shape = image_shape.copy()
            image_shape[0] = image_shape[0] * (put_num+1)
            image_shape[1] = image_shape[1] * (put_num+1)
            # sparse background with photons
            resultRecordsDF = resultRecordsDF.copy()
            resultRecordsDF = ColorPointDF.make_sparse(resultRecordsDF, put_num=put_num)
            # sparse arrows
            if connect_lines is not None:
                connect_lines = connect_lines.copy()
                connect_lines = ArrowsDF.make_sparse(connect_lines, put_num)
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
        indices = resultRecordsDF[["x_idx", "y_idx"]].round().to_numpy(dtype=int)
        new_arr2D[indices[:,0], indices[:,1], :] = resultRecordsDF[["R", "G", "B"]].to_numpy()
        # Make PIL Image
        PIL_image = Image.fromarray(np.uint8(new_arr2D)).convert('RGB')
        return PIL_image
    
    def background_img(self, image_size):
        # New array with rgb values
        # new_arr2D = np.zeros((image_size[0], image_size[1], 3))
        # put default background color
        # default_color = ImageColor.getrgb("black")
        # new_arr2D[:,:,0] = default_color[0]
        # new_arr2D[:,:,1] = default_color[1]
        # new_arr2D[:,:,2] = default_color[2]
        # Make PIL Image
        # PIL_image = Image.fromarray(np.uint8(new_arr2D)).convert('RGB')
        PIL_image = Image.new('RGB', image_size, (0,0,0))
        return PIL_image
    
    def rgb_to_rgba(self, img):
        img = img.copy()
        if img.mode == "RGB":
            a_channel = Image.new('L', img.size, 255)   # 'L' 8-bit pixels, black and white
            img.putalpha(a_channel)
        return img
    
    def blend_with_connect_lines(self, photons_img: Image.Image, connect_lines=None, hide_points=False):
        # blending
        if connect_lines is None:
            img = photons_img
        else:
            image_size = photons_img.size
            if hide_points:
                background = self.background_img(image_size)
            else:
                background = photons_img
            arrows_rgba = self.connect_lines_img_pil(connect_lines, image_size)
            background_rgba = self.rgb_to_rgba(background)
            #create a mask using RGBA to define an alpha channel to make the overlay transparent
            alpha = 220
            # mask = Image.new('RGBA', arrows_rgba.size, (0,0,0,alpha))
            # mask = Image.new('L', arrows_rgba.size, alpha)
            mask = arrows_rgba.copy().convert('L')
            mask = mask.point( lambda p: alpha if p > 0 else 0 )
            img = Image.composite(arrows_rgba, background_rgba, mask).convert('RGB')
        return img
    
    def connect_lines_img_cv2(self, connect_lines: pd.DataFrame, image_size):
        # Create an empty transparent image
        im = Image.new('RGBA', image_size, (0,0,0,0))
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
            x,y,x2,y2,r,g,b,a = [int(val) for val in [x,y,x2,y2,r,g,b,a]]
            if x == x2 and y == y2:
                continue
            # OpenCV uses BGR rather than RGB
            width = 1
            na = cv2.arrowedLine(na, (y,x), (y2,x2), (b,g,r,a), width)
        # to PIL Image
        img = Image.fromarray(na)
        return img
    
    def connect_lines_img_pil(self, connect_lines: pd.DataFrame, image_size):
        # Create an empty transparent image
        im = Image.new('RGBA', image_size, (0,0,0,0))
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
            x,y,x2,y2,r,g,b,a = [int(val) for val in [x,y,x2,y2,r,g,b,a]]
            if x == x2 and y == y2:
                continue
            width = 1
            im = self.arrowedLine(im, ptA=(y,x), ptB=(y2,x2), width=width, color=(r,g,b,a))
        return im
    
    @staticmethod
    def arrowedLine(im, ptA, ptB, width=1, color=(0,255,0,255)):
        """
        Draw line from ptA to ptB with arrowhead at ptB
        source: https://stackoverflow.com/questions/63671018/how-can-i-draw-an-arrow-using-pil
        [modified]
        """
        # Get drawing context
        draw = ImageDraw.Draw(im)
        # Draw the line without arrows
        draw.line((ptA,ptB), width=width, fill=color)
        # Now work out the arrowhead
        # = it will be a triangle with one vertex at ptB
        # - it will start n pixels before ptB
        # - it will extend m pixels either side of the line
        x0, y0 = ptA
        x1, y1 = ptB
        vec_len = np.linalg.norm([x1-x0, y1-y0])
        # Now we can work out the x,y coordinates of the bottom of the arrowhead triangle
        n = 5.0
        xb = x1 - n*(x1-x0)/vec_len
        yb = y1 - n*(y1-y0)/vec_len
        # Work out the other two vertices of the triangle
        # Check if line is vertical
        m = 3
        if x0==x1:
            vtx0 = (xb-m, yb)
            vtx1 = (xb+m, yb)
        # Check if line is horizontal
        elif y0==y1:
            vtx0 = (xb, yb+m)
            vtx1 = (xb, yb-m)
        else:
            alpha = math.atan2(y1-y0,x1-x0)-90*math.pi/180
            a = m*math.cos(alpha)
            b = m*math.sin(alpha)
            # (yx mode)
            vtx0 = (xb+a, yb+b)
            vtx1 = (xb-a, yb-b)
            # (xy mode)
            # vtx0 = (xb+a, yb-b)
            # vtx1 = (xb-a, yb+b)
        # Now draw the arrowhead triangle
        draw.polygon([vtx0, vtx1, ptB], fill=color)
        return im
    
    def make_img_sparse(self, img, put_num):
        scale_factor = put_num+1
        img_arr = np.array(img)
        sh = img_arr.shape
        output_arr = np.full(shape=(sh[0]*scale_factor, sh[1]*scale_factor, 3), fill_value=0.0)
        output_arr[0::scale_factor, 0::scale_factor, :] = img_arr
        output_img = Image.fromarray(np.uint8(output_arr)).convert('RGB')
        return output_img
