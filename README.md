# Piecewise Sampling Curving

---
## Usage

#### 1. Demo
<font size=2>Simply run command below, you can get AUC of FGSM, BIM and PGD on MNIST.</font>
```
Python psc.py
```

#### 2. Test
<font size=2>Please put your result (csv file) into the csv/data/YourAdv.csv, then run:</font>
```
Python psc.py --data=MNIST --attack=['FGSM', 'BIM', 'PGD', 'YourAdv'] \
              --d=5 --r=10 --range=[0., 3.] --lines=[129, 252, 502, n]
```
* <font size=2> data: dataset your attack performs on. </font>
* <font size=2> attack: attack methods you want to compare with. </font>
* <font size=2> d: the order of the Polynomial. </font>
* <font size=2> r: resolution of your x-axis. </font>
* <font size=2> range: the range of your x-axis. </font>
* <font size=2> lines: the max line number for attack methods to search in csv. </font>

#### 3. Reporduce
<font size=2>Results on this project can be generated based on settings below.</font>

##### 3.1. Prerequisites
* <font size=2> Python 3.6 </font>
* <font size=2> Pytorch 1.0+ </font>

##### 3.2. Pretrained Model
<font size=2> We used three pretrained models in this project.</font>
* <font size=2> [Net](https://drive.google.com/drive/folders/1cO1lEXiiQgUE9PKdXsuVr5TsPEAS4ras) for MNIST </font>
* <font size=2> [VGG16](https://drive.google.com/drive/folders/1zMUAV4rV0pYIayOCWB4iCIMN0vHOfWUs) for CIFAR-10 </font>
* <font size=2> VGG16 for ImageNet: Pytorch pre-trained model </font>

##### 3.3. Adversarial Attacks
Tool |  Attacks
---------|----------
[Foolbox](https://foolbox.readthedocs.io/) |  Boundary[[8]](https://arxiv.org/abs/1712.04248)
[ART](https://github.com/Trusted-AI/adversarial-robustness-toolbox) | Square[[6]](https://arxiv.org/abs/1912.00049), HSJA[[9]](https://arxiv.org/abs/1904.02144)
[Advertorch](https://advertorch.readthedocs.io/en/latest/index.html) | FGSM[[1]](https://arxiv.org/abs/1412.6572), BIM[[2]](https://arxiv.org/abs/1607.02533), PGD[[3]](https://arxiv.org/abs/1706.06083), MIA[[4]](https://arxiv.org/abs/1710.06081)
Official | [Bandits](https://github.com/MadryLab/blackbox-bandits)[[5]](https://arxiv.org/abs/1807.07978), [Simba-DCT](https://github.com/cg563/simple-blackbox-attack)[[7]](https://arxiv.org/abs/1905.07121), [RayS](https://github.com/uclaml/RayS)[[10]](https://arxiv.org/abs/2006.12792)

---
## Benchmarking

We benchmark various adversarial attack methods under PSC (Piecewise Sampling Curving) framework thoroughly on three datasets: MNIST, CIFAR-10 and ImageNet.

#### 1. MNIST
##### 1.1 Gradient-based Attacks (x - attack distance $\ell_2$, y - attack success rate)
<table>
    <tr>
        <td rowspan='2' style="text-align:center">Attack</td>
        <td rowspan='2' style="text-align:center">Model</td>
        <td colspan='2' style="text-align:center">AUC@[0.0, 3.0]</td>
    </tr>
    <tr>
        <td style="text-align:center">Untargeted</td>
        <td style="text-align:center">Targeted</td>
    </tr>
    <tr>
        <td style="text-align:left">FGSM</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">0.26</td>
        <td style="text-align:center">-</td>
    </tr>
    <tr>
        <td style="text-align:left">BIM</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">1.37</td>
        <td style="text-align:center">-</td>
    </tr>
    <tr>
        <td style="text-align:left">PGD</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">1.48</td>
        <td style="text-align:center">-</td>
    </tr>
    <tr>
        <td style="text-align:left">MIA</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">-</td>
        <td style="text-align:center">-</td>
    </tr>
<table>

##### 1.2.1 Score-based Attacks (x - attack distance $\ell_2$, y - attack success rate)
<table>
    <tr>
        <td rowspan='2' style="text-align:center">Attack</td>
        <td rowspan='2' style="text-align:center">Model</td>
        <td colspan='2' style="text-align:center">AUC@[0.0, 3.0]</td>
    </tr>
    <tr>
        <td style="text-align:center">Untargeted</td>
        <td style="text-align:center">Targeted</td>
    </tr>
    <tr>
        <td style="text-align:left">Bandits</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">-</td>
        <td style="text-align:center">-</td>
    </tr>
    <tr>
        <td style="text-align:left">Square</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">-</td>
        <td style="text-align:center">-</td>
    </tr>
    <tr>
        <td style="text-align:left">SimBA-DCT</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">-</td>
        <td style="text-align:center">-</td>
    </tr>
<table>

##### 1.2.2 Score-based Attacks (x - number of queries, y - attack success rate)
<table>
    <tr>
        <td rowspan='2' style="text-align:center">Attack</td>
        <td rowspan='2' style="text-align:center">Model</td>
        <td colspan='2' style="text-align:center">AUC@[-, -]</td>
    </tr>
    <tr>
        <td style="text-align:center">Untargeted</td>
        <td style="text-align:center">Targeted</td>
    </tr>
    <tr>
        <td style="text-align:left">Bandits</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">-</td>
        <td style="text-align:center">-</td>
    </tr>
    <tr>
        <td style="text-align:left">Square</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">-</td>
        <td style="text-align:center">-</td>
    </tr>
    <tr>
        <td style="text-align:left">SimBA-DCT</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">-</td>
        <td style="text-align:center">-</td>
    </tr>
<table>

##### 1.3. Decision-based Attacks (x - number of queries, y - attack distance $\ell_2$)
<table>
    <tr>
        <td rowspan='2' style="text-align:center">Attack</td>
        <td rowspan='2' style="text-align:center">Model</td>
        <td colspan='2' style="text-align:center">AUC@[-, -]</td>
    </tr>
    <tr>
        <td style="text-align:center">Untargeted</td>
        <td style="text-align:center">Targeted</td>
    </tr>
    <tr>
        <td style="text-align:left">Boundary</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">-</td>
        <td style="text-align:center">-</td>
    </tr>
    <tr>
        <td style="text-align:left">HSJA</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">-</td>
        <td style="text-align:center">-</td>
    </tr>
    <tr>
        <td style="text-align:left">RayS</td>
        <td style="text-align:center">VGG-16</td>
        <td style="text-align:center">-</td>
        <td style="text-align:center">-</td>
    </tr>
<table>

#### 2. CIFAR-10

#### 3. ImageNet

---
## Reference
<font size=1>

[1] Goodfellow, I. J., Shlens, J., and Szegedy, C. Explaining and harnessing adversarial examples. ICLR, 2015.

[2] Kurakin, A., Goodfellow, I., and Bengio, S. Adversarial examples in the physical world. ICLR, 2017.

[3] Madry, A., Makelov, A., Schmidt, L., Tsipras, D., and Vladu, A. Towards deep learning models resistant to adversarial attacks. ICLR, 2018.

[4] Dong, Y., Liao, F., Pang, T., Su, H., Zhu, J., Hu, X., and Li, J. Boosting Adversarial Attacks with Momentum. CVPR, 2018.

[5] Ilyas, A., Engstrom, L., and Madry, A. Prior convictions: Black-box adversarial attacks with bandits and priors. ICLR, 2019.

[6] Andriushchenko, M., Croce, F., Flammarion, N., and Hein, M. Square attack: a query-efficient black-box adversarial attack via random search. In European Conference on Computer Vision, pp. 484–501. Springer, 2020.

[7] Guo, C., Gardner, J., You, Y., Wilson, A. G., and Weinberger, K. Simple black-box adversarial attacks. In International Conference on Machine Learning, pp. 2484–2493, 2019.

[8] Brendel, W., Rauber, J., and Bethge, M. Decision-based adversarial attacks: Reliable attacks against black-box machine learning models. arXiv preprint arXiv:1712.04248, 2017.

[9] Chen, J., Jordan, M., and Wainwright, M. HopSkipJumpAttack: A Query-Efficient Decision-Based Attack. arXiv preprint arXiv:1904.0214, 2019.

[10] Chen, J. and Gu, Q. Rays: A ray searching method for hard-label adversarial attack. In Proceedings of the 26rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 2020.
</font>
