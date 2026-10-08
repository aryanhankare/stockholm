# Stockholm Architecture — SLE-3 C4 Explanation

Stockholm is an intelligent inventory management project.

The main part of the project is the **Inventory Agent**. It looks at the current inventory, analyzes it, and decides what action should be taken.

The project also has a **Warehouse Search** module. It uses BFS to find where a product is located.

For SLE-3, I have represented the project using the **C4 architecture model**.

C4 has four levels:

1. **Context** — shows the complete system and the user.
2. **Container** — shows the main parts of the system.
3. **Component** — shows the important parts inside one container.
4. **Code** — shows the actual classes and functions.

---

# C4 Level 1 — Context

```text
                  BUSINESS USER / OPERATOR
                           |
                           | inventory data / requests
                           v
                +--------------------------+
                |        STOCKHOLM         |
                |                          |
                |  Inventory Agent         |
                |  + Warehouse Search      |
                +--------------------------+
                           |
                           v
                    Inventory decisions
                    and order updates
```

## What I would say

> This is the Context level of my C4 architecture.
>
> At the highest level, we have the **Business User or Operator** and the **Stockholm system**.
>
> The user provides or manages inventory information.
>
> Stockholm takes this information and analyzes the inventory using the Inventory Agent.
>
> The system then gives inventory decisions, such as whether a product should be monitored or reordered.
>
> The system also uses warehouse search to find the location of a product.
>
> Currently, there are no external production systems connected to Stockholm. The prototype works with its own inventory data.

---

# C4 Level 2 — Container

```text
                 BUSINESS USER / OPERATOR
                           |
                           v
                 +--------------------+
                 |    Flask API       |
                 |      app.py        |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 |   Inventory Agent  |
                 | inventory_agent.py |
                 +---------+----------+
                           |
                           v
                 +--------------------+
                 |  Warehouse Search  |
                 | warehouse_search.py|
                 +--------------------+
                           |
                           v
                          BFS
```

## What I would say

> This is the Container level.
>
> Here I have divided Stockholm into its main parts.
>
> First is the **Flask API**, which is present in `app.py`. It provides an entry point for sending inventory data and running the agent.
>
> The second and most important part is the **Inventory Agent**, present in `inventory_agent.py`.
>
> This is where the main inventory reasoning happens. It checks the inventory, calculates sales velocity, calculates target stock, and decides what action to take.
>
> The third part is **Warehouse Search**, present in `warehouse_search.py`.
>
> It contains the BFS algorithm. The Inventory Agent uses it when it needs to find the location of a product.
>
> So, in simple words, the flow is:
> **User → Flask API → Inventory Agent → Warehouse Search → BFS.**
>
> There is also `search_experiment.py`, but that is used separately for the SLE-2 BFS versus DFS experiment. It is not a runtime container of the Inventory Agent.

---

# C4 Level 3 — Component

The component level focuses on the **Inventory Agent**, because it contains the main intelligent decision-making logic.

```text
                 INVENTORY AGENT
                       |
                       v
                +-------------+
                |  Perception |
                |  perceive() |
                +------+------+
                       |
                       v
             +---------------------+
             | Sales Velocity      |
             | calculate_sales_    |
             | velocity()          |
             +----------+----------+
                        |
                        v
                +---------------+
                | Decision      |
                | Engine        |
                | decide()      |
                +-------+-------+
                        |
              +---------+---------+
              |                   |
              v                   v
       +-------------+     +-------------+
       | Plan Action |     | Warehouse   |
       | plan_actions|     | Locator     |
       +------+------+     | search_     |
              |            | location()  |
              |            +------+------+
              |                   |
              |                   v
              |                  BFS
              v
       +-------------+
       | Action      |
       | act()       |
       +------+------+
              |
              v
       +-------------+
       | Receiving   |
       | receive_    |
       | orders()    |
       +-------------+
```

## What I would say

> This is the Component level.
>
> Here I have gone inside the Inventory Agent and shown its main functions.
>
> First, **`perceive()`** receives the current inventory state.
>
> Then **`calculate_sales_velocity()`** calculates how many units are being sold per day.
>
> After that, **`decide()`** is the main decision-making function.
>
> It checks the current quantity, sales velocity, lead time, pending orders, target stock and safety stock.
>
> Based on these values, it decides what should happen.
>
> The current actions are **MONITOR**, **PLACE_REORDER**, and **EMERGENCY_REORDER**.
>
> Then **`plan_actions()`** converts the decision into a simple action plan.
>
> **`act()`** updates the pending order when a reorder is required.
>
> **`receive_orders()`** simulates the arrival of those pending orders by adding them to the available stock.
>
> At the same time, **`search_location()`** uses BFS to find the warehouse path for a product.
>
> Finally, **`run()`** connects all these steps and runs the complete agent cycle.

---

# C4 Level 4 — Code

At the Code level, I show the actual class and functions implemented in the project.

