# Python and shell reference

The same ordinary functions normalize Unicode whitespace/case and report text,
word count and character count. Characters are Unicode code points, not display
cells or grapheme clusters. Empty text has zero words and characters.

The base package supports Python 3.11+ and has no runtime dependencies:

```sh
uv sync --locked
uv run wispsy-reference ' Hello   WORLD '
uv run python -m wispsy ' Hello   WORLD '
```

```python
from wispsy.reference import normalize, report, run_reference

assert report(text=normalize(text=" Hello   WORLD ")) == run_reference(" Hello WORLD ")
```

Select the optional source-qualified workflow profile for Hidden Moves:

```sh
uv sync --locked --extra workflow
uv run hm plugins list
uv run hm --plugin wispsy-reference moves list --json
uv run python -c 'from wispsy.integration import run_catalog; print(run_catalog(" Hello WORLD "))'
```

Provider discovery reads metadata; the `--plugin` flag explicitly activates the
provider's trusted Python. Activation only constructs MoveSet definitions, and
the reference catalog selects `text.normalize` and `text.report`. No external
clients, files or storage are opened by assembly.

The following POSIX shell example uses the same functions. `pipefail` propagates
any process's failure; Windows shells should use their own process/error controls.
The cross-platform checks connect the same processes through native subprocess
pipes without depending on shell syntax.

```sh
set -o pipefail
printf '%s' '{"text":" Hello   WORLD "}' |
  uv run hm --plugin wispsy-reference moves call text.normalize --stdin |
  uv run hm --plugin wispsy-reference moves call text.report --stdin --input-key text
```

The first result is a scalar string. `--input-key text` explicitly maps that
string to the next function's named input. There is no hidden string-to-object
conversion. The final JSON is:

```json
{"text":"hello world","words":2,"characters":11}
```

The [Hidden Moves transport contract](https://github.com/wispsy/hidden_moves/blob/main/docs/JSON_TRANSPORT.md)
defines finite bounded UTF-8 JSON, diagnostics on stderr and structured errors.
An upstream failure emits no success value; the next process rejects empty input.
For workflows with side effects, process pipes alone do not provide checkpoints,
rollback, safe retries or an execution lifecycle.

## Reproduce artifact qualification

```sh
uv build --out-dir dist
uv run python scripts/check_distribution.py dist
uv run python scripts/qualify.py dist --profile workflow
```

Each artifact is installed in a fresh temporary environment outside the checkout.
Base behavior and absent optional packages are checked before installing the
workflow extra. Tests then compare direct Python/catalog results, two connected
CLI processes, Unicode, explicit activation and upstream failure behavior.
CI qualifies Linux/Python 3.11 and 3.14, macOS/3.14 and Windows/3.11. The optional
profile pins an immutable Hidden Moves source; it does not claim an existing
published release contains these new interfaces.
