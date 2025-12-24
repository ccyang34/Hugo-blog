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
        print(f"执行命令出错: {command}")
        print(e.stderr)
        if exit_on_error:
            sys.exit(1)
        return False

def main():
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 默认提交信息
    commit_msg = f"更新: 内容更新 {current_time}"
    
    # 如果提供了命令行参数，使用参数作为提交信息
    if len(sys.argv) > 1:
        commit_msg = sys.argv[1]
    
    print("开始同步到 GitHub...")
    print(f"提交信息: {commit_msg}")
    
    # 执行 Git 命令
    run_command("git add .")
    
    try:
        # 尝试提交，允许失败（例如没有变更）
        subprocess.run(f'git commit -m "{commit_msg}"', shell=True, check=True, text=True)
    except subprocess.CalledProcessError:
        print("Git 提交失败 (可能没有新的变更需要提交)。继续执行...")

    # 尝试推送，如果失败则拉取并重新推送
    if not run_command("git push", exit_on_error=False):
        print("推送失败。正在尝试拉取远程更改 (自动变基)...")
        if run_command("git pull --rebase", exit_on_error=False):
            print("变基成功。正在再次推送...")
            run_command("git push")
        else:
            print("自动拉取/变基失败。请手动检查 git 状态。")
            sys.exit(1)
    
    print("同步完成！")

if __name__ == "__main__":
    main()
