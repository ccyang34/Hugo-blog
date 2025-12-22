import subprocess
import sys
import datetime

def run_command(command):
    """运行 shell 命令并打印输出"""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(e.stderr)
        sys.exit(1)

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
    
    # 注意：如果没有任何更改需要提交，git commit 可能会返回非零退出码，
    # 这里我们简单处理，允许它失败（例如没有暂存的更改）而不中断，或者并在脚本中更精细处理。
    # 为了脚本的健壮性，我们可以先检查状态，或者允许 commit 失败但继续 push（虽然没 commit push 也没用）。
    # 这里采用标准流程，如果 commit 失败（比如无变更），通常不应继续 push。
    # 但为了简单起见，我们使用 subprocess.run 的 check=False 来允许 'nothing to commit' 的情况
    
    try:
        subprocess.run(f'git commit -m "{commit_msg}"', shell=True, check=True, text=True)
    except subprocess.CalledProcessError:
        print("Git commit failed (possibly nothing to commit). Continuing...")

    run_command("git push")
    
    print("Sync completed!")

if __name__ == "__main__":
    main()
