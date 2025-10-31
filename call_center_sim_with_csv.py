import simpy          # SimPy is a library for running time-based simulations
import random         # Random is used to make arrivals and service times random
import csv            # Used to save simulation results into a CSV file


# Function: customer

# Represents a single caller (customer) who arrives, waits for an agent,
# gets served, and then leaves.
def customer(env, name, agents, service_time, stats):
    arrival_time = env.now  # Record arrival time
    print(f"{name} arrives at time {arrival_time:.2f}")

    # Request an available agent (if busy, caller waits)
    with agents.request() as request:
        yield request  # Wait until an agent is available

        # Calculate waiting time
        wait = env.now - arrival_time
        stats["wait_times"].append(wait)
        print(f"{name} starts call at {env.now:.2f} (Waited {wait:.2f} min)")

        # Serve the caller (random service time based on average)
        yield env.timeout(random.expovariate(1 / service_time))
        print(f"{name} ends call at {env.now:.2f}")

        # Count finished call
        stats["finished_calls"] += 1




# Function: generate_customers

# Continuously creates new callers at random time intervals.
def generate_customers(env, agents, arrival_gap, service_time, stats):
    i = 0
    while True:
        # Wait a random amount of time before the next call
        yield env.timeout(random.expovariate(1 / arrival_gap))
        i += 1
        env.process(customer(env, f"Caller {i}", agents, service_time, stats))
        stats["arrived_calls"] += 1



# Function: watch_queue

# Records how many people are waiting in the queue over time.
def watch_queue(env, agents, stats, sample_time=1.0):
    while True:
        stats["queue_sizes"].append(len(agents.queue))
        yield env.timeout(sample_time)



# Function: run_simulation

# Runs the call center simulation for given parameters and returns results.
def run_simulation(sim_time, num_agents, arrival_gap, service_time, seed=0):
    random.seed(seed)  # Ensures same results every time
    env = simpy.Environment()  # Create simulation environment
    agents = simpy.Resource(env, capacity=num_agents)  # Number of available agents

    # Store statistics
    stats = {
        "arrived_calls": 0,
        "finished_calls": 0,
        "wait_times": [],
        "queue_sizes": []
    }

    # Start processes
    env.process(generate_customers(env, agents, arrival_gap, service_time, stats))
    env.process(watch_queue(env, agents, stats))

    # Run the simulation
    env.run(until=sim_time)

    # Calculate results
    if stats["wait_times"]:
        avg_wait = sum(stats["wait_times"]) / len(stats["wait_times"])
    else:
        avg_wait = 0.0

    if stats["queue_sizes"]:
        avg_queue = sum(stats["queue_sizes"]) / len(stats["queue_sizes"])
    else:
        avg_queue = 0.0

    throughput = stats["finished_calls"] / sim_time  # Calls completed per minute
    utilization = throughput * service_time / num_agents  # Agent busy percentage

    return {
        "Agents": num_agents,
        "Average Wait (min)": round(avg_wait, 2),
        "Average Queue Length": round(avg_queue, 2),
        "Throughput (calls/min)": round(throughput, 3),
        "Utilization": round(utilization, 3),
        "Arrived Calls": stats["arrived_calls"],
        "Finished Calls": stats["finished_calls"]
    }



# MAIN PROGRAM

if __name__ == "__main__":
    print("SIMPLE CALL CENTER SIMULATION (WITH MULTIPLE SCENARIOS)\n")

    # Define three different scenarios
    scenarios = [
        ("Scenario A", 2, 5, 8),   # 2 agents, 8-minute average service time
        ("Scenario B", 3, 5, 7),   # 3 agents, 7-minute average service time
        ("Scenario C", 5, 5, 9)    # 5 agents, 9-minute average service time
    ]

    results_list = []  # List to store all scenario results

    for label, num_agents, arrival_gap, service_time in scenarios:
        print(f"Running {label}...")

        # Run each scenario
        result = run_simulation(
            sim_time=100,          # Run for 100 minutes
            num_agents=num_agents,
            arrival_gap=arrival_gap,
            service_time=service_time,
            seed=10
        )

        # Display results on screen
        print(f"\n{label}:")
        print(f"  Agents: {result['Agents']}")
        print(f"  Average Wait (min): {result['Average Wait (min)']}")
        print(f"  Average Queue Length: {result['Average Queue Length']}")
        print(f"  Throughput (calls/min): {result['Throughput (calls/min)']}")
        print(f"  Utilization: {result['Utilization']}")
        print(f"  Total Calls Arrived: {result['Arrived Calls']}")
        print(f"  Total Calls Finished: {result['Finished Calls']}")
        print("----------------------------------\n")

        # Save results for CSV
        results_list.append((label, num_agents, result))

    # SAVE RESULTS TO CSV
    with open("call_Center_sim_results.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Scenario",
            "Agents",
            "Avg Wait",
            "Avg Queue",
            "Throughput",
            "Utilization",
            "Arrived",
            "Finished"
        ])
        for label, num_agents, r in results_list:
            writer.writerow([
                label,
                num_agents,
                r["Average Wait (min)"],
                r["Average Queue Length"],
                r["Throughput (calls/min)"],
                r["Utilization"],
                r["Arrived Calls"],
                r["Finished Calls"]
            ])

    print("All scenario results saved to 'call_Center_sim_results.csv'")