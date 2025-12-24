import subprocess
import sys
import datetime

def run_command(command, exit_on_error=True):
    """运行 shell 命令并打印输出"""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(e.stderr)
        if exit_on_error:
            sys.exit(1)
        return False

def main():
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 默认提交信息
    commit_msg = f"update: content update {current_time}"
    
    # 如果提供了命令行参数，使用参数作为提交信息
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    
    print("Start syncing to GitHub...")
    print(f"Commit message: {commit_msg}")
    
    # 执行 Git 命令
    run_command("git add .")
    
    try:
        # 尝试提交，允许失败（例如没有变更）
        subprocess.run(f'git commit -m "{commit_msg}"', shell=True, check=True, text=True)
    except subprocess.CalledProcessError:
        print("Git commit failed (possibly nothing to commit). Continuing...")

    # 尝试推送，如果失败则拉取并重新推送
    if not run_command("git push", exit_on_error=False):
        print("Push failed. Attempting to pull remote changes (rebase)...")
        if run_command("git pull --rebase", exit_on_error=False):
            print("Rebase successful. Pushing again...")
            run_command("git push")
        else:
            print("Automatic pull/rebase failed. Please check git status manually.")
            sys.exit(1)
    
    print("Sync completed!")
    
    print("Sync completed!")

if __name__ == "__main__":
    main()
