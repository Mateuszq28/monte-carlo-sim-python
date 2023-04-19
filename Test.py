from FeatureSampling import *
import matplotlib.pyplot as plt
import math
import numpy as np
from Slice import Slice
import time
from Object3D import *
from PropEnv import *
from ByMatplotlib import *
from ByVispy import *

class Test():
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
            # title = r'$\mathregular{{p(s) = exp1(a,s) = \frac{{e^{{-a\cdot{{s}}}}}}{{a}}; |a={}| = \frac{{e^{{-{}\cdot{{s}}}}}}{{{}}}}}$'.format(a_round,a_round,a_round)
            t_ps = r'$\mathregular{p(s)}$'
            t_exp = r'$\mathregular{exp1(a,s)}$'
            t_undf = r'$\mathregular{\frac{e^{-a\cdot{s}}}{a}; |a=a1|}$'.replace('a1', str(a_round))
            t_df = r'$\mathregular{\frac{e^{-a1\cdot{s}}}{a1}}$'.replace('a1', str(a_round))
            title = ' = '.join([t_ps, t_exp, t_undf, t_df])
            plt.title(title)
            plt.xlabel("s")
            plt.ylabel("p(s)")
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
            # title = r'$\mathregular{\int exp1(a,s) \,ds = \int \frac{e^{-a\cdot{s}}}{a} \,ds = \frac{-e^{-a\cdot{s}}}{a^{2}}; |a=a1| = \frac{-e^{-a1\cdot{s}}}{a1^{2}}}$'.replace('a1', str(a_round))
            t_int = r'$\mathregular{\int exp1(a,s) \,ds}$'
            t_int_undf = r'$\mathregular{\int \frac{e^{-a\cdot{s}}}{a} \,ds}$'
            t_undf = r'$\mathregular{\frac{-e^{-a\cdot{s}}}{a^{2}}; |a=a1|}$'.replace('a1', str(a_round))
            t_df = r'$\mathregular{\frac{-e^{-a1\cdot{s}}}{a1^{2}}}$'.replace('a1', str(a_round))
            title = ' = '.join([t_int, t_int_undf, t_undf, t_df])
            plt.title(title)
            plt.xlabel("s")
            # ylabel = "Integral(exp1(a,s))ds"
            ylabel = r'$\int exp1(a,s) \,ds$'
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
            title = r"$\mathregular{F(s) = RND = \frac{1 - e^{-a\cdot{s}}}{a^2}; |a=a1| = \frac{1 - e^{-a1\cdot{s}}}{a1^2}}$".replace("a1",str(a_round))
            t_fs = r'$\mathregular{F(s)}$'
            t_rnd = r'$\mathregular{RND}$'
            t_int = r'$\mathregular{\int_0 ^s \frac{e^{-a\cdot{s}}}{a} \,ds}$'
            t_undf = r'$\mathregular{\frac{1 - e^{-a\cdot{s}}}{a^2}; |a=a1|}$'.replace('a1', str(a_round))
            t_df = r'$\mathregular{\frac{1 - e^{-a1\cdot{s}}}{a1^2}}$'.replace('a1', str(a_round))
            title = ' = '.join([t_fs, t_rnd, t_int, t_undf, t_df])
            plt.title(title)
            plt.xlabel("s")
            plt.ylabel("F(s) = distribution")
            plt.show()

            # funSampling
            a = 1
            rnd_min = monteCarloSampling.exp1.distribution(a=a, s=0)
            rnd_max = monteCarloSampling.exp1.distribution(a=a, s=10)
            scope = np.append(np.arange(rnd_min, rnd_max, 0.01), rnd_max)
            y = [monteCarloSampling.exp1.functionForSampling(a=a, rnd=x) for x in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            a_round = round(a, 3)
            # title = "math.log(1 - a**2 * RND) / -a |a={}| = math.log(1 - {}**2 * RND) / -{}".format(a_round,a_round,a_round)
            # title = r"$\mathregular{\frac{\ln{(1 - a^2 \cdot{RND})}}{-a}; |a=a1| = \frac{\ln{(1-a1^2\cdot{RND})}}{-a1}}$".replace("a1",str(a_round))
            t_gen = 'generator I'
            t_undf = r'$\mathregular{\frac{\ln{(1 - a^2 \cdot{RND})}}{-a}; |a=a1|}$'.replace('a1', str(a_round))
            t_df = r'$\mathregular{\frac{\ln{(1-a1^2\cdot{RND})}}{-a1}}$'.replace('a1', str(a_round))
            title = ' = '.join([t_gen, t_undf, t_df])
            plt.title(title)
            plt.xlabel("rnd = F(S)")
            plt.ylabel("s")
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
            t_ps = 'p(s)'
            t_parab = r'$\mathregular{parabola1(s)}$'
            t_df = r'$\mathregular{-s^2+\pi^2}$'
            title = ' = '.join([t_ps, t_parab, t_df])
            plt.title(title)
            plt.xlabel(r"$\pi\cdot{s}$")
            plt.ylabel("p(s) = parabola1(s)")
            plt.show()

            # funIntegral
            scope = np.arange(-6,6,0.01)
            y = [monteCarloSampling.parabola1.integral(s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "(math.pi**2)*x-(x**3)/3"
            t_int = r'$\mathregular{\int parabola1(s) \,ds}$'
            t_int_undf = r'$\mathregular{\int (-s^2+\pi^2) \,ds}$'
            t_undf = r'$\mathregular{-\frac{1}{3}x^3 + \pi^2 x}$'
            title = ' = '.join([t_int, t_int_undf, t_undf])
            plt.title(title)
            plt.xlabel("s")
            ylabel = r'$\int parabola1(s) \,ds$'
            plt.ylabel(ylabel)
            # lines that show how roots of the equation will be changing with adding (-rnd) value
            int_max = monteCarloSampling.parabola1.integral(s=math.pi)
            int_min = monteCarloSampling.parabola1.integral(s=-math.pi)
            avg = (int_min + int_max)/2
            plt.plot([-math.pi, math.pi], [int_min, int_min], 'g--')
            plt.plot([-math.pi, math.pi], [avg, avg], 'g--')
            plt.plot([-math.pi, math.pi], [int_max, int_max], 'g--')
            plt.show()

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
            t_fs = r'$\mathregular{F(s)}$'
            t_rnd = r'$\mathregular{RND}$'
            t_int = r'$\mathregular{\int_{-\pi} ^s (-s^2+\pi^2) \,ds}$'
            t_1 = r'$\mathregular{-\frac{1}{3}(x-2\pi)(x+\pi)^2}$'
            t_2 = r'$\mathregular{-\frac{1}{3}x^3 + \pi^2 x + \frac{2}{3} \pi^3}$'
            title = ' = '.join([t_fs, t_rnd, t_int, t_1, t_2])
            plt.title(title)
            plt.xlabel("s")
            plt.ylabel("F(s) = distribution")
            # lines that show how roots of the equation will be changing with adding (-rnd) value
            rnd_max = monteCarloSampling.parabola1.distribution(s=math.pi)
            plt.plot([-math.pi, math.pi], [0, 0], 'g--')
            plt.plot([-math.pi, math.pi], [rnd_max/2, rnd_max/2], 'g--')
            plt.plot([-math.pi, math.pi], [rnd_max, rnd_max], 'g--')
            plt.show()

            # funIntegral scope
            scope = np.append(np.arange(-math.pi,math.pi,0.01), math.pi)
            y = [monteCarloSampling.parabola1.integral(s=s) for s in scope]
            print('y[0] =', y[0])
            print('y[-1] =', y[-1])
            if len(y) == 1:
                plt.scatter(scope, y)
            else:
                plt.plot(scope, y)
            # title = "(math.pi**2)*x-(x**3)/3"
            t_int = r'$\mathregular{\int parabola1(s) \,ds}$'
            t_int_undf = r'$\mathregular{\int (-s^2+\pi^2) \,ds}$'
            t_undf = r'$\mathregular{-\frac{1}{3}x^3 + \pi^2 x}$'
            title = ' = '.join([t_int, t_int_undf, t_undf])
            plt.title(title)
            plt.title(title)
            plt.xlabel("s")
            ylabel = r'$\int parabola1(s) \,ds$'
            plt.ylabel(ylabel)
            plt.show()

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
            t_fs = r'$\mathregular{F(s)}$'
            t_rnd = r'$\mathregular{RND}$'
            t_int = r'$\mathregular{\int_{-\pi} ^s (-s^2+\pi^2) \,ds}$'
            t_1 = r'$\mathregular{-\frac{1}{3}(x-2\pi)(x+\pi)^2}$'
            t_2 = r'$\mathregular{-\frac{1}{3}x^3 + \pi^2 x + \frac{2}{3} \pi^3}$'
            title = ' = '.join([t_fs, t_rnd, t_int, t_1, t_2])
            plt.title(title)
            plt.xlabel("s")
            plt.ylabel("F(s) = distribution")
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
            t0 = "generator II"
            t1 = r"$\mathregular{roots(F(s) - RND)}$"
            t2 = r'$\mathregular{roots(-\frac{1}{3}x^3 + \pi^2 x + \frac{2}{3} \pi^3 - RND)}$ dla s $\in$ $<-\pi, \pi>$'
            title = ' = '.join([t0, t1, t2])
            plt.title(title)
            plt.xlabel("rnd = F(S)")
            plt.ylabel("s")
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
            t_ps = r'$\mathregular{p(s)}$'
            t_exp = r'$\mathregular{exp1(a,s)}$'
            t_undf = r'$\mathregular{\frac{e^{-a\cdot{s}}}{a}; |a=a1|}$'.replace('a1', str(a_round))
            t_df = r'$\mathregular{\frac{e^{-a1\cdot{s}}}{a1}}$'.replace('a1', str(a_round))
            title = ' = '.join([t_ps, t_exp, t_undf, t_df])
            plt.title(title)
            plt.xlabel("s")
            plt.ylabel("p(s)")
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
            # title = r"$\mathregular{\frac{\ln{(1 - a^2 \cdot{RND})}}{-a}; |a=a1| = \frac{\ln{(1-a1^2\cdot{RND})}}{-a1}}$".replace("a1",str(a_round))
            t_gen = 'generator I'
            t_undf = r'$\mathregular{\frac{\ln{(1 - a^2 \cdot{RND})}}{-a}; |a=a1|}$'.replace('a1', str(a_round))
            t_df = r'$\mathregular{\frac{\ln{(1-a1^2\cdot{RND})}}{-a1}}$'.replace('a1', str(a_round))
            title = ' = '.join([t_gen, t_undf, t_df])
            plt.title(title)
            plt.xlabel("s")
            # ylabel = "Integral(exp1(a,s))ds"
            ylabel = r'$\int exp1(a,s) \,ds$'
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
            title = r"$\mathregular{F(s) = RND = \frac{1 - e^{-a\cdot{s}}}{a^2}; |a=a1| = \frac{1 - e^{-a1\cdot{s}}}{a1^2}}$".replace("a1",str(a_round))
            t_fs = r'$\mathregular{F(s)}$'
            t_rnd = r'$\mathregular{RND}$'
            t_int = r'$\mathregular{\int_0 ^s \frac{e^{-a\cdot{s}}}{a} \,ds}$'
            t_undf = r'$\mathregular{\frac{1 - e^{-a\cdot{s}}}{a^2}; |a=a1|}$'.replace('a1', str(a_round))
            t_df = r'$\mathregular{\frac{1 - e^{-a1\cdot{s}}}{a1^2}}$'.replace('a1', str(a_round))
            title = ' = '.join([t_fs, t_rnd, t_int, t_undf, t_df])
            plt.title(title)
            plt.xlabel("s")
            plt.ylabel("F(s) = distribution")
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
            # title = r"$\mathregular{\frac{\ln{(1 - a^2 \cdot{RND})}}{-a}; |a=a1| = \frac{\ln{(1-a1^2\cdot{RND})}}{-a1}}$".replace("a1",str(a_round))
            t_gen = 'generator I'
            t_undf = r'$\mathregular{\frac{\ln{(1 - a^2 \cdot{RND})}}{-a}; |a=a1|}$'.replace('a1', str(a_round))
            t_df = r'$\mathregular{\frac{\ln{(1-a1^2\cdot{RND})}}{-a1}}$'.replace('a1', str(a_round))
            title = ' = '.join([t_gen, t_undf, t_df])
            plt.title(title)
            plt.xlabel("rnd = F(S)")
            plt.ylabel("s")
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
            t_ps = 'p(s)'
            t_parab = r'$\mathregular{parabola1(s)}$'
            t_df = r'$\mathregular{-s^2+\pi^2}$'
            title = ' = '.join([t_ps, t_parab, t_df])
            plt.title(title)
            plt.xlabel(r"$\pi\cdot{s}$")
            plt.ylabel("p(s) = parabola1(s)")
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
            t_int = r'$\mathregular{\int parabola1(s) \,ds}$'
            t_int_undf = r'$\mathregular{\int (-s^2+\pi^2) \,ds}$'
            t_undf = r'$\mathregular{-\frac{1}{3}x^3 + \pi^2 x}$'
            title = ' = '.join([t_int, t_int_undf, t_undf])
            plt.title(title)
            plt.xlabel("s")
            ylabel = r'$\int parabola1(s) \,ds$'
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
            t_fs = r'$\mathregular{F(s)}$'
            t_rnd = r'$\mathregular{RND}$'
            t_int = r'$\mathregular{\int_{-\pi} ^s (-s^2+\pi^2) \,ds}$'
            t_1 = r'$\mathregular{-\frac{1}{3}(x-2\pi)(x+\pi)^2}$'
            t_2 = r'$\mathregular{-\frac{1}{3}x^3 + \pi^2 x + \frac{2}{3} \pi^3}$'
            title = ' = '.join([t_fs, t_rnd, t_int, t_1, t_2])
            plt.title(title)
            plt.xlabel("s")
            plt.ylabel("F(s) = distribution")
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
            t_int = r'$\mathregular{\int parabola1(s) \,ds}$'
            t_int_undf = r'$\mathregular{\int (-s^2+\pi^2) \,ds}$'
            t_undf = r'$\mathregular{-\frac{1}{3}x^3 + \pi^2 x}$'
            title = ' = '.join([t_int, t_int_undf, t_undf])
            plt.title(title)
            plt.xlabel("s")
            ylabel = r'$\int parabola1(s) \,ds$'
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
            t_fs = r'$\mathregular{F(s)}$'
            t_rnd = r'$\mathregular{RND}$'
            t_int = r'$\mathregular{\int_{-\pi} ^s (-s^2+\pi^2) \,ds}$'
            t_1 = r'$\mathregular{-\frac{1}{3}(x-2\pi)(x+\pi)^2}$'
            t_2 = r'$\mathregular{-\frac{1}{3}x^3 + \pi^2 x + \frac{2}{3} \pi^3}$'
            title = ' = '.join([t_fs, t_rnd, t_int, t_1, t_2])
            plt.title(title)
            plt.xlabel("s")
            plt.ylabel("F(s) = distribution")
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
            t0 = "generator II"
            t1 = r"$\mathregular{roots(F(s) - RND)}$"
            t2 = r'$\mathregular{roots(-\frac{1}{3}x^3 + \pi^2 x + \frac{2}{3} \pi^3 - RND)}$ dla s $\in$ $<-\pi, \pi>$' + '<{}, {}>'.format(round(min_s_scope, 2), round(max_s_scope, 2))
            title = ' = '.join([t0, t1, t2])
            plt.title(title)
            plt.xlabel("rnd = F(S)")
            plt.ylabel("s")
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
            scope_half_cr = np.append(np.arange(0,1,0.01), 1)[1:]
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


    class Test_Slice():
        def __init__(self):
            pass

        def fromObj3D(self):
            # create objects
            test_Object3D = Test.Test_Object3D()
            ob = test_Object3D.obj3d_array_for_tests(method="end_p")
            # ob = ob[5:]
            # visualize
            vis = ByVispy()
            matplot = ByMatplotlib()
            for i in range(len(ob)):
                o = ob[i]
                title = "ob" + str(i)
                # vis.show_body(o, title=title)
                matplot.show_stride(o, stride=10, title=title)
                





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
        t.fromObj3D()


def main():
    test = Test()

    # generator liczb losowych
    # test.test8()
    # test.test9()

    # generator liczb losowych scope
    # test.test10()
    # test.test11()

    # wizualizacja i slice
    # test.test13()
    # test.test14()

    # testy generatory raport
    test.test1()

if __name__ == '__main__':
    main()