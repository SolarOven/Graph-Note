# Graph-Note v1.0

# usage
## English
put GN.py in your jupyter-notebook workpath,and import them in notebook.

it will make a html file ,GN_assfile,GN_assfile/GN_tags.csv,in that page,you can double click node to open a page in new browser tag.

use function ass(tag1,tag2,...) can associate this notebook with tags


if some notebooks(>=2) associated with same-name tag,it will linked eatch other in GN.html(after refresh the page)

more question please put it in issues,i will help you as soon as possibl

## Chinese
将GN.py放在jupyter-notebook的工作目录，在jupyter中import GN

GN导入时会自动创建GN.html，GN_assfile文件夹，在GN.html中双击节点能在新标签打开notebook

在notebook用ass(tag1,tag2,...)可以将notebook和众多tag关联起来。

若是两个及以上notebook关联了同名的tag，那么在GN.html中会互相连接起来（需要刷新）

有问题就issue，有问必答

# will update 更新方向

嘛、我笔记还没全都迁移到jupyternotebook，不过可以想象当笔记多了的时候肯定是一团乱吧？但是现在既然没有这个问题就不改变node的连接方法了。

下一步：
1 准备引入能不刷新就能改变网页中json数据的方法。

2 准备添加能过滤tag的输入框

3 准备添加单击能高亮邻接节点的功能
