import random
import json
import math
import numpy as np

class MyRandom():

    def __init__(self):
        pass

    def wiawib(self, a, b, precision):
        """
        Generate random number from closed interval <a, b>
        (WIth A WIth B)
        """
        rnd = random.randint(a, (b-a)*10 ** precision) / float((b-a)*10 ** precision)
        return rnd
        

class FeatureSampling():

    def __init__(self):
        with open("config.json") as f:
            # get simulation config parameters
            config = json.load(f)
        random.seed = config["random_seed"]
        self.precision = config["precision"]
        self.funSampling = FunSampling(self.precision)
    
    def light_source_point_sampling(self):
        return self.funSampling.exp1(2)


class MonteCarloSampling():
    def __init__(self):
        # 1. classes interfaces
        funOrigin = FunOrigin()
        funIntegral = FunIntegral()
        funDistibution = FunDistibution()
        funSampling = FunSampling()
        # 2. mathematical functions
        self.exp1 = FunInterface(funOrigin.exp1, funIntegral.exp1, funDistibution.exp1, funSampling.exp1)
        self.exp1_d = FunInterface(funOrigin.exp1, funIntegral.exp1, funDistibution.exp1_d, funSampling.exp1_d)
        self.parabola1 = FunInterface(funOrigin.parabola1, funIntegral.parabola1, funDistibution.parabola1, funSampling.parabola1)
        # 3. functions labels

        # 3.1. exp1

        # 3.1.1. function origin
        t_ps = r'$\mathregular{p(s)}$'
        t_exp = r'$\mathregular{exp1(a,s)}$'
        t_undf = r'$\mathregular{\frac{e^{-a\cdot{s}}}{a}; |a=a1|}$'
        t_df = r'$\mathregular{\frac{e^{-a1\cdot{s}}}{a1}}$'
        title = ' = '.join([t_ps, t_exp, t_undf, t_df])
        xlabel = "s"
        ylabel = "p(s)"
        self.exp1.function_label = ChartLabel(xlabel, ylabel, title)

        # 3.1.2. integral
        t_int = r'$\mathregular{\int exp1(a,s) \,ds}$'
        t_int_undf = r'$\mathregular{\int \frac{e^{-a\cdot{s}}}{a} \,ds}$'
        t_undf = r'$\mathregular{\frac{-e^{-a\cdot{s}}}{a^{2}}; |a=a1|}$'
        t_df = r'$\mathregular{\frac{-e^{-a1\cdot{s}}}{a1^{2}}}$'
        title = ' = '.join([t_int, t_int_undf, t_undf, t_df])
        xlabel = "s"
        # ylabel = "Integral(exp1(a,s))ds"
        ylabel = r'$\int exp1(a,s) \,ds$'
        self.exp1.integral_label = ChartLabel(xlabel, ylabel, title)

        # 3.1.3. distribution
        t_fs = r'$\mathregular{F(s)}$'
        t_rnd = r'$\mathregular{RND}$'
        t_int = r'$\mathregular{\int_0 ^s \frac{e^{-a\cdot{s}}}{a} \,ds}$'
        t_undf = r'$\mathregular{\frac{1 - e^{-a\cdot{s}}}{a^2}; |a=a1|}$'
        t_df = r'$\mathregular{\frac{1 - e^{-a1\cdot{s}}}{a1^2}}$'
        title = ' = '.join([t_fs, t_rnd, t_int, t_undf, t_df])
        xlabel = "s"
        ylabel = "F(s) = distribution"
        self.exp1.distribution_label = ChartLabel(xlabel, ylabel, title)

        # 3.1.4. functionForSampling
        t_gen = 'generator I'
        t_undf = r'$\mathregular{\frac{\ln{(1 - a^2 \cdot{RND})}}{-a}; |a=a1|}$'
        t_df = r'$\mathregular{\frac{\ln{(1-a1^2\cdot{RND})}}{-a1}}$'
        title = ' = '.join([t_gen, t_undf, t_df])
        xlabel = "rnd = F(S)"
        ylabel = "s"
        self.exp1.functionForSampling_label = ChartLabel(xlabel, ylabel, title)

        # 3.2. parabola1

        # 3.2.1. function origin
        t_ps = 'p(s)'
        t_parab = r'$\mathregular{parabola1(s)}$'
        t_df = r'$\mathregular{-s^2+\pi^2}$'
        title = ' = '.join([t_ps, t_parab, t_df])
        xlabel = r"$\pi\cdot{s}$"
        ylabel = "p(s) = parabola1(s)"
        self.parabola1.function_label = ChartLabel(xlabel, ylabel, title)

        # 3.2.2. integral
        t_int = r'$\mathregular{\int parabola1(s) \,ds}$'
        t_int_undf = r'$\mathregular{\int (-s^2+\pi^2) \,ds}$'
        t_undf = r'$\mathregular{-\frac{1}{3}x^3 + \pi^2 x}$'
        title = ' = '.join([t_int, t_int_undf, t_undf])
        xlabel = "s"
        ylabel = r'$\int parabola1(s) \,ds$'
        self.parabola1.integral_label = ChartLabel(xlabel, ylabel, title)

        # 3.2.3. distribution
        t_fs = r'$\mathregular{F(s)}$'
        t_rnd = r'$\mathregular{RND}$'
        t_int = r'$\mathregular{\int_{-\pi} ^s (-s^2+\pi^2) \,ds}$'
        t_1 = r'$\mathregular{-\frac{1}{3}(x-2\pi)(x+\pi)^2}$'
        t_2 = r'$\mathregular{-\frac{1}{3}x^3 + \pi^2 x + \frac{2}{3} \pi^3}$'
        title = ' = '.join([t_fs, t_rnd, t_int, t_1, t_2])
        xlabel = "s"
        ylabel = "F(s) = distribution"
        self.parabola1.distribution_label = ChartLabel(xlabel, ylabel, title)

        # 3.2.4. funSampling
        t0 = "generator II"
        t1 = r"$\mathregular{roots(F(s) - RND)}$"
        t2 = r'$\mathregular{roots(-\frac{1}{3}x^3 + \pi^2 x + \frac{2}{3} \pi^3 - RND)}$ dla s $\in$ $<-\pi, \pi>$'
        title = ' = '.join([t0, t1, t2])
        xlabel = "rnd = F(S)"
        ylabel = "s"
        self.parabola1.functionForSampling_label = ChartLabel(xlabel, ylabel, title)



