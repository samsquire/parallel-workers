# parallel-workers

How do you execute a work graph in parallel.

You have a list of named pieces of work and you want to run them in parallel. Some of them have ordering dependencies.

# Tree structure of dependencies of what depends on what - maximum parallelisation

Imagine you have a data structure like this. You can execute this tree in parallel, see treeworkers-incremental.py

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

# List of threads with run groups - things in the group must finish before the next item can begin

Each top level list in the list can be done in paralell to the other list
The items in a sublist can be done in parallel.
Sublists have to finish before the next sublist is picked up.

```
[  # sequence of threads
[ ["task1", "task2"], ["task3", task4"], [] # sequence of run groups   ],

[ ["task8", "task9"], ["task10", "task11"], [] # sequence of run groups   ],
]
```
