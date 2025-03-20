# Maked: A Command-Line Tool to Automate Markdown Processing

Makedown is a simple yet powerful command-line tool that automates the execution of shell commands embedded within Markdown files. By reading the YAML front matter, Makedown extracts and runs commands, making it perfect for use cases like automating document generation or code execution from Markdown.

## Features

- Command Extraction: Extracts shell commands from the YAML front matter in Markdown files.
- Flexible Input: Supports both file-based input and stdin for seamless integration into any workflow.
- Automation: Automatically executes the command defined in the YAML front matter (e.g., pandoc for converting Markdown to PDF).
- Easy Setup: Installable via pip and can be run locally or as part of any CI/CD pipeline.

## Installation

Makedown can be easily installed using Poetry, Python’s dependency management tool.

### Install via Poetry

```bash
poetry add maked
```

Alternatively, you can install it globally using `pip`:

```bash
pip install maked
```

## Usage

Once installed, you can use Makedown directly from the command line.

### Run with a File

```
maked example.md
```

#### Run with Stdin

You can also pipe content to Makedown:

```bash
echo -e "---\nmaked: 'pandoc example.md -o output.pdf'\n---\nSome content here" | maked
```

## What It Does

The script looks for the maked field in the YAML front matter of a Markdown file or stdin.
It executes the corresponding shell command (e.g., pandoc, make, etc.).
If the front matter is missing or incorrectly formatted, Makedown gracefully handles errors and displays relevant messages.

## Why Makedown?

- Simplicity: Easily integrate Markdown document processing into your workflow.
- Versatility: Use with any shell command, from documentation generation to running scripts.
- Automation: Automate your Markdown file processing, reducing manual effort.

## Example Markdown with YAML Front Matter

```markdown
---
maked: 'pandoc example.md -o example.pdf'
---

# Example Markdown File

This is an example of a Markdown file with a YAML front matter that includes a `maked` field to execute a shell command.
```

## Contributing

We welcome contributions to make Makedown even better! Feel free to fork the repository, open issues, or submit pull requests.
