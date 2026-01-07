# ⚡ Operational Evaluation

## 📌 Overview

**Operational Evaluation** focuses on measuring and monitoring the performance, reliability, and efficiency of AI agents in production. While functional evaluation checks if the agent gives correct answers, operational evaluation ensures it does so quickly, reliably, and cost-effectively.

Key metrics include response time, tool usage, task success rate, and failure rate — all essential for production-ready systems.

---

## 🎯 Why Operational Metrics Matter

### The Production Reality

```
┌─────────────────────────────────────────────────────────────────┐
│              OPERATIONAL CONCERNS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  "The agent gives correct answers..."                           │
│                                                                  │
│  BUT:                                                           │
│  • Takes 30 seconds to respond (users leave)                    │
│  • Fails 20% of the time (unreliable)                          │
│  • Costs $0.50 per query (unsustainable)                       │
│  • Uses wrong tools 15% of the time (inefficient)              │
│                                                                  │
│  Operational metrics catch these issues!                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Operational Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Response Time** | Time from query to response | < 3 seconds |
| **Tool Usage** | Which tools called, how often | Varies |
| **Task Success %** | Queries successfully completed | > 95% |
| **Tool Failure Rate** | Tool calls that fail | < 5% |
| **User Satisfaction** | User ratings/feedback | > 4/5 |
| **Cost per Query** | LLM + tool costs | Budget dependent |

---

## ⏱️ Response Time Metrics

### Measuring Latency

```
┌─────────────────────────────────────────────────────────────────┐
│                    LATENCY BREAKDOWN                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Query                                                     │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                            │
│  │ Input Processing│ ← P1: Preprocessing time                   │
│  └────────┬────────┘                                            │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │   LLM Call      │ ← P2: Model inference time                 │
│  └────────┬────────┘                                            │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │   Tool Calls    │ ← P3: External API latency                 │
│  └────────┬────────┘                                            │
│           ▼                                                      │
│  ┌─────────────────┐                                            │
│  │ Response Format │ ← P4: Post-processing time                 │
│  └────────┬────────┘                                            │
│           ▼                                                      │
│  Response to User                                               │
│                                                                  │
│  Total Latency = P1 + P2 + P3 + P4                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Performance Evaluation with Agno

```python
from agno.eval.performance import PerformanceEval
from inventory_agent import inventory_agent

def agent_call():
    resp1 = inventory_agent.run("How many MacBook Air M3 units are in stock?")
    print(resp1.content)
    resp2 = inventory_agent.run("Can you tell me the recipe of Vada pav?")
    print(resp2.content)

perf = PerformanceEval(
    func=agent_call,
    num_iterations=10,
    warmup_runs=2  # Ignore first 2 runs (cold start)
)

perf.run(print_results=True)
```

### Output Example

```
Performance Evaluation Results
==============================
Total Iterations: 10
Warmup Runs: 2

Latency Statistics:
  Mean:   2.34s
  Median: 2.21s
  P95:    3.45s
  P99:    4.12s
  Min:    1.89s
  Max:    4.23s

Throughput: 4.27 queries/second
```

### Custom Latency Tracking

```python
import time
from dataclasses import dataclass
from typing import List

@dataclass
class LatencyMetrics:
    total_time: float
    llm_time: float
    tool_time: float
    preprocessing_time: float

def preprocess(query: str) -> str:
    """Preprocess the query (stub implementation).
    
    In production, this might include:
    - Input sanitization
    - Query normalization
    - Language detection
    """
    return query.strip()

def measure_latency(agent, query):
    start = time.time()
    
    # Preprocessing
    preprocess_start = time.time()
    processed_query = preprocess(query)
    preprocessing_time = time.time() - preprocess_start
    
    # LLM + Tools (tracked internally by agent)
    response = agent.run(processed_query)
    
    total_time = time.time() - start
    
    # Safely extract metrics with defaults
    metrics = getattr(response, 'metrics', {}) or {}
    
    return LatencyMetrics(
        total_time=total_time,
        llm_time=metrics.get("llm_time", 0),
        tool_time=metrics.get("tool_time", 0),
        preprocessing_time=preprocessing_time
    )
```

