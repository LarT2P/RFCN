# RFCN 
pytorch版的做显著性检测的RFCN[1]的代码。和matlab原版有点不同。
* 我没有实现原版产生prior map的方法，而是训练时输入prior map。
* 加入了扩张卷积
* 不同层预测结果用串联结合（原版是相加）

还没有测试过效果。

## requirement
pytorch, [tensorboard-pytorch](https://github.com/lanpa/tensorboard-pytorch), tensorboard

如果不需要可视化就不需要tensorboard和tensorboard-pytorch。删除代码里可视化的部分就能运行。
（现在新版改名叫tensorboardX了，如果下载了新版的tensorboard-pytorch就把import tensorboard改成import tensorboardX）

## usage
1. 准备训练图片和validation图片，包括prior maps。图片的文件夹如此组织：
```
DATASET/images/images/图片们.jpg
DATASET/先验图文件夹名字/priormaps.png
DATASET/masks/真值们.png
```
2. 改代码里的数据集路径。ptag改成先验图文件夹名字。
3. 打开tensorboard
```shell
tensorboard --logdir runs

```
4. 运行
* 有循环的
```shell
python train_rfcn.py
```
* 没有循环的
```angular2html
python train_fcn.py
```


[1] Wang, Linzhao, et al. "Saliency detection with recurrent fully convolutional networks." European Conference on Computer Vision. Springer International Publishing, 2016.
