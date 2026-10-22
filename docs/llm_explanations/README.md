# LLM explanations

Short, mentor-mode notes written after each completed logical task (feature,
fix, refactor, significant decision). One file per task, not per file edit.

## Naming

`{n}_explanation_{dd}_{mm}_{yy}_{hh}_{mm}.md` where `{n}` is the next integer
after the highest existing number.

## Template

```
# {n} — {task name} | {dd}/{mm}/{yy} {hh}:{mm}

## What
2 lines: what was built, changed, or fixed

## Why
3 lines: the problem, the reasoning, the key design choice

## Concepts
- **{Term or pattern}**: one-line definition
3–5 bullets

## Assumptions
- assumption the user might not know was made
1–3 bullets

## Watch out
- failure mode, edge case, or gotcha
1–2 bullets
```

Hard cap ~200 words. Code comments stay minimal — reasoning belongs here.
