# RE-Maya-Animation-Export-Tool
[English](./README.en.md) | [中文](./README.md)

参考[fmt_RE_MESH-Noesis-Plugin](https://github.com/alphazolam/fmt_RE_MESH-Noesis-Plugin)插件中的maxscript，手搓了一个maya的版本，支持以下特性：

* 在maya里面打开`.mesh` / `.motlist`文件并导入
* 批量动画切分
* 修复使用Noesis导出动画会将帧率默认设置为30fps，导致动画看起来像是以0.5倍速播放的问题

## REEM插件设置
* 打开Maya，窗口->常规编辑器->脚本编辑器。
* 在**脚本编辑器窗口，文件->打开脚本**。打开下载好的**RE Engine Mesh/Animtion Noesis Tool**脚本
* 在**脚本编辑器窗口，文件->将脚本保存至工具架**。

打开REEM插件，通过**Browse**查找，或者直接填入Noesis所在路径

## 从.motlist.中导出动画
点击REEM插件的**Import Mesh/Animtaion**按钮，找到要解包的`.motlist.XXXXXXXXXX`动画文件

点击打开后，出现动画选择面板。双击第一个`[ALL]`开头的，这个文件会出现在下面的**Motions to load**中。在**Motions to load**中双击它也可以取消导出。

之前安装的插件`fmt_RE_MESH-Noesis-Plugin`会给每个 `.motlist.` 内包含的所有动画打包生成一个 `[ALL]` 开头的动画序列。

点击**Load**将它导出，等待导出完成，所有动画就都会被打包进maya场景。

<img width="600" height="800" alt="image" src="https://github.com/user-attachments/assets/19f60429-88bc-4002-997d-7ef66e92ae8d" />


## Maya拆分动画
动画导入成功后，会根据`fmt_RE_MESH-Noesis-Plugin`输出的log自动填充**Animation List**列表。

切换其中的条目，时间轴也会切换到对应的范围。

在**ExportOptions**中：

* **Export Seleted Animations**选项：可以将目前列表中选中的动画片段导出；
* **Export All Animations**选项：可以将列表中所有的动画都切片导出。

选中场景中的动画骨骼，点击**Export**，选好路径后即可执行导出。

<img width="464" height="871" alt="image" src="https://github.com/user-attachments/assets/679f471a-e128-4e3a-b698-c586ed59b9c4" />


## 特别注意
有时候`fmt_RE_MESH-Noesis-Plugin`无法解析motlist中的一些动画，然后只会输出这个动画的第一帧，但log中依然会输出其完整的帧数。这会导致**AnimationList**中的动画片段无法与场景中的动画片段正确匹配。

目前已对下面几种情况进行了修复：

* log中直接报错Warning，报告该动画无法导出，该动画会被直接从**AnimationList**中剔除掉
* log中直接报告帧数为0帧的动画，会被标记为1帧
* 名称中包含**blend_pose**类型的动画，会被标记为1帧

尽管进行了修复，但依然会有部分动画出现只导出1帧但却不报错的情况。

打开脚本编辑器，在log面板找到类似于下面的文本，这里记录了所有导出动画的log
复制出来，修改有问题条目的`frames`为1
点击**Manually Paste Noesis List**按钮，将修改后的文本填入对话框，即可完成**AnimationList**条目的修复。
此时重新选中**AnimationList**中有问题的条目可以看到它会被标记为只有1帧。

⚠️这些有问题的动画进入UE5.6会报错。

<img width="865" height="565" alt="image" src="https://github.com/user-attachments/assets/3762740e-14ac-4374-9953-fa18dccfd5c7" />

