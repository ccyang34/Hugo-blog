#!/bin/bash

# 获取当前时间
current_time=$(date "+%Y-%m-%d %H:%M:%S")

# 默认提交信息
msg="update: content update $current_time"

# 如果提供了参数，则使用参数作为提交信息
if [ -n "$1" ]; then
    msg="$1"
fi

echo "Start syncing to GitHub..."
echo "Commit message: $msg"

# 执行 Git 命令
git add .
git commit -m "$msg"
git push

echo "Sync completed!"
