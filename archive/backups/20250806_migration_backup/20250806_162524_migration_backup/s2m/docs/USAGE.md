# Script to Manual (S2M) Converter Usage Guide

## Overview

The Script to Manual Converter (`s2m`) converts AIAI Scripts into human-readable documentation and installation manuals.

## Features

- **Documentation Generation**: Converts AIAI Scripts to markdown, HTML, or PDF
- **Installation Manuals**: Creates step-by-step installation guides
- **Template System**: Supports custom documentation templates
- **Multiple Formats**: Output in various documentation formats

## Installation

```bash
cd s2m
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# Convert a single script to documentation
python src/converter.py path/to/script.yaml --output manual.md

# Convert with custom template
python src/converter.py script.yaml --template custom-template.md --output manual.md

# Convert to HTML
python src/converter.py script.yaml --format html --output manual.html

# Convert to PDF
python src/converter.py script.yaml --format pdf --output manual.pdf
```

### Python API

```python
from s2m.src.converter import ScriptConverter

# Initialize converter
converter = ScriptConverter()

# Convert script to documentation
converter.convert_script("path/to/script.yaml", "output/manual.md")

# Convert with custom template
converter.convert_script("script.yaml", "manual.md", template="custom-template.md")
```

## Templates

### Default Template Structure

```markdown
# {script_name}

## Overview
{script_description}

## Prerequisites
{prerequisites}

## Installation Steps

{steps_formatted}

## Validation
{validation_steps}

## Troubleshooting
{troubleshooting}
```

### Custom Templates

Create custom templates to match your documentation standards:

```markdown
# {script_name} Installation Guide

## Quick Start
{quick_start}

## Detailed Steps
{detailed_steps}

## Verification
{verification_steps}
```

## Output Formats

### Markdown
- Default format
- GitHub-compatible
- Easy to version control

### HTML
- Web-ready documentation
- Styled with CSS
- Interactive elements

### PDF
- Print-ready documentation
- Professional formatting
- Distribution-friendly

## Integration

### GitHub Actions

```yaml
- name: Generate Documentation
  run: |
    cd s2m
    python src/converter.py ../packages/ubuntu-btrfs-aiai/src/*.yaml --output ../docs/
```

### Documentation Pipeline

```bash
# Generate all documentation
find packages/*/src/*.yaml -exec python s2m/src/converter.py {} --output docs/ \;
```

## Configuration

### Template Configuration

```yaml
# s2m-config.yaml
templates:
  default: "templates/default.md"
  ubuntu: "templates/ubuntu.md"
  docker: "templates/docker.md"

output:
  format: "markdown"
  directory: "docs/"
  filename_pattern: "{script_name}_manual.md"
```

## Contributing

See the main repository documentation for contribution guidelines. 