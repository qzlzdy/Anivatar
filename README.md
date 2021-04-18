毕业设计：**基于生成对抗网络的动漫头像生成软件开发**

Graduation Project: **Generative Adversarial Network Based Anime Avatar Generator Development**

# 目录

[toc]

# 一、国内外研究动态，选题依据和意义

​        近些年,动漫产业发展迅速,对于动漫角色的设计也愈发丰富,喜欢使用动漫人物的头像作为自己社交平台的头像的用户也大量存在,人们开始追求更加个性化的、与众不同的动漫头像。但创作动漫头像具有一定的难度,创作者需要具备一定的艺术素养和专业技能。生成式对抗网络(Generative Adversarial Network, GAN)的出现^[1]^,带给了动漫爱好者们一个有力的工具,其在生成真实人脸的能力被人们广泛关注。动漫头像与真实人脸并非是完全不同的两种图像,它们之间也存在着一定的关联。正式这种关联使得将生成式对抗网络应用于动漫头像的生成成为可能。GAN提出后,为了提升生成图像的质量,人们在网络结构,损失函数设计,数据集的选择等方面都做了不少尝试。通过使用深度卷积网络,DCGAN^[2]^将图像质量提升了一个水平。WGAN^[3,4]^,WGAN-GP^[5]^则是从损失函数下手,致力于提高训练GAN的稳定性以及避免模式崩塌的问题。PGGAN^[6]^使用了一种渐进式的训练手段,将生成图像的分辨率逐渐由低变高进行训练。这一想法被在后来的许多GAN模型中都有体现。最近,StyleGAN的提出^[7-9]^又使得GAN的生成图像质量获得了显著提升。基于StyleGAN的人脸图像生成和动漫头像生成模型都能生成出高质量的图像,但如果想要对某个特定的条件进行约束,只能从已经随机生成的图像当中寻找特征与潜在空间中的向量之间的关系。为了对生成图像的内容进行控制,人们也提出了更具给定条件来生成图像的CGAN^[10]^,以及在CGAN之后提出的ACGAN^[11]^,LMV-ACGAN^[12]^。对在特定条件下生成动漫人物头像这一任务做出针对性优化的 MakeGirlsMoe^[13]^在一定程度上满足了动漫爱好者对于个性化的需求。StyleGAN提出后,CStyleGAN^[14]^将StyleGAN生成图像的高质量与CGAN根据条件生成图像的可控性结合起来,并应用在商标的生成当中。

​        生成式对抗网络不仅能够用来从“零”生成图片,还可以用于将一种类型的图像转换成另一种类型。这种图像的变换被称作图像翻译^[15]^。但要训练此网络要求使用成对的图像作为训练集,而在现实中获得成对图像的难度较大。针对这一问题,能够使用不成对图像训练的网络CycleGAN^[16]^被提出。CycleGAN使用两组GAN,分别用于两种类型图像的相互转换。能够将真实图像转换为动漫风格图像的网络也开始出现^[17]^。针对CycleGAN的弊端,先后又有人提出了能够在两个以上类型之间相互转换的StarGAN^[18]^,进一步提升转换质量的U-GAT-IT^[19]^等模型。这些模型在生成动漫头像的邻域中也都取得了超过CGAN的效果。在实际的应用中,有时候我们只要求能够做单向的转换,而不需要从目标类型转换回原类型。但CycleGAN的结构要求必须同时训练两组GAN,造成了训练的时间开销和计算资源上的浪费。CouncilGAN^[20]^对此进行了改进,使得图像转换不再需要同时训练两个方向的转换,因此在生成的目标图像当中不再需要保留原图像的某些特征,从而能够生成更加符合目标类型的图像。特别是在动漫头像生成的课题上,类似CycleGAN结构的模型会在生成的动漫头像上仍然保留一些真实人脸的特征,但使用CouncilGAN生成的图像可以看到有明显的改善。

# 二、研究基本内容，拟解决主要问题

​        出于对个性化的追求,人们希望能够按照自己的要求来生成动漫头像。Aaron Gokaslan提供的预训练模型[^1]使用了StyleGAN2,在Danbooru[^2]数据集上训练,能够生成512×512分辨率的动漫头像,但该预训练模型不能由用户设置条件,缺乏一定的可控性。MakeGirlsMoe中提供的在线生成网站[^3]能够满足可控性,使用DRAGAN^[21]^作为基础,在生成图像的质量上稍有不足。此外,人们也尝试使用过PGGAN,MSG-GAN^[22]^,BigGAN^[23]^,SAGAN^[24]^,GAN-QP^[25]^,WGAN-GP等模型用于生成动漫头像,但效果均不理想[^4]。

​        综上所述,为了能够满足用户想要根据自己要求生成特定动漫头像的需求,和解决现存模型生成图像质量不佳的问题,本毕业设计将参考CStyleGAN的做法,StyleGAN2与CGAN结合,旨在训练一个兼具高质量图片和可控性的动漫头像生成模型。同时为了方便广大动漫爱好者使用,将训练好的模型打包为移动应用。用户能够通过安装本应用,设置自己喜欢的动漫头像内容,生成随机头像,并且能够对生产的头像进行简单的修改,以满足自己的要求。

