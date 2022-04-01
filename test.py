import make_sim_env
import time


class Test_make_sim_env:

    def help_file(self):
        help(make_sim_env)

    def test_init(self):
        self.propEnv = make_sim_env.PropEnv()

    def test_vizualize(self):
        self.propEnv.vizualize()

    def test_vizualize_stride(self):
        # self.propEnv.vizualize_params(stride=(20, 20, 20))
        self.propEnv.vizualize_params(20)

    def test_fill_cube(self):
        self.propEnv.fill_cube(1, [0, 0, 0], end_p=[1.0, 0.25, 0.5])

    def test_all(self):
        self.test_init()
        # self.test_vizualize()
        #from matplotlib import pyplot as plt
        #plt.ion()
        self.test_vizualize_stride()
        self.test_fill_cube()
        self.test_vizualize_stride()



if __name__ == '__main__':

    test_make_sim_env = Test_make_sim_env()
    #test_make_sim_env.helpFile()
    test_make_sim_env.test_all()