class FunInterface():
    def __init__(self, fun, integral, distribution, funSamp):
        # mathematical functions
        self.function = fun
        self.integral = integral
        self.distribution = distribution
        self.functionForSampling = funSamp
        # functions labels
        self.function_label = ChartLabel()
        self.integral_label = ChartLabel()
        self.distribution_label = ChartLabel()
        self.functionForSampling_label = ChartLabel()


class ChartLabel():
    def __init__(self, xlabel="", ylabel="", title=""):
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title


class FunOrigin():

    def __init__(self):
        pass

    def exp1(self, a, s):
        """
        p(s) = exp1()
        p(s) = exp(-as)/a
        F(s) = RND = (1 - exp(-as))/a**2
        F(s) - distribution function
        s - value of the feature
        p(s) - probability of value s of the feature
        RND - random number <0,1>
        a - parameter
        :param a: parameter
        :param s: feature value of which probability we want to get
        """
        return math.exp(-a*s)/a
    
    def parabola1(self, x):
        a = -1
        b = 0
        c = math.pi**2
        return a*x**2 + b*x + c


class FunIntegral():
    def __init__(self):
        pass

    def exp1(self, a, s):
        return (-math.exp(-a*s))/a**2
    
    def parabola1(self, s):
        return (math.pi**2)*s-(s**3)/3


class FunDistibution():
    # constant beginning of integration scope

    def __init__(self):
        pass

    def exp1(self, a, s):
        # constant integration scope <0, s> (in distribution)
        return (1 - math.exp(-a*s))/a**2
    
    def exp1_d(self, a, s, s1):
        # dynamic integration scope <s1, s> (in distribution)
        funIntegral = FunIntegral()
        distFun = funIntegral.exp1
        return distFun(a=a, s=s) - distFun(a=a, s=s1)
    
    def parabola1(self, s):
        # constant integration scope <-pi, s> (in distribution)
        polyval = np.polynomial.polynomial.polyval(s, [2/3*(math.pi**3), math.pi**2, 0, -1/3])
        return polyval




