# Stardog SPARQL Profiler TUI

A textual user interface (TUI) for [profiling SPARQL queries in Stardog](https://docs.stardog.com/operating-stardog/database-administration/managing-query-performance#sparql-profiler).

<img width="1624" alt="image" src="https://github.com/noahgorstein/stardog_sparql_profiler_tui/assets/23270779/9ce48173-3354-4530-8247-62499aa1755f">

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

https://github.com/noahgorstein/stardog_sparql_profiler_tui/assets/23270779/f6147240-35ca-45a5-8fe2-cbc378d44b11

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
