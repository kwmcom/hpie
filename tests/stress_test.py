import pytest
import subprocess
import os
import time

# List of example files to use for stress testing
EXAMPLES = [os.path.join("examples", f) for f in os.listdir("examples") if f.endswith(".hpy")]

def test_infinite_loop():
    """Stress test by running examples repeatedly."""
    # We will run this for a set number of iterations or a time duration.
    # Given the request for "endless" stress testing, we will run for a reasonable 
    # batch size and report results.
    iterations = 100
    for i in range(iterations):
        for example in EXAMPLES:
            try:
                # Execute the interpreter on each example
                # Assuming 'hs.py' can be run as a CLI tool
                result = subprocess.run(
                    ["python3", "hs.py", example], 
                    capture_output=True, 
                    text=True, 
                    timeout=2  # Timeout to detect infinite loops or hangs
                )
                assert result.returncode == 0, f"Example {example} failed in iteration {i}"
            except subprocess.TimeoutExpired:
                pytest.fail(f"Example {example} timed out (potential infinite loop or hang) in iteration {i}")

if __name__ == "__main__":
    # Allow manual invocation of the stress test
    print("Running stress test batch...")
    test_infinite_loop()
    print("Stress test batch completed successfully.")
