# libimobiledevice-wrapper Makefile

.PHONY: help install install-dev test lint format clean build publish

help: ## 显示帮助信息
	@echo "可用的命令:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## 安装包
	python -m pip install -e .

install-dev: ## 安装开发依赖
	python -m pip install -e ".[dev]"

test: ## 运行测试
	python -m pytest libimobiledevice_wrapper/tests.py -v

test-basic: ## 运行基本测试
	python libimobiledevice_wrapper/tests.py

lint: ## 代码检查
	python -m flake8 libimobiledevice_wrapper/
	python -m mypy libimobiledevice_wrapper/

format: ## 代码格式化
	python -m black libimobiledevice_wrapper/

clean: ## 清理临时文件
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.log
	rm -rf *.png
	rm -rf device_log_*.log
	rm -rf screenshot_*.png
	rm -rf backup_*.txt

build: ## 构建包
	python -m build

publish: ## 发布到 PyPI
	python -m twine upload dist/*

check-deps: ## 检查依赖
	python install.py

example: ## 运行示例
	python example.py

cli-test: ## 测试 CLI 工具
	python3 -m libimobiledevice_wrapper.cli --help
	python3 -m libimobiledevice_wrapper.cli list-devices

all: clean install-dev test lint ## 运行所有检查和测试

setup: ## 初始设置
	python install.py
	make install-dev
	make test-basic
