import os
from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CppExtension, CUDAExtension

# --- 环境配置 ---
from distutils.sysconfig import get_config_vars
(opt,) = get_config_vars("OPT")
if opt:
    os.environ["OPT"] = " ".join(
        flag for flag in opt.split() if flag != "-Wstrict-prototypes"
    )

# --- 扩展配置 ---
src_root = "src"
package_name = "spseg"

# 在这里列出所有的子模块名
# 对应的源码目录应该是: src/scannet
extension_names = ["scannet"] 

extensions = []

for ext_name in extension_names:
    ext_dir = os.path.join(src_root, ext_name)
    
    # 查找源文件
    sources_cpp = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(ext_dir)
        for file in files
        if file.endswith(".cpp")
    ]
    sources_cu = [
        os.path.join(root, file)
        for root, dirs, files in os.walk(ext_dir)
        for file in files
        if file.endswith(".cu")
    ]
    
    sources = sources_cpp + sources_cu
    
    if not sources:
        print(f"Warning: No source files found for extension {ext_name}")
        continue

    # 有 .cu 就用 CUDAExtension, 否则用 CppExtension
    if len(sources_cu) > 0:
        ExtensionClass = CUDAExtension
        print(f"Building {ext_name} with CUDA support...")
    else:
        ExtensionClass = CppExtension
        print(f"Building {ext_name} with CPU support...")

    # 构建完整的包路径: spseg.scannet._C
    full_package_path = f"{package_name}.{ext_name}._C"
    
    extensions.append(
        ExtensionClass(
            name=full_package_path,
            sources=sources,
            # 注意：NVCC (CUDA) 和 GCC 的 flag 不完全通用，建议分开写，或者让 PyTorch 处理
            # 这里 -O3 对两者都通用
            extra_compile_args={"cxx": ["-O3", "-std=c++17"], "nvcc": ["-O3"]}
        )
    )

setup(
    ext_modules=extensions,
    cmdclass={"build_ext": BuildExtension},
)