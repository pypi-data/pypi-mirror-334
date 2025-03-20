# Example script showing how to copy text to the system clipboard
import argparse
import subprocess
import sys


def copy_to_clipboard(text):
    """
    Copy text to system clipboard.
    Works on Linux, macOS, and Windows.

    Args:
        text (str): The text to copy to clipboard

    Returns:
        bool: True if successful, False otherwise
    """
    platform = sys.platform

    try:
        if platform == "linux" or platform.startswith("linux"):
            # For Linux, use xclip or xsel
            try:
                # Try xclip first
                process = subprocess.Popen(
                    ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
                )
                process.communicate(input=text.encode("utf-8"))
                return True
            except FileNotFoundError:
                # Try xsel if xclip is not available
                try:
                    process = subprocess.Popen(
                        ["xsel", "--clipboard", "--input"], stdin=subprocess.PIPE
                    )
                    process.communicate(input=text.encode("utf-8"))
                    return True
                except FileNotFoundError:
                    print(
                        "Error: Neither xclip nor xsel is installed. Please install one of them."
                    )
                    return False

        elif platform == "darwin":  # macOS
            process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            process.communicate(input=text.encode("utf-8"))
            return True

        elif platform == "win32" or platform == "cygwin":  # Windows
            try:
                # Try using pywin32 if available
                import win32clipboard

                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text)
                win32clipboard.CloseClipboard()
                return True
            except ImportError:
                # Fallback to using clip.exe
                process = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
                process.communicate(input=text.encode("utf-8"))
                return True
        else:
            print(f"Unsupported platform: {platform}")
            return False

    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Copy text to system clipboard")
    parser.add_argument("text", nargs="?", help="Text to copy to clipboard")
    parser.add_argument("-f", "--file", help="File to read text from")

    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r") as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    elif args.text:
        text = args.text
    else:
        # Read from stdin if no text or file is provided
        print("Enter text to copy (Ctrl+D to finish):")
        text = sys.stdin.read()

    if copy_to_clipboard(text):
        print("Text copied to clipboard successfully!")
    else:
        print("Failed to copy text to clipboard.")


if __name__ == "__main__":
    main()
