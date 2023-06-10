# Stardog SPARQL Profiler TUI

A textual user interface (TUI) for profiling SPARQL queries in Stardog.

<img width="1624" alt="image" src="https://github.com/noahgorstein/profiler_tui/assets/23270779/3cef56e8-2843-47d3-a741-5f829262eddd">

## Installation

Install `sparql-profiler` CLI tool to launch the TUI:

```
❯ pip3 install --editable .
```

Check installation:

```
❯ sparql-profiler --help
Usage: sparql-profiler [OPTIONS] [QUERY]

  Profiles the QUERY.

  If both the query_file option and QUERY argument are provided, the QUERY
  argument will take precedence.

  If token is provided in addition to a username and password for
  authentication, the token will take precedence.

Options:
  -u, --username TEXT        Stardog username (applicable only if token not
                             provided)  [default: admin]
  -p, --password TEXT        Stardog password (applicable only if token not
                             provided)  [default: admin]
  -t, --token TEXT           Auth JWT token (applicable only if username and
                             password are not provided)
  -e, --endpoint TEXT        Stardog endpoint  [default:
                             http://localhost:5820; required]
  -d, --database TEXT        Stardog database  [required]
  -r, --reasoning            Enables reasoning for the query to be profiled.
  -f, --query_file FILENAME  File containing query to profile
  -h, --help                 Show this message and exit.
```

## In Action

https://github.com/noahgorstein/profiler_tui/assets/23270779/2737e438-c1a5-47c4-8f77-9f774c215880

## Usage

```text
❯ sparql-profiler --help
Usage: sparql-profiler [OPTIONS] [QUERY]

  Profiles the QUERY.

  If both the query-file option and QUERY argument are provided, the QUERY argument
  will take precedence.

  If token is provided in addition to a username and password for
  authentication, the token will take precedence.

Options:
  -u, --username TEXT        Stardog username (applicable only if token not
                             provided)  [default: admin]
  -p, --password TEXT        Stardog password (applicable only if token not
                             provided)  [default: admin]
  -t, --token TEXT           Auth JWT token (applicable only if username and
                             password are not provided)
  -e, --endpoint TEXT        Stardog endpoint  [default:
                             http://localhost:5820; required]
  -d, --database TEXT        Stardog database  [required]
  -r, --reasoning            Enables reasoning for the query to be profiled.
  -f, --query_file FILENAME  File containing query to profile
  -h, --help                 Show this message and exit.
```
