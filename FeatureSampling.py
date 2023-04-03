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
        funOrigin = FunOrigin()
        funIntegral = FunIntegral()
        funDistibution = FunDistibution()
        funSampling = FunSampling()

        self.exp1 = FunInterface(funOrigin.exp1, funIntegral.exp1, funDistibution.exp1, funSampling.exp1)
        self.exp1_d = FunInterface(funOrigin.exp1, funIntegral.exp1, funDistibution.exp1_d, funSampling.exp1_d)
        self.parabola1 = FunInterface(funOrigin.parabola1, funIntegral.parabola1, funDistibution.parabola1, funSampling.parabola1)


class FunInterface():
    def __init__(self, fun, integral, distribution, funSamp):
        self.function = fun
        self.integral = integral
        self.distribution = distribution
        self.functionForSampling = funSamp


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
    
    def parabola1(self, rnd=None, filt_roots=True, debug=True,  min_rnd=0, max_rnd=4*(math.pi**3)/3, min_scope=-math.pi, max_scope=math.pi):
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