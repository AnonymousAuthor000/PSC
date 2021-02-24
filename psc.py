import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics
import numpy as np
import argparse
import csv
import os

font1 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 12,
}

def parse_args():

    parser = argparse.ArgumentParser(description='PSC')
    parser.add_argument('--root', dest='root',
                        help='where results (csv file) exit',
                        default='./csv', type=str)
    parser.add_argument('--data', dest='data',
                        help='MNIST, CIFAR10, ImageNet',
                        default='MNIST', type=str)
    parser.add_argument('--attack', dest='attack',
                        help='FGSM, BIM, PGD',
                        default=['FGSM', 'BIM', 'PGD'], type=list)
    parser.add_argument('--d', dest='d',
                        help='the order of the Polynomial',
                        default=5, type=int)
    parser.add_argument('--r', dest='r',
                        help='resolution of the attack distance',
                        default=10, type=int)
    parser.add_argument('--range', dest='range',
                        help='the range of the attack distance',
                        default=[0.0, 3.0], type=list)
    parser.add_argument('--lines', dest='lines',
                        help='line numbers in csv',
                        default=[129, 252, 502], type=list)
    args = parser.parse_args()
    return args

args = parse_args()
ploy = PolynomialFeatures(args.d)
# the range of the attack distance
dist_range = np.array([i/100. for i in range(int(args.range[1]*100)+1)]).reshape(int(args.range[1]*100)+1, 1)
dist_range_ploy = ploy.fit_transform(dist_range)

divd = (args.range[1] - args.range[0]) / args.r
xMajorLocator = MultipleLocator(divd)
xMinorLocator = MultipleLocator(divd/2)
xMajorFormatter = FormatStrFormatter('%1.1f')

def ComputePSC(x, y, length=args.r+1, dist_range=dist_range, dist_range_ploy=dist_range_ploy):
    # fit
    fit_ary = np.array(x).reshape(length, 1)
    fit_ploy = ploy.fit_transform(fit_ary)
    lr = LinearRegression()
    lr.fit(fit_ploy, y)
    pred = lr.predict(dist_range_ploy)
    psc_fit = metrics.auc(dist_range, pred)
    return psc_fit, pred

def Readcsv(csvfile, start, end, divd, r):
    l2 = [0.]
    asr = [0.]
    tmp = 0.
    x = 0.
    y = 0.
    i = 1
    for item in csvfile:
        if csvfile.line_num < start:
            continue
        if csvfile.line_num > end:
            print('no more numbers')
            break
        if round(float(item[1]), 2) < divd * i + 0.01:
            if float(item[2]) > tmp:
                tmp = float(item[2])
                x = round(float(item[1]), 2)
                y = round(float(item[2])/100, 2)
            if abs(round(float(item[1]), 2) - divd * i) < 0.05:
                l2.append(x)
                asr.append(y)
                i = i + 1
        if i > r:
            # print('done')
            break
    return l2, asr

fig, (ax_fit, ax_ply) = plt.subplots(1, 2, figsize=(9, 4))
clr_scatter = ["#006d2c", "#08519c", "#a50f15", "#6a51a3"]
clr_plot = ["#4daf4a", "#377eb8", "#e41a1c", "#984ea3"]
def DrawPic(x, y, x_fit, y_fit, fitStr, plyStr, i):
    ax_fit.scatter(x, y, facecolor=clr_scatter[i], edgecolor=clr_scatter[i], s=20)
    ax_fit.plot(x_fit, y_fit, c=clr_plot[i], linestyle=(0, (3, 1, 1, 1)), label=fitStr)
    ax_fit.set_ylabel('Attack Success Rate', fontdict=font1)
    ax_fit.set_xlabel('Average Attack Distance ($\ell_2$)', fontdict=font1)
    ax_fit.set_title(args.data + ' ($r=' + str(args.r) + ',d=' + str(args.d) + ')$', fontdict=font1)
    ax_fit.legend(ncol=1, loc=2, framealpha=0.5)
    ax_fit.spines['right'].set_visible(False)
    ax_fit.spines['top'].set_visible(False)
    ax_fit.grid(axis='x', linestyle='-.')
    ax_fit.xaxis.set_major_locator(xMajorLocator)
    ax_fit.xaxis.set_major_formatter(xMajorFormatter)
    ax_fit.xaxis.set_minor_locator(xMinorLocator)

    ax_ply.scatter(x, y, facecolor=clr_scatter[i], edgecolor=clr_scatter[i], s=20)
    ax_ply.plot(x, y, c=clr_plot[i], linestyle=(0, (3, 1, 1, 1)), label=plyStr)
    ax_ply.set_ylabel('Attack Success Rate', fontdict=font1)
    ax_ply.set_xlabel('Average Attack Distance ($\ell_2$)', fontdict=font1)
    ax_ply.set_title(args.data + ' ($r=' + str(args.r) + ')$', fontdict=font1)
    ax_ply.legend(ncol=1, loc=2, framealpha=0.5)
    ax_ply.spines['right'].set_visible(False)
    ax_ply.spines['top'].set_visible(False)
    ax_ply.grid(axis='x', linestyle='-.')
    ax_ply.xaxis.set_major_locator(xMajorLocator)
    ax_ply.xaxis.set_major_formatter(xMajorFormatter)
    ax_ply.xaxis.set_minor_locator(xMinorLocator)

if __name__ == '__main__':

    n = len(args.attack)
    for i in range(n):
        # read data
        path = os.path.join(args.root, args.data, args.attack[i]+'.csv')
        # print('path', path)
        csv_file = open(path, 'r')
        reader = csv.reader(csv_file)
        x, y = Readcsv(csvfile=reader, start=4,
                       end=args.lines[i], divd=divd, r=args.r)
        csv_file.close()
        if len(x) < args.r + 1:
            print('find no enough numbers!')
            break

        # compute psc
        fitPSC, fitPred = ComputePSC(x=x, y=y, length=args.r+1)
        fitStr = args.attack[i] + ' (AUC=' + str(round(fitPSC, 2)) +')'
        plyPSC = metrics.auc(x, y)
        plyStr = args.attack[i] + ' (AUC=' + str(round(plyPSC, 2)) +')'

        # draw
        DrawPic(x=x, y=y, x_fit=dist_range, y_fit=fitPred,
                fitStr=fitStr, plyStr=plyStr, i=i)

    # show
    plt.tight_layout()
    plt.show()
