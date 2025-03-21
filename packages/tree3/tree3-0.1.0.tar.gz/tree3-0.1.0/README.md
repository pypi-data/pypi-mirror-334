# tree3

A command line utility to display and create directory structures.

## Installation

```bash
pip install tree3
```

## Usage

### Display directory structure

```bash
tree3 [path]
```

### Save directory structure to file

```bash
tree3 [path] -o output.txt
```

### Create directories from structure file

```bash
tree3 -i input.txt
```

### Respect .gitignore rules

```bash
tree3 -g
```

### Copy structure to clipboard

```bash
tree3 --copy
```

### Get help

```bash
tree3 -h
```

## Examples

### Example 1: Display current directory structure

```bash
tree3
```

### Example 2: Save structure to file and copy to clipboard

```bash
tree3 myproject -o project-structure.txt --copy
```

### Example 3: Create directory structure from file

```bash
tree3 -i project-structure.txt
```