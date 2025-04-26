from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse


# Index page
def index(request):
    return render(request, 'Algorithms/index.html')


# optional -> if we find any need, we will use it.
# def result(request):
# return render(request, 'Algorithms/result.html')


# FCFS Algorithm
def fcfs(request):
    if request.method == 'POST':
        at_list = list(map(int, request.POST['arrival_time'].split(',')))
        bt_list = list(map(int, request.POST['burst_time'].split(',')))

        n = len(at_list)
        completion_times = [0] * n
        waiting_times = [0] * n
        turnaround_times = [0] * n

        # Calculate Completion Time
        completion_times[0] = at_list[0] + bt_list[0]
        for i in range(1, n):
            completion_times[i] = max(completion_times[i - 1], at_list[i]) + bt_list[i]

        # Calculate Turnaround Time and Waiting Time
        for i in range(n):
            turnaround_times[i] = completion_times[i] - at_list[i]
            waiting_times[i] = turnaround_times[i] - bt_list[i]

        avg_waiting_time = sum(waiting_times) / n
        avg_turnaround_time = sum(turnaround_times) / n

        return render(request, 'Algorithms/result.html', {
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        })

    return render(request, 'Algorithms/fcfs.html')


# priority scheduling algorithm
def priority(request):
    if request.method == 'POST':
        at_list = list(map(int, request.POST['arrival_time'].split(',')))
        bt_list = list(map(int, request.POST['burst_time'].split(',')))
        pr_list = list(map(int, request.POST['priority'].split(',')))

        n = len(at_list)
        processes = list(range(n))

        # Sort processes by arrival time and priority
        processes.sort(key=lambda x: (at_list[x], pr_list[x]))

        completion_times = [0] * n
        waiting_times = [0] * n
        turnaround_times = [0] * n

        current_time = 0
        for i in processes:
            if current_time < at_list[i]:
                current_time = at_list[i]
            current_time += bt_list[i]
            completion_times[i] = current_time

        for i in range(n):
            turnaround_times[i] = completion_times[i] - at_list[i]
            waiting_times[i] = turnaround_times[i] - bt_list[i]

        avg_waiting_time = sum(waiting_times) / n
        avg_turnaround_time = sum(turnaround_times) / n

        return render(request, 'algorithms/result.html', {
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        })

    return render(request, 'algorithms/priority.html')


# Non-Preemptive Shortest Job First Algorithm
def sjf(request):
    if request.method == 'POST':
        at_list = list(map(int, request.POST['arrival_time'].split(',')))
        bt_list = list(map(int, request.POST['burst_time'].split(',')))

        n = len(at_list)
        processes = list(zip(range(n), at_list, bt_list))  # Process ID, Arrival Time, Burst Time
        processes.sort(key=lambda x: (x[1], x[2]))  # Sort by Arrival Time, then Burst Time

        current_time = 0
        waiting_times = [0] * n
        turnaround_times = [0] * n
        completed = []

        # Process scheduling
        while len(completed) < n:
            available = [p for p in processes if p[1] <= current_time and p not in completed]
            if available:
                shortest = min(available, key=lambda x: x[2])  # Select process with the shortest burst time
                pid, at, bt = shortest
                current_time += bt
                turnaround_times[pid] = current_time - at
                waiting_times[pid] = turnaround_times[pid] - bt
                completed.append(shortest)
            else:
                current_time += 1  # If no process is available, increment time

        avg_waiting_time = sum(waiting_times) / n
        avg_turnaround_time = sum(turnaround_times) / n

        return render(request, 'algorithms/result.html', {
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        })

    return render(request, 'algorithms/sjf.html')


