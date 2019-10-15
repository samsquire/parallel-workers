from threading import Thread

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

class Worker(Thread):
	def __init__(self, threads, item):
		super(Worker, self).__init__()
		self.threads = threads
		self.item = item
		
	def run(self):
		for ancestor in self.item["ancestors"]:
			self.threads[ancestor].join()
		print("<- {}".format(self.item["name"]))
		
		for successor in self.item["successors"]:
			self.threads[successor].start()
		
threads = {}
for item in work:
	threads[item["name"]] = Worker(threads, item)
for item in work:
	if item["position"] == 0:
		threads[item["name"]].start()
	

	