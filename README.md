# project deepGTA5

1.在deepgta5/collect_data/getkeys/screen.py中，采集屏幕时之所以不使用python自带的pillow库（PIL），是因为用pillow采集速度很慢，如果希望每1s采集一个较大的区域，采集下来的图片会有大量没有采集到的地方，也就形成的大块的黑色区域。使用win32API速度会快很多，足以1s采较大的图像，所以选择了使用win32API。

2.参考了NVIDIA论文的[End to End Learning for Self-Driving Cars](https://arxiv.org/abs/1604.07316)，以及论文[Driving in the Matrix: Can Virtual Worlds Replace Human-Generated Annotations for Real World Tasks?](https://arxiv.org/abs/1610.01983)。前者提供了一个可行的卷积神经网络架构，后者说明了在GTA5中训练的self-drving model可以迁移到现实世界中。

## 神经网络架构