---

## 🔧 Tool Usage Analytics

### What to Track

| Metric | Description | Why It Matters |
|--------|-------------|----------------|
| **Tool Call Count** | How many tools called per query | Efficiency |
| **Tool Selection** | Which tools are used | Optimization |
| **Tool Success Rate** | % of successful tool calls | Reliability |
| **Tool Latency** | Time per tool call | Performance |
| **Unnecessary Calls** | Tools called but not needed | Cost |

### Tool Usage Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL USAGE DASHBOARD                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Tool Call Distribution (Last 24h)                              │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ inventory_tool    ████████████████████████  45%         │    │
│  │ search_tool       ████████████             25%          │    │
│  │ calculator_tool   ████████                 18%          │    │
│  │ email_tool        █████                    12%          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  Tool Success Rates                                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ inventory_tool    ████████████████████  98%             │    │
│  │ search_tool       ████████████████     85%              │    │
│  │ calculator_tool   ████████████████████ 99%              │    │
│  │ email_tool        ██████████████       72%  ⚠️          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Implementation

```python
from collections import defaultdict
from math import ceil
import time
import json

class ToolAnalytics:
    def __init__(self):
        self.tool_calls = defaultdict(list)
    
    def log_tool_call(self, tool_name, params, result, latency, success):
        self.tool_calls[tool_name].append({
            "timestamp": time.time(),
            "params": params,
            "latency": latency,
            "success": success
        })
    
    def get_stats(self, tool_name=None):
        tools = [tool_name] if tool_name else self.tool_calls.keys()
        stats = {}
        
        for tool in tools:
            calls = self.tool_calls[tool]
            if calls:
                latencies = [c["latency"] for c in calls]
                n = len(latencies)
                sorted_latencies = sorted(latencies)
                # Proper P95 calculation
                p95_index = min(ceil(0.95 * n) - 1, n - 1)
                
                stats[tool] = {
                    "total_calls": n,
                    "success_rate": sum(c["success"] for c in calls) / n,
                    "avg_latency": sum(latencies) / n,
                    "p95_latency": sorted_latencies[p95_index] if n > 0 else 0
                }
        
        return stats
```

---

## 📈 Task Success Rate

### Defining Success

| Success Type | Definition | Measurement |
|--------------|------------|-------------|
| **Completion** | Agent provided a response | Binary |
| **Correctness** | Response was accurate | Accuracy score |
| **Helpfulness** | User found it useful | User feedback |
| **Task Completion** | User's goal achieved | Task-specific |

### Tracking Success

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TaskResult:
    query: str
    response: str
    completed: bool
    correct: bool
    user_rating: Optional[int]
    error: Optional[str]

class SuccessTracker:
    def __init__(self):
        self.results: List[TaskResult] = []
    
    def log(self, result: TaskResult):
        self.results.append(result)
    
    def get_metrics(self):
        total = len(self.results)
        if total == 0:
            return {}
        
        metrics = {
            "completion_rate": sum(r.completed for r in self.results) / total,
            "correctness_rate": sum(r.correct for r in self.results) / total,
            "error_rate": sum(1 for r in self.results if r.error) / total
        }
        
        # Only compute avg_user_rating if there are rated results
        rated_results = [r for r in self.results if r.user_rating is not None]
        if rated_results:
            metrics["avg_user_rating"] = sum(r.user_rating for r in rated_results) / len(rated_results)
        
        return metrics
```

---

## 📊 Logging and Storage

### Where to Store Metrics

| Storage | Best For | Examples |
|---------|----------|----------|
| **Log Files** | Development, debugging | JSON logs, text logs |
| **Database** | Structured queries, dashboards | PostgreSQL, MongoDB |
| **Monitoring Service** | Real-time alerts, visualization | Elasticsearch, BigQuery, Snowflake |
| **APM Tools** | Full observability | Datadog, New Relic |

### Structured Logging

```python
import json
import logging
from datetime import datetime

