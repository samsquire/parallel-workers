# parallel-workers

How do you execute a work graph in parallel.

# Strams of parallel work

Each top level list in the list can be done in paralell to the other list
The items in a sublist can be done in parallel.
Sublists have to finish before the next sublist is picked up.

```
[  # sequence of threads
[ ["task1", "task2"], ["task3", task4"], [] # sequence of run groups   ],

[ ["task8", "task9"], ["task10", "task11"], [] # sequence of run groups   ],
]
```
