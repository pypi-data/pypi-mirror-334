# dotcat: Cat Structured Data, in Style

Dealing with structured data in shell scripts is all but impossible.
`dotcat` gives you the ability to fetch structured data as easily as using cat it.

```bash
# Access data by attribute path
dotcat data.json person.name.first
# John
dotcat data.json person.name.last
# Doe

# Controle your output format
dotcat data.json person.name --output=yaml
# name:
#   first: John
#   last: Doe
dotcat data.json person.name --output=json
# {"first": "John", "last": "Doe"}

# List access
dotcat data.json person.friends@0
# {"name":{"first": "Alice", "last": "Smith"}, "age": 25} -> item access
dotcat data.json person.friends@2:4
# [{"name":{"first": "Alice", "last": "Smith"}, "age": 25}, {"name":{"first": "Bob", "last": "Johnson"}, "age": 30}]  -> slice access
dotcat data.json person.friends@4:-1
# ... from 5th to last item
```

## The good times are here

Easily read values from **JSON, YAML, TOML, and INI** files without complex scripting or manual parsing.

Access deeply **nested values** using intuitive dot-separated paths (e.g., **`person.first.name`**) while controlling the **output format** with `--output` flag.

Dotcat is a good **unix citizen** with well structured **exit codes** so it can take part of your command pipeline like cat or grep would.

## Installation

If you have a global pip install, this will install dotcat globally:

```bash
pip install dotcat
```
