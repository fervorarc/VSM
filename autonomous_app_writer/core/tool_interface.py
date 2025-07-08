"""
Interface for S1 agents to interact with external tools.
(e.g., compilers, linters, APIs, shell commands).
"""

import subprocess
from autonomous_app_writer.core.logging_setup import get_logger

logger = get_logger(__name__)

class ToolInterface:
    """
    Provides methods for agents to execute external tools.
    """
    def __init__(self):
        logger.info("Tool Interface initialized.")

    def execute_shell_command(self, command, timeout=60):
        """
        Executes a shell command and returns its output.

        Args:
            command (str): The command to execute.
            timeout (int): The timeout in seconds.

        Returns:
            dict: A dictionary containing 'stdout', 'stderr', and 'return_code'.
        """
        logger.info(f"Executing shell command: {command}")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False  # Do not raise exception on non-zero exit codes
            )
            
            if result.returncode != 0:
                logger.warning(f"Command '{command}' exited with code {result.returncode}")
                logger.warning(f"Stderr: {result.stderr}")

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            logger.error(f"Command '{command}' timed out after {timeout} seconds.")
            return {
                "stdout": "",
                "stderr": f"TimeoutExpired: Command timed out after {timeout} seconds.",
                "return_code": -1
            }
        except Exception as e:
            logger.error(f"An error occurred while executing command '{command}': {e}")
            return {
                "stdout": "",
                "stderr": str(e),
                "return_code": -1
            }

    def run_linter(self, file_path, linter_command="pylint"):
        """
        Runs a linter on a specific file.

        Args:
            file_path (str): The path to the file to lint.
            linter_command (str): The linter command to use.

        Returns:
            dict: The output from execute_shell_command.
        """
        command = f"{linter_command} {file_path}"
        return self.execute_shell_command(command)

    def run_compiler(self, source_file, output_file, compiler_command="gcc"):
        """
        Runs a compiler on a source file.

        Args:
            source_file (str): The path to the source code file.
            output_file (str): The path for the output binary.
            compiler_command (str): The compiler command to use.

        Returns:
            dict: The output from execute_shell_command.
        """
        command = f"{compiler_command} {source_file} -o {output_file}"
        return self.execute_shell_command(command)

# Singleton instance
tool_interface = ToolInterface()

def get_tool_interface():
    """
    Returns the singleton ToolInterface instance.
    """
    return tool_interface
