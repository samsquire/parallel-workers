work = [
	{
	"position": 4,
	"name": "@ansible/machines/test",
	"successors": [
	  
	],
	"ancestors": [
		"@ansible/machines/run"
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
        "position": 0,
        "name": "@ansible/machines/package",
        "successors": [
            "@ansible/machines/validate"
        ],
        "ancestors": []
    },
	{
	"position": 0,
	"name": "@ansible/machines/documentation",
	"successors": [
		
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
	"position": 4,
	"name": "@ansible/provision-workers/run",
	"successors": [
	  
	],
	"ancestors": [
		"@ansible/machines/run"
	]
	}

]

function createWorker(item, promises, timeout) {
	return async function(resolve, reject) {
			for (var k = 0 ; k < item.ancestors.length; k++) {
				console.log("Waiting for parent...", item.ancestors[k]);
				await promises[item.ancestors[k]];
			}
			console.log("Running", item.name);
			setTimeout(function() { console.log("Finished", item.name); resolve(1); }, timeout);
		}
}

async function run(work) {
	work.sort((a, b) => (a.position > b.position) ? 1 : -1 );
	promises = {};
	promiseFns = {};
	var item ;
	for (var i = 0 ; i < work.length ; i++) {
		item = work[i];
		var timeout = 3000;
		var promiseFn = createWorker(item, promises, timeout);
		promiseFns[item.name] = promiseFn;
	}
	
	for (var i = 0 ; i < work.length ; i++) {
		item = work[i];
		
		var promise = new Promise(promiseFns[item.name]);
		promises[item.name] = promise;
		
		for (var k = 0 ; k < item.successors.length; k++) {
			var childPromise = promiseFns[item.successors[k].name];
			promise.then(childPromise);
		}
	}
	
}

run(work);