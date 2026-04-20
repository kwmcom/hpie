import unittest
import os
import subprocess
import sys

class TestIntegration(unittest.TestCase):
    def test_examples(self):
        examples_dir = os.path.join(os.getcwd(), 'examples')
        # We need an interpreter to execute the code.
        # Assuming hs.py is the entry point as seen in the root.
        
        for filename in os.listdir(examples_dir):
            if filename.endswith(".hpy"):
                filepath = os.path.join(examples_dir, filename)
                # Run the example and check if it runs without errors
                result = subprocess.run([sys.executable, 'hs.py', filepath], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, f"Example {filename} failed with output: {result.stderr}")

if __name__ == '__main__':
    unittest.main()
