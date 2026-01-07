from dotenv import load_dotenv

load_dotenv()

from inventory_agent import inventory_agent

from agno.eval.performance import PerformanceEval

def agent_call():
    resp1 = inventory_agent.run("How many MacBook Air M3 units are in stock?")
    print(resp1.content)
    resp2 = inventory_agent.run("Can you tell me the recipe of Vada pav?")
    print(resp2.content)


if __name__ == "__main__":
    perf = PerformanceEval(
        func=agent_call,
        num_iterations=2,
        warmup_runs=0
    )

    perf.run(print_results=True)
