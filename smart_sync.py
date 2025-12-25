#!/usr/bin/env python3
"""
smart_sync.py - 智能同步脚本
根据文件的 lastmod 时间戳决定保留哪个版本

逻辑：
- 如果本地文件的 lastmod 更新 → 保留本地版本
- 如果远程文件的 lastmod 更新 → 保留远程版本

适用于 Hugo 博客的 Markdown 文件（含 Front Matter）
"""

import subprocess
import sys
import datetime
import os
import re
import tempfile

def run_command(command, capture=True):
    """运行 shell 命令"""
    env = os.environ.copy()
    env["LANG"] = "zh_CN.UTF-8"
    
    try:
        result = subprocess.run(command, shell=True, check=False, text=True, capture_output=capture, env=env)
        if capture and result.stdout:
            print(result.stdout.strip())
        return result.returncode == 0, result.stdout if result.stdout else ""
    except Exception as e:
        print(f"执行命令出错: {command} - {e}")
        return False, ""

def get_lastmod_from_content(content):
    """从 Markdown 文件内容中提取 lastmod 时间"""
    # 匹配 Front Matter 中的 lastmod 或 date 字段
    patterns = [
        r'lastmod:\s*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',
        r'lastmod:\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})',
        r'lastmod:\s*(\d{4}-\d{2}-\d{2})',
        r'date:\s*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',
        r'date:\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})',
        r'date:\s*(\d{4}-\d{2}-\d{2})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            date_str = match.group(1)
            try:
                # 尝试多种日期格式
                for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
                    try:
                        return datetime.datetime.strptime(date_str, fmt)
                    except ValueError:
                        continue
            except:
                pass
    
    return None

def get_remote_file_content(filepath):
    """获取远程版本的文件内容"""
    success, content = run_command(f'git show origin/main:"{filepath}" 2>/dev/null', capture=True)
    if success and content:
        return content
    return None

def get_local_file_content(filepath):
    """获取本地文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return None

def compare_versions(filepath):
    """
    比较本地和远程版本的 lastmod 时间
    返回: 'local' | 'remote' | 'same' | 'unknown'
    """
    local_content = get_local_file_content(filepath)
    remote_content = get_remote_file_content(filepath)
    
    if not local_content:
        return 'remote' if remote_content else 'unknown'
    if not remote_content:
        return 'local'
    
    local_time = get_lastmod_from_content(local_content)
    remote_time = get_lastmod_from_content(remote_content)
    
    if local_time and remote_time:
        if local_time > remote_time:
            return 'local'
        elif remote_time > local_time:
            return 'remote'
        else:
            return 'same'
    
    # 无法比较时间，默认保留本地
    return 'local'

def fix_git_state():
    """修复 Git 异常状态"""
    print("🔍 检查 Git 仓库状态...")
    
    if os.path.exists(".git/rebase-merge") or os.path.exists(".git/rebase-apply"):
        print("⚠️ 检测到残留的变基状态，正在强制中止...")
        run_command("git rebase --abort")

    res = subprocess.run("git symbolic-ref -q HEAD", shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print("⚠️ 检测到游离 HEAD 状态，正在切回 main 分支...")
        run_command("git checkout main")

    res = subprocess.run("git config user.name", shell=True, capture_output=True, text=True)
    if not res.stdout or not res.stdout.strip():
        print("👤 配置临时 Git 身份...")
        run_command('git config --local user.name "Robot-Sync"')
        run_command('git config --local user.email "robot@sync.local"')

def smart_sync(commit_msg):
    """智能同步：根据 lastmod 时间决定保留哪个版本"""
    
    # 1. 先获取远程最新状态（不合并）
    print("📡 获取远程仓库状态...")
    run_command("git fetch origin main")
    
    # 2. 检查是否有差异
    success, diff_output = run_command("git diff HEAD origin/main --name-only", capture=True)
    
    # 3. 提交本地变更
    run_command("git add .")
    print(f"📝 提交变更: {commit_msg}")
    run_command(f'git commit -m "{commit_msg}"')
    
    # 4. 尝试直接推送
    print("🚀 尝试直接推送...")
    success, _ = run_command("git push")
    if success:
        print("✅ 直接推送成功！")
        return True
    
    # 5. 推送失败，需要处理冲突
    print("⚔️ 远程有更新，开始智能合并...")
    
    # 获取冲突文件列表
    run_command("git fetch origin main")
    
    # 尝试 rebase
    success, _ = run_command("git pull --rebase")
    if success:
        print("🚀 再次推送...")
        run_command("git push")
        return True
    
    # 有冲突，逐个文件处理
    print("🧠 检测到冲突，开始智能分析...")
    
    # 获取冲突文件
    success, status_output = run_command("git status --porcelain", capture=True)
    conflicted_files = []
    for line in status_output.split('\n'):
        if line.startswith('UU ') or line.startswith('AA '):
            conflicted_files.append(line[3:].strip())
    
    for filepath in conflicted_files:
        print(f"\n📄 处理冲突文件: {filepath}")
        
        # 对于 content/posts 下的 .md 文件，智能比较 lastmod
        if filepath.startswith("content/posts/") and filepath.endswith(".md"):
            # 获取本地原始版本（冲突前）
            local_content = None
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    local_content = f.read()
                # 提取冲突标记中的本地部分
                local_match = re.search(r'<<<<<<< HEAD\n(.*?)\n=======', local_content, re.DOTALL)
                remote_match = re.search(r'=======\n(.*?)\n>>>>>>>', local_content, re.DOTALL)
                
                if local_match and remote_match:
                    local_part = local_match.group(1)
                    remote_part = remote_match.group(1)
                    
                    local_time = get_lastmod_from_content(local_part)
                    remote_time = get_lastmod_from_content(remote_part)
                    
                    if local_time and remote_time:
                        if local_time >= remote_time:
                            print(f"   ⏱️ 本地版本更新 ({local_time} vs {remote_time})，保留本地")
                            run_command(f'git checkout --theirs "{filepath}"')
                        else:
                            print(f"   ⏱️ 远程版本更新 ({remote_time} vs {local_time})，保留远程")
                            run_command(f'git checkout --ours "{filepath}"')
                    else:
                        print(f"   ⚠️ 无法解析时间戳，默认保留本地")
                        run_command(f'git checkout --theirs "{filepath}"')
                else:
                    print(f"   ⚠️ 无法解析冲突标记，默认保留本地")
                    run_command(f'git checkout --theirs "{filepath}"')
            except Exception as e:
                print(f"   ❌ 处理失败: {e}，默认保留本地")
                run_command(f'git checkout --theirs "{filepath}"')
        else:
            # 非 Markdown 文件，默认保留本地
            print(f"   📌 非 Markdown 文件，保留本地版本")
            run_command(f'git checkout --theirs "{filepath}"')
        
        run_command(f'git add "{filepath}"')
    
    # 继续 rebase
    print("\n🔄 继续 rebase...")
    run_command("git -c core.editor=true rebase --continue")
    
    # 最终推送
    print("🚀 最终推送...")
    success, _ = run_command("git push")
    if success:
        return True
    
    # 如果还是失败，强制推送
    print("⚠️ 常规推送失败，执行强制推送...")
    success, _ = run_command("git push --force-with-lease")
    return success

def main():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"智能同步: {current_time}"
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    
    print(f"--- 智能同步 (lastmod 优先) [{current_time}] ---")
    fix_git_state()
    
    if smart_sync(commit_msg):
        print("✨ 智能同步完成！")
    else:
        print("💥 同步失败，请检查上方日志。")
        sys.exit(1)

if __name__ == "__main__":
    main()