class FunSampling():

    def __init__(self, precision=6):
        self.precision = precision

    def exp1(self, a, rnd=None, min_rnd=0, max_rnd=1-math.exp(-10), min_scope=0, max_scope=10):
        """
        constant integration scope <0, s> (in distribution)
        min_rnd=0 and min_scope=0 should not be changed
        these is because of constant integration scope <0, s> (in distribution)

        p(s) = exp(-as)/a
        F(s) = RND = (1 - exp(-as))/a**2
        F(s) - distribution function
        s = exp1()
        s - value of the feature
        s = math.log(1 - a**2 * RND) / -a
        p(s) - probability of value s of the feature
        RND - random number <0,1>
        a - parameter
        :param a: parameter
        :param rnd: if None (default), algorithm will rand this number from <min_rnd, max_rnd>
        :param min_rnd: minimum value used in uniform random number generator = distribution(min_scope), if None count auto using min_scope
        :param max_rnd: maximum value used in uniform random number generator = distribution(max_scope), if None count auto using max_scope
        :param min_scope: minimum value of feature s, that will be generated
        :param max_scope: maximum value of feature s, that will be generated
        """
        prec = self.precision
        if rnd is None:
            myRandom = MyRandom()
            if max_rnd is None:
                funDistibution = FunDistibution()
                max_rnd = funDistibution.exp1(a,s=max_scope)
            if min_rnd is None:
                funDistibution = FunDistibution()
                min_rnd = funDistibution.exp1(a,s=min_scope)
            rnd = myRandom.wiawib(a=min_rnd, b=max_rnd, precision=prec)
        # else rnd is given for test reasons as a parameter
        s = math.log(1 - a**2 * rnd) / -a
        return s
    
    def exp1_d(self, a, min_rnd, max_rnd, min_scope, max_scope, rnd=None):
        """
        dynamic integration scope <s1, s> (in distribution)
        min_rnd=0 and min_scope=0 CAN be changed

        p(s) = exp(-as)/a
        F(s) = RND = (1 - exp(-as))/a**2
        F(s) - distribution function
        s = exp1()
        s - value of the feature
        s = math.log(1 - a**2 * RND) / -a
        p(s) - probability of value s of the feature
        RND - random number <0,1>
        a - parameter
        :param a: parameter
        :param rnd: if None (default), algorithm will rand this number from <min_rnd, max_rnd>
        :param min_rnd: minimum value used in uniform random number generator = distribution(min_scope), if None count auto using min_scope
        :param max_rnd: maximum value used in uniform random number generator = distribution(max_scope), if None count auto using max_scope
        :param min_scope: minimum value of feature s, that will be generated
        :param max_scope: maximum value of feature s, that will be generated
        """
        prec = self.precision
        if rnd is None:
            myRandom = MyRandom()
            if max_rnd is None:
                funDistibution = FunDistibution()
                max_rnd = funDistibution.exp1_d(a, s1=min_scope, s=max_scope)
            if min_rnd is None:
                funDistibution = FunDistibution()
                min_rnd = funDistibution.exp1_d(a, s1=min_scope, s=min_scope)
            rnd = myRandom.wiawib(a=min_rnd, b=max_rnd, precision=prec)
        # else rnd is given for test reasons as a parameter
        s = math.log(math.exp(-a*min_scope) - a**2 * rnd) / -a
        return s
    
    def exp1_aprox(self, a, rnd=None, min_rnd=0, max_rnd=1-math.exp(-10), min_scope=0, max_scope=10):
        """
        constant integration scope <0, s> (in distribution)
        min_rnd=0 and min_scope=0 should not be changed
        these is because of constant integration scope <0, s> (in distribution)

        variant from the literature
        
        p(s) = exp(-as)/a
        F(s) = RND = (1 - exp(-as))/a**2
        F(s) - distribution function
        s = exp1()
        s - value of the feature
        p(s) - probability of value s of the feature
        RND - random number <0,1>
        a - parameter
        :param a: parameter
        :param rnd: if None (default), algorithm will rand this number from <0,1>
        :param min_rnd: minimum value used in uniform random number generator = distribution(min_scope), if None count auto using min_scope
        :param max_rnd: maximum value used in uniform random number generator = distribution(max_scope), if None count auto using max_scope
        :param min_scope: minimum value of feature s, that will be generated
        :param max_scope: maximum value of feature s, that will be generated
        """
        prec = self.precision
        if rnd is None:
            myRandom = MyRandom()
            if max_rnd is None:
                funDistibution = FunDistibution()
                max_rnd = funDistibution.exp1(a,s=max_scope)
            if min_rnd is None:
                funDistibution = FunDistibution()
                min_rnd = funDistibution.exp1(a,s=min_scope)
            rnd = myRandom.wiawib(a=min_rnd, b=max_rnd, precision=prec)
        # else rnd is given for test reasons as a parameter
        # s = -math.log(1-rnd) / a
        s = -math.log(rnd) / a #flipped
        return s
    
    def parabola1(self, rnd=None, filt_roots=True, debug=False,  min_rnd=0, max_rnd=4*(math.pi**3)/3, min_scope=-math.pi, max_scope=math.pi):
        """"
        constant integration scope <-pi, s> (in distribution)
        these values should not be changed:
        min_rnd=0, max_rnd=4*(math.pi**3)/3, min_scope=-math.pi, max_scope=math.pi
        you can set another values only for test reasons, but they will not have a sense,
        because of constant integration scope <-pi, s> (in distribution)
        also the probability function is only positive in scope (-pi, pi)
        """
        prec = self.precision
        if rnd is None:
            myRandom = MyRandom()
            if max_rnd is None:
                funDistibution = FunDistibution()
                max_rnd = funDistibution.parabola1(s=max_scope)
            if min_rnd is None:
                funDistibution = FunDistibution()
                min_rnd = funDistibution.parabola1(s=min_scope)
            rnd = myRandom.wiawib(a=min_rnd, b=max_rnd, precision=prec)
        # else rnd is given for test reasons as a parameter
        poly = np.polynomial.polynomial.Polynomial([2/3*(math.pi**3)-rnd, math.pi**2, 0, -1/3])
        roots = poly.roots()
        if debug:
            print(roots)
        roots_real = np.real(roots)
        if filt_roots:
            filt1 = min_scope <= roots_real
            filt2 = roots_real <= max_scope
            filt = filt1 & filt2
            roots_scope = roots_real[filt]
            if debug:
                print(roots_scope)
            if len(roots_scope) > 1:
                result = roots_scope[1]
            elif len(roots_scope) < 1:
                raise NotADirectoryError("roots are not in scope")
            else:
                result = roots_scope[0]
        else:
            result = roots_real
        return result