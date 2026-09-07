# Compare Backtracking and Forward Checking Methods for Graph Coloring

An AI-course practice project that implements and empirically compares two classic CSP search strategies — plain chronological **backtracking search** and **backtracking with forward checking** — on the **graph (map) coloring problem**, using randomly generated graphs of increasing density.

## Overview

Graph coloring is modeled here as a Constraint Satisfaction Problem (CSP):

- **Variables** — the graph's vertices
- **Domain** — a set of colors
- **Constraints** — adjacent vertices must not share the same color

The script runs both search strategies against the same series of randomly generated test graphs and logs solve time and timeout/failure counts, to compare their practical performance as graphs get denser.

## Repository contents

| File / folder | Purpose |
|---|---|
| `CSP_BackTrakcing.py` | Main script — CSP solver (backtracking & forward checking), graph visualization, and the benchmark loop |
| `gen_text.py` | Random test-case generator — builds a random 51-vertex graph and writes its edge list |
| `testCase2.txt` | Edge list of the most recently generated random test graph (regenerated/overwritten on each run) |
| `IranTestCase.txt` | A real-world sample instance — adjacency list of Iran's 31 provinces (by abbreviation), a classic small map-coloring example |
| `resault.txt` | Full console log of the latest benchmark run |
| `Outputs__resault/` | Archive folder — a timestamped copy of `resault.txt` is saved here at the end of every run |
| `.gitignore` | Ignored files/folders |

## How it works

**1. Test-case generation (`gen_text.py`)**
`main(P_Edge)` builds a random graph over 51 vertices (`0`–`50`): for every pair of vertices, an edge is added independently with probability `P_Edge`. The resulting edges are written to `testCase2.txt` as `a,b` lines.

**2. Building the constraint graph (`CreateTestCase`)**
`CreateTestCase(Probility_Edge)` calls the generator above, then reads `testCase2.txt` back in to build:
- `Constraing_Graph` — a dict mapping each vertex to a `NodeStar` object holding its neighbors
- `VERTEX_LIST` — a dict mapping each vertex to its current color, initialized to the "unassigned" sentinel value (`-97`)

**3. Solving (`DFS_BACKtracking_Coloring`)**
One class holds the whole solver as static state and exposes two strategies through `DFS_BACK_Coloring(graph, method, color_domain, vertex_list)`:

- **`"BACK"`** — plain backtracking: assigns colors to vertices in a fixed order, tries each color from `ColorDomain`, validates the whole graph after each assignment, and backtracks on conflict.
- **`"FORWARDING"`** — backtracking with forward checking: repeatedly picks the unassigned vertex with the smallest remaining domain (MRV heuristic), assigns it a color, and immediately removes that color from all of its neighbors' domains. If a neighbor's domain empties out, the search backtracks and restores the pruned values.

Both strategies share a wall-clock timeout (`MAX_TIME_LENGTH_GLOBAL = 30` seconds by default) — a run that exceeds it is stopped and counted as a timeout rather than left running indefinitely.

**4. Visualization (`GraphVisualization`)**
Each generated test graph is drawn with `networkx`/`matplotlib` and saved as `testCase_<i>.png`. Old visualization PNGs from previous runs are deleted at the start of each script run.

**5. Benchmark loop**
The bottom of `CSP_BackTrakcing.py` runs 24 trials. The edge probability starts at `0.05` and increases by `0.05` every 5 trials, giving 5 trials each at densities `0.05, 0.10, 0.15, 0.20` and a final 4 trials at `0.25`, all against `ColorDomain = [1, 2, 3, 4, 5]` (5 available colors). For each trial the script:
1. Generates a new random graph and saves its visualization
2. Solves it with forward checking, then with plain backtracking
3. Updates a running average solve time and a failure/timeout count for each method

Output is written to the console and to `resault.txt` at the same time (via the `Tee` helper class). At the end, average solve times and failure counts for both methods are printed, and the log is archived into `Outputs__resault/` under a timestamped filename.

## Requirements

- Python 3
- `numpy`
- `networkx`
- `matplotlib`

```bash
pip install numpy networkx matplotlib
```

## Usage

Run the full benchmark from the repository root:

```bash
python CSP_BackTrakcing.py
```

This will:
- generate 24 random test graphs of increasing edge density,
- solve each one with both backtracking and forward checking,
- save a visualization (`testCase_<i>.png`) per test graph,
- print progress and results to the console, and
- write the full log to `resault.txt`, archiving a timestamped copy in `Outputs__resault/`.

To generate a single test case at a custom edge probability instead of running the full benchmark:

```python
import gen_text
gen_text.main(0.1)  # writes testCase2.txt at ~10% edge probability
```

### Trying the real-world example

`IranTestCase.txt` holds the adjacency list for Iran's 31 provinces — a well-known small map-coloring instance. It isn't wired into the benchmark loop by default (which always regenerates `testCase2.txt` from a random graph), but it uses the same `a,b`-per-line edge format, so it can be used in place of `testCase2.txt` for a quick manual solve.

## Notes

- Colors are small integers; `-97` is the internal sentinel for "unassigned."
- The benchmark always uses 5 colors against randomly generated graphs, so at higher edge densities a valid 5-coloring may not exist, or may not be found within the 30-second timeout — that's expected, and is exactly what the failure/timeout counters are measuring.
- Running the script deletes old `testCase_*.png` files and overwrites `testCase2.txt` and `resault.txt`.

## Course context

Built as an assignment for an AI course, comparing backtracking search and forward checking as CSP-solving strategies for graph coloring.
