import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from contextlib import contextmanager

import pytest
from simple_reload import run_simple_reload


@pytest.fixture
def temp_script_dir():
    """Fixture providing a temporary directory for test scripts."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


def create_test_script(path, version='one'):
    """Helper to create a test script with specified version."""
    with open(path, 'w') as f:
        f.write(f"""
import sys
from threading import Event
from contextlib import suppress
from simple_reload import run_simple_reload

def main():
    print("{version}-enter")
    with suppress(KeyboardInterrupt):
        Event().wait()
    print("{version}-exit")

if __name__ == "__main__":
    run_simple_reload([sys.modules[__name__]])
    main()
""")


@contextmanager
def run_script_process(script_path):
    """Context manager for running and safely terminating a script subprocess."""
    process = subprocess.Popen(
        [sys.executable, str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        yield process
    finally:
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def test_reload_on_file_change(temp_script_dir):
    script_path = temp_script_dir / 'test_script.py'

    # Create initial script version
    create_test_script(script_path, version='one')

    with run_script_process(script_path) as process:
        time.sleep(0.2)  # Wait for the script to run

        # Modify the script to change the version
        create_test_script(script_path, version='two')

        time.sleep(0.2)  # Wait for the script to reload

        process.send_signal(subprocess.signal.SIGINT)
        stdout, stderr = process.communicate(timeout=5)

        output = stdout.decode().strip().split('\n')
        assert 'one-enter' in output, "First version didn't run"
        assert 'one-exit' in output, "First version didn't exit properly"
        assert 'two-enter' in output, "Second version didn't run after reload"
        assert 'two-exit' in output, "Second version didn't exit properly"


def test_direct_mode(temp_script_dir):
    script_path = temp_script_dir / 'direct_script.py'

    with open(script_path, 'w') as f:
        f.write("""
import sys
from simple_reload import run_simple_reload

# This should pass through without blocking in direct mode
run_simple_reload([sys.modules[__name__]])

print("completed")
""")

    # Run with SIMPLE_RELOAD_DISABLE=1
    env = os.environ.copy()
    env['SIMPLE_RELOAD_DISABLE'] = '1'

    result = subprocess.run(
        [sys.executable, str(script_path)],
        env=env,
        capture_output=True,
        text=True,
        timeout=5,
    )

    assert (
        'completed' in result.stdout
    ), "Script didn't get past run_simple_reload in direct mode"


def test_module_validation():
    class FakeModule:
        pass

    fake_module = FakeModule()
    # No __file__ attribute

    with pytest.raises(ValueError, match=r'Could not find source path for module.*'):
        run_simple_reload([fake_module])
