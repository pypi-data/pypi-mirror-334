# GitHub CLI Mamba

一个用Python和Typer构建的GitHub命令行工具。

## 安装

```bash
pip install github-cli-mamba
```

## 使用

首先，设置GitHub Token环境变量：

```bash
export GITHUB_TOKEN="your_github_token"
```

或者创建`.env`文件，添加：

```
GITHUB_TOKEN=your_github_token
```

### 命令

#### 仓库命令

列出用户的所有仓库：

```bash
github-cli-mamba repo list -u username
```

删除用户的仓库：

```bash
github-cli-mamba repo delete -u username -r repo_name
```

#### 用户命令

查看用户资料：

```bash
github-cli-mamba user profile -u username
```
