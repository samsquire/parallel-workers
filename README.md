# parallel-workers

This repository has methods of executing work graphs. A work graph is a directed acyclic graph of tasks that have a topological ordering. There are dependencies between pieces of work that is captured by the relationship of connections.

See [devops-schedule](https://github.com/samsquire/devops-schedule) for schedulers for this code.

# treeworkers.js

Runs tree in parallel

# treeworkers.py

Runs tree in parallel

# treeworkers.rb

Runs tree in parallel

You have a list of named pieces of work and you want to run them in parallel. Some of them have ordering dependencies.

# TreeWorkers.java

Runs data.json

# Tree structure of dependencies of what depends on what - maximum parallelisation

Imagine you have a tree graph data structure like this. You can execute this tree in parallel, see treeworkers-incremental.py and treeworkers.py.

```
work =   [{
        "position": 0,
        "name": "@ansible/machines/package",
        "successors": [
            "@ansible/machines/validate"
        ],
        "ancestors": []
    },
    {
        "position": 1,
        "name": "@ansible/machines/validate",
        "successors": [
            "@ansible/machines/plan"
        ],
        "ancestors": [
            "@ansible/machines/package"
        ]
    },
    {
        "position": 2,
        "name": "@ansible/machines/plan",
        "successors": [
            "@ansible/machines/run"
        ],
        "ancestors": [
            "@ansible/machines/validate"
        ]
    },
    {
        "position": 3,
        "name": "@ansible/machines/run",
        "successors": [
            "@ansible/machines/test",
			"@ansible/provision-workers/run"
        ],
        "ancestors": [
            "@ansible/machines/plan"
        ]
    },
	{
	"position": 4,
	"name": "@ansible/provision-workers/run",
	"successors": [
	  
	],
	"ancestors": [
		"@ansible/machines/run"
	]
	},
	{
	"position": 4,
	"name": "@ansible/machines/test",
	"successors": [
	  
	],
	"ancestors": [
		"@ansible/machines/run"
	]
	}
]
```

# runner.py

List of threads with run groups - things in the group must finish before the next item can begin

Each top level list in the list can be done in paralell to the other list
The items in a sublist can be done in parallel.
Sublists have to finish before the next sublist is picked up.

```
[  # sequence of threads
[ ["task1", "task2"], ["task3", task4"], [] # sequence of run groups   ],

[ ["task8", "task9"], ["task10", "task11"], [] # sequence of run groups   ],
]
```
