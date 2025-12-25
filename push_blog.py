#!/usr/bin/env python3
"""
push_blog.py - 上传优先的同步脚本
适用于本地运行分析脚本后，强制推送本地版本

与 sync_blog.py 的区别：
- sync_blog.py: 先拉取远程，再推送（适合日常同步）
- push_blog.py: 本地优先，冲突时覆盖远程（适合本地运行分析脚本后）
"""

import subprocess
import sys
import datetime
import os

def run_command(command, exit_on_error=True, capture=True):
    """运行 shell 命令"""
    env = os.environ.copy()
    env["LANG"] = "zh_CN.UTF-8"
    
    try:
        result = subprocess.run(command, shell=True, check=False, text=True, capture_output=capture, env=env)
        if capture and result.stdout:
            print(result.stdout.strip())
        if capture and result.stderr and result.returncode != 0:
            print(result.stderr.strip())
        return result.returncode == 0
    except Exception as e:
        print(f"执行命令出错: {command} - {e}")
        if exit_on_error:
            sys.exit(1)
        return False

def fix_git_state():
    """修复 Git 异常状态"""
    print("🔍 检查 Git 仓库状态...")
    
    # 取消残留的变基
    if os.path.exists(".git/rebase-merge") or os.path.exists(".git/rebase-apply"):
        print("⚠️ 检测到残留的变基状态，正在强制中止...")
        run_command("git rebase --abort", exit_on_error=False)

    # 检查游离 HEAD
    res = subprocess.run("git symbolic-ref -q HEAD", shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print("⚠️ 检测到游离 HEAD 状态，正在切回 main 分支...")
        run_command("git checkout main", exit_on_error=False)

    # 检查身份配置
    res = subprocess.run("git config user.name", shell=True, capture_output=True, text=True)
    if not res.stdout or not res.stdout.strip():
        print("👤 配置临时 Git 身份...")
        run_command('git config --local user.name "Robot-Sync"')
        run_command('git config --local user.email "robot@sync.local"')

def push_first_sync(commit_msg):
    """上传优先的同步流程：本地版本覆盖远程冲突"""
    
    # 1. 提交本地变更
    run_command("git add .")
    print(f"📝 提交变更: {commit_msg}")
    run_command(f'git commit -m "{commit_msg}"', exit_on_error=False)
    
    # 2. 尝试直接推送
    print("🚀 尝试直接推送...")
    if run_command("git push", exit_on_error=False):
        return True
    
    # 3. 推送失败，说明远程有新提交，执行 pull --rebase 但本地优先
    print("⚔️ 远程有更新，拉取并解决冲突（本地优先）...")
    
    if not run_command("git pull --rebase", exit_on_error=False):
        # 冲突时，保留本地版本（在 rebase 中 --ours 是远程，--theirs 是本地）
        print("📌 冲突检测，保留本地版本...")
        run_command("git checkout --theirs .", exit_on_error=False)
        run_command("git add .")
        
        # 继续 rebase
        if not run_command("git -c core.editor=true rebase --continue", exit_on_error=False):
            # 可能还在冲突，再尝试一次
            run_command("git checkout --theirs .", exit_on_error=False)
            run_command("git add .")
            run_command("git -c core.editor=true rebase --continue", exit_on_error=False)
    
    # 4. 再次推送
    print("🚀 再次推送...")
    if run_command("git push", exit_on_error=False):
        return True
    
    # 5. 如果还是失败，强制推送（最后手段）
    print("⚠️ 常规推送失败，执行强制推送...")
    if run_command("git push --force-with-lease", exit_on_error=False):
        return True
    
    print("❌ 推送失败，请手动处理")
    return False

def main():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"本地更新: {current_time}"
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    
    print(f"--- 上传优先同步 [{current_time}] ---")
    fix_git_state()
    
    if push_first_sync(commit_msg):
        print("✨ 上传完成！")
    else:
        print("💥 上传失败，请检查上方日志。")
        sys.exit(1)

if __name__ == "__main__":
    main()
