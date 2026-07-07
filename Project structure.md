# Drone Pathfinding Project Roadmap

<details>
<summary><strong>Phase 2 — Build the parser first</strong></summary>

## Support

The parser should support input lines such as:

```txt
nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10
hub: roof1 3 4 [zone=restricted color=red]
connection: hub-roof1 [max_link_capacity=2]
```

## Strict validation rules

The parser must validate the following rules strictly:

- Exactly one start hub must be defined.
- Exactly one end hub must be defined.
- Drone count must be positive.
- Zone names must be unique.
- Zone names must not contain dashes or spaces.
- Zone types must be valid.
- Capacities must be positive.
- Duplicate connections are not allowed.
- Connections may only reference already-defined zones.

## Error handling requirement

Parser errors must stop the program immediately with a clear error message that includes:

- The line where the error occurred.
- The cause of the error.

</details>

---

<details>
<summary><strong>Phase 3 — Implement basic pathfinding</strong></summary>

## Initial scope

Start with a simple implementation:

- Ignore multiple drones.
- Ignore capacities.
- Find one shortest valid path from the start hub to the end hub.
- Block zones marked as `zone=blocked`.

## Movement cost rules

Use destination-zone cost:

| Zone type | Cost | Behavior |
|---|---:|---|
| `normal` | 1 | Standard movement |
| `priority` | 1 | Same cost as normal, but slightly preferred |
| `restricted` | 2 | Takes longer to enter |
| `blocked` | Forbidden | Cannot be entered |

## Algorithm choice

Use **Dijkstra’s algorithm**, not BFS, because restricted zones cost `2` turns. BFS assumes all edges have equal cost, which would produce incorrect results when zone costs differ.

</details>

---

<details>
<summary><strong>Phase 4 — Find multiple candidate paths</strong></summary>

## Goal

Generate multiple valid candidate routes so drones can be distributed across more than one path.

## Suggested approach

Generate candidate routes by:

1. Running Dijkstra once to find the best path.
2. Adding temporary penalties to zones or edges already used.
3. Running Dijkstra again several times.
4. Keeping only valid, unique paths.

## Important guidance

Do not try to solve perfect optimization immediately. First, build a working “good enough” solution that can find several usable paths.

</details>

---

<details>
<summary><strong>Phase 5 — Build the turn simulator</strong></summary>

## Per-turn simulation logic

Each turn:

1. Look at each drone.
2. Decide its next move along its assigned path.
3. Check zone capacity after outgoing drones leave.
4. Check connection capacity.
5. Handle restricted-zone movement as a 2-turn transit.
6. Output only drones that moved.

## Required output format

The output format must look like this:

```txt
D1-roof1 D2-corridorA
D1-roof2 D2-tunnelB
D1-goal D2-goal
```

## End condition

The simulation ends when all drones reach the end hub.

</details>

---

<details>
<summary><strong>Phase 6 — Add scheduling intelligence</strong></summary>

## Improvements after basic simulation works

Once the basic simulator works, improve scheduling behavior:

- Send drones to shorter paths first.
- Avoid sending too many drones into the same bottleneck.
- Prefer paths with higher capacity.
- Allow drones to wait when moving would cause a conflict.
- Dynamically choose among candidate paths when a drone leaves the start hub.

## Suggested scoring formula

A useful path scoring formula is:

```txt
path_score = path_cost + drones_already_assigned_to_path / path_throughput
```

Use this score to decide which path should receive the next drone.

</details>

---

<details>
<summary><strong>Phase 7 — Add visual output</strong></summary>

## Start with colored terminal output

Begin with simple colored terminal output before attempting a GUI.

Example:

```txt
Turn 4:
D1: roof2 -> goal
D2: corridorA -> tunnelB
Occupied: roof2[1/1], corridorA[1/2]
```

## Requirement

The subject requires visual feedback through:

- Terminal colors,
- GUI,
- or both.

</details>

---

<details>
<summary><strong>Phase 8 — Testing roadmap</strong></summary>

## Create custom test maps

Build your own maps to test the project thoroughly:

- Single straight path.
- No path to end.
- Blocked zone in the middle.
- Restricted zone.
- Two paths, one short and one long.
- Zone capacity `2`.
- Connection capacity `2`.
- Duplicate connection error.
- Invalid metadata error.
- Many drones stress test.

</details>

---

<details>
<summary><strong>Phase 9 — README and evaluation prep</strong></summary>

## README requirements

The README must explain:

- Project goal.
- How to install and run the project.
- Algorithm choices.
- Visual representation.
- AI usage.
- Resources.

## Evaluation note

The subject explicitly requires these README sections, so make sure they are clearly visible and easy to find.

</details>



