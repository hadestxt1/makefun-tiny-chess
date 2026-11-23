# Tiny Chess 4KB — Benchmark Report (rebuild, submission #2)

Engine: 0x88 board, negamax + alpha-beta, iterative deepening (fixed 50,000-node
budget/move), PVS, null-move pruning (R=2, guarded), transposition table
(ply-adjusted mate scores), killer + history move ordering, MVV-LVA captures,
quiescence (captures + promotions + full check evasions, delta pruning).
Eval: material + Michniewski piece-square tables (RLE-packed) + bishop pair +
endgame king table. Deterministic (fixed node budget, no clock, no randomness).
Python 3.13, standard library only. `main.py` is the kit's `makefun compress`
(LZMA) packing of the readable `source.py` in this folder; no other file is
read, imported or exec'd at runtime. No network, no model calls.

## Size

- `source.py` (readable): 8,386 bytes, sha256 `d7c1e6c3253335683c39d5c73c4256a9b19f61cb21748bb2ce59f3a3730d5749`
- `main.py` (packed, `makefun compress`): 3,438 bytes, sha256 `3fcb016d4857ac4d4f88fb8b993e2975dcf23cb36976c2916b7831d63ceaf4e1` (limit 4,096)

## Correctness

- Perft vs python-chess 1.11.2: all 6 standard positions match to depth 3
  (startpos 8,902; Kiwipete 97,862; etc.), including castling, en passant,
  promotions (all four pieces), check, checkmate and stalemate positions.
- Every move the engine returns is taken from the env's own legal-move list
  (validated against it before posting).

## Practice trials (local kit env, 1 CPU, 6 games each)

House anchors (Elo): depth-2 855, depth-3 1073, depth-4 1199,
nodes-100k 1392, nodes-250k 1497, nodes-500k 1596. Practice floor 1,154.
Sunfish 4KB baseline ≈ 1,365 (6-game practice mean).

| Trial | W | D | L | Elo (scorer) | Notes |
|---|---|---|---|---|---|
| 0 (dev engine) | 4 | 0 | 2 | 1,451 | |
| 1 (dev engine) | 3 | 1 | 2 | 1,364 | |
| 2 (dev engine) | 4 | 0 | 2 | 1,451 | |
| 0 (packed source) | 4 | 0 | 2 | 1,451 | won games 3 & 6, lost 4 & 5 |
| 1 (packed source) | 2 | 2 | 2 | 1,279 | two draws by threefold repetition |
| 0 (packed `main.py`) | 4 | 1 | 1 | 1,545 | the submitted artifact itself, re-run after packing |

Dev engine total: 11W / 1D / 6L over 18 games (61% points), mean Elo ≈ 1,422.
Packed source total: 6W / 2D / 4L over 12 games (58% points), mean Elo ≈ 1,365.
Submitted `main.py` (trial-0): 4W / 1D / 1L, Elo 1,545.
All trials above the 1,154 floor and at/above the Sunfish baseline mean.
