# Bounded run-event stream contract

Contract ID: `wispsy.run-event/1`. Selection task: [JSONL-01](https://github.com/wispsy/wispsy/issues/14).
Implementation/proof task: [JSONL-02](https://github.com/wispsy/wispsy/issues/28).

The implementation owner is [Hypnosis ProcessRun and its explicit stream command](https://github.com/wispsy/hypnosis/blob/main/docs/process-streams.md). The application qualification profile exercises actual processes and preserves the separate in-process Carets API.

Hypnosis live output supplies the concrete workflow: a producer emits incremental
run state for a terminal application or another process. This document selects
framing and failure semantics. The current in-process Carets stream is a separate
API. Existing CLI commands continue to emit single-document JSON. No command may
advertise JSONL transport until the real-process acceptance matrix below passes.

## Records and limits

Each physical line contains exactly one UTF-8 JSON object followed by LF. CRLF
is accepted by stripping a single CR immediately before LF. A final unterminated
record, blank record, BOM, invalid UTF-8 or malformed JSON fails the transport.
Newlines and control characters inside text must be JSON-escaped. Never normalize
Unicode or silently repair malformed bytes. Parse incrementally in bounded byte
buffers; do not call an unbounded read/readline on a child pipe.

Exact fields are `schema`, `run_id`, `sequence`, `kind`, `text`, `code`:

- `schema`: exact string `wispsy.run-event/1`.
- `run_id`: 1–128 ASCII letters, digits, underscore, dot or hyphen, starting
  with a letter or digit. Exactly one run ID per process stream in this profile.
- `sequence`: exact integer (Boolean excluded), starts at zero and increases
  by one for every record. No gaps, duplicates or reordering.
- `kind`: started, delta, completed, canceled, failed or limited.
- `text`: exact Unicode string; only delta may carry nonempty text.
- `code`: exact string; empty except failed/limited outcomes. It carries a
  documented structural code, never private exception text or credentials.

Reject unknown/missing fields, duplicate JSON keys, NaN/Infinity, unsupported
schema versions and wrong types. The flat initial profile has structural depth
one. A future payload/schema version can extend it deliberately. Sequence
integers stay within the portable finite JSON range; the record ceiling is
stricter than that numeric limit.

The producer/consumer enforce all of: 65,536 encoded bytes per record including
LF/CRLF, 16,777,216 encoded bytes per stream, and 100,000 records per stream.
Ceilings include framing, not just text. Lower caller limits are allowed and
must be recorded. A single unbounded text chunk cannot bypass the per-record
ceiling. Input prefetch and output queues are finite; use at most 64 buffered
records initially. Retained presentation state has its own independent budget.

The fixture [run-events.jsonl](run-events.jsonl) is a complete successful stream.

## Lifecycle and process outcome

The first record is started, with empty text/code. It is followed by zero or more
deltas, then exactly one terminal record. Terminal kinds are completed, canceled,
failed and limited; no records follow a terminal event. EOF alone is never success.
An empty stream is a protocol failure. A successful transport needs the valid
completed terminal record, complete EOF and producer process exit status zero.
A terminal record cannot override a later nonzero exit or malformed trailing data.

The initial process statuses are 0 completed, 130 canceled, 1 failed and 3 limited.
Usage/framing failures use status 2 and a structural stderr diagnostic where the
process can still report one. The parent reports signal termination separately.
A valid failed/limited/canceled record is an application outcome, distinct from
malformed transport, but never a successful operation. A producer that dies after
started/deltas without a terminal record leaves an incomplete run and uncertain
partial effects.

Initial failure codes are source_error, source_close_error and command_error.
Initial limit codes are time_budget, event_budget and output_budget. Transport
failures such as invalid_record, record_limit, stream_limit, sequence_error,
missing_terminal, process_exit and downstream_closed are parent diagnostics;
they must not forge a successful application terminal event. Keep raw exception
messages out of default diagnostics. Existing nonstream CLI exit formats remain
compatible; these selected process codes apply only to the future JSONL mode.

## Backpressure, cancellation and partial effects

Await bounded writes and bounded reads. OS pipes provide additional pressure;
they do not replace application budgets. A slow consumer blocks upstream at a
cooperative boundary. Stop reading/producing on schema/sequence/limit/downstream
failure. Close stdin/stdout ends, request producer cancellation, apply a finite
grace deadline, terminate/kill only the child process owned by this invocation
when required, and await/reap it. Do not terminate unrelated processes.

Drain stderr concurrently into a separate bounded tail (64 KiB initial ceiling)
to prevent pipe deadlock. Count/mark truncation. Never merge diagnostics into
stdout records. A finite tail does not make secret-bearing provider prints safe;
providers own value-safe output and credential handling. Native terminal cleanup
must happen before diagnostics are written over the restored screen.

BrokenPipe/downstream closure stops upstream work; never retry automatically.
Cancellation of a consumer task propagates after owned iterator/process cleanup.
Synchronous inference threads remain cooperative at token boundaries; the wire
profile needs an owned process for enforceable process deadlines. Accepted text,
tool calls, checkpoint writes or external effects before failure remain partial
results. There is no rollback or exactly-once claim. Durable uncertain recovery
continues to use func_seq's explicit retry/restart semantics.

No shell parser, globbing, implicit argument wrapping/coercion or automatic
provider activation is added to Hidden Moves. Existing single-document workflows
and direct Python calls retain their contracts.

## Required actual-subprocess acceptance

| Scenario | Required result |
| --- | --- |
| Producer pauses after first delta | Consumer sees the record before producer exits |
| Fragmented multibyte UTF-8 and escaped newlines | Exact text, physical framing preserved |
| Slow consumer/large producer | Bounded lead and retained memory, preserved order |
| Duplicate keys/nonfinite/wrong schema or sequence | Stop upstream and report structural transport failure |
| Oversized/unterminated/empty record or exceeded totals | Refuse before unbounded buffering; no success |
| Failed/limited/canceled terminal record | Application outcome and matching nonzero process status |
| Completed record followed by nonzero exit/trailing data | Transport failure, never successful completion |
| Producer disappears after a partial delta | Incomplete run and explicit uncertain effects |
| Downstream closes or consumer task cancels | Upstream stops; child reaped; terminal restored |
| Stderr flooding | Concurrent bounded drain without stdout contamination/deadlock |
| Child ignores cooperative cancel | Grace timeout and owned child termination/reaping |
| Existing single-document pipeline | Unchanged stdout/stderr/exit behavior |

Fixture validation alone is not subprocess support. JSONL-02 must retain actual
process receipts before implementation consumers claim this profile.