[^1]: https://www.gwern.net/Faces#stylegan-2

[^2]: https://www.gwern.net/Danbooru2020
[^3]: https://make.girls.moe/#/
[^4]:https://www.gwern.net/Faces#appendix

# 三、研究步骤、方法及措施

## （一）准备充足的数据集

​        为了训练一个高质量的模型,需要准备一个好的数据集。Danbooru是一个大规模的动漫图像数据库,包含有420万以上的动漫图像,以及130万准确标注的标签。该数据库的作者每隔一年都会将新创作的动漫图像加入到数据库中,使数据库中的图像更加丰富。上文中提到的StyleGAN2预训练动漫头像生成模型,比较知名的TWDNE(This Waifu Does Not Exist)模型[^5]都使用此数据库训练。完整的Danbooru数据库的大小约为3.7TB,需要使用大量的磁盘空间储存。因此,本毕业设计使用Kaggle上提供的数据库子集[^6],约33万张动漫图像。此外,还有本人从Pixiv[^7],Twitter[^8]等创作或社交平台搜集的约1万张高质量的动漫图像。

[^5]:https://www.gwern.net/TWDNE
[^6]:https://www.kaggle.com/mylesoneill/tagged-anime-illustrations
[^7]:https://www.pixiv.net/
[^8]:https://twitter.com/

## （二）根据标签选择合适的图像

​        Kaggle提供的数据库子集中,图片与标签通过md5哈希值对应。为了方便在训练过程中快速根据文件名获得标签信息,首先需要进行转换,将结果储存为json格式。

​        对于自行搜集的部分图像,使用Github用户RF5提供的预训练动漫图像标注模型[^9]进行标注。该预训练模型同样使用了Danbooru数据库,能够对动漫图像标注六千个不同的标签,并输出相应的概率。这些标签是Danbooru数据库标签的子集,与Kaggle中的标签兼容。本毕业设计使用0.25为概率阈值,对自行搜集的图像进行标注。

​        标注完成后,需要对所有标签进行过滤。Danbooru数据库包含了角色名、作品名、作品类型等种类的标签。本毕业设计中只使用描述外观的标签。对每种外观标签对应的图像数目进行统计后,选择在总数量5%至50%的标签作为训练用的标签,共23个。同时,将风格差异较大的带有素描、漫画等标签的图像丢弃,最后剩余13万张图像。

[^9]:https://github.com/RF5/danbooru-pretrained

## （三）将完整图像裁剪为动漫头像

​        无论是Kaggle的数据集还是自行搜集的数据集,其中包含的图像都是完整的一副作品,无法直接输入进网络进行训练。

​        通过ultraist提供的基于OpenCV的动漫头像检测算法[^10]。该算法返回一张图片中所有可能是人物头像的位置和大小。通过适当的设置后,能够裁剪出肩部以上,包含头顶及两侧耳朵位置的正方形人物头像。

​        剪裁后,还需要人工检查剪裁结果,将错误剪裁的图片及头部姿势不理想的头像删除。最终的训练集大小约为11万张头像。

[^10]:http://ultraist.hatenablog.com/entry/20110718/1310965532

## （四）改进现有模型

​        Github用户rosinality提供了Pytorch框架实现的StyleGAN2模型[^11],PieraRiccio在此基础上添加了对条件的处理[^12],使其能够学习生成单一条件的图像。本毕业设计在此基础上进行修改,使其能够学习多重条件下的图像生成。为了节省训练时间及计算资源,通过GAN生成的图像大小为128×128,随后将使用第(六)节中描述的超分辨率技术将图像放大到512×512大小。

[^11]:https://github.com/rosinality/stylegan2-pytorch
[^12]:https://github.com/PieraRiccio/stylegan2-pytorch

## （五）使用数据集训练模型

​        有了改进的模型后,即可对使用处理好的训练集进行训练。根据数据集的图像质量和模型的参数,训练过程可能持续几天。

## （六）使用超分辨率模型放大图像

​        训练结束后,即可使用模型生成128×128大小动漫头像。为了进一步提升用户体验及展示效果,对生成的动漫头像进行放大。Github用户nagadomi的waifu2x模型[^13]能完成这一任务。

## （七）对生成的图像进一步处理

​        得到256×256大小的动漫头像后,用户可能对某些部分还不太满意,需要进行修正。此处使用传统的数字图像处理方式即能满足用户的大部分需求,包括但不限于缩放,裁剪,调整饱和度等常见操作。

## （八）WEB应用集成

​        最后,以训练好的网络作为核心,将各个子系统集成在一个WEB应用当中。本毕业设计基于Flask框架进行WEB应用的开发。在未来如果条件允许,也会陆续推出Android或PC版本的动漫头像生成应用。

# 四、研究工作进度

