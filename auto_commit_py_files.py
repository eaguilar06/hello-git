import subprocess
import datetime

def run_command(cmd: list[str]) -> str:
    """Run a shell command and return its output as text."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running {' '.join(cmd)}:\n{result.stderr}")
        return ""
    return result.stdout.strip()

def get_changed_py_files() -> list[str]:
    """Return a list of changed or untracked Python files."""
    diff_output = run_command(["git", "status", "--porcelain"])
    changed_files = []

    for line in diff_output.splitlines():
        status, path = line[:2].strip(), line[3:].strip()
        if path.endswith(".py") and status in {"M", "A", "??"}:
            changed_files.append(path)
    return changed_files

def commit_and_push(changed_files: list[str]) -> None:
    """Commit and push changed Python files."""
    if not changed_files:
        print("✅ No Python files have changed.")
        return

    # Stage the changed files
    subprocess.run(["git", "add"] + changed_files)

    # Create a commit message with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Auto-commit Python file updates ({timestamp})"
    subprocess.run(["git", "commit", "-m", commit_msg])

    # Push the changes
    subprocess.run(["git", "push", "origin", "main"])
    print(f"✅ Committed and pushed {len(changed_files)} file(s): {changed_files}")

def main():
    print("🔍 Checking for changed Python files...")
    changed_files = get_changed_py_files()
    commit_and_push(changed_files)

if __name__ == "__main__":
    main()
