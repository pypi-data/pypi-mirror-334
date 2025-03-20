# Updating zen-completions Dependency

This document explains how to update the projects that depend on zen-completions to use the PyPI package instead of the Git repository.

## For Projects Using pyproject.toml (Poetry)

Update your `pyproject.toml`:

```toml
# Before
zen-completions = {git = "https://github.com/zenafide/zen-completions.git"}

# After
zen-completions = "^0.1.0"  # Use the appropriate version number
```

Then run:
```bash
poetry update
```

## For Projects Using requirements.txt

Update your `requirements.txt`:

```
# Before
git+https://github.com/zenafide/zen-completions.git

# After
zen-completions==0.1.0  # Use the appropriate version number
```

Then run:
```bash
pip install -r requirements.txt
```

## For Dockerfile-based Projects

If your Docker build is failing because Git isn't installed, you now have two options:

1. Use the PyPI package (recommended):
   Update your dependency management file as shown above.

2. Install Git in your Docker image:
   If you still need to install from Git for some reason, you can add Git to your Dockerfile:

   ```dockerfile
   RUN apt-get update && apt-get install -y --no-install-recommends \
       git \
       # other dependencies
       && pip install -r requirements.txt \
       && apt-get purge -y --auto-remove git \
       && apt-get clean \
       && rm -rf /var/lib/apt/lists/*
   ```

The PyPI approach is preferred as it:
- Reduces build time
- Reduces image size
- Makes explicit the version being used
- Follows Python best practices 