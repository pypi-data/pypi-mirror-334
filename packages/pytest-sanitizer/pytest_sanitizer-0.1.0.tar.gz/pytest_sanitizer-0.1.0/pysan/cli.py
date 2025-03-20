"""
Command-line interface for pysan.
"""
import sys
import subprocess
from pathlib import Path


def main():
    """
    Run pytest with sanitization enabled.
    
    This is a simple wrapper around pytest that ensures the pysan plugin
    is enabled, even if not installed via pip.
    """
    args = sys.argv[1:]
    
    # Ensure our plugin is in the Python path
    pysan_dir = Path(__file__).parent.parent.absolute()
    
    # Run pytest with our plugin enabled
    cmd = [sys.executable, "-m", "pytest", "-p", "pysan.plugin"] + args
    
    try:
        subprocess.run(cmd, check=False)
    except Exception as e:
        print(f"Error running pytest: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 