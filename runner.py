import threading
from threading import Thread
work = [[['terraform/users/validate'],
  ['terraform/users/plan'],
  ['terraform/users/run'],
  ['terraform/users/test'],
  ['integration'],
  ['terraform/services/validate']],
 [['terraform/vpc/validate'],
  ['terraform/vpc/plan'],
  ['terraform/vpc/run'],
  ['terraform/vpc/test', 'terraform/vpc/deploy'],
  ['integration'],
  ['terraform/services/validate']],
 [['terraform/bastion/validate'],
  ['terraform/bastion/plan'],
  ['terraform/bastion/run'],
  ['terraform/bastion/test']]]

class Doer(Thread):
    def __init__(self, group, doer_cache):
        super(Doer, self).__init__()
        self.group = group
        self.doer_cache = doer_cache

    def run(self):
        for item in self.group:
            if item in self.doer_cache:
                doer_cache[item].join()
                print("Waiting for already started process {}".format(item))
            else:
                print("Running {}".format(item))
                doer_cache[item] = self

class Worker(Thread):
    def __init__(self, run_groups, doer_cache):
        super(Worker, self).__init__()   
        self.run_groups = run_groups
        self.doer_cache = doer_cache
        
    def run(self):
        doers = []
        for group in self.run_groups: 
            doer = Doer(group, doer_cache)
            doers.append(doer)
            doer.start()
        print("waiting for doers")
        for doer in doers:
            doer.join()


stream_workers = []     
doer_cache = {}

for stream in work:
    stream_worker = Worker(stream, doer_cache)
    stream_workers.append(stream_worker)
    stream_worker.start()

for stream_worker in stream_workers:
    stream_worker.join()

print("Finished")