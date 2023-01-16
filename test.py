import make_sim_env
import time
import slice
import numpy as np


class Test_make_sim_env:

    def help_file(self):
        help(make_sim_env)

    def test_init(self):
        self.propEnv = make_sim_env.PropEnv()

    def test_vizualize(self):
        # self.propEnv.vizualize()
        self.propEnv.vizualize_vispy()

    def test_vizualize_stride(self):
        # self.propEnv.vizualize_params(stride=(20, 20, 20))
        self.propEnv.vizualize_params(10)

    def test_fill_cube(self):
        self.propEnv.fill_cube(1, [0, 0, 0], end_p=[1.0, 0.25, 0.5])

    def test_all(self):
        self.test_init()
        # self.test_vizualize()
        #from matplotlib import pyplot as plt
        #plt.ion()
        # self.test_vizualize_stride()
        self.test_fill_cube()
        self.test_vizualize()
        self.test_vizualize_stride()
        # self.test_vizualize()


class Test_slice:

    def test_slice_arr():
        a = np.arange(0,100**3).astype(int).reshape(100,100,100)
        a_slice = slice.slice_arr3p(a)
        a_slice3d = a_slice.reshape(a_slice.shape[0],a_slice.shape[1],-1)

        propEnv = make_sim_env.PropEnv(arr=a_slice3d)
        propEnv.vizualize_params(20)

    def save_slice_image1():
        a = np.arange(0,100**3).astype(int).reshape(100,100,100)
        a_slice = slice.slice_arr3p(a)
        slice.save_slice_image(a_slice)

    def save_slice_image2():
        propEnv = make_sim_env.PropEnv()
        propEnv.fill_cube(1, [0, 0, 0], end_p=[1.0, 0.25, 0.5])
        a = propEnv.Env
        a_slice = slice.slice_arr3p(a)
        slice.save_slice_image(a_slice)

    def save_slice_image3():
        propEnv = make_sim_env.PropEnv()
        propEnv.fill_cube(1, [0, 0, 0], end_p=[1.0, 0.25, 0.5])
        a = propEnv.Env
        a_slice = a[:,:,0]
        slice.save_slice_image(a_slice)








if __name__ == '__main__':

    test_make_sim_env = Test_make_sim_env()
    #test_make_sim_env.helpFile()
    test_make_sim_env.test_all()


    # slice tests
    #Test_slice.test_slice_arr()
    Test_slice.save_slice_image2()