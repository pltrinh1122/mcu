# MCU Scripts

This directory contains utility scripts for working with MCU files.

## Available Scripts

### **validate_mcu.py**
Validates MCU files for compliance with the MCU specification.

**Usage**:
```bash
python validate_mcu.py <directory>
```

**Features**:
- Checks metadata completeness
- Validates content structure
- Ensures required sections are present
- Validates format and syntax

### **check_links.py**
Checks for broken links in MCU documentation files.

**Usage**:
```bash
python check_links.py <directory>
```

**Features**:
- Validates internal links
- Checks relative file references
- Validates anchor links
- Reports broken links

### **generate_mcu.py**
Generates new MCU files from templates with proper metadata.

**Usage**:
```bash
python generate_mcu.py <type> <name> [output_dir]
python generate_mcu.py --list
```

**Features**:
- Generates MCUs from templates
- Automatically creates metadata
- Supports all MCU types
- Lists available templates

## Examples

### Validate All MCU Files
```bash
python scripts/validate_mcu.py .
```

### Check Links in Documentation
```bash
python scripts/check_links.py docs/
```

### Generate New Reference MCU
```bash
python scripts/generate_mcu.py reference my-new-reference
```

### List Available Templates
```bash
python scripts/generate_mcu.py --list
```

## Requirements

- Python 3.6+
- No external dependencies required

## Integration

These scripts can be integrated into:
- Pre-commit hooks
- CI/CD pipelines
- Development workflows
- Quality assurance processes

---

*These scripts help maintain MCU quality and consistency.*
