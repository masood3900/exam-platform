import subprocess
import tempfile
import os
import ast


class CodeExecutor:
    """اجرای کد پایتون و جاوااسکریپت"""

    @staticmethod
    def execute(code, language="python", test_input=""):
        if language == "python":
            return CodeExecutor.execute_python(code, test_input)
        elif language == "javascript":
            return CodeExecutor.execute_javascript(code, test_input)
        else:
            return {
                "success": False,
                "stdout": "",
                "stderr": "زبان پشتیبانی نمی‌شود",
                "returncode": -1,
            }

    @staticmethod
    def execute_python(code, test_input=""):
        try:
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False,
            ) as f:
                f.write(code)
                temp_file = f.name

            result = subprocess.run(
                ['python', temp_file],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5,
            )

            os.unlink(temp_file)

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "زمان اجرا تمام شد (۵ ثانیه)",
                "returncode": -1,
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
            }

    @staticmethod
    def execute_javascript(code, test_input=""):
        try:
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.js',
                delete=False,
            ) as f:
                f.write(code)
                temp_file = f.name

            result = subprocess.run(
                ['node', temp_file],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=5,
            )

            os.unlink(temp_file)

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "زمان اجرا تمام شد (۵ ثانیه)",
                "returncode": -1,
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
            }

    @staticmethod
    def check_python_syntax(code):
        try:
            ast.parse(code)
            return None
        except SyntaxError as e:
            return f"خط {e.lineno}: {e.msg}"
        except Exception as e:
            return str(e)

    @staticmethod
    def check_answer(code, language, test_input, expected_output):
        if language == "python":
            syntax_error = CodeExecutor.check_python_syntax(code)
            if syntax_error:
                return {
                    "is_correct": False,
                    "message": f"❌ خطای نحوی (Syntax Error):\n{syntax_error}",
                    "stderr": syntax_error,
                    "stdout": "",
                }

        result = CodeExecutor.execute(code, language, test_input)

        if not result["success"]:
            return {
                "is_correct": False,
                "message": f"❌ خطا در اجرا:\n{result['stderr']}",
                **result,
            }

        actual_output = result["stdout"].strip()
        expected = expected_output.strip()

        is_correct = actual_output == expected

        return {
            "is_correct": is_correct,
            "message": "✅ درست است!" if is_correct else "❌ خروجی مورد انتظار مطابقت ندارد",
            **result,
        }
