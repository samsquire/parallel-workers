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
    def __init__(self, item, doer_cache):
        super(Doer, self).__init__()
        self.item = item
        self.doer_cache = doer_cache

    def run(self):
        print("Running {}".format(self.item))
            

class Grouper(Thread):
    def __init__(self, run_groups, doer_cache):
        super(Grouper, self).__init__()   
        self.run_groups = run_groups
        self.doer_cache = doer_cache
        
    def run(self):
        doers = []
        for group in self.run_groups: 
            if group in doer_cache:
                doer = doer_cache[group]
                print("Waiting for existing running {}".format(group))
                doer_cache[group].join()
            else:
                doer = Doer(group, doer_cache)
                doer.start()
                doer_cache[group] = doer
            doers.append(doer)
            
        print("waiting for doers")
        for doer in doers:
            doer.join()


class StreamWorker(Thread):
    def __init__(self, run_groups, doer_cache):
        super(StreamWorker, self).__init__()   
        self.run_groups = run_groups
        self.doer_cache = doer_cache
        
    def run(self):
        doers = []
        for group in self.run_groups: 
            doer = Grouper(group, doer_cache)
            doers.append(doer)
            doer.start()
        print("waiting for grouper")
        for doer in doers:
            doer.join()


stream_workers = []     
doer_cache = {}

for stream in work:
    stream_worker = StreamWorker(stream, doer_cache)
    stream_workers.append(stream_worker)
    stream_worker.start()

for stream_worker in stream_workers:
    stream_worker.join()

print("Finished")