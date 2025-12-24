import subprocess
import sys
import datetime
import os

def run_command(command, exit_on_error=True, capture=True):
    """运行 shell 命令并根据配置处理错误和输出"""
    env = os.environ.copy()
    env["LANG"] = "zh_CN.UTF-8"
    
    # 某些命令不自动退出，由调用者处理结果
    should_check = True
    if any(x in command for x in ["commit", "push", "pull", "rebase"]):
        should_check = False

    try:
        result = subprocess.run(command, shell=True, check=should_check, text=True, capture_output=capture, env=env)
        if capture and result.stdout:
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        if capture:
            print(f"执行命令出错: {command}")
            if e.stderr: print(e.stderr.strip())
        if exit_on_error:
            sys.exit(1)
        return False

def fix_git_state():
    """修复 Git 异常状态（游离 HEAD、残留变基等）"""
    print("🔍 检查 Git 仓库状态...")
    
    # 1. 检查是否在变基中，如果是则取消（假设开始新一轮同步）
    if os.path.exists(".git/rebase-merge") or os.path.exists(".git/rebase-apply"):
        print("⚠️ 检测到残留的变基状态，正在强制中止...")
        run_command("git rebase --abort", exit_on_error=False)

    # 2. 检查游离 HEAD
    res = subprocess.run("git symbolic-ref -q HEAD", shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print("⚠️ 检测到游离 HEAD 状态，正在切回 main 分支...")
        run_command("git checkout main", exit_on_error=False)

    # 3. 检查身份配置
    res = subprocess.run("git config user.name", shell=True, capture_output=True, text=True)
    if not res.stdout or not res.stdout.strip():
        print("👤 配置临时 Git 身份...")
        run_command('git config --local user.name "Robot-Sync"')
        run_command('git config --local user.email "robot@sync.local"')

def safe_sync(commit_msg):
    """鲁棒的同步流程"""
    run_command("git add .")
    
    # 提交
    print(f"📝 提交变更: {commit_msg}")
    run_command(f'git commit -m "{commit_msg}"', exit_on_error=False)
    
    # 尝试拉取并变基
    print("📡 同步远程库 (Pull & Rebase)...")
    if not run_command("git pull --rebase", exit_on_error=False):
        print("⚔️ 发现同步冲突，尝试自动处理报告类文件冲突...")
        
        # 针对内容文件和图表图片，在 rebase 冲突中：
        # --theirs 指代“我的当前提交（即将要合并进去的变更）”
        # 我们优先保留本地最新生成的内容
        run_command("git checkout --theirs content/posts/*.md static/img/charts/*.png static/images/charts/*.png", exit_on_error=False)
        run_command("git add .")
        
        # 再次尝试继续变基
        if not run_command("git -c core.editor=true rebase --continue", exit_on_error=False):
            print("❌ 自动修复失败，可能存在非报告类冲突。请手动处理。")
            return False

    # 推送
    print("🚀 推送至远程仓库...")
    if not run_command("git push", exit_on_error=False):
        print("❌ 推送失败。")
        return False
        
    return True

def main():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"更新: 内容更新 {current_time}"
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    
    print(f"--- 自动化同步启动 [{current_time}] ---")
    fix_git_state()
    
    if safe_sync(commit_msg):
        print("✨ 同步任务圆满完成！")
    else:
        print("💥 同步失败，请检查上方日志。")
        sys.exit(1)

if __name__ == "__main__":
    main()
