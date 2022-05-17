import numpy as np
import PIL
from PIL import ImageColor, Image

def p3_to_normal_vec(p1, p2, p3):
    p12 = np.array(p2) - np.array(p1)
    p13 = np.array(p3) - np.array(p1)
    vec = np.cross(p13, p12)
    normal_vec = vec/np.linalg.norm(vec)
    return normal_vec


# NEEDS_REFACTOR
def slice_arr3p(arr, p1=(0,0,0), p2=None, p3=None, clip_idx=False):
    if p3 is None:
        p3 = (arr.shape[0]-1, arr.shape[1]-1, arr.shape[2]-1)
    if p2 is None:
        p2 = (p1[0], (p1[1]+p3[1])//2, p3[2])

    normal_vec = p3_to_normal_vec(p1, p2, p3)
    n = normal_vec

    depth_cords = np.arange(p1[0], p3[0]+1)
    height_cords = np.arange(p1[1], p3[1]+1)
    if clip_idx:
        depth_cords = np.clip(depth_cords, a_min=0, a_max=(arr.shape[0]-1))
        height_cords = np.clip(height_cords, a_min=0, a_max=(arr.shape[1]-1))
    z_vals = np.zeros((len(depth_cords),len(height_cords)))

    # sampling
    for i in range(len(depth_cords)):
        for j in range(len(height_cords)):
            x = depth_cords[i]
            y = height_cords[j]

            '''
            z = (-(n[0]*(x-p1[0]) + n[1]*(y-p1[1]))/n[2]) + p1[2] # doesn't work (but it should...)
            z = (-(n[1]*(x-p1[1]) + n[2]*(y-p1[2]))/n[0]) + p1[0] # doesn't work
            z = (-(n[1]*(x-p1[1]) + n[0]*(y-p1[0]))/n[2]) + p1[2] # doesn't work
            z = (-(n[2]*(x-p1[2]) + n[0]*(y-p1[0]))/n[1]) + p1[1] # works
            z = (-(n[2]*(x-p1[2]) + n[1]*(y-p1[1]))/n[0]) + p1[0] # doesn't work
            '''
            z = (-(n[0]*(x-p1[0]) + n[2]*(y-p1[2]))/n[1]) + p1[1] # works

            z_vals[i,j] = z
    width_cords = np.around(z_vals).astype(int)
    if clip_idx:
        width_cords = np.clip(width_cords, a_min=0, a_max=(arr.shape[2]-1))

    # NEEDS_REFACTOR
    print_debug = False
    if print_debug:
        print(depth_cords)
        print(height_cords)
        print(width_cords)
        print(p1)
        print(p2)
        print(p3)
        print(p3_to_normal_vec(p1,p2,p3))
        for val in width_cords.reshape(-1):
            if val > 99:
                #print(val)
                pass

    out_arr = np.zeros((len(depth_cords),len(height_cords)))
    for i in range(out_arr.shape[0]):
        for j in range(out_arr.shape[1]):
            out_arr[i,j] = arr[depth_cords[i], height_cords[j], width_cords[i,j]]
    return out_arr.astype(int)


def slice2image(slice):
    color_names = ['green', 'yellow', 'orange', 'red', 'purple', 'blue', 'pink', '#339933',
                   '#FF3366', '#CC0066', '#99FFCC', '#3366FF', '#0000CC']
    # 1. Preparing dict for translating vals in slice into rgb color
    uniq_vals = np.unique(slice)
    colors_len = len(color_names)
    uniq_len = len(uniq_vals)
    if colors_len > uniq_len:
        color_names = color_names[0:uniq_len]
    else:
        for i in range(uniq_len - colors_len):
            color_names.append(color_names[i % colors_len])
    colors_rgb = [PIL.ImageColor.getrgb(c) for c in color_names]
    trans_color = dict(zip(uniq_vals, colors_rgb))
    # 2. New array with rgb values
    new_slice = np.zeros((slice.shape[0], slice.shape[1], 3))
    for i in range(new_slice.shape[0]):
        for j in range(new_slice.shape[1]):
            rgb = trans_color[slice[i,j]]
            new_slice[i,j,0] = rgb[0]
            new_slice[i,j,1] = rgb[1]
            new_slice[i,j,2] = rgb[2]
    # 3. Make PIL Image
    PIL_image = Image.fromarray(np.uint8(new_slice)).convert('RGB')
    return PIL_image


def save_slice_image(slice):
    PIL_image = slice2image(slice)
    PIL_image.save('slice.png')



    
