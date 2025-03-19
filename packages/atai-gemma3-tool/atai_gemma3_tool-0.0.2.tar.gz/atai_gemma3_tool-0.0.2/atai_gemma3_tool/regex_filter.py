import sys
import re

class RegexFilterStream:
    def __init__(self, stream, patterns):
        self.stream = stream
        # Combine all patterns into one regex
        self.pattern = re.compile("|".join(patterns))

    def write(self, data):
        # Write data only if it does not match any of the patterns.
        if not self.pattern.search(data):
            self.stream.write(data)

    def flush(self):
        self.stream.flush()

def setup_logging_filter():
    import os
    os.environ["DISABLE_TQDM"] = "1"

    import logging
    logging.getLogger("transformers").setLevel(logging.ERROR)

    import warnings
    warnings.filterwarnings("ignore", message="Using a slow image processor")
    
    # Define regex patterns for messages you want to ignore.
    ignore_patterns = [
        r"Loading checkpoint shards:",
        r"Using a slow image processor"
    ]
    # Replace sys.stderr with our filtered stream.
    sys.stderr = RegexFilterStream(sys.stderr, ignore_patterns)
