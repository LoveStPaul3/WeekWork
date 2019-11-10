# WeekWork
每周的作业

**#2019-11-3**  
==
#总的来说，这周过得很充实，在学习之余，周末有很多好看的比赛，哈哈哈，喜欢的队伍也获得了胜利。这周做的任务是第二部分代码作业，官方已经给出基本框架以及实验内容，自己做的事是关键代码的实现。锻炼的不仅仅是写代码的能力，还有纠错的能力，不由得感叹作业设计的合理性。  
  
  
**计划下一周**开始接触object detection，先在博客上搜索一下object detection的相关只是，然后找几个小的methods复现一下代码，然后做一点实验。同时能够学习更多readme的语法，做出一个较好的报告。
  
  
  
#下面介绍文件夹中各个文件的内容：  
#1.FullyConnectedNets.ipynb： 全连接网络及相关实验  
#2.Dropout.ipynb： 对dropout的实验  
#3.ConvolutionalNetworks.ipynb： 卷积网络（只实现了代码，但是这个运行有点问题，因为电脑对cpython环境出了点问题）  
#4.BatchNormalization.ipynb： 批归一化  
#5.layers.py： 实现一些前向传播、反向传播（包括池化、bn、ReLU、全连接、）  
#6.optim.py： 一些优化算法（sgd，sgd_momentum，rmsprop，adam），部分由官方提供。  
#7.solver.py： 官方提供的接口，由此建立model并进行训练  
#8.fc_net.py： 两个类：1) 两层神经网络 2）多层神经网络  



**#2019-11-10**  
==
这周看完了《Deep Learning for Generic Object Detection: A Survey》，总结了object detection的Two Stage Framework模型，并对Mask-RCNN进行了实验。但是，没有阅读论文进行更深入的阅读，个人计划先做好综述，后面再选择性的深入。  

**计划下一周**再完成Unified Pipeline (One Stage Pipeline)的网络综述，DetectorNet、YOLO、SSD等等。同时也做一个详细的计划表，不然每天有点不清楚自己一天到底做了什么，应该做什么。  

#此次附件中文件比较简单，一个是综述报告，一个是简单实现Mask RCNN的Demo  
