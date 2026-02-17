# 贡献指南

感谢您对TransBench的贡献。

## 开发环境配置

1. 使用`uv`或者 pip。

2. 根据`.env.example`文件创建`.env`文件，并填写所需的值。

3. 安装必要的依赖项，然后运行以下命令：

```bash
# uv
uv sync
./run.sh
#或者
uv run python -m src.main "$@"
```
```bash
# pip
pip install .
python -m src.main "$@"
```

## 项目结构

- `src/parser.py`：解析`exam.txt`文件。

- `src/translator.py`：LLM翻译逻辑。

- `src/main.py`：命令行接口协调与并发处理。

- `src/writer.py`：将结果输出为CSV格式。

## 提交请求的规则

- 确保提交的请求内容简洁且针对性强。

- 当功能发生变化时，请更新相关文档。

- 在提交请求之前，请确保相关命令能够正常执行：

```bash
python -m compileall src
```

## 合并请求的描述规则

建议使用清晰的前缀来描述请求内容：

- `feat:`：新增的功能。

- `fix:`：修复的错误。

- `docs:`：仅用于更新文档。

- `refactor:`：代码重构。

- `archive`: 提交测试样本。

## 报告问题的方法

请使用问题模板，并包含以下信息：

- 预期的行为。

- 实际发生的行为。

- 重现问题的步骤。

- 可用的示例输入/输出数据。