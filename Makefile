# --- Makefile for spseg ---

# 定义变量，方便日后修改
PYTHON := python
PIP := pip
PACKAGE_NAME := torch-spseg

# .PHONY 告诉 Make 这些不是文件名，而是操作指令
.PHONY: all clean install rebuild uninstall test help

# 默认目标：只输入 make 时执行 help
all: help

# 1. 帮助命令：显示所有可用指令
help:
	@echo "----------------------------------------------------------------"
	@echo "项目管理指令 (Makefile):"
	@echo "  make install   : 安装包 (Editable模式, 无构建隔离)"
	@echo "  make clean     : 清理所有编译产物、缓存和构建临时文件"
	@echo "  make rebuild   : 先清理，再重新编译安装 (开发调试最常用)"
	@echo "  make uninstall : 卸载当前包"
	@echo "  make test      : 运行简单的测试脚本"
	@echo "----------------------------------------------------------------"

# 2. 安装命令
# 核心逻辑：使用 -e 和 --no-build-isolation 加速 PyTorch 扩展编译
install:
	@echo "正在安装 $(PACKAGE_NAME)..."
	$(PIP) install -e . -v --no-build-isolation

# 3. 清理命令 (你的痛点救星)
# 删得非常干净：包括 build 文件夹、egg-info、所有 .so 扩展、所有 pycache
clean:
	@echo "正在清理构建产物..."
	rm -rf build/ dist/ *.egg-info .pytest_cache
	find . -name "*.so" -type f -delete
	find . -name "*.pyd" -type f -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "清理完成！"

# 4. 重建命令 (组合拳)
# 当你修改了 C++ 代码 (.cpp/.cu) 后，必须运行这个
rebuild: clean install

# 5. 卸载命令
uninstall:
	@echo "正在卸载..."
	$(PIP) uninstall $(PACKAGE_NAME) -y
	make clean