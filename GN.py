

### get name

import json
import os.path
import re
import ipykernel
import requests
import pandas as pd
#try:  # Python 3
#    from urllib.parse import urljoin
#except ImportError:  # Python 2
#    from urlparse import urljoin

# Alternative that works for both Python 2 and 3:
from requests.compat import urljoin

try:  # Python 3 (see Edit2 below for why this may not work in Python 2)
    from notebook.notebookapp import list_running_servers
except ImportError:  # Python 2
    import warnings
    from IPython.utils.shimmodule import ShimWarning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=ShimWarning)
        from IPython.html.notebookapp import list_running_servers
        
def get_notebook_name():
    """
    Return the full path of the jupyter notebook.
    """
    kernel_id = re.search('kernel-(.*).json',
                          ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                params={'token': ss.get('token', '')})
        for nn in json.loads(response.text):
            if nn['kernel']['id'] == kernel_id:
                relative_path = nn['notebook']['path']
                return os.path.join(ss['notebook_dir'], relative_path)



### 全局变量

Graph_Note_Path='./GN_assfiles/GN_tags.csv'
Graph_Note_Mainpage="./GN.html"
Graph_Note_Assdir='./GN_assfiles'
__name=get_notebook_name().split('/')[-1]

### write html

def write_html():
    def GN_create_nodes_list():
        #生成df中的node
        df=pd.read_csv(Graph_Note_Path,encoding="utf-8")
        nodes=[]
        nodenum={}
        #df
        num=0
        for num,name in enumerate(set(df["note"])):
            nodes.append(name)
            nodenum[name]=num


        #生成无tag的node
        endnum=num

        files=os.listdir()
        s=re.compile(".{1,}\.ipynb")
        exp_files=set(files).difference(set(nodes))
    #     print(files,len(files))
    #     print(exp_files,len(exp_files))
    #     print(nodes,len(nodes))
        for file in exp_files:
            if s.match(file):
                endnum+=1
                nodes.append(file)
                nodenum[file]=endnum
        return nodes,nodenum
    
    def GN_creat_edges_json(nodes,nodenum):
        global Graph_Note_Path
        df=pd.read_csv(Graph_Note_Path,encoding="utf-8")
        tags=set(df["tag"])

        edged={}
        for tag in tags:
            edged[tag]=list(set(df.loc[df["tag"]==tag]["note"]))

        def create_ass(as_notes):
            result=[]
            L=len(as_notes)
            for i in range(L):
                for j in range(i+1,L):
                    result.append({"source":nodenum[as_notes[i]],"target":nodenum[as_notes[j]]})
            return result

        edges=[]
        #生成links
        for tag in tags:
            ass_notes=edged[tag]
            if ass_notes!=[]:
                edges.extend(create_ass(ass_notes))
        return edges
    
    def Graph_Note_create_json(nodes,edges):
        Graph_Note_Data={"nodes":[],"edges":[]}
        for note in nodes:
            Graph_Note_Data["nodes"].append({"name":note[:-6],"url":"http://localhost:8888/notebooks/"+note})
        Graph_Note_Data["edges"]=edges
        return Graph_Note_Data
    
    def Graph_Note_write_html(GNjson):
        with open(Graph_Note_Mainpage,"r") as f:
            text=f.read()
        json_raw = str(GNjson).replace('\'nodes\'','nodes')
        json_raw = json_raw.replace("'name'","name").replace("\'url\''","url")
        json_raw = json_raw.replace("\'edges\'","edges")
        json_raw = json_raw.replace("\'source\'","source").replace("\'target\'","target")
        json_raw = json_raw.replace("\'","\"")
        json_fami=json_raw

        sb=re.compile("dataset=(.*)")
        ttry=re.sub("(?s)dataset=.*?;","dataset="+json_fami+";\n",text)

        with open("GN.html","w") as f:
            f.write(ttry)
            
    Graph_Note_Nodes,Graph_Note_Nodenum=GN_create_nodes_list()
    
    Graph_Note_Edges=GN_creat_edges_json(Graph_Note_Nodes,Graph_Note_Nodenum)
    
    Graph_Note_Data=Graph_Note_create_json(Graph_Note_Nodes,Graph_Note_Edges)
    
    Graph_Note_write_html(Graph_Note_Data)

