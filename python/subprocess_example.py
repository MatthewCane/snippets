from subprocess import PIPE, CalledProcessError, CompletedProcess, run


def execute_command(command: str) -> CompletedProcess:
    """
    Execute a shell command and return the CompletedProcess object.
    """
    try:
        return run(
            command,
            shell=True,  # Use the default system shell (bash, zsh, e.t.c)
            stdout=PIPE,  # Captures stdout and makes it available
            stderr=PIPE,  # Same as above but for stderr
            text=True,  # Auto decodes piped bytes into text
            check=True,  # Raises an error on non-zero return code
        )

    except CalledProcessError as e:
        error_message = f"Command failed with exit code {e.returncode}\n"
        error_message += f"stdout: {e.stdout}\n"
        error_message += f"stderr: {e.stderr}"
        raise RuntimeError(error_message) from e


if __name__ == "__main__":
    result = execute_command("echo foo")
    print(result.stdout)

    result = execute_command("ls | grep README")
    print(result.stdout)
