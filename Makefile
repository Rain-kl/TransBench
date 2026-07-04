.PHONY: help install sync run check docs-install docs-dev docs-build docs-preview clean

help: ## 显示可用命令
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

install: sync docs-install ## 安装 Python 与文档依赖

sync: ## 同步 Python 依赖 (uv)
	uv sync

docs-install: ## 安装文档站点依赖 (pnpm)
	pnpm install

run: ## 运行基准测试
	./run.sh

check: ## 检查 Python 源码语法
	uv run python -m compileall src

docs-dev: ## 启动文档站点开发服务器
	pnpm run docs:dev

docs-build: ## 构建文档静态站点
	pnpm run docs:build

docs-preview: ## 预览已构建的文档站点
	pnpm run docs:preview

clean: ## 清理构建产物与缓存
	rm -rf docs/.vitepress/cache docs/.vitepress/dist
	find src -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true