#!/usr/bin/env python3
"""
Script to install zsh completions for dotcat.
This script is run during package installation.
"""

import os
import shutil
import subprocess
import sys


def is_zsh_available():
    """Check if zsh is available on the system."""
    try:
        subprocess.run(
            ["zsh", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        return True
    except FileNotFoundError:
        return False


def get_zsh_completion_dirs():
    """Get potential zsh completion directories."""
    # Common system-wide completion directories
    system_dirs = [
        "/usr/share/zsh/site-functions",
        "/usr/local/share/zsh/site-functions",
    ]

    # User-specific completion directories
    home = os.path.expanduser("~")
    user_dirs = [
        os.path.join(home, ".zsh", "completions"),
        os.path.join(home, ".oh-my-zsh", "completions"),
        os.path.join(home, ".zsh", "site-functions"),
    ]

    # Check which directories exist and are writable
    valid_dirs = []

    # First check user directories (preferred)
    for d in user_dirs:
        if not os.path.exists(d):
            try:
                os.makedirs(d, exist_ok=True)
                valid_dirs.append(d)
            except (OSError, PermissionError):
                continue
        elif os.access(d, os.W_OK):
            valid_dirs.append(d)

    # Then check system directories if running with sufficient privileges
    if not valid_dirs:
        for d in system_dirs:
            if os.path.exists(d) and os.access(d, os.W_OK):
                valid_dirs.append(d)

    return valid_dirs


def install_completions():
    """Install zsh completions."""
    if not is_zsh_available():
        print("ZSH not found. Skipping completion installation.")
        return

    # Get the directory where this script is located (zsh/)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to the completion files (already in the zsh directory)
    completion_script = os.path.join(script_dir, "_dotcat")
    helper_script = os.path.join(script_dir, "dotcat-completion.py")

    if not os.path.exists(completion_script):
        print(
            f"Completion script not found at {completion_script}. Skipping installation."
        )
        return

    # Find a suitable completion directory
    completion_dirs = get_zsh_completion_dirs()
    if not completion_dirs:
        print(
            "No suitable zsh completion directory found. Please install completions manually."
        )
        print(f"Completion files are located at: {script_dir}")
        return

    # Install the completion script
    target_dir = completion_dirs[0]
    target_completion = os.path.join(target_dir, "_dotcat")

    try:
        shutil.copy2(completion_script, target_completion)
        os.chmod(target_completion, 0o755)  # Make executable
        print(f"Installed zsh completion to {target_completion}")

        # Install the helper script if possible
        if os.path.exists(helper_script):
            # Try to find a directory in PATH
            path_dirs = os.environ.get("PATH", "").split(os.pathsep)
            user_bin = os.path.expanduser("~/bin")

            # Create ~/bin if it doesn't exist
            if not os.path.exists(user_bin):
                try:
                    os.makedirs(user_bin, exist_ok=True)
                    path_dirs.insert(0, user_bin)
                except OSError:
                    pass

            # Find a writable directory in PATH
            target_helper = None
            for d in path_dirs:
                if os.path.exists(d) and os.access(d, os.W_OK):
                    target_helper = os.path.join(d, "dotcat-completion.py")
                    break

            if target_helper:
                shutil.copy2(helper_script, target_helper)
                os.chmod(target_helper, 0o755)  # Make executable
                print(f"Installed completion helper to {target_helper}")
            else:
                print(
                    "Could not find a writable directory in PATH for the helper script."
                )
                print(f"Please install the helper script manually from {helper_script}")
    except (OSError, PermissionError) as e:
        print(f"Error installing completions: {e}")
        print(f"Please install completions manually from {script_dir}")


def main():
    """Main entry point."""
    try:
        install_completions()
    except Exception as e:
        print(f"Error during completion installation: {e}")
        # Don't fail the installation if completion setup fails
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
