#!/bin/bash

# 检查是否提供了文件路径作为参数
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 path_to_your_file.py"
    exit 1
fi

input_file_path="$1"
output_file_path="${input_file_path%.py}_cleaned.py"  # 生成新文件名

# 使用 awk 删除空行和注释行，并将结果写入新文件
awk '!/^ *#/ && NF' "$input_file_path" > "$output_file_path"

echo "Empty lines and comment lines removed and result saved to $output_file_path"