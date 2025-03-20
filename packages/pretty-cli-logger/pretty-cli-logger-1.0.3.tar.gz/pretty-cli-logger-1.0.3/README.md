# Pretty CLI Logger 🌈⏱️

A **zero-dependency**, minimalist CLI logger with colorful output and smart terminal color detection. Perfect for CLI tools, scripts, and devops pipelines!

---

## Features ✨
- 🎨 **Automatic color detection**: Colors only appear in TTYs (no messy escape codes in logs!).
- ⏱️ **Precise UTC timestamps** down to milliseconds.
- 📦 **Zero dependencies**: Won’t bloat your project.
- 🔥 **Simple API**: Just `log_info()`, `log_warn()`, `log_err()`, `log_debug()`.

---

## Installation 📦
```bash
pip install pretty-cli-logger
```

## Usage 🚀
```python
from pretty_cli_logger import log_info, log_warn, log_err, log_debug

log_info("System check passed")       # Green label
log_warn("Low disk space")            # Yellow label
log_err("Failed to connect to DB")    # Red label
log_debug("Cache miss for user:123")  # Gray label
```

## Notes 📝
- Colors use ANSI escape codes (supported by most modern terminals).
- Timestamps are in UTC for consistency across timezones.
- Want to disable colors? Set NO_COLOR=1 in your environment.
