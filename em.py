# -*- coding: utf-8 -*-
from collections import Counter

import numpy as np
from numpy import math
import matplotlib.pyplot as plt

def averageWeight(height,gamma,num):
    mu=0
    for i in range(0,len(height)):
        mu+=gamma[i]*height[i]/num
    return mu

def varianceWeight(height,gamma,mu,num):
    sigma=0
    for i in range(0,len(height)):
        sigma+=gamma[i]*pow((height[i]-mu),2)/num
    return sigma

def isSame(cur,now):
    bool=True
    for i in range(0,len(cur)):
        if abs(cur[i]-now[i])>math.pow(10,-3) :
            bool=False
            break
    return bool

def gauss(x,mu,sigma):
    result=np.exp(-(x - mu) ** 2 / (2 * sigma)) / (math.sqrt(2 * math.pi * sigma))
    return result

def cslcEM(height):
    N=len(height)
    gp=0.5#男，女的概率都为0.5
    bp=0.5
    gmu,gsigma=min(height),1
    bmu,bsigma=max(height),1
    ggamma=range(N)
    bgamma=range(N)
    cur=[gp,bp,gmu,gsigma,bmu,bsigma]
    now=[]

    times=0
    while times<1000:
        i=0
        for x in height:
            ggamma[i]=gp*gauss(x,gmu,gsigma)
            bgamma[i]=bp*gauss(x,bmu,bsigma)
            s=ggamma[i]+bgamma[i]
            ggamma[i]/=s
            bgamma[i]/=s
            i+=1

        gn=sum(ggamma)
        gp=float(gn)/float(N)
        bn=sum(bgamma)
        bp=float(bn)/float(N)
        gmu=averageWeight(height,ggamma,gn)
        gsigma=varianceWeight(height,ggamma,gmu,gn)
        bmu=averageWeight(height,bgamma,bn)
        bsigma=varianceWeight(height,bgamma,bmu,bn)

        now=[gp,bp,gmu,gsigma,bmu,bsigma]
        if isSame(cur,now):
            break
        cur=now

        print "Times:\t",times
        print "Girl mean/gsigma:\t",gmu,gsigma
        print "Boy mean/bsigma:\t",bmu,bsigma
        print "Boy/Girl:\t",bn,gn,bn+gn
        print "\n\n"
        times+=1
    return now

if __name__ == '__main__':
    data = np.loadtxt('HeightWeight.csv', dtype=np.float, delimiter=',', skiprows=1)
    height=data[:,1]
    result=data[:,0]
    boy=float(Counter(result).get(1.0))/float((Counter(result).get(1.0)+Counter(result).get(0.0)))
    girl=float(Counter(result).get(0.0))/float((Counter(result).get(1.0)+Counter(result).get(0.0)))
    now=cslcEM(height)
    x = np.linspace(140, 190, 100)
    bb=1-abs(now[1]-boy)/boy
    gg=1-abs(now[0]-girl)/girl
    print now
    print boy,girl
    print "男性的正确率为%.3f%%"%bb
    print "女性的正确率为%.3f%%"%gg
    plt.plot(x,gauss(x,now[2],now[3]), "r-", linewidth=2)
    plt.plot(x, gauss(x, now[4], now[5]), "b-", linewidth=2)
    plt.grid(True)
    plt.show()