| 序号 |         时间         |              内容              |
| :--: | :------------------: | :----------------------------: |
|  1   | 2020.12.2-2020.12.25 | 选好毕业设计题目并准备相关资料 |
|  2   | 2020.12.26-2021.1.10 |           接受任务书           |
|  3   | 2021.1.11-2021.3.14  |     搜集资料,准备开题报告      |
|  4   | 2021.3.15-2021.3.19  |           开题报告会           |
|  5   | 2021.3.20-2021.3.26  |          软件需求分析          |
|  6   |  2021.3.27-2021.4.2  |          软件总体设计          |
|  7   |  2021.4.3-2021.4.9   |          软件详细设计          |
|  8   |  2021.4.10-2021.5.7  |            软件实现            |
|  9   |  2021.5.8-2021.5.20  |            撰写论文            |
|  10  | 2021.5.21-2021.5.27  |         论文评审及查重         |
|  11  |  2021.5.28-2021.6.9  |           答辩报告会           |

# 五、主要参考文献

[1] Goodfellow I J, Pouget-Abadie J, Mirza M, et al. Generative adversarial networks[J]. arXiv preprint arXiv:1406.2661, 2014 

[2] Radford A, Metz L, Chintala S. Unsupervised representation learning with deep convolutional generative adversarial networks[J]. arXiv preprint arXiv:1511.06434, 2015. 

[3] Arjovsky M, Bottou L. Towards principled methods for training generative adversarial networks[J]. arXiv preprint arXiv:1701.04862, 2017. 

[4] Arjovsky M, Chintala S, Bottou L. Wasserstein generative adversarial networks[C]//International conference on machine learning. PMLR, 2017: 214-223. 

[5] Gulrajani I, Ahmed F, Arjovsky M, et al. Improved training of wasserstein gans[J]. arXiv preprint arXiv:1704.00028, 2017. 

[6] Karras T, Aila T, Laine S, et al. Progressive growing of gans for improved quality, stability, and variation[J]. arXiv preprint arXiv:1710.10196, 2017. 

[7] Karras T, Laine S, Aila T. A style-based generator architecture for generative adversarial networks[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2019: 4401-4410. 

[8] Karras T, Laine S, Aittala M, et al. Analyzing and improving the image quality of stylegan[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2020: 8110-8119. 

[9] Karras T, Aittala M, Hellsten J, et al. Training generative adversarial networks with limited data[J]. arXiv preprint arXiv:2006.06676, 2020. 

[10] Mirza M, Osindero S. Conditional generative adversarial nets[J]. arXiv preprint arXiv:1411.1784, 2014. 

[11] Odena A, Olah C, Shlens J. Conditional image synthesis with auxiliary classifier gans[C]//International conference on machine learning. PMLR, 2017: 2642-2651. 

[12] 张扬, 马小虎. 基于改进生成对抗网络的动漫人物头像生成算法[J]. 计算机 科学, 48(1): 182-189. 

[13] Jin Y, Zhang J, Li M, et al. Towards the automatic anime characters creation with generative adversarial networks[J]. arXiv preprint arXiv:1708.05509, 2017. 

[14] Oeldorf C, Spanakis G. LoGANv2: Conditional style-based logo generation with generative adversarial networks[C]//2019 18th IEEE International Conference On Machine Learning And Applications (ICMLA). IEEE, 2019: 462-468. 

[15] Isola P, Zhu J Y, Zhou T, et al. Image-to-image translation with conditional adversarial networks[C]//Proceedings of the IEEE conference on computer vision and pattern recognition. 2017: 1125-1134. 

[16] Zhu J Y, Park T, Isola P, et al. Unpaired image-to-image translation using cycle-consistent adversarial networks[C]//Proceedings of the IEEE international conference on computer vision. 2017: 2223-2232. 

[17] Chen Y, Lai Y K, Liu Y J. Cartoongan: Generative adversarial networks for photo cartoonization[C]//Proceedings of the IEEE conference on computer vision and pattern recognition. 2018: 9465-9474. 

[18] Choi Y, Choi M, Kim M, et al. Stargan: Unified generative adversarial networks for multi-domain image-to-image translation[C]//Proceedings of the IEEE conference on computer vision and pattern recognition. 2018: 8789-8797. 

[19] Kim J, Kim M, Kang H, et al. U-GAT-IT: unsupervised generative attentional networks with adaptive layer-instance normalization for image-to-image translation[J]. arXiv preprint arXiv:1907.10830, 2019. 

[20] Nizan O, Tal A. Breaking the cycle-colleagues are all you need[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2020: 7860-7869. 

[21] Kodali N, Abernethy J, Hays J, et al. On convergence and stability of gans[J]. arXiv preprint arXiv:1705.07215, 2017. 

[22] Karnewar A, Wang O. Msg-gan: Multi-scale gradients for generative adversarial networks[C]//Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition. 2020: 7799-7808. 

[23] Brock A, Donahue J, Simonyan K. Large scale GAN training for high fidelity natural image synthesis[J]. arXiv preprint arXiv:1809.11096, 2018. 

[24] Zhang H, Goodfellow I, Metaxas D, et al. Self-attention generative adversarial networks[C]//International conference on machine learning. PMLR, 2019: 7354-7363. 

[25] Gan-qp J S. A novel gan framework without gradient vanishing and lipschitz constraint[J]. arXiv preprint arXiv:1811.07296, 2018.