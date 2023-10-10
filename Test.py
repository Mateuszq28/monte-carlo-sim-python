from FeatureSampling import *
from SumProjection import SumProjection
import matplotlib.pyplot as plt
import math
import numpy as np
from Slice import Slice
import time
from Object3D import *
from PropEnv import *
from ByMatplotlib import *
from ByVispy import *
from Print import *
from Projection import *
from Sim import Sim
import matplotlib.pyplot as plt
import numpy as np
from ResultEnvProcessing import ResultEnvProcessing

class Test():

    myRandom = MyRandom()

    def __init__(self):
        pass

    class Test_MonteCarloSampling():
        def __init__(self):
            pass

        def exp1(self):
            monteCarloSampling = MonteCarloSampling()

            # funOrigin
            a = 1
            scope = np.append(np.arange(0,10,0.01), 10)
            y = [monteCarloSampling.exp1.function(a=a, s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "exp1(a,s) = math.exp(-a*s)/a |a={}| = math.exp(-{}*s)/{}".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp1.function_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp1.function_label.xlabel
            ylabel = monteCarloSampling.exp1.function_label.ylabel
            # plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funIntegral scope
            scope = np.append(np.arange(0,10,0.01), 10)
            a = 1
            y = [monteCarloSampling.exp1.integral(a=a, s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "(-math.exp(-a*s))/a**2 |a={}| = (-math.exp(-{}*s))/{}**2".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp1.integral_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp1.integral_label.xlabel
            ylabel = monteCarloSampling.exp1.integral_label.ylabel
            # plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funDistribution scope
            scope = np.append(np.arange(0,10,0.01), 10)
            a = 1
            y = [monteCarloSampling.exp1.distribution(a=a, s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "F(s) = RND = (1 - exp(-as))/a**2 |a={}| = (1 - exp(-{}s))/{}**2".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp1.distribution_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp1.distribution_label.xlabel
            ylabel = monteCarloSampling.exp1.distribution_label.ylabel
            # plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funSampling
            a = 1
            rnd_min = monteCarloSampling.exp1.distribution(a=a, s=0)
            rnd_max = monteCarloSampling.exp1.distribution(a=a, s=10)
            # rnd_min = 0.0
            # rnd_max = 0.99999
            scope = np.append(np.arange(rnd_min, rnd_max, 0.01), rnd_max)
            y = [monteCarloSampling.exp1.functionForSampling(a=a, rnd=x) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            title = "math.log(1 - a**2 * RND) / -a |a={}| = math.log(1 - {}**2 * RND) / -{}".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp1.functionForSampling_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp1.functionForSampling_label.xlabel
            ylabel = monteCarloSampling.exp1.functionForSampling_label.ylabel
            # plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()


        def exp2(self, a=1):
            monteCarloSampling = MonteCarloSampling()

            # funOrigin
            scope = np.arange(-5,15,0.01)
            y = [monteCarloSampling.exp2.function(a=a, s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "exp1(a,s) = math.exp(-a*s)/a |a={}| = math.exp(-{}*s)/{}".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp2.function_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp2.function_label.xlabel
            ylabel = monteCarloSampling.exp2.function_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funIntegral scope
            scope = np.arange(-5,15,0.01)
            y = [monteCarloSampling.exp2.integral(a=a, s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "(-math.exp(-a*s))/a**2 |a={}| = (-math.exp(-{}*s))/{}**2".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp2.integral_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp2.integral_label.xlabel
            ylabel = monteCarloSampling.exp2.integral_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funDistribution scope
            scope = np.arange(-5,15,0.01)
            y = [monteCarloSampling.exp2.distribution(a=a, s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "F(s) = RND = (1 - exp(-as))/a**2 |a={}| = (1 - exp(-{}s))/{}**2".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp2.distribution_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp2.distribution_label.xlabel
            ylabel = monteCarloSampling.exp2.distribution_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funSampling
            rnd_min = monteCarloSampling.exp2.distribution(a=a, s=0)
            rnd_max = monteCarloSampling.exp2.distribution(a=a, s=10)
            scope = np.append(np.arange(rnd_min, rnd_max, 0.01), rnd_max)
            y = [monteCarloSampling.exp2.functionForSampling(a=a, rnd=x) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "math.log(1 - a**2 * RND) / -a |a={}| = math.log(1 - {}**2 * RND) / -{}".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp2.functionForSampling_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp2.functionForSampling_label.xlabel
            ylabel = monteCarloSampling.exp2.functionForSampling_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()


        def parabola1(self):
            monteCarloSampling = MonteCarloSampling()

            # funOrigin
            scope = np.append(np.arange(-math.pi,math.pi,0.01), math.pi)
            y = [monteCarloSampling.parabola1.function(x=x) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope/math.pi, y)
            # title = "p(s) = parabola1(s) = -s**2 + math.pi**2"
            title = monteCarloSampling.parabola1.function_label.title
            xlabel = monteCarloSampling.parabola1.function_label.xlabel
            ylabel = monteCarloSampling.parabola1.function_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # # funIntegral
            # scope = np.arange(-6,6,0.01)
            # y = [monteCarloSampling.parabola1.integral(s=s) for s in scope]
            # print('y[0] =', y[0])
            # print('y[-1] =', y[-1])
            # if len(y) == 1:
            #     plt.scatter(scope, y)
            # else:
            #     plt.plot(scope, y)
            # # title = "(math.pi**2)*x-(x**3)/3"
            # title = monteCarloSampling.parabola1.integral_label.title
            # xlabel = monteCarloSampling.parabola1.integral_label.xlabel
            # ylabel = monteCarloSampling.parabola1.integral_label.ylabel
            # plt.title(title)
            # plt.xlabel(xlabel)
            # plt.ylabel(ylabel)
            # # lines that show how roots of the equation will be changing with adding (-rnd) value
            # int_max = monteCarloSampling.parabola1.integral(s=math.pi)
            # int_min = monteCarloSampling.parabola1.integral(s=-math.pi)
            # avg = (int_min + int_max)/2
            # plt.plot([-math.pi, math.pi], [int_min, int_min], 'g--')
            # plt.plot([-math.pi, math.pi], [avg, avg], 'g--')
            # plt.plot([-math.pi, math.pi], [int_max, int_max], 'g--')
            # plt.show()

            # funDistribution
            scope = np.arange(-6,6,0.01)
            y = [monteCarloSampling.parabola1.distribution(s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "F(s) = RND = -1/3(x-2*pi)(x+pi)^2 = -1/3x^3 + pi^2*x + 2/3*pi^3"
            title = monteCarloSampling.parabola1.distribution_label.title
            xlabel = monteCarloSampling.parabola1.distribution_label.xlabel
            ylabel = monteCarloSampling.parabola1.distribution_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            # lines that show how roots of the equation will be changing with adding (-rnd) value
            rnd_max = monteCarloSampling.parabola1.distribution(s=math.pi)
            plt.plot([-math.pi, math.pi], [0, 0], 'g--')
            plt.plot([-math.pi, math.pi], [rnd_max/2, rnd_max/2], 'g--')
            plt.plot([-math.pi, math.pi], [rnd_max, rnd_max], 'g--')
            plt.show()

            # # funIntegral scope
            # scope = np.append(np.arange(-math.pi,math.pi,0.01), math.pi)
            # y = [monteCarloSampling.parabola1.integral(s=s) for s in scope]
            # print('y[0] =', y[0])
            # print('y[-1] =', y[-1])
            # if len(y) == 1:
            #     plt.scatter(scope, y)
            # else:
            #     plt.plot(scope, y)
            # # title = "(math.pi**2)*x-(x**3)/3"
            # title = monteCarloSampling.parabola1.integral_label.title
            # xlabel = monteCarloSampling.parabola1.integral_label.xlabel
            # ylabel = monteCarloSampling.parabola1.integral_label.ylabel
            # plt.title(title)
            # plt.xlabel(xlabel)
            # plt.ylabel(ylabel)
            # plt.show()

            # funDistribution scope
            scope = np.append(np.arange(-math.pi,math.pi,0.01), math.pi)
            y = [monteCarloSampling.parabola1.distribution(s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "F(s) = RND = -1/3(x-2*pi)(x+pi)^2 = -1/3x^3 + pi^2*x + 2/3*pi^3"
            title = monteCarloSampling.parabola1.distribution_label.title
            xlabel = monteCarloSampling.parabola1.distribution_label.xlabel
            ylabel = monteCarloSampling.parabola1.distribution_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funSampling
            rnd_min = monteCarloSampling.parabola1.distribution(s=-math.pi)
            rnd_max = monteCarloSampling.parabola1.distribution(s=math.pi)
            scope = np.append(np.arange(rnd_min,rnd_max,0.01), rnd_max)
            y = [monteCarloSampling.parabola1.functionForSampling(rnd=x, filt_roots=True) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            title = monteCarloSampling.parabola1.functionForSampling_label.title
            xlabel = monteCarloSampling.parabola1.functionForSampling_label.xlabel
            ylabel = monteCarloSampling.parabola1.functionForSampling_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

        def parabola2(self):
            monteCarloSampling = MonteCarloSampling()

            # funOrigin
            scope = np.append(np.arange(-math.pi,math.pi,0.01), math.pi)
            y = [monteCarloSampling.parabola2.function(x=x) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope/math.pi, y)
            title = monteCarloSampling.parabola2.function_label.title
            xlabel = monteCarloSampling.parabola2.function_label.xlabel
            ylabel = monteCarloSampling.parabola2.function_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # # funIntegral
            # scope = np.arange(-6,6,0.01)
            # y = [monteCarloSampling.parabola2.integral(s=s) for s in scope]
            # print('y[0] =', y[0])
            # print('y[-1] =', y[-1])
            # if len(y) == 1:
            #     plt.scatter(scope, y)
            # else:
            #     plt.plot(scope, y)
            # # title = "(math.pi**2)*x-(x**3)/3"
            # title = monteCarloSampling.parabola2.integral_label.title
            # xlabel = monteCarloSampling.parabola2.integral_label.xlabel
            # ylabel = monteCarloSampling.parabola2.integral_label.ylabel
            # plt.title(title)
            # plt.xlabel(xlabel)
            # plt.ylabel(ylabel)
            # # lines that show how roots of the equation will be changing with adding (-rnd) value
            # int_max = monteCarloSampling.parabola2.integral(s=math.pi)
            # int_min = monteCarloSampling.parabola2.integral(s=-math.pi)
            # avg = (int_min + int_max)/2
            # plt.plot([-math.pi, math.pi], [int_min, int_min], 'g--')
            # plt.plot([-math.pi, math.pi], [avg, avg], 'g--')
            # plt.plot([-math.pi, math.pi], [int_max, int_max], 'g--')
            # plt.show()

            # funDistribution
            scope = np.arange(-6,6,0.01)
            y = [monteCarloSampling.parabola2.distribution(s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "F(s) = RND = -1/3(x-2*pi)(x+pi)^2 = -1/3x^3 + pi^2*x + 2/3*pi^3"
            title = monteCarloSampling.parabola2.distribution_label.title
            xlabel = monteCarloSampling.parabola2.distribution_label.xlabel
            ylabel = monteCarloSampling.parabola2.distribution_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            # lines that show how roots of the equation will be changing with adding (-rnd) value
            rnd_max = monteCarloSampling.parabola2.distribution(s=math.pi)
            plt.plot([-math.pi, math.pi], [0, 0], 'g--')
            plt.plot([-math.pi, math.pi], [rnd_max/2, rnd_max/2], 'g--')
            plt.plot([-math.pi, math.pi], [rnd_max, rnd_max], 'g--')
            plt.show()

            # # funIntegral scope
            # scope = np.append(np.arange(-math.pi,math.pi,0.01), math.pi)
            # y = [monteCarloSampling.parabola2.integral(s=s) for s in scope]
            # print('y[0] =', y[0])
            # print('y[-1] =', y[-1])
            # if len(y) == 1:
            #     plt.scatter(scope, y)
            # else:
            #     plt.plot(scope, y)
            # # title = "(math.pi**2)*x-(x**3)/3"
            # title = monteCarloSampling.parabola2.integral_label.title
            # xlabel = monteCarloSampling.parabola2.integral_label.xlabel
            # ylabel = monteCarloSampling.parabola2.integral_label.ylabel
            # plt.title(title)
            # plt.xlabel(xlabel)
            # plt.ylabel(ylabel)
            # plt.show()

            # funDistribution scope
            scope = np.append(np.arange(-math.pi,math.pi,0.01), math.pi)
            y = [monteCarloSampling.parabola2.distribution(s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "F(s) = RND = -1/3(x-2*pi)(x+pi)^2 = -1/3x^3 + pi^2*x + 2/3*pi^3"
            title = monteCarloSampling.parabola2.distribution_label.title
            xlabel = monteCarloSampling.parabola2.distribution_label.xlabel
            ylabel = monteCarloSampling.parabola2.distribution_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funSampling
            rnd_min = monteCarloSampling.parabola2.distribution(s=-math.pi)
            rnd_max = monteCarloSampling.parabola2.distribution(s=math.pi)
            rnd_min = 0.01
            rnd_max = 0.99
            # rnd_max = 40
            scope = np.append(np.arange(rnd_min,rnd_max,0.01), rnd_max)
            y = [monteCarloSampling.parabola2.functionForSampling(rnd=x, filt_roots=True) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            title = monteCarloSampling.parabola2.functionForSampling_label.title
            xlabel = monteCarloSampling.parabola2.functionForSampling_label.xlabel
            ylabel = monteCarloSampling.parabola2.functionForSampling_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()


        def normal_scope(self, min_s_scope=-math.pi, max_s_scope=math.pi, loc=0, scale=1):
            monteCarloSampling = MonteCarloSampling()

            # funOrigin
            scope = np.append(np.arange(min_s_scope, max_s_scope, 0.01), max_s_scope)
            y = [monteCarloSampling.normal.function(x=x, loc=loc, scale=scale) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "p(s) = parabola1(s) = -s**2 + math.pi**2"
            title = monteCarloSampling.normal.function_label.title
            xlabel = monteCarloSampling.normal.function_label.xlabel
            ylabel = monteCarloSampling.normal.function_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funIntegral
            m = max(abs(min_s_scope), abs(max_s_scope))
            scope = np.arange(-m*2.5,m*2.5,0.01)
            y = [monteCarloSampling.normal.integral(x=x, loc=loc, scale=scale) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "(math.pi**2)*x-(x**3)/3"
            title = monteCarloSampling.normal.integral_label.title
            xlabel = monteCarloSampling.normal.integral_label.xlabel
            ylabel = monteCarloSampling.normal.integral_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            # lines that show how roots of the equation will be changing with adding (-rnd) value
            int_min = monteCarloSampling.normal.integral(x=min_s_scope, loc=loc, scale=scale)
            int_max = monteCarloSampling.normal.integral(x=max_s_scope, loc=loc, scale=scale)
            avg = (int_min + int_max)/2
            plt.plot([min_s_scope, max_s_scope], [int_min, int_min], 'g--')
            plt.plot([min_s_scope, max_s_scope], [avg, avg], 'g--')
            plt.plot([min_s_scope, max_s_scope], [int_max, int_max], 'g--')
            plt.show()

            # funDistribution
            m = max(abs(min_s_scope), abs(max_s_scope))
            scope = np.arange(-m*2.5,m*2.5,0.01)
            y = [monteCarloSampling.normal.distribution(x=s, loc=loc, scale=scale) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "F(s) = RND = -1/3(x-2*pi)(x+pi)^2 = -1/3x^3 + pi^2*x + 2/3*pi^3"
            title = monteCarloSampling.normal.distribution_label.title
            xlabel = monteCarloSampling.normal.distribution_label.xlabel
            ylabel = monteCarloSampling.normal.distribution_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            # lines that show how roots of the equation will be changing with adding (-rnd) value
            rnd_min = monteCarloSampling.normal.distribution(x=min_s_scope, loc=loc, scale=scale)
            rnd_max = monteCarloSampling.normal.distribution(x=max_s_scope, loc=loc, scale=scale)
            avg = (rnd_min + rnd_max)/2
            plt.plot([min_s_scope, max_s_scope], [rnd_min, rnd_min], 'g--')
            plt.plot([min_s_scope, max_s_scope], [avg, avg], 'g--')
            plt.plot([min_s_scope, max_s_scope], [rnd_max, rnd_max], 'g--')
            plt.show()

            # funIntegral scope
            scope = np.append(np.arange(min_s_scope, max_s_scope, 0.01), max_s_scope)
            y = [monteCarloSampling.normal.integral(x=s, loc=loc, scale=scale) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "(math.pi**2)*x-(x**3)/3"
            title = monteCarloSampling.normal.integral_label.title
            xlabel = monteCarloSampling.normal.integral_label.xlabel
            ylabel = monteCarloSampling.normal.integral_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funDistribution scope
            scope = np.append(np.arange(min_s_scope, max_s_scope, 0.01), max_s_scope)
            y = [monteCarloSampling.normal.distribution(x=s, loc=loc, scale=scale) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "F(s) = RND = -1/3(x-2*pi)(x+pi)^2 = -1/3x^3 + pi^2*x + 2/3*pi^3"
            title = monteCarloSampling.normal.distribution_label.title
            xlabel = monteCarloSampling.normal.distribution_label.xlabel
            ylabel = monteCarloSampling.normal.distribution_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funSampling
            scope = np.arange(0, 1000, 1)
            # y = monteCarloSampling.normal.functionForSampling(loc=loc, scale=scale, size=len(scope))
            y = [monteCarloSampling.normal.functionForSampling(loc=loc, scale=scale) for _ in scope]
            y.sort()
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "roots(poly) = roots(parabola1(s) - RND) dla s w <{}, {}>".format(min_s_scope, max_s_scope)
            title = monteCarloSampling.normal.functionForSampling_label.title
            xlabel = monteCarloSampling.normal.functionForSampling_label.xlabel
            ylabel = monteCarloSampling.normal.functionForSampling_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

        

        def exp1_scope(self, min_s_scope=0, max_s_scope=10, a=1):
            """
            using FunDistibution.exp1_d and FunSampling.exp1_d
            (dynamic scope in definite integral to accomplish dynamic distribution function)
            """
            monteCarloSampling = MonteCarloSampling()

            # funOrigin
            scope = np.append(np.arange(min_s_scope, max_s_scope,0.01), max_s_scope)
            y = [monteCarloSampling.exp1_d.function(a=a, s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "exp1(a,s) = math.exp(-a*s)/a |a={}| = math.exp(-{}*s)/{}".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp1_d.function_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp1_d.function_label.xlabel
            ylabel = monteCarloSampling.exp1_d.function_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funIntegral scope
            scope = np.append(np.arange(min_s_scope ,max_s_scope, 0.01), max_s_scope)
            y = [monteCarloSampling.exp1_d.integral(a=a, s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "math.log(1 - a**2 * RND) / -a |a={}| = math.log(1 - {}**2 * RND) / -{}".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp1_d.integral_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp1_d.integral_label.xlabel
            ylabel = monteCarloSampling.exp1_d.integral_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funDistribution scope
            scope = np.append(np.arange(min_s_scope, max_s_scope, 0.01), max_s_scope)
            y = [monteCarloSampling.exp1_d.distribution(a=a, s1=min_s_scope, s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "F(s) = RND = (1 - exp(-as))/a**2 |a={}| = (1 - exp(-{}s))/{}**2".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp1_d.distribution_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp1_d.distribution_label.xlabel
            ylabel = monteCarloSampling.exp1_d.distribution_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funSampling
            rnd_min = monteCarloSampling.exp1_d.distribution(a=a, s1=min_s_scope, s=min_s_scope)
            rnd_max = monteCarloSampling.exp1_d.distribution(a=a, s1=min_s_scope, s=max_s_scope)
            print("rnd_min =", rnd_min)
            print("rnd_max =", rnd_max)
            scope = np.append(np.arange(rnd_min, rnd_max, 0.01), rnd_max)
            y = [monteCarloSampling.exp1_d.functionForSampling(a=a, min_rnd=None, max_rnd=None, min_scope=min_s_scope, max_scope=max_s_scope, rnd=x) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "math.log(1 - a**2 * RND) / -a |a={}| = math.log(1 - {}**2 * RND) / -{}".format(a_round,a_round,a_round)
            title = monteCarloSampling.exp1_d.functionForSampling_label.title.replace('a1', str(a_round))
            xlabel = monteCarloSampling.exp1_d.functionForSampling_label.xlabel
            ylabel = monteCarloSampling.exp1_d.functionForSampling_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()


        def parabola1_scope(self, min_s_scope=-math.pi, max_s_scope=math.pi):
            """
            these is only for experimenting
            scope another then <-pi, pi> has no sense
            """
            monteCarloSampling = MonteCarloSampling()

            # funOrigin
            scope = np.append(np.arange(min_s_scope, max_s_scope, 0.01), max_s_scope)
            y = [monteCarloSampling.parabola1.function(x=x) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope/math.pi, y)
            # title = "p(s) = parabola1(s) = -s**2 + math.pi**2"
            title = monteCarloSampling.parabola1.function_label.title
            xlabel = monteCarloSampling.parabola1.function_label.xlabel
            ylabel = monteCarloSampling.parabola1.function_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funIntegral
            m = max(abs(min_s_scope), abs(max_s_scope))
            scope = np.arange(-m*2.5,m*2.5,0.01)
            y = [monteCarloSampling.parabola1.integral(s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "(math.pi**2)*x-(x**3)/3"
            title = monteCarloSampling.parabola1.integral_label.title
            xlabel = monteCarloSampling.parabola1.integral_label.xlabel
            ylabel = monteCarloSampling.parabola1.integral_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            # lines that show how roots of the equation will be changing with adding (-rnd) value
            int_min = monteCarloSampling.parabola1.integral(s=min_s_scope)
            int_max = monteCarloSampling.parabola1.integral(s=max_s_scope)
            avg = (int_min + int_max)/2
            plt.plot([min_s_scope, max_s_scope], [int_min, int_min], 'g--')
            plt.plot([min_s_scope, max_s_scope], [avg, avg], 'g--')
            plt.plot([min_s_scope, max_s_scope], [int_max, int_max], 'g--')
            plt.show()

            # funDistribution
            m = max(abs(min_s_scope), abs(max_s_scope))
            scope = np.arange(-m*2.5,m*2.5,0.01)
            y = [monteCarloSampling.parabola1.distribution(s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "F(s) = RND = -1/3(x-2*pi)(x+pi)^2 = -1/3x^3 + pi^2*x + 2/3*pi^3"
            title = monteCarloSampling.parabola1.distribution_label.title
            xlabel = monteCarloSampling.parabola1.distribution_label.xlabel
            ylabel = monteCarloSampling.parabola1.distribution_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            # lines that show how roots of the equation will be changing with adding (-rnd) value
            rnd_min = monteCarloSampling.parabola1.distribution(s=min_s_scope)
            rnd_max = monteCarloSampling.parabola1.distribution(s=max_s_scope)
            avg = (rnd_min + rnd_max)/2
            plt.plot([min_s_scope, max_s_scope], [rnd_min, rnd_min], 'g--')
            plt.plot([min_s_scope, max_s_scope], [avg, avg], 'g--')
            plt.plot([min_s_scope, max_s_scope], [rnd_max, rnd_max], 'g--')
            plt.show()

            # funIntegral scope
            scope = np.append(np.arange(min_s_scope, max_s_scope, 0.01), max_s_scope)
            y = [monteCarloSampling.parabola1.integral(s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "(math.pi**2)*x-(x**3)/3"
            title = monteCarloSampling.parabola1.integral_label.title
            xlabel = monteCarloSampling.parabola1.integral_label.xlabel
            ylabel = monteCarloSampling.parabola1.integral_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funDistribution scope
            scope = np.append(np.arange(min_s_scope, max_s_scope, 0.01), max_s_scope)
            y = [monteCarloSampling.parabola1.distribution(s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "F(s) = RND = -1/3(x-2*pi)(x+pi)^2 = -1/3x^3 + pi^2*x + 2/3*pi^3"
            title = monteCarloSampling.parabola1.distribution_label.title
            xlabel = monteCarloSampling.parabola1.distribution_label.xlabel
            ylabel = monteCarloSampling.parabola1.distribution_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()

            # funSampling
            rnd_min = monteCarloSampling.parabola1.distribution(s=min_s_scope)
            rnd_max = monteCarloSampling.parabola1.distribution(s=max_s_scope)
            scope = np.append(np.arange(rnd_min,rnd_max,0.01), rnd_max)
            y = [monteCarloSampling.parabola1.functionForSampling(rnd=x, filt_roots=True, min_scope=min_s_scope, max_scope=max_s_scope) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "roots(poly) = roots(parabola1(s) - RND) dla s w <{}, {}>".format(min_s_scope, max_s_scope)
            title = monteCarloSampling.parabola1.functionForSampling_label.title
            xlabel = monteCarloSampling.parabola1.functionForSampling_label.xlabel
            ylabel = monteCarloSampling.parabola1.functionForSampling_label.ylabel
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.show()


    class Test_FunOrigin():
        def __init__(self):
            pass

        def exp1(self):
            funOrigin = FunOrigin()
            scope1 = np.arange(-1000,1000,0.01)
            scope2 = np.arange(0,1000,0.01)
            scope3 = np.arange(0,100,0.01)
            scope4 = np.arange(0,10,0.01)
            scope5 = np.arange(0,10,1)
            scope6 = np.arange(0,100,1)
            list_scope = [scope6]
            list_a = [1]
            # try negative param a values
            # list_a = [-x for x in list_a]
            """
            best scope:
            good scope: scope3, scope4, scope5, scope6
            no sense scope: scope1, scope2
            bad scope:

            best a: 1 or 0.999
            good a: 0.1, 0.2, 0.5, math.pi/4, 0.9, 0.99, 0.999, 1
            no sense a: math.pi/2, math.pi*3/4, math.e, math.pi
            bad a: 0
            """
            for a in list_a:
                for scope in list_scope:
                    y = [funOrigin.exp1(a=a, s=x) for x in scope]
                    print('y[0] =', y[0])
                    print('y[-1] =', y[-1])
                    if len(y) == 1:
                        plt.scatter(scope, y)
                    else:
                        plt.plot(scope, y)
                    a_round = round(a, 3)
                    title = "exp1(a,s) = math.exp(-a*s)/a |a={}| = math.exp(-{}*s)/{}".format(a_round,a_round,a_round)
                    plt.title(title)
                    plt.xlabel("s")
                    plt.ylabel("exp1(a,s) = p(s)")
                    plt.show()


        def parabola1(self):
            funOrigin = FunOrigin()
            scope1 = np.arange(-1000,1000,0.01)
            scope2 = np.append(np.arange(-math.pi,math.pi,0.01), math.pi)
            list_scope = [scope1, scope2]
            """
            best scope: scope2
            good scope:
            no sense scope: scope1
            bad scope:
            """
            for scope in list_scope:
                y = [funOrigin.parabola1(x=x) for x in scope]
                print('y[0] =', y[0])
                print('y[-1] =', y[-1])
                if len(y) == 1:
                    plt.scatter(scope, y)
                else:
                    plt.plot(scope/math.pi, y)
                title = "parabola1(s) = -s**2 + math.pi**2"
                plt.title(title)
                plt.xlabel(r"$\pi\cdot{s}$")
                plt.ylabel("parabola1(s) = p(s)")
                plt.show()


    class Test_FunDistribution():
        def __init__(self):
            pass

        def exp1(self):
            funDistibution = FunDistibution()
            scope1 = np.arange(-100,100,0.01)
            scope2 = np.arange(-10,10,0.01)
            scope3 = np.arange(0,10,0.01)
            scope4 = np.arange(0,100,0.01)
            list_scope = [scope3, scope4]
            list_a = [1]
            # try negative param a values
            # list_a = [-x for x in list_a]
            """
            best scope:
            good scope: scope3, scope4
            no sense scope: scope1, scope2
            bad scope:

            best a: 1 or 0.999
            good a: 0.1, 0.2, 0.5, math.pi/4, 0.9, 0.99, 0.999, 1
            no sense a: math.pi/2, math.pi*3/4, math.e, math.pi
            bad a: 0
            """
            for a in list_a:
                for scope in list_scope:
                    y = [funDistibution.exp1(a=a, s=x) for x in scope]
                    print('y[0] =', y[0])
                    print('y[-1] =', y[-1])
                    if len(y) == 1:
                        plt.scatter(scope, y)
                    else:
                        plt.plot(scope, y)
                    a_round = round(a, 3)
                    title = "F(s) = RND = (1 - exp(-as))/a**2 |a={}| = (1 - exp(-{}s))/{}**2".format(a_round,a_round,a_round)
                    plt.title(title)
                    plt.xlabel("s")
                    plt.ylabel("F(s) = distribution")
                    plt.show()


        def parabola1(self):
            funDistibution = FunDistibution()
            scope1 = np.arange(-1000,1000,0.01)
            scope2 = np.append(np.arange(-math.pi,math.pi,0.01), math.pi)
            scope3 = np.arange(-1,1,0.01)
            list_scope = [scope1, scope2, scope3]
            """
            best scope: scope2
            good scope:
            no sense scope: scope1, scope3
            bad scope:
            """
            for scope in list_scope:
                y = [funDistibution.parabola1(s=s) for s in scope]
                print('y[0] =', y[0])
                print('y[-1] =', y[-1])
                if len(y) == 1:
                    plt.scatter(scope, y)
                else:
                    plt.plot(scope, y)
                title = "F(s) = RND = -1/3(x-2*pi)(x+pi)^2 = -1/3x^3 + pi^2*x + 2/3*pi^3"
                plt.title(title)
                plt.xlabel("s")
                plt.ylabel("F(s) = distribution")
                plt.show()


    class Test_FunSampling():
        def __init__(self):
            pass

        def exp1(self):
            funSampling = FunSampling()
            scope1 = [0]
            scope2 = [1]
            scope3 = [math.pi]
            scope4 = [math.pi*2]
            scope5 = np.arange(0, 2*math.pi, math.pi/8)
            
            scope_closed = np.append(np.arange(0,1,0.01), 1)
            scope_open = np.arange(0,1,0.01)[1:]
            scope_half_cl = np.arange(0,1,0.01)
            scope_half_cr = np.append(np.arange(0,1,0.01), 1)[1:]
            list_scope = [scope_half_cl]
            list_a = [1]
            # try negative param a values
            # list_a = [-x for x in list_a]
            """
            best scope: scope_half_cl (with a=1) or scope_closed (with a=0.999)
            good scope:
            no sense scope:
            bad scope:

            best a: 1 or 0.999
            good a: 0.1, 0.2, 0.5, math.pi/4, 0.9, 0.99, 0.999, 1
            no sense a:
            bad a: 0, math.pi/2, math.pi*3/4, math.e, math.pi
            """
            for a in list_a:
                for scope in list_scope:
                    y = [funSampling.exp1(a=a, rnd=x) for x in scope]
                    print('y[0] =', y[0])
                    print('y[-1] =', y[-1])
                    if len(y) == 1:
                        plt.scatter(scope, y)
                    else:
                        plt.plot(scope, y)
                    a_round = round(a, 3)
                    title = "exp1(a,rnd) = math.log(1 - a**2 * RND) / -a |a={}| = math.log(1 - {}**2 * RND) / -{}".format(a_round,a_round,a_round)
                    plt.title(title)
                    plt.xlabel("rnd = F(S)")
                    plt.ylabel("s")
                    plt.show()


        def exp1_aprox(self):
            funSampling = FunSampling()
            scope1 = [0]
            scope2 = [1]
            scope3 = [math.pi]
            scope4 = [math.pi*2]
            scope5 = np.arange(0, 2*math.pi, math.pi/8)
            
            scope_closed = np.append(np.arange(0,1,0.01), 1)
            scope_open = np.arange(0,1,0.01)[1:]
            scope_half_cl = np.arange(0,1,0.01)
            scope_half_cr = np.append(np.arange(0,1,0.01), 1)
            scope_half_cr = np.arange(0,1,0.01)
            list_scope = [scope_half_cr]
            list_a = [1]
            # try negative param a values
            # list_a = [-x for x in list_a]
            """
            best scope: scope_half_cr (with a=1 or a=0.999)
            good scope:
            no sense scope:
            bad scope: scope_closed, scope_half_cl

            best a: 1 or 0.999
            good a: 0.1, 0.2, 0.5, math.pi/4, 0.9, 0.99, 0.999, 1
            no sense a:
            bad a: 0, math.pi/2, math.pi*3/4, math.e, math.pi
            """
            for a in list_a:
                for scope in list_scope:
                    y = [funSampling.exp1_aprox(a=a, rnd=x) for x in scope]
                    print('y[0] =', y[0])
                    print('y[-1] =', y[-1])
                    if len(y) == 1:
                        plt.scatter(scope, y)
                    else:
                        plt.plot(scope, y)
                    a_round = round(a, 3)
                    title = "exp1_aprox(a,rnd) = -math.log(rnd) / a |a={}| = -math.log(rnd) / -{}".format(a_round,a_round)
                    plt.title(title)
                    plt.xlabel("rnd = F(S)")
                    plt.ylabel("s")
                    plt.show()


        def exp1_aprox_master_thesis(self):
            funSampling = FunSampling()
            a = 24.26
            scope = np.arange(0,1,0.01)
            y = [funSampling.exp1_aprox(a=a, rnd=x) for x in scope]
            plt.plot(scope, y)
            # title = "Wartość zwróconego kroku fotonu funkcji exp1_aprox w zależności od wylosowanej liczby RND"
            # plt.title(title)
            plt.xlabel("RND")
            plt.ylabel("s [cm]")
            plt.show()

        def parabola1(self):
            funSampling = FunSampling()
            scope1 = [0]
            scope2 = [1]
            scope3 = [math.pi]
            scope4 = [math.pi*2]
            scope5 = np.arange(0, 2*math.pi, math.pi/8)
            
            scope_half_cl0 = np.arange(-1000,1000,0.01)
            scope_half_cl1 = np.arange(-1,1,0.01)
            scope_half_cl2 = np.arange(-math.pi,math.pi,0.01)

            rnd_max = 4*(math.pi**3)/3
            scope_half_cl = np.arange(0,rnd_max,0.01)
            scope_closed = np.append(scope_half_cl, rnd_max)
            scope_open = scope_half_cl[1:]
            scope_half_cr = np.append(scope_half_cl, rnd_max)[1:]
            # list_scope = [scope1, scope2, scope3, scope4]
            # list_scope = [scope5, scope_half_cl0, scope_half_cl1, scope_half_cl2, scope_closed]
            list_scope = [scope_closed]
            """
            best scope: scope_closed
            good scope:
            no sense scope: scope1, scope2, scope3, scope4, scope5, scope_half_cl0, scope_half_cl1, scope_half_cl2
            bad scope:
            """
            for scope in list_scope:
                y = [funSampling.parabola1(rnd=x, filt_roots=True) for x in scope]
                print('y[0] =', y[0])
                print('y[-1] =', y[-1])
                if len(y) == 1:
                    plt.scatter(scope, y)
                else:
                    plt.plot(scope, y)
                title = "parabola1(rnd) = roots(poly)"
                plt.title(title)
                plt.xlabel("rnd = F(S)")
                plt.ylabel("s")
                plt.show()

        def henyey_greenstein(self):
            # φ
            # θ
            g = 0.5
            funSampling = FunSampling()
            samp_num = 10000
            hist_bins = 200
            density = True
            linspace = np.linspace(start=0.0, stop=1.0, num=samp_num, endpoint=True)
            samples = np.array([funSampling.henyey_greenstein(g, rnd=rnd) for rnd in linspace]) * 180 / math.pi
            plt.plot(linspace, samples)
            # plt.title("henyey_greenstein, g = {}".format(g))
            # plt.xlabel("rnd = F(S)")
            plt.xlabel("RND")
            plt.ylabel("θ [°]")
            plt.show()
            # histogram
            plt.hist(samples, bins=hist_bins, density=density)
            # plt.title("histogram henyey_greenstein, g = {}".format(g))
            plt.xlabel("θ [°]")
            plt.ylabel("prawdopodobieństwo")
            plt.show()
            # histogram 2
            samples2 = np.array([funSampling.henyey_greenstein(g) for _ in range(samp_num)]) * 180 / math.pi
            plt.hist(samples2, bins=hist_bins, density=False)
            # plt.title("histogram henyey_greenstein, g = {}".format(g))
            plt.xlabel("θ [°]")
            plt.ylabel("liczba wylosowanych próbek")
            plt.show()
            samp_num = 20
            # histogram 3
            samples2 = np.array([funSampling.henyey_greenstein(g) for _ in range(samp_num)]) * 180 / math.pi
            plt.hist(samples2, bins=hist_bins, density=density)
            plt.title("histogram henyey_greenstein, g = {}".format(g))
            plt.xlabel("theta [deg]")
            plt.ylabel("amount of samples")
            plt.show()


    class Test_Object3D():
        def __init__(self):
            pass

        def help_file(self):
            help(Object3D)

        def test_vizualize(self):
            propEnv = PropEnv()
            mat = ByMatplotlib()
            vis = ByVispy()
            mat.show_body(propEnv)
            vis.show_body(propEnv)

        def test_vizualize_stride(self):
            propEnv = PropEnv()
            mat = ByMatplotlib()
            vis = ByVispy()
            mat.show_stride(propEnv, stride=(20, 20, 20))
            vis.show_stride(propEnv, stride=(20, 20, 20))
            mat.show_stride(propEnv, stride=10)
            vis.show_stride(propEnv, stride=10)

        def test_fill_cube(self):
            propEnv = PropEnv()
            propEnv.fill_cube(1, [0, 0, 0], end_p=[1.0, 0.25, 0.5])
            mat = ByMatplotlib()
            vis = ByVispy()
            # mat.show_stride(propEnv, stride=(20, 20, 20))
            # vis.show_stride(propEnv, stride=(20, 20, 20))
            mat.show_stride(propEnv, stride=10)
            vis.show_stride(propEnv, stride=10)

        def obj3d_array_for_tests(self, method="end_p"):
            ob = [Object3D() for _ in range(7)]
            if method == "end_p" or method == "end_p_float":
                ob[0].fill_cube(fill=1, start_p=(0.,0.,0.), fill_rec=None, end_p=(0.2, 0.2, 0.2))
                ob[1].fill_cube(fill=1, start_p=(0,0,0), fill_rec=None, end_p=(0.5, 0.5, 0.5))
                ob[1].fill_cube(fill=1, start_p=(0.5,0.5,0.5), fill_rec=None, end_p=(1.0, 1.0, 1.0))
                ob[2].fill_cube(fill=2, start_p=(0,0,0), fill_rec=None, end_p=(0.5, 0.5, 0.5))
                ob[2].fill_cube(fill=3, start_p=(0.5,0.5,0.5), fill_rec=None, end_p=(1.0, 1.0, 1.0))
                ob[3].fill_cube(fill=1, start_p=(0.25,0.25,0.25), fill_rec=None, end_p=(0.75, 0.9, 0.5))
                ob[4].fill_cube(fill=1, start_p=(0,0,0), fill_rec=None, end_p=(0.8, 0.2, 0.4))
                ob[5].fill_cube(fill=1, start_p=(0.25,0.25,0.25), fill_rec=None, end_p=(0.75, 0.75, 0.75))
                ob[6].fill_cube(fill=1, start_p=(0.2,0.2,0.2), fill_rec=None, end_p=(0.8, 0.8, 0.8))
            elif method == "end_p_int":
                ob[0].fill_cube(fill=1, start_p=(0.,0.,0.), fill_rec=None, end_p=(20, 20, 20))
                ob[1].fill_cube(fill=1, start_p=(0,0,0), fill_rec=None, end_p=(50, 50, 50))
                ob[1].fill_cube(fill=1, start_p=(0.5,0.5,0.5), fill_rec=None, end_p=(100, 100, 100))
                ob[2].fill_cube(fill=2, start_p=(0,0,0), fill_rec=None, end_p=(50, 50, 50))
                ob[2].fill_cube(fill=3, start_p=(0.5,0.5,0.5), fill_rec=None, end_p=(100, 100, 100))
                ob[3].fill_cube(fill=1, start_p=(0.25,0.25,0.25), fill_rec=None, end_p=(75, 90, 50))
                ob[4].fill_cube(fill=1, start_p=(0,0,0), fill_rec=None, end_p=(80, 20, 40))
                ob[5].fill_cube(fill=1, start_p=(0.25,0.25,0.25), fill_rec=None, end_p=(75, 75, 75))
                ob[6].fill_cube(fill=1, start_p=(0.2,0.2,0.2), fill_rec=None, end_p=(80, 80, 80))
            elif method == "fill_rec" or method == "fill_rec_int":
                ob[0].fill_cube(fill=1, start_p=(0,0,0), fill_rec=(20, 20, 20))
                ob[1].fill_cube(fill=1, start_p=(0,0,0), fill_rec=(50, 50, 50))
                ob[1].fill_cube(fill=1, start_p=(0.5,0.5,0.5), fill_rec=(50, 50, 50))
                ob[2].fill_cube(fill=2, start_p=(0,0,0), fill_rec=(50, 50, 50))
                ob[2].fill_cube(fill=3, start_p=(0.5,0.5,0.5), fill_rec=(50, 50, 50))
                ob[3].fill_cube(fill=1, start_p=(0.25,0.25,0.25), fill_rec=(50, 65, 25))
                ob[4].fill_cube(fill=1, start_p=(0,0,0), fill_rec=(80, 20, 40))
                ob[5].fill_cube(fill=1, start_p=(0.25,0.25,0.25), fill_rec=(50,50,50))
                ob[6].fill_cube(fill=1, start_p=(0.2,0.2,0.2), fill_rec=(60,60,60))
            elif method == "fill_rec_float":
                ob[0].fill_cube(fill=1, start_p=(0.,0.,0.), fill_rec=(0.2, 0.2, 0.2))
                ob[1].fill_cube(fill=1, start_p=(0,0,0), fill_rec=(0.5, 0.5, 0.5))
                ob[1].fill_cube(fill=1, start_p=(0.5,0.5,0.5), fill_rec=(0.5, 0.5, 0.5))
                ob[2].fill_cube(fill=2, start_p=(0,0,0), fill_rec=(0.5, 0.5, 0.5))
                ob[2].fill_cube(fill=3, start_p=(0.5,0.5,0.5), fill_rec=(0.5, 0.5, 0.5))
                ob[3].fill_cube(fill=1, start_p=(0.25,0.25,0.25), fill_rec=(0.5, 0.65, 0.25))
                ob[4].fill_cube(fill=1, start_p=(0,0,0), fill_rec=(0.8, 0.2, 0.4))
                ob[5].fill_cube(fill=1, start_p=(0.25,0.25,0.25), fill_rec=(0.5,0.5,0.5))
                ob[6].fill_cube(fill=1, start_p=(0.2,0.2,0.2), fill_rec=(0.6,0.6,0.6))
            else:
                raise ValueError("bad method string")
            return ob
        
        def visualize_Obj3d_list(self, oblist, prefix_title=""):
            vis = ByVispy()
            matplot = ByMatplotlib()
            for i in range(len(oblist)):
                o = oblist[i]
                title = prefix_title + "_ob" + str(i)
                vis.show_body(o, title=title, omit_labels=[0])
                # matplot.show_stride(o, stride=10, title=title)

        def print_png_Obj3d_list(self, oblist, prefix_title="", dir="tests"):
            print_obj = Print()
            dirname = os.path.join("slice_img", dir)
            for i in range(len(oblist)):
                o = oblist[i]
                title = prefix_title + "_ob" + str(i) + ".png"
                print_obj.obj3D_to_png(o, axis=2, xray=1, dir=dirname, filename=title)


    class Test_Slice():
        def __init__(self):
            pass

        def test_fromObj3D(self, method="default"):
            # create objects
            test_Object3D = Test.Test_Object3D()
            ob = test_Object3D.obj3d_array_for_tests(method="end_p")
            # choose some
            ob = ob[:5]
            # ob = ob[0:1]
            # visualize raw data
            # test_Object3D.visualize_Obj3d_list(ob)
            # slice list
            all_preset_list = ["max_cross_middle", "xy", "xz", "yz", "max_cross_up", "max_cross_down"]
            preset = all_preset_list[3]
            start = time.time()
            if method == "default":
                sl = [Slice().fromObj3D(o, preset=preset, min_dist=0.2) for o in ob]
            else:
                sl = [Slice().fromObj3D_byPlaneEq(o, preset=preset) for o in ob]
            end = time.time()
            making_slice_time = end - start
            print("making_slice_time", making_slice_time)
            # visualize slices
            test_Object3D.visualize_Obj3d_list(sl, prefix_title=preset)

        def test_fromObj3D_to_projection(self):
            # create objects
            test_Object3D = Test.Test_Object3D()
            ob = test_Object3D.obj3d_array_for_tests(method="end_p")
            # choose some
            # ob = ob[:5]
            # ob = ob[0:1]
            # visualize raw data
            # test_Object3D.visualize_Obj3d_list(ob, prefix_title=preset)
            # projection list
            all_preset_list = ["max_cross_middle", "xy", "xz", "yz", "max_cross_up", "max_cross_down"]
            preset = all_preset_list[0]
            start = time.time()
            slice = Slice()
            sl = [slice.fromObj3D_to_projection(o, preset=preset) for o in ob]
            end = time.time()
            making_slice_projection_time = end - start
            print("making_slice_projection_time", making_slice_projection_time)
            # visualize projections
            test_Object3D.visualize_Obj3d_list(sl, prefix_title=preset)
            # print png images
            test_Object3D.print_png_Obj3d_list(sl, prefix_title=preset, dir=preset)

        def test_middle_slices(self, method="default"):
            # create objects
            test_Object3D = Test.Test_Object3D()
            ob = test_Object3D.obj3d_array_for_tests(method="end_p")
            # choose some
            # ob = ob[:5]
            # ob = ob[0:1]
            # visualize raw data
            # test_Object3D.visualize_Obj3d_list(ob, prefix_title=preset)
            # slice list
            all_preset_list = ["xy-middle", "xz-middle", "yz-middle"]
            all_print_preset = [2, 1, 0]
            choice_idx = 2
            preset = all_preset_list[choice_idx]
            start = time.time()
            if method == "default":
                sl = [Slice().fromObj3D(o, preset=preset, min_dist=0.2) for o in ob]
            else:
                sl = [Slice().fromObj3D_byPlaneEq(o, preset=preset) for o in ob]
            end = time.time()
            making_slice_time = end - start
            print("making_slice_time", making_slice_time)
            # visualize slices
            # test_Object3D.visualize_Obj3d_list(sl, prefix_title=preset)
            # print png images
            print_obj = Print()
            ax = all_print_preset[choice_idx]
            dirname = os.path.join("slice_img", preset)
            for i in range(len(sl)):
                filename = preset + "-ob" + str(i) + ".png"
                proj = Projection().throw(sl[i], axis=ax, xray=1)
                print_obj.obj3D_to_png(proj, axis=2, xray=1, dir=dirname, filename=filename)

        def test_simple_middle_slices(self):
            # create objects
            test_Object3D = Test.Test_Object3D()
            ob = test_Object3D.obj3d_array_for_tests(method="end_p")
            # choose some
            # ob = ob[:5]
            # ob = ob[0:1]
            # visualize raw data
            # test_Object3D.visualize_Obj3d_list(ob, prefix_title=preset)
            # slice list
            start = time.time()
            sl_xy = [o.body[:,:,50] for o in ob]
            sl_xz = [o.body[:,50,:] for o in ob]
            sl_yz = [o.body[50,:,:] for o in ob]
            end = time.time()
            making_slice_time = end - start
            print("making_slice_time", making_slice_time)
            # print png images - prepare to loop
            print_obj = Print()
            sl = [sl_xy, sl_xz, sl_yz]
            seria_name = ["xy-middle_simple", "xz-middle_simple", "yz-middle_simple"]
            # print png images - loop
            for s, sn in list(zip(sl, seria_name)):
                dirname = os.path.join("slice_img", sn)
                for i in range(len(s)):
                    filename = sn + "-ob" + str(i) + ".png"
                    print_obj.arr2D_to_png(s[i], dir=dirname, filename=filename)


    class Test_Projection():
        def __init__(self):
            pass

        def simple_projections(self):
            # create objects
            test_Object3D = Test.Test_Object3D()
            ob = test_Object3D.obj3d_array_for_tests(method="end_p")
            # choose some
            # ob = ob[:5]
            # ob = ob[0:1]
            # visualize raw data
            # test_Object3D.visualize_Obj3d_list(ob, prefix_title=preset)
            # projection list
            all_fun_name_list = ["x_high", "x_low", "y_high", "y_low", "z_high", "z_low"]
            fun_name = all_fun_name_list[5]
            start = time.time()
            proj = [getattr(Projection(), fun_name)(o) for o in ob]
            end = time.time()
            making_projection_time = end - start
            print("making_projection_time", making_projection_time)
            # visualize projections
            test_Object3D.visualize_Obj3d_list(proj, prefix_title=fun_name)
            # print png images
            test_Object3D.print_png_Obj3d_list(proj, prefix_title=fun_name, dir=fun_name)


    class Test_Print():
        def __init__(self):
            pass

        def simple_prints(self):
            # create objects
            test_Object3D = Test.Test_Object3D()
            ob = test_Object3D.obj3d_array_for_tests(method="end_p")
            # choose some
            # ob = ob[:5]
            # ob = ob[0:1]
            # visualize raw data
            # test_Object3D.visualize_Obj3d_list(ob, prefix_title=preset)
            # print preset functions
            all_fun_name_list = ["x_high", "x_low", "y_high", "y_low", "z_high", "z_low"]
            start = time.time()
            for i in range(len(all_fun_name_list)):
                fun_name = all_fun_name_list[i]
                for j in range(len(ob)):
                    dirname = os.path.join("slice_img", "print", fun_name)
                    filename = fun_name + "-ob" + str(j) + ".png"
                    fun = getattr(Print(), fun_name)
                    fun(ob[j], dir=dirname, filename=filename)
            end = time.time()
            making_png_prints_time = end - start
            print("making_png_prints_time", making_png_prints_time)

    
    class Test_Space3dTools():
        def __init__(self):
            pass

        def internal_reflectance(self):
            n1 = 1.1
            n2 = 1.5
            # n1 = n2 = 1.000293
            theta1 = [i/100*math.pi/2 for i in range(0,101)]

            if n1 > n2:
                # Total internal reflection angle
                theta1_critical = math.asin(n2 / n1)
                theta1 = [t1 for t1 in theta1 if t1 <= theta1_critical]

            theta2 = [math.asin(math.sin(t1)*n1/n2) for t1 in theta1] 
            ref = [Space3dTools.internal_reflectance(t1, t2) for t1, t2 in zip(theta1, theta2)]

            theta1_deg = [t*180/math.pi for t in theta1]
            theta2_deg = [t*180/math.pi for t in theta2]
            plt.plot(theta1_deg, ref)

            # error debugging
            # theta1_err = 2.168525411247653
            # theta2_err = 0.9730672423421401
            # plt.scatter(theta1_err*180/math.pi, Space3dTools.internal_reflectance(theta1_err, theta1_err))

            plt.xlabel('theta1 [deg]')
            plt.ylabel('internal_reflectance')
            plt.show()

            plt.plot(theta1_deg, theta2_deg)
            plt.xlabel('theta1 [deg]')
            plt.ylabel('theta2 [deg]')
            plt.show()


    class Test_ResultEnvProcessing():
        def __init__(self):
            pass

        @staticmethod
        def are_2_variants_equal_resultEnv(resultEnv, photon_num, volume_per_bin, escaped_photons_weight):
            print("TEST NORMALIZATION resultEnv")

            start_time = time.time()
            normal_output_1 = ResultEnvProcessing.normalize_resultEnv(resultEnv, photon_num, volume_per_bin, escaped_photons_weight, inplace=False, print_debug=True)
            end_time = time.time()
            print("norm1 calculation time:", end_time-start_time)

            start_time = time.time()
            normal_output_2 = ResultEnvProcessing.normalize_resultEnv_2(resultEnv, volume_per_bin, inplace=False, print_debug=True)
            end_time = time.time()
            print("norm2 calculation time:", end_time-start_time)

            test_result = np.allclose(normal_output_1.body, normal_output_2.body)
            if not test_result:
                raise ValueError("Normalize methods are not equal!")
            return test_result
        
        @staticmethod
        def are_2_variants_equal_resultRecords(resultRecords, photon_num, volume_per_bin, borders, escaped_photons_weight):
            print("TEST NORMALIZATION resultRecords")

            start_time = time.time()
            normal_output_1 = ResultEnvProcessing.normalize_resultRecords(resultRecords, photon_num, volume_per_bin, escaped_photons_weight, inplace=False, print_debug=True)
            end_time = time.time()
            print("norm1 calculation time:", end_time-start_time)

            start_time = time.time()
            normal_output_2 = ResultEnvProcessing.normalize_resultRecords_2(resultRecords, volume_per_bin, borders, inplace=False, print_debug=True)
            end_time = time.time()
            print("norm2 calculation time:", end_time-start_time)

            arr1 = np.array([col[4] for col in normal_output_1])
            arr2 = np.array([col[4] for col in normal_output_2])
            test_result = np.allclose(arr1, arr2)
            if not test_result:
                raise ValueError("Normalize methods are not equal!")
            return test_result
        
        
    class Test_ColorPointDF():
        def __init__(self):
            pass

        @staticmethod
        def stack_color_scheme():
            # make test object
            o_size = 20
            arr = np.full((o_size, o_size, o_size), fill_value=0.0)
            o1 = Object3D(arr=arr)
            o2 = Object3D(arr=arr.copy())
            o1.fill_cube(0, start_p=(0.0,0.0,0.0), end_p=(0.75,0.75,0.75), random_fill=True)
            o2.fill_cube(0, start_p=(0.25,0.25,0.25), end_p=(1.0,1.0,1.0), random_fill=True)
            # make color schemes (data frames)
            colorPointDF = ColorPointDF()
            df1 = colorPointDF.from_Object3d(o1, color_scheme="loop", drop_values=[0])
            # print("df1\n", df1)
            df2 = colorPointDF.from_Object3d(o2, color_scheme="threshold", drop_values=[0])
            # print("df2\n", df2)
            # stack
            df_stack = colorPointDF.stack_color_scheme([df1, df2])
            # print("df_stack\n", df_stack)
            # show
            vis = ByVispy()
            vis.show_ColorPointDF(df_stack)

        @staticmethod
        def sum_same_idx():
            x_idx = [1, 1, 2, 3, 3, 4, 5, 6, 7, 7, 7, 8, 8, 8, 8, 9]
            y_idx = [1, 1, 2, 3, 3, 4, 5, 6, 7, 7, 7, 8, 8, 8, 8, 9]
            z_idx = [1, 1, 2, 3, 3, 4, 5, 6, 7, 7, 7, 8, 8, 8, 8, 9]
            value = [1 for _ in range(len(x_idx))]
            rnd = Test.myRandom
            random_col = [rnd.uniform_half_open(0.0, 1.0) for _ in range(len(x_idx))]
            dic = {"x_idx": x_idx,
                  "y_idx": y_idx,
                  "z_idx": z_idx,
                  "value": value,
                  "random_col": random_col}
            df = pd.DataFrame(dic)
            df = df.sample(frac = 1)
            print("df\n", df)
            colorPointDF = ColorPointDF()
            colorPointDF.sum_same_idx(df)
            print("res_df\n", df)

    class Test_ArrowsDF():
        def __init__(self):
            pass

        @staticmethod
        def check_arrow_dirs(arrowsDF: pd.DataFrame):
            flag_ok = True
            not_ok = []
            not_ok_dir_vecs = []
            for id in arrowsDF["photon_id"].unique():
                same_id_df = arrowsDF[arrowsDF["photon_id"] == id]
                if len(same_id_df) < 3:
                    continue
                # calculate normalized dir vector
                vec = same_id_df[["x_idx_2", "y_idx_2", "z_idx_2"]].to_numpy() - same_id_df[["x_idx", "y_idx", "z_idx"]].to_numpy()
                dist = np.linalg.norm(vec, axis=1)
                norm_dir = vec / dist.reshape(-1,1)
                # check if the dir is not the same in pairs (incident[i], incident[i+2])
                even = norm_dir[0:]
                odd = norm_dir[2:]
                limit = min(len(even), len(odd))
                are_the_same = np.isclose(even[:limit], odd[:limit])
                # check if there is at least one same dir vector
                are_rows_ok = ~np.all(are_the_same == True, axis=1)
                is_photon_ok = np.all(are_rows_ok == True)
                flag_ok = flag_ok and is_photon_ok
                if not is_photon_ok:
                    not_ok.append(id)
                    not_ok_vec1 = even[:limit][~are_rows_ok]
                    not_ok_vec2 = odd[:limit][~are_rows_ok]
                    print("photon_id:", id)
                    print("not_ok_vec1")
                    print(not_ok_vec1)
                    print("not_ok_vec2")
                    print(not_ok_vec2)
                    not_ok_dir_vecs.append([not_ok_vec1, not_ok_vec2])
            if not flag_ok:
                print()
                print("Not every pair of direction vectors in every third arrows is different.")
                print("Not ok num:", len(not_ok))
                print()
                return False
            else:
                return True
                    







    def test1(self):
        test_FunOrigin = self.Test_FunOrigin()
        test_FunOrigin.exp1()

    
    def test2(self):
        test_FunSampling = self.Test_FunSampling()
        test_FunSampling.exp1()


    def test3(self):
        test_FunSampling = self.Test_FunSampling()
        test_FunSampling.exp1_aprox()


    def test4(self):
        test_funDistribution = self.Test_FunDistribution()
        test_funDistribution.exp1()


    def test5(self):
        test_funOrigin = self.Test_FunOrigin()
        test_funOrigin.parabola1()


    def test6(self):
        test_funDistribution = self.Test_FunDistribution()
        test_funDistribution.parabola1()


    def test7(self):
        test_FunSampling = self.Test_FunSampling()
        test_FunSampling.parabola1()

    def test_MonteCarloSampling_exp1(self):
        test_MonteCarloSampling = self.Test_MonteCarloSampling()
        test_MonteCarloSampling.exp1()

    def test_MonteCarloSampling_parabola1(self):
        test_MonteCarloSampling = self.Test_MonteCarloSampling()
        test_MonteCarloSampling.parabola1()

    def test_MonteCarloSampling_exp1_scope(self):
        test_MonteCarloSampling = self.Test_MonteCarloSampling()
        test_MonteCarloSampling.exp1_scope(min_s_scope = -10, max_s_scope = 20)

    def test_MonteCarloSampling_parabola1_scope(self):
        test_MonteCarloSampling = self.Test_MonteCarloSampling()
        test_MonteCarloSampling.parabola1_scope(min_s_scope = -math.pi, max_s_scope = math.pi)

    def test8(self):
        self.test_MonteCarloSampling_exp1()

    def test9(self):
        self.test_MonteCarloSampling_parabola1()

    def test10(self):
        self.test_MonteCarloSampling_exp1_scope()

    def test11(self):
        self.test_MonteCarloSampling_parabola1_scope()

    def test12(self):
        t = self.Test_Object3D()
        t.help_file()

    def test13(self):
        t = self.Test_Object3D()
        t.test_vizualize()
        t.test_vizualize_stride()
        t.test_fill_cube()

    def test14(self):
        t = self.Test_Slice()
        t.test_fromObj3D()

    def test_MonteCarloSampling_exp2(self):
        test_MonteCarloSampling = self.Test_MonteCarloSampling()
        test_MonteCarloSampling.exp2()

    def test_MonteCarloSampling_parabola2(self):
        test_MonteCarloSampling = self.Test_MonteCarloSampling()
        test_MonteCarloSampling.parabola2()

    def test_MonteCarloSampling_normal_scope(self):
        test_MonteCarloSampling = self.Test_MonteCarloSampling()
        test_MonteCarloSampling.normal_scope(loc=0, scale=1)

    def test15(self):
        self.test_MonteCarloSampling_exp2()
        
    def test16(self):
        self.test_MonteCarloSampling_parabola2()

    def test17(self):
        self.test_MonteCarloSampling_normal_scope()

    def test18(self):
        # Slice.fromObj3D_to_projection
        t = self.Test_Slice()
        t.test_fromObj3D_to_projection()

    def test19(self):
        # slice method by equation - faster, but not accurate
        t = self.Test_Slice()
        t.test_fromObj3D(method="fast")

    def test20(self):
        # simple projections test (x_high, x_low...)
        t = self.Test_Projection()
        t.simple_projections()

    def test21(self):
        # simple png prints (x_high, x_low...)
        t = self.Test_Print()
        t.simple_prints()

    def test22(self):
        # middle xy xz yz slices + print
        t = self.Test_Slice()
        t.test_middle_slices()

    def test23(self):
        # (simple method) middle xy xz yz print
        t = self.Test_Slice()
        t.test_simple_middle_slices()

    def test24(self):
        # Reflectance function
        t = self.Test_Space3dTools()
        t.internal_reflectance()

    def test25(self):
        # color scheme stack
        t = self.Test_ColorPointDF()
        t.stack_color_scheme()

    def test26(self):
        # sum same idx
        t = self.Test_ColorPointDF()
        t.sum_same_idx()

    def test27(self):
        # henyey_greenstein
        t = self.Test_FunSampling()
        t.henyey_greenstein()

    def test28(self):
        # exp1 aprox
        t = self.Test_FunSampling()
        t.exp1_aprox_master_thesis()


def main():
    test = Test()

    # generator liczb losowych
    # test.test8() # exp1
    # test.test9() # parabola

    # generator liczb losowych scope
    # test.test10() # exp1
    # test.test11() # parabola

    # wizualizacja
    # test.test13()

    # slice
    # test.test14()

    # slice method by equation - faster, but not accurate
    # test.test19()

    # Slice.fromObj3D_to_projection
    # test.test18()

    # Projections test
    # test.test20()

    # simple png prints (x_high, x_low...)
    # test.test21()

    # middle xy xz yz slices + print
    # test.test22()

    # simple middle xy xz yz print
    # test.test23()

    # normal generator
    # test.test_MonteCarloSampling_normal_scope()

    # poprawione generatory (stały przedział)
    # print("exp2")
    # test.test_MonteCarloSampling_exp2()
    # print("parabola2")
    # test.test_MonteCarloSampling_parabola2()

    # Reflectance function
    # test.test24()

    # test color scheme stack
    # test.test25()

    # test sum same idx ColorPointDF
    # test.test26()

    # henyey_greenstein
    # test.test27()

    # exp1_aprox master thesis
    test.test28()



if __name__ == '__main__':
    main()