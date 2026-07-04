# 快速入门

## 1. 准备环境

```bash
cp .env.example .env
```

在 `.env` 中填写：

- `OPENAI_API_KEY`
- `MODEL_NAME`

## 2. 运行测试

```bash
./run.sh
```

或使用自定义参数：

```bash
./run.sh --tasks zh_en,en_zh --workers 8 --zh_en_limit 50 --en_zh_limit 50 --random_seed 42
```

## 3. 输入格式

`exam.txt` 使用 XML 风格标签划分翻译方向：

```text
<exam>
<zh_en>
# 注释行会被跳过
高质量发展
</zh_en>
<en_zh>
High-quality development
</en_zh>
</exam>
```

## 4. 输出结果

翻译结果保存在 `outputs/` 目录：

| 文件 | 说明 |
| --- | --- |
| `result_zh_en.csv` | 中译英结果 |
| `result_en_zh.csv` | 英译中结果 |
| `result_combine.csv` | 合并结果 |

## 5. 质量评分

将 CSV 结果与 [评分标准](/guide/scoring) 中的裁判提示词一并提交给大模型，按以下结构归档到 `docs/result/`：

```
result/<exam-version>/<bench-model>/
├── result_combine.csv
└── <评分模型>.md
```

文档站点会自动扫描目录并更新导航，无需手动维护索引。

欢迎通过 PR 提交新的评测结果，丰富样本库。