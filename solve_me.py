from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    usage_str="""
Usage :-
$ python tasks.py add 2 hello world         # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls                        # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER       # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER      # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help                      # Show usage
$ python tasks.py report                    # Statistics
$ python tasks.py runserver                 # Starts the tasks management server
"""

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
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

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

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
        elif command == "runserver":
            self.runserver()
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

    def render_pending_tasks(self):
        # Complete this method to return all incomplete tasks as HTML
        self.read_current()
        return_str="""
        <head>
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');
        body { background-color: powderblue; }
        h1   {color: blue; text-align: center; font-family: 'Lobster', cursive;}
        ol, li   {font-weight: bold; font-size:20px;}
        .main {max-width:700px;  margin:0 auto;}
        .tasks-box {padding: 40px; background-color: pink; margin:0 auto;}
        </style>
        </head>
        <body><div class="main"><h1> Pending tasks: </h1>"""
        return_str+="<div class='tasks-box'><ol>"
        for i in sorted (self.current_items.keys()) :
            task= self.current_items.get(i,None)
            if task!=None:
                return_str+=(f"<li> {task} [{i}] </li>")
        return_str+="</ol></div>"

        return_str+="</div></body>"

        return return_str

    def render_completed_tasks(self):
        # Complete this method to return all completed tasks as HTML
        self.read_completed()
        return_str="""
        <head>
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lobster&display=swap');
        body { background-color: rgb(38, 172, 116); }
        h1   {color: black; text-align: center; font-family: 'Lobster', cursive;}
        ol, li   {font-weight: bold; font-size:20px;}
        .main {max-width:700px;  margin:0 auto;}
        .tasks-box {padding: 40px; background-color: rgb(231, 176, 112); margin:0 auto;}
        </style>
        </head>
        <body><div class="main"><h1> Completed tasks: </h1>"""
        
        return_str+="<div class='tasks-box'><ol>"
        for i in range(1,len(self.completed_items)+1):
            return_str+=(f"<li> {self.completed_items[i-1]} </li>")

        return_str+="</ol></div>"
        return_str+="</div></body>"
        return return_str


class TasksServer(TasksCommand,  BaseHTTPRequestHandler): 

    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path== "/":
            content = "<h2> Go to path  /tasks to see the pending tasks or path  /completed to view the list of completed tasks </h2>"
        elif self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())
