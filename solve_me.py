class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"
    usage_str="""
Usage :-
$ python tasks.py add 2 hello world         # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls                        # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER       # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER      # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help                      # Show usage
$ python tasks.py report                    # Statistics
"""

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            print("error while reading task.txt")

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items.clear()
            for line in file.readlines():
                self.completed_items.append(line[:-1])
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "help":
            self.help()

    def help(self):
        print(self.usage_str)

    def add(self, args):
        self.read_current()
        pr= int(args[0])
        newtask= args[1]
        for i in sorted (self.current_items.keys(), reverse=True) :
            if((i==pr) or (i>=pr and (self.current_items.get(i-1,None)!=None))):
                self.current_items[i+1] = self.current_items.pop(i)
        self.current_items[pr]= newtask    
        self.write_current()
        print(f'Added task: "{newtask}" with priority {pr}')

    def done(self, args):
        pr_done= int(args[0])
        self.read_current()
        print(self.completed_items)
        if self.current_items.get(pr_done, None)!= None:
            completed_task= self.current_items.pop(pr_done)
            self.read_completed()
            self.completed_items.append(completed_task)
            print(self.completed_items)
            self.write_completed()
            print("Marked item as done.")
        else:
            print(f"Error: Error: no incomplete item with priority {pr_done} exists.")    
        self.write_current()

    def delete(self, args):
        pr_to_del= int(args[0])
        self.read_current()
        if self.current_items.get(pr_to_del, None)!= None:
            del self.current_items[pr_to_del]
            print(f"Deleted item with priority {pr_to_del}")
        else:
            print(f"Error: item with priority {pr_to_del} does not exist. Nothing deleted.")    
        self.write_current()


    def ls(self):
        self.read_current()
        cnt=1
        for i in sorted (self.current_items.keys()) :
            task= self.current_items.get(i,None)
            if task!=None:
                print(f"{cnt}. {task} [{i}]")
                cnt+=1    

    
    def report(self):
        self.read_current()
        print(f"Pending : {len(self.current_items)}")
        cnt=1
        for i in sorted (self.current_items.keys()) :
            task= self.current_items.get(i,None)
            if task!=None:
                print(f"{cnt}. {task} [{i}]")
                cnt+=1  
        print()
        self.read_completed()
        print(f"Completed : {len(self.completed_items)}")
        for i in range(1,len(self.completed_items)+1):
            if i==len(self.completed_items):
                print(f"{i}. {self.completed_items[i-1]}", end="")
            else:    
                print(f"{i}. {self.completed_items[i-1]}")


