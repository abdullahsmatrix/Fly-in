Let's use a real map

Suppose the file contains:

start_hub: home

hub: roof1
hub: roof2
hub: corridorA

end_hub: goal

connection: home-roof1
connection: home-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-goal

Visually:

          roof1 ----- roof2
         /                \
home                         goal
         \                /
          corridorA ------
Adjacency List

The graph stores:

home:
    roof1
    corridorA

roof1:
    home
    roof2

roof2:
    roof1
    goal

corridorA:
    home
    goal

goal:
    roof2
    corridorA

Or in Python-like form:

{
    "home": ["roof1", "corridorA"],
    "roof1": ["home", "roof2"],
    "roof2": ["roof1", "goal"],
    "corridorA": ["home", "goal"],
    "goal": ["roof2", "corridorA"]
}
How it behaves

Imagine Dijkstra or BFS is standing at:

home

and asks:

Where can I go?

The graph immediately answers:

adjacency["home"]

↓

roof1
corridorA

Now the algorithm explores those two possibilities.

Then suppose it reaches:

roof1

and asks:

Where can I go now?

Graph answers:

adjacency["roof1"]

↓

home
roof2

This is why adjacency lists are so useful.

The graph can instantly answer:

Who are my neighbors?
Now let's watch a pathfinding algorithm

Start:

home

Graph says:

Neighbors:
roof1
corridorA

Explore both.

Choose:

roof1

Graph says:

Neighbors:
home
roof2

Ignore home (already visited).

Go to:

roof2

Graph says:

Neighbors:
roof1
goal

Goal found.

Path:

home -> roof1 -> roof2 -> goal

Every step depends on adjacency.