class AgentLogger:
    def __init__(self, log_file="agent_metrics.jsonl"):
        self.log_file = log_file
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(message)s'
        )
    
    def log_query(self, query_id, query, response, metrics):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query_id": query_id,
            "query": query,
            "response_length": len(response),
            "latency_ms": metrics.get("latency_ms"),
            "tools_used": metrics.get("tools_used", []),
            "token_count": metrics.get("token_count"),
            "success": metrics.get("success", True),
            "error": metrics.get("error")
        }
        logging.info(json.dumps(log_entry))
```

### Forwarding to Monitoring Services

```python
from elasticsearch import Elasticsearch

class MetricsForwarder:
    def __init__(self, es_host="localhost:9200"):
        self.es = Elasticsearch([es_host])
        self.index = "agent-metrics"
    
    def forward(self, metrics):
        self.es.index(
            index=self.index,
            document={
                **metrics,
                "@timestamp": datetime.utcnow().isoformat()
            }
        )

# Usage
forwarder = MetricsForwarder()
forwarder.forward({
    "query_id": "abc123",
    "latency_ms": 2340,
    "success": True,
    "tools_used": ["inventory_tool"]
})
```

---

## 🚨 Alerting and Monitoring

### Alert Conditions

| Condition | Threshold | Action |
|-----------|-----------|--------|
| **High Latency** | P95 > 5s | Page on-call |
| **Low Success Rate** | < 90% | Slack alert |
| **Tool Failures** | > 10% | Email team |
| **Error Spike** | 5x normal | Page on-call |
| **Cost Spike** | > 2x budget | Email finance |

### Alert Implementation

```python
class AlertManager:
    def __init__(self, thresholds):
        self.thresholds = thresholds
        self.alerts = []
    
    def check(self, metrics):
        if metrics["p95_latency"] > self.thresholds["latency_p95"]:
            self.alert("HIGH_LATENCY", f"P95 latency: {metrics['p95_latency']}s")
        
        if metrics["success_rate"] < self.thresholds["min_success_rate"]:
            self.alert("LOW_SUCCESS", f"Success rate: {metrics['success_rate']}")
        
        if metrics["error_rate"] > self.thresholds["max_error_rate"]:
            self.alert("HIGH_ERRORS", f"Error rate: {metrics['error_rate']}")
    
    def alert(self, alert_type, message):
        self.alerts.append({
            "type": alert_type,
            "message": message,
            "timestamp": datetime.utcnow()
        })
        # Send to Slack, PagerDuty, etc.
        send_notification(alert_type, message)
```

---

## 📋 Operational Dashboard

### Key Visualizations

```
┌─────────────────────────────────────────────────────────────────┐
│                 AGENT OPERATIONS DASHBOARD                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Response Time (Last Hour)                               │    │
│  │     3s ┤                    ╭─╮                         │    │
│  │     2s ┤  ╭──╮    ╭──╮    │  │    ╭──╮                 │    │
│  │     1s ┤──╯  ╰────╯  ╰────╯  ╰────╯  ╰──               │    │
│  │        └────────────────────────────────────────────    │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐   │
│  │ Success Rate     │  │ Queries/Min      │  │ Avg Latency  │   │
│  │     96.5%        │  │     127          │  │    2.1s      │   │
│  │     ▲ 1.2%       │  │     ▲ 15%        │  │    ▼ 0.3s    │   │
│  └──────────────────┘  └──────────────────┘  └──────────────┘   │
│                                                                  │
│  Recent Errors:                                                 │
│  • 14:32 - Tool timeout: search_tool (3 occurrences)           │
│  • 14:28 - Rate limit exceeded (1 occurrence)                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Takeaways

1. **Response time matters** — Users won't wait; track P50, P95, P99 latencies
2. **Tool analytics reveal inefficiencies** — Monitor which tools are used and their success rates
3. **Task success is multi-dimensional** — Completion, correctness, and user satisfaction
4. **Structured logging enables analysis** — Use JSON logs forwarded to monitoring services
5. **Alerting prevents outages** — Set thresholds and automate notifications
6. **Dashboards provide visibility** — Real-time metrics for operational awareness

---

## 📖 Further Reading

- [Elasticsearch for Log Analytics](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Datadog APM](https://docs.datadoghq.com/tracing/)
- [Prometheus Metrics](https://prometheus.io/docs/introduction/overview/)
- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/)