| Code Element | Simple Responsibility |
|---|---|
| `InventoryAgent` | Main class containing the agent logic |
| `__init__()` | Sets thresholds, safety-stock settings and warehouse graph |
| `perceive()` | Receives the current inventory |
| `calculate_sales_velocity()` | Calculates sales per day |
| `decide()` | Makes the inventory decision |
| `plan_actions()` | Creates the action plan |
| `search_location()` | Finds the product using BFS |
| `act()` | Updates pending orders |
| `receive_orders()` | Moves pending orders into available stock |
| `run()` | Runs the complete agent cycle |

## What I would say

> This is the Code level of C4.
>
> Here I am showing the actual implementation behind the components.
>
> The main class is **`InventoryAgent`**.
>
> The `__init__()` function sets the configuration values and creates the warehouse graph.
>
> `perceive()` receives the inventory.
>
> `calculate_sales_velocity()` calculates the sales rate.
>
> `decide()` contains the main decision logic.
>
> `plan_actions()` creates the action plan.
>
> `search_location()` calls BFS to find the warehouse location.
>
> `act()` updates pending orders.
>
> `receive_orders()` simulates receiving the order.
>
> And `run()` controls the complete process.
>
> So the Code level connects the architecture directly to the actual Python implementation.

---

# How the Agent Makes a Decision

The agent uses a simple rule-based approach.

## Sales Velocity

```text
sales velocity = units sold / number of days
```

For example, if a product sold 20 units in 7 days:

```text
20 / 7 = 2.86 units per day
```

## Target Stock

The agent considers:

- sales velocity
- lead time
- safety stock
- base target stock

It also considers any **pending orders** before deciding whether more stock is needed.

## What I would say

> The current agent is rule-based, not a machine-learning model.
>
> First, it calculates sales velocity using units sold divided by the number of days.
>
> Then it calculates the target stock by considering demand, lead time, safety stock and the base target.
>
> It also checks pending orders.
>
> If the product is out of stock, it can make an emergency reorder decision.
>
> If the available stock including pending orders is below the target, it can place a reorder.
>
> Otherwise, it continues to monitor the product.
>
> This approach is transparent, so I can clearly explain why the agent made a particular decision.

---

# Example of the Decision Flow

```text
Inventory
    |
    v
Perceive
    |
    v
Calculate sales velocity
    |
    v
Calculate target stock
    |
    v
Check current stock + pending orders
    |
    +----------------------+
    |                      |
    v                      v
Enough stock?            Not enough?
    |                      |
    v                      v
 MONITOR             PLACE REORDER
                           |
                           v
                    Is stock zero?
                           |
                    +------+------ +
                    |             |
                    v             v
                   Yes            No
                    |             |
                    v             v
              EMERGENCY       Normal reorder
```

## What I would say

> This is the basic decision flow of the agent.
>
> It first receives the inventory.
>
> Then it calculates the sales velocity and target stock.
>
> After that, it checks the current stock along with pending orders.
>
> If enough stock is available, it monitors the product.
>
> If there is not enough stock, it decides to place a reorder.
>
> If the current stock is zero, it marks the situation as an emergency reorder.
>
> This is how the agent converts inventory data into an action.

---

# Warehouse Search

The warehouse is represented as a graph.

```text
search_location()
        |
        v
      BFS
        |
        v
Product location / path
```

## What I would say

> The second important part of the project is warehouse search.
>
> The warehouse is represented as a graph, where storage areas and products are nodes.
>
> The agent starts from `Receiving` and uses BFS to find the product.
>
> BFS explores the graph level by level and returns the path when it finds the product.
>
> This search logic was developed and compared with DFS during SLE-2, and now the BFS implementation is used by the Inventory Agent.

---

# Design Decisions

## What I would say

> There are a few important design decisions in this architecture.
>
> First, the **Inventory Agent is the core of Stockholm**, because the current project is focused on inventory intelligence.
>
> Second, I kept **warehouse search separate** from the agent. This gives each part a clear responsibility and allows BFS to be reused.
>
> Third, I used a **rule-based approach** for the current version. It is transparent and easy to test, and it gives a foundation for adding more advanced AI later.
>
> Fourth, the architecture only represents features that are actually implemented in the code.
>
> Finally, order receiving is currently simulated in memory. There is no real supplier or database connection.

---

# AI Contribution

## What I would say

> I used ChatGPT as an AI development assistant.
>
> It helped me understand and organize the C4 architecture, review the code structure, improve documentation, and assist with development and debugging.
>
> I selected the project direction, implemented and tested the code, made the final architecture decisions, and verified that the architecture matches the actual repository.

---

# Conclusion

## What I would say

> To conclude, the C4 model helps me explain Stockholm from the highest level down to the actual code.
>
> At the Context level, I show the user and the complete system.
>
> At the Container level, I show the Flask API, Inventory Agent and Warehouse Search.
>
> At the Component level, I show the internal functions of the Inventory Agent.
>
> And at the Code level, I connect those components to the actual Python functions.
>
> The main idea of Stockholm is that the Inventory Agent takes inventory information, analyzes it, makes a decision, and performs the required inventory update, while BFS helps it locate products in the warehouse.