### ass函数

def ass(*tags):
    global Graph_Note_Path
    global __name

    this_tags = tags
    df = pd.read_csv(Graph_Note_Path,encoding="utf-8")
    df = df.drop(df.loc[df["note"] == __name].index)
    df = df.append(pd.DataFrame([[__name,i] for i in this_tags],columns=["note","tag"])).reset_index(drop=True)
    df.to_csv(Graph_Note_Path,index_label=False)
    write_html()

### 其他函数

def ass_list():
    print(pd.read_csv(Graph_Note_Path))
    
def ass_clear():
    emp_df=pd.DataFrame(columns=["note","tag"])
    emp_df.to_csv(Graph_Note_Path,index_label=False)

print("welcome to Graph Note version-1.0")

print("view \"https://github.com/SolarOven/Graph-Note\" to get help")

def init_html():
    html=r'''

    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>--GN--</title>
        <script type="text/javascript" src="http://d3js.org/d3.v3.js"></script>
        <style type="text/css">
        </style>
    </head>
    <body>
    <script type="text/javascript">
    var h=600;
    var w=1300;
    // 颜色函数
    var colors=d3.scale.category20()//创建序数比例尺和包括20中颜色的输出范围

    //(1)定义节点和联系对象数组
    var dataset={};








    //(2)转化数据为适合生成力导向图的对象数组
    var force=d3.layout.force()
        .nodes(dataset.nodes)//加载节点数据
        .links(dataset.edges)//加载边数据
        .size([w,h])//设置有效空间的大小
        .linkDistance(100)//连线的长度
        .charge(-400)//负电荷量，相互排斥设置的负值越大越排斥
        .start();//设置生效

    var svg=d3.select("body")
        .append("svg")
        .attr("width",w)
        .attr("height",h);

    //(3)创建作为连线的svg直线
    var edges=svg.selectAll("line")
        .data(dataset.edges)
        .enter()
        .append("line")
        .style("stroke",d=>"grey");

    //(4) 创建作为连线的svg圆形
    var node=svg.selectAll("node")
        .data(dataset.nodes)
        .enter()
        .append("g")
        .attr("class","node")
        .append("circle")
        .attr("r",10).style("fill","pink")
        .on("dblclick",function(d){window.open(d.url);})
        .call(force.drag);


    //me 另设一个text
    var texts = svg
            .selectAll(".forceText")
            .data(dataset.nodes) // 文本的数目与节点的数目相同
            .enter()
            .append("text")
            .attr("class", "forceText")
            .text(d=>d.name)
            .on("dblclick",function(d){window.open(d.url);})
            .call(force.drag);


    //(5)打点更新，没有的话就显示不出来了
    force.on("tick",function(){
        //边
        edges.attr("x1",function(d){
            return  d.source.x;
        })
        .attr("y1",function(d){
            return  d.source.y;
        })
        .attr("x2",function(d){
            return  d.target.x;
        })
        .attr("y2",function(d){
            return  d.target.y;
        });
        //节点
        node.attr("cx",function(d){
            return d.x;
        })
        .attr("cy",function(d){
            return d.y;
        });
        //字
        texts.attr("x",function(d){
            return d.x;
        })
        .attr("y",function(d){
            return d.y;
        });
    })
    </script>

    </body>
    </html>
    '''
    f=open(Graph_Note_Mainpage,"w")
    f.write(html)
    f.close()

def check():
    #检测'./GN_assfile'
    try:
        os.listdir(Graph_Note_Assdir)
    except:
        print("检测到"+Graph_Note_Assdir+"不存在,已自动创建")
        os.mkdir(Graph_Note_Assdir)
        print("创建完成")

    try:
        df = pd.read_csv(Graph_Note_Path,encoding="utf-8")
    except:
        
        print("检测到"+Graph_Note_Path+"不存在,正在自动创建")
        emp_df=pd.DataFrame(columns=["note","tag"])
        emp_df.to_csv(Graph_Note_Path,index_label=False)
        print("创建完成")
        
    try:
        f = open(Graph_Note_Mainpage)
        text=f.read()
        f.close()
    except:
        print("检测到"+Graph_Note_Mainpage+"不存在，正在创建")
        init_html()
        write_html()
        print("创建完成")

check()
