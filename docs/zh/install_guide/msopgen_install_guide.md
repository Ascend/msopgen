# MindStudio Ops Generator安装指南

<br>

## 1. 安装说明

msOpGen工具的安装方式包括：

- 二进制安装：msOpGen工具完整功能已集成在CANN包中发布，可直接安装CANN包，请参考《[CANN 官方安装指南](https://www.hiascend.com/cann/download)》，按文档逐步完成安装与配置。
- 源码安装：如需使用最新代码的功能，或对源码进行修改以增强功能，可下载本仓库代码，自行编译、打包工具并完成安装，具体请参见[源码安装](#2-源码安装)。

## 2. 源码安装

如需使用最新代码的功能，或对源码进行修改以增强功能，可下载本仓库代码，自行编译、打包工具并完成安装。

### 2.1 环境准备

请按照以下文档进行环境配置：《[算子工具开发环境安装指导](https://gitcode.com/Ascend/msot/blob/26.0.0/docs/zh/common/dev_env_setup.md)》。

安装python依赖

```sh
pip install -r requirements.txt
```

### 2.2 安装

#### 2.2.1 执行编译打包

生成的whl包位于output目录，包含mindstudio_opgen和mindstudio_opst两个whl包

```py
python build.py
```

#### 2.2.2 安装whl包

```sh
cd output
pip install mindstudio_opgen-xxxxx.whl
pip install mindstudio_opst-xxxxx.whl
```

### 2.3 卸载

卸载则通过如下命令卸载：

```sh
pip uninstall mindstudio_opgen-xxxxx.whl 
pip uninstall mindstudio_opst-xxxxx.whl
```

### 2.4 升级

如需使用whl包替换运行环境原有已安装的whl包，执行如下安装操作：

```sh
pip install mindstudio_opgen-xxxxx.whl --force-reinstall
pip install mindstudio_opst-xxxxx.whl --force-reinstall
```

安装过程中，若提示是否替换原有安装包：
输入"y"，则安装包会自动完成升级操作。

### 2.5 运行ut、st测试用例

`3.7 <= python版本要求 <=3.10`，\$\{INSTALL_DIR\}请替换为CANN软件安装后文件存储路径。例如，若安装的Ascend\-cann\-toolkit软件包，安装后文件存储路径示例为：$HOME/Ascend/cann

```shell
source ${INSTALL_DIR}/set_env.sh
```

测试报告在output目录

```sh
python build.py test
```
