import os
import subprocess
import sys
import time
import signal
import platform


def run_ui_tests():
    # Define paths
    base_dir = os.getcwd()
    parent_dir = os.path.dirname(base_dir)

    # Make sure we're in the project root directory (where manage.py is)
    os.chdir(parent_dir)
    django_root = os.getcwd()
    print(f"Django project root: {django_root}")

    # Start Django server
    print("Starting Django server...")
    server_cmd = [
        sys.executable,
        "manage.py", "runserver", "--noreload"
    ]

    server = subprocess.Popen(
        server_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(3)

        # Run Playwright tests
        print("Running Playwright tests...")

        # Change to the UITests directory to run tests
        os.chdir(os.path.join(django_root, "UITests"))
        print(f"Test directory: {os.getcwd()}")

        test_cmd = [
            sys.executable,
            "-m", "pytest",
            # "ui/test_departments.py",
            # "ui/test_ensembles.py",
            # "ui/test_instruments.py",
            "ui/test_rehearsals.py",
            "-v"
        ]

        test_process = subprocess.run(test_cmd)

        # Change back to project root
        os.chdir(django_root)

        # Stop the server
        print("Stopping server...")
        if platform.system() == "Windows":
            server.terminate()
        else:
            os.kill(server.pid, signal.SIGTERM)

        time.sleep(2)
        return test_process.returncode

    except Exception as e:
        print(f"Error: {e}")
        return 1
    finally:
        try:
            if server.poll() is None:
                server.terminate()
                server.wait(timeout=5)
        except:
            if platform.system() == "Windows":
                try:
                    subprocess.run(["taskkill", "/F", "/PID", str(server.pid)])
                except:
                    pass
            else:
                try:
                    os.kill(server.pid, signal.SIGKILL)
                except:
                    pass


if __name__ == "__main__":
    sys.exit(run_ui_tests())
