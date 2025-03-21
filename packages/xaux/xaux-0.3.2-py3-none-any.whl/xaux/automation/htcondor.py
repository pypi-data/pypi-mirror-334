class BatchProcess:
    pass

class HTCondorBatchProcess(BatchProcess):
    _registry = {}

    @classmethod
    def submit():
        pass

    def status():
        pass

    def retrieve():
        pass




class JobManager:
    def __init__(self):
        batch_type = HTCondorBatchProcess()



    def submit(self):
        self.job_list
        self.batch_type.submit()