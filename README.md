### 环境设置

关于如何安装及配置Anaconda Python发行版，详情请参阅：[此文档](https://github.com/NewMoe-Technology/VALLEX-Inference-Http/blob/master/README.md)中的Python相关章节。

### 使用conda创建新的env

由于最近ustc(中科大镜像源)出现了`429 (Too Many Requests)`的异常，因此我们需要更换镜像源。
这里建议使用清华大学的镜像源，具体操作如下：

```shell
# 首先将conda的channels进行重置
conda config --remove-key channels
# 接下来依次导入清华大学的channels
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/
```

接下来我们就可以创建一个新的env了：

```shell
conda env create -f ACTAgent.yml
```

> ※请注意，`ACTAgent.yml`中的`PREFIX`字段指定了新的conda环境(即：ACTAgent)在系统上的存储位置
> 这里默认是以我的WSL2位置进行存储，因此您需要修改为：$CONDA_HOME/env/ACTAgent
> 这里的`$CONDA_HOME`指的是您系统上的conda的安装位置，通常它位于：/home/<$USER_NAME>/anaconda3/ 或者 /home/<$USER_NAME>/miniconda3/

### 激活环境

```shell
conda activate ACTAgent
# 请记得在环境变量中添加OPENAI_API_KEY
export OPENAI_API_KEY=sk-xxxxxx
```

或者在`~/.bashrc`或者`~/.zshrc`中添加：

```shell
export OPENAI_API_KEY=sk-xxxxxx
```

### 进行测试

```shell
python TestingScript.py
```

对于测试的结果您可以，您可以在LLM执行完成后检查其项目根目录下的`TestingResult.json`以核查LLM
生成的准确性。届时，您也可以自行修改`Cases.txt`以定制您的特化测试用例，每个单独的用例问题请以回车分隔。

### Todo List

- [ ]  针对国服玩家的环境创建单独的Agent。
