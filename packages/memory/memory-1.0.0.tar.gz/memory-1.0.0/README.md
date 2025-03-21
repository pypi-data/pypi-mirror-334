```markdown
# Memory Library

Memory is a comprehensive Python library designed for efficient memory management and experience storage in artificial intelligence projects, especially in reinforcement learning. It provides a wide range of features, including caching with TTL, system and memory information collection, plugin extensibility, uniform and prioritized experience replay buffers, memory monitoring tools, and an interactive dashboard using Streamlit.

Users can easily install this library via pip:

```bash
pip install memory
```

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [INFO Class](#info-class)
  - [Memoize Decorator](#memoize-decorator)
  - [Plugin System](#plugin-system)
  - [Experience Replay](#experience-replay)
  - [Prioritized Experience Replay](#prioritized-experience-replay)
  - [Memory Monitoring and Dashboard](#memory-monitoring-and-dashboard)
- [Example Projects](#example-projects)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Features

- **INFO Class**: Collects and displays complete system information including virtual memory and swap details.
- **Memoize Decorator**: Caches results of expensive function calls with an optional time-to-live (TTL) to improve performance.
- **Plugin System**: Easily extend the library's functionality with custom plugins that respond to events such as storing or sampling experiences.
- **Uniform Experience Replay Buffer**: Store and uniformly sample experiences, ideal for reinforcement learning algorithms.
- **Prioritized Experience Replay Buffer**: Uses a SumTree data structure to sample experiences based on priority, which can accelerate learning.
- **Memory Monitoring**: Tools to monitor system memory usage periodically.
- **Interactive Dashboard**: A simple dashboard built with Streamlit to visualize the status of your experience buffers and memory usage.

---

## Installation

Memory requires Python 3.6 or above and the following packages:
- [numpy](https://numpy.org/)
- [psutil](https://psutil.readthedocs.io/)
- [streamlit](https://streamlit.io/) *(optional, for the dashboard)*

You can install these dependencies using pip:

```bash
pip install numpy psutil streamlit
```

After installing the dependencies, simply install Memory with:

```bash
pip install memory
```

---

## Usage

### INFO Class

The `INFO` class gathers system, virtual memory, and swap memory information. Use it to quickly get details about your hardware and software environment.

```python
from memory import INFO

info = INFO()
print(info.display_info())
```

### Memoize Decorator

Cache expensive function calls with an optional TTL to avoid redundant computations.

```python
from memory import memoize
import time

@memoize(ttl=5)
def expensive_computation(x):
    time.sleep(1)  # Simulate heavy computation
    return x * x

print(expensive_computation(4))  # Computation is performed
print(expensive_computation(4))  # Result is fetched from the cache
time.sleep(6)
print(expensive_computation(4))  # TTL expired, computation is performed again
```

### Plugin System

Extend the library by creating custom plugins. For example, a plugin that logs experience storage and sampling events:

```python
from memory import MemoryPlugin, PluginManager

class LoggerPlugin(MemoryPlugin):
    def on_experience_stored(self, experience):
        print("LoggerPlugin: Experience stored:", experience)
    def on_sample(self, batch):
        print("LoggerPlugin: Sampled a batch of", len(batch), "experiences.")

plugin_manager = PluginManager()
logger_plugin = LoggerPlugin()
plugin_manager.register_plugin(logger_plugin)
```

### Experience Replay

Store and uniformly sample experiences with the `ExperienceReplay` class.

```python
from memory import ExperienceReplay

replay_buffer = ExperienceReplay(capacity=1000, plugin_manager=plugin_manager)

# Example: storing an experience (state, action, reward, next_state, done)
state = [0.1, 0.2, 0.3, 0.4]
action = 1
reward = 0.5
next_state = [0.2, 0.3, 0.4, 0.5]
done = False

replay_buffer.store(state, action, reward, next_state, done)
batch = replay_buffer.sample(5)
print("Uniform sample batch:", batch)
```

### Prioritized Experience Replay

Store and sample experiences based on their priority using the `PrioritizedExperienceReplay` class.

```python
from memory import PrioritizedExperienceReplay

prioritized_buffer = PrioritizedExperienceReplay(capacity=1000, plugin_manager=plugin_manager)

# Store an experience
prioritized_buffer.store(state, action, reward, next_state, done)
# Sample experiences with importance sampling weights
idxs, batch, weights = prioritized_buffer.sample(5)
print("Prioritized sample batch:", batch)
print("Importance sampling weights:", weights)
```

### Memory Monitoring and Dashboard

Monitor your system's memory usage or launch an interactive dashboard with Streamlit.

#### Memory Monitoring

```python
from memory import monitor_memory_usage
import threading

monitor_thread = threading.Thread(target=monitor_memory_usage, args=(2,), daemon=True)
monitor_thread.start()
```

#### Interactive Dashboard

To run the dashboard, execute the following command in your terminal:

```bash
streamlit run memory.py
```

---

## Example Projects

### Project 1: Reinforcement Learning

- **Uniform Experience Replay**: Use `ExperienceReplay` to store and sample experiences for DQN or other RL algorithms.
- **Prioritized Experience Replay**: Use `PrioritizedExperienceReplay` to improve learning efficiency by sampling important experiences more frequently.

### Project 2: Optimizing Heavy Computations

- **Memoize Decorator**: Cache results of expensive functions to reduce redundant computations in data processing pipelines.

### Project 3: System Monitoring and Dashboard

- **Memory Monitoring**: Integrate `monitor_memory_usage` into your server application to log memory usage.
- **Dashboard**: Use `run_dashboard` with Streamlit to create a real-time visualization of system memory and experience buffer status.

### Project 4: Custom Plugin Development

- Extend Memory's functionality by developing plugins that can log activities, send alerts, or perform custom analytics when experiences are stored or sampled.

---

## Contributing

Contributions are welcome! If you would like to contribute to Memory:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Follow Python coding standards and add appropriate documentation and tests.
4. Submit a pull request with a detailed description of your changes.

---

## License

This library is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Author

**Mohammad Taha Gorji**

For issues, feature requests, or other inquiries, please open an issue on the GitHub repository or contact the author directly.

---

Enjoy using the Memory Library in your projects!
```