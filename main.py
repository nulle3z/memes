import os
import shutil
from pathlib import Path

def is_target_file(file_path: Path) -> bool:
    """判断文件是否满足移动条件"""
    # 需要匹配的扩展名列表（全部小写，含双后缀情况）
    target_extensions = {'.jpg', '.png', '.webp', '.avif', '.jpeg', '.jpeg.png', '.gif'}
    
    # 获取文件名（含扩展名）
    name = file_path.name
    name_lower = name.lower()
    
    # 检查是否以任一目标扩展名结尾
    matched_ext = None
    for ext in target_extensions:
        if name_lower.endswith(ext):
            matched_ext = ext
            break
    
    if matched_ext is None:
        return False
    
    # 提取去掉扩展名后的基名
    base_name = name[:-len(matched_ext)]  # 去除匹配到的后缀
    # 基名不能为空
    if not base_name:
        return False
    
    # 条件1：基名为纯数字
    if base_name.isdigit():
        return True
    # 条件2：基名以 v2- 开头
    if base_name.startswith('v2-'):
        return True
    
    return False

def main():
    source_dir = Path.cwd()          # 当前工作目录
    target_dir = source_dir / 'ForLLM'
    
    # 创建目标文件夹（如果不存在）
    target_dir.mkdir(exist_ok=True)
    
    # 遍历当前目录下的所有文件（不递归子目录）
    for item in source_dir.iterdir():
        if item.is_file() and is_target_file(item):
            dest_path = target_dir / item.name
            try:
                # 如果目标已存在，先删除（实现覆盖，与 copy2 行为一致）
                if dest_path.exists():
                    dest_path.unlink()
                shutil.move(str(item), str(dest_path))
                print(f"已移动: {item.name} -> {dest_path}")
            except Exception as e:
                print(f"移动失败 {item.name}: {e}")

if __name__ == '__main__':
    main()

