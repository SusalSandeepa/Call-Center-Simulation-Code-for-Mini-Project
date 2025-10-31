# Call-Center-Simulation-Code-for-Mini-Project

This project simulates a simple **call center system** where a limited number of agents handle incoming calls.  
It is built using **SimPy**, a Python library for discrete event simulation.  
The project models the arrival of customers, the waiting queue, and agent utilization to analyze performance under different conditions.

---

## 🎯 **Objective**

The main objective is to understand how **the number of available agents** and **service time** affect key performance metrics like:

- Average waiting time of customers  
- Queue length  
- Throughput (calls handled per minute)  
- Agent utilization rate  

The simulation helps identify the best balance between service quality and efficiency.

---

## ⚙️ **How It Works**

- **Customers (Callers)** arrive randomly based on an exponential distribution.
- **Agents** are limited and serve one customer at a time.
- When all agents are busy, customers wait in a queue.
- The simulation records:
  - Wait times
  - Queue sizes
  - Completed calls
  - Utilization

---

## 🧩 **Test Scenarios**

Three different scenarios are tested:

| Scenario | Agents | Average Service Time (min) | Description |
|-----------|---------|-----------------------------|--------------|
| A | 2 | 8 | High load, fewer agents |
| B | 3 | 7 | Balanced setup |
| C | 5 | 9 | More agents, lower waiting time |

The simulation runs for 100 minutes in each case and logs the results in both the console and a CSV file.

---

## 📊 **Output**

The program prints results for each scenario and also creates a file named: results.csv

