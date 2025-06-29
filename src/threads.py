import threading


class Thread:
    def __init__(self,program,func,args=list()) -> None:
        self.program=program   
        self.args = args
        self.args.append(self)
        self.func=func
        self.running=False
        self.__thread= threading.Thread(target=self.func,args=self.args)
        self.__name__="function : "+self.func.__name__

    def start(self):
        self.running=True
        self.program.threadPool.add(self)
        self.__thread.start()

    def stop(self):
        self.program.threadPool.remove(self)
        self.running=False

    def finish(self):
        self.__thread.join()

    def __str__(self) -> str:
        return "function : "+self.func.__name__



class ThreadPool():
    def __init__(self) -> None:
        self.__pool=list()

    def add(self,thread:Thread):
        self.__pool.append(thread)
    
    def remove(self,thread:Thread):
        if thread in self.__pool:
            self.__pool.remove(thread)
       
    def __str__(self) -> str:
        str=""
        for i in self.__pool:
            str+=i.__name__
        return str    
        