# preemptive sjf algorithm
def preemptive_sjf(request):
    if request.method == 'POST':
        at_list = list(map(int, request.POST['arrival_time'].split(',')))
        bt_list = list(map(int, request.POST['burst_time'].split(',')))

        n = len(at_list)
        remaining_time = bt_list[:]  # To keep track of remaining burst times
        waiting_times = [0] * n
        turnaround_times = [0] * n

        current_time = 0
        completed = 0
        shortest = -1
        finish_time = 0
        check = False

        # Process scheduling
        while completed != n:
            # Find the process with the shortest remaining time at the current time
            for i in range(n):
                if at_list[i] <= current_time and remaining_time[i] > 0:
                    if shortest == -1 or remaining_time[i] < remaining_time[shortest]:
                        shortest = i
                        check = True

            if not check:
                current_time += 1
                continue

            # Execute the shortest process
            remaining_time[shortest] -= 1
            current_time += 1

            # If the process is completed
            if remaining_time[shortest] == 0:
                completed += 1
                finish_time = current_time
                turnaround_times[shortest] = finish_time - at_list[shortest]
                waiting_times[shortest] = turnaround_times[shortest] - bt_list[shortest]

            shortest = -1
            check = False

        avg_waiting_time = sum(waiting_times) / n
        avg_turnaround_time = sum(turnaround_times) / n

        return render(request, 'algorithms/result.html', {
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        })

    return render(request, 'algorithms/preemptive_sjf.html')


# round_robin Algorithm
def round_robin(request):
    if request.method == 'POST':
        at_list = list(map(int, request.POST['arrival_time'].split(',')))
        bt_list = list(map(int, request.POST['burst_time'].split(',')))
        quantum = int(request.POST['quantum_time'])

        n = len(at_list)
        remaining_time = bt_list[:]  # Copy of burst times
        waiting_times = [0] * n
        turnaround_times = [0] * n

        # Track the current time and queue for processes
        time = 0
        queue = []
        completed = 0
        visited = [False] * n

        # Add processes to the queue as they arrive
        while completed != n:
            # Add all processes that have arrived
            for i in range(n):
                if at_list[i] <= time and not visited[i]:
                    queue.append(i)
                    visited[i] = True

            if not queue:
                time += 1
                continue

            # Process the first process in the queue
            current = queue.pop(0)
            execution_time = min(quantum, remaining_time[current])
            remaining_time[current] -= execution_time
            time += execution_time

            # Add newly arrived processes during this time to the queue
            for i in range(n):
                if at_list[i] <= time and not visited[i]:
                    queue.append(i)
                    visited[i] = True

            # If the process is not finished, re-add it to the queue
            if remaining_time[current] > 0:
                queue.append(current)
            else:
                # Process finished
                completed += 1
                turnaround_times[current] = time - at_list[current]
                waiting_times[current] = turnaround_times[current] - bt_list[current]

        avg_waiting_time = sum(waiting_times) / n
        avg_turnaround_time = sum(turnaround_times) / n

        return render(request, 'algorithms/result.html', {
            'avg_waiting_time': avg_waiting_time,
            'avg_turnaround_time': avg_turnaround_time
        })
    return render(request, 'algorithms/round_robin.html')

import ast
def parse_2d_list(text):
    try:
        result = ast.literal_eval(text)
        if not isinstance(result, list) or not all(isinstance(row, list) for row in result):
            raise ValueError
        return result
    except:
        return None

def bankers(request):
    context = {}
    if request.method == "POST":
        try:
            processes = request.POST.get("processes[]", "").split(",")
            processes = [p.strip() for p in processes]
            available = list(map(int, request.POST.get("available[]", "").split(",")))
            allocation = parse_2d_list(request.POST.get("allocation", "[]"))
            max_demand = parse_2d_list(request.POST.get("max_demand", "[]"))

            if not allocation or not max_demand or len(allocation) != len(max_demand) or len(allocation) != len(processes):
                context["error"] = "Mismatch or invalid format in inputs."
                return render(request, "Algorithms/bankers_form.html", context)

            n = len(processes)
            m = len(available)

            need = [[max_demand[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
            finish = [False] * n
            safe_seq = []
            work = available[:]

            while len(safe_seq) < n:
                progress = False
                for i in range(n):
                    if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                        for j in range(m):
                            work[j] += allocation[i][j]
                        finish[i] = True
                        safe_seq.append(processes[i])
                        progress = True
                if not progress:
                    break

            if len(safe_seq) == n:
                context["message"] = "System is in a safe state."
                context["success"] = True
                context["sequence"] = safe_seq
            else:
                context["message"] = "System is NOT in a safe state."
                context["success"] = False

        except Exception as e:
            context["error"] = f"Error: {str(e)}"
    return render(request, "Algorithms/bankers_form.html", context)
