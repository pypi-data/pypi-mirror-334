import time
import random
import threading
import numpy as np
import psutil
import platform
import logging

# Configure logging to display debug messages
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

# ------------------------------------------------------------------
# 1. Memoize decorator with TTL
# ------------------------------------------------------------------
def memoize(ttl: float = None):
    """
    Decorator to cache the results of expensive function calls with an optional TTL.

    :param ttl: Time-to-live in seconds (optional).
    """
    cache = {}
    lock = threading.Lock()

    def decorator(func):
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            with lock:
                if key in cache:
                    result, timestamp = cache[key]
                    if ttl is None or (time.time() - timestamp) < ttl:
                        logging.debug("Cache hit for key: %s", key)
                        return result
                    else:
                        logging.debug("Cache expired for key: %s", key)
                logging.debug("Cache miss for key: %s", key)
                result = func(*args, **kwargs)
                cache[key] = (result, time.time())
                return result
        return wrapper
    return decorator

# ------------------------------------------------------------------
# 2. INFO class to gather system and memory information
# ------------------------------------------------------------------
class INFO:
    """
    Class to collect and display full system information, including virtual memory and swap.
    """
    def __init__(self):
        self.system_info = platform.uname()
        self.virtual_memory = psutil.virtual_memory()
        self.swap_memory = psutil.swap_memory()

    def get_system_info(self):
        """
        Return basic system information.
        """
        return {
            "System": self.system_info.system,
            "Node Name": self.system_info.node,
            "Release": self.system_info.release,
            "Version": self.system_info.version,
            "Machine": self.system_info.machine,
            "Processor": self.system_info.processor
        }

    def get_virtual_memory_info(self):
        """
        Return virtual memory details.
        """
        return {
            "Total": self.virtual_memory.total,
            "Available": self.virtual_memory.available,
            "Percent": self.virtual_memory.percent,
            "Used": self.virtual_memory.used,
            "Free": self.virtual_memory.free,
        }

    def get_swap_memory_info(self):
        """
        Return swap memory details.
        """
        return {
            "Total": self.swap_memory.total,
            "Used": self.swap_memory.used,
            "Free": self.swap_memory.free,
            "Percent": self.swap_memory.percent,
            "Sin": getattr(self.swap_memory, 'sin', None),
            "Sout": getattr(self.swap_memory, 'sout', None)
        }

    def display_info(self):
        """
        Display all collected information as a formatted string.
        """
        info_str = "System Information:\n"
        for key, value in self.get_system_info().items():
            info_str += f"{key}: {value}\n"
        info_str += "\nVirtual Memory Information:\n"
        for key, value in self.get_virtual_memory_info().items():
            if key in ["Total", "Available", "Used", "Free"]:
                value = f"{value / (1024**3):.2f} GB"
            info_str += f"{key}: {value}\n"
        info_str += "\nSwap Memory Information:\n"
        for key, value in self.get_swap_memory_info().items():
            if key in ["Total", "Used", "Free"] and value is not None:
                value = f"{value / (1024**3):.2f} GB"
            info_str += f"{key}: {value}\n"
        return info_str

# ------------------------------------------------------------------
# 3. Plugin system for extending functionalities
# ------------------------------------------------------------------
class MemoryPlugin:
    """
    Base class for plugins to extend the library's functionality.
    """
    def on_experience_stored(self, experience):
        logging.debug("MemoryPlugin on_experience_stored: default implementation")

    def on_sample(self, batch):
        logging.debug("MemoryPlugin on_sample: default implementation")

class PluginManager:
    """
    Manager to register and notify plugins.
    """
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin: MemoryPlugin):
        self.plugins.append(plugin)
        logging.debug("Registered plugin: %s", plugin.__class__.__name__)

    def notify_experience_stored(self, experience):
        for plugin in self.plugins:
            plugin.on_experience_stored(experience)
            logging.debug("Plugin %s notified of stored experience.", plugin.__class__.__name__)

    def notify_sample(self, batch):
        for plugin in self.plugins:
            plugin.on_sample(batch)
            logging.debug("Plugin %s notified of sample batch.", plugin.__class__.__name__)

# ------------------------------------------------------------------
# 4. Uniform Experience Replay Buffer
# ------------------------------------------------------------------
class ExperienceReplay:
    """
    Experience Replay buffer for storing and sampling experiences uniformly.
    """
    def __init__(self, capacity: int = 10000, plugin_manager: PluginManager = None):
        self.capacity = capacity
        self.buffer = []
        self.position = 0
        self.plugin_manager = plugin_manager

    def store(self, state, action, reward, next_state, done):
        """
        Store an experience as a tuple.
        """
        experience = (state, action, reward, next_state, done)
        if len(self.buffer) < self.capacity:
            self.buffer.append(experience)
        else:
            self.buffer[self.position] = experience
        self.position = (self.position + 1) % self.capacity
        logging.debug("Stored experience at position %d", self.position)
        if self.plugin_manager:
            self.plugin_manager.notify_experience_stored(experience)

    def sample(self, batch_size: int):
        """
        Randomly sample a batch of experiences.
        """
        if len(self.buffer) < batch_size:
            raise ValueError("Not enough experiences in buffer to sample the requested batch size.")
        batch = random.sample(self.buffer, batch_size)
        if self.plugin_manager:
            self.plugin_manager.notify_sample(batch)
        logging.debug("Sampled a batch of size %d", batch_size)
        return batch

    def __len__(self):
        return len(self.buffer)

# ------------------------------------------------------------------
# 5. SumTree data structure for prioritized sampling
# ------------------------------------------------------------------
class SumTree:
    """
    SumTree data structure for efficient prioritized sampling.
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1, dtype=np.float32)
        self.data = np.empty(capacity, dtype=object)
        self.data_pointer = 0

    def add(self, priority: float, data):
        """
        Add data with a given priority.
        """
        idx = self.data_pointer + self.capacity - 1
        self.data[self.data_pointer] = data
        self.update(idx, priority)
        self.data_pointer = (self.data_pointer + 1) % self.capacity

    def update(self, idx: int, priority: float):
        """
        Update the priority of a node and propagate the change.
        """
        change = priority - self.tree[idx]
        self.tree[idx] = priority
        while idx != 0:
            idx = (idx - 1) // 2
            self.tree[idx] += change

    def get_leaf(self, v: float):
        """
        Retrieve a leaf node given a value v in the range [0, total_priority].
        """
        idx = 0
        while idx < self.capacity - 1:
            left = 2 * idx + 1
            right = left + 1
            if v <= self.tree[left]:
                idx = left
            else:
                v -= self.tree[left]
                idx = right
        data_idx = idx - self.capacity + 1
        return idx, self.tree[idx], self.data[data_idx]

    @property
    def total_priority(self) -> float:
        return self.tree[0]

# ------------------------------------------------------------------
# 6. Prioritized Experience Replay Buffer
# ------------------------------------------------------------------
class PrioritizedExperienceReplay:
    """
    Prioritized Experience Replay buffer for sampling experiences based on priority weights.
    """
    def __init__(self, capacity: int = 10000, alpha: float = 0.6, beta: float = 0.4,
                 beta_increment_per_sampling: float = 0.001, epsilon: float = 1e-6,
                 plugin_manager: PluginManager = None):
        self.tree = SumTree(capacity)
        self.capacity = capacity
        self.alpha = alpha
        self.beta = beta
        self.beta_increment_per_sampling = beta_increment_per_sampling
        self.epsilon = epsilon
        self.max_priority = 1.0
        self.plugin_manager = plugin_manager

    def store(self, state, action, reward, next_state, done):
        """
        Store an experience with an initial maximum priority.
        """
        data = (state, action, reward, next_state, done)
        priority = self.max_priority ** self.alpha
        self.tree.add(priority, data)
        logging.debug("Stored prioritized experience with priority %f", priority)
        if self.plugin_manager:
            self.plugin_manager.notify_experience_stored(data)

    def sample(self, batch_size: int):
        """
        Sample a batch of experiences based on their priorities.
        Returns indices, experiences, and importance sampling weights.
        """
        if len(self.tree.data) < batch_size:
            raise ValueError("Not enough experiences in buffer to sample the requested batch size.")
        batch = []
        idxs = []
        priorities = []
        segment = self.tree.total_priority / batch_size

        for i in range(batch_size):
            a = segment * i
            b = segment * (i + 1)
            s = random.uniform(a, b)
            idx, priority, data = self.tree.get_leaf(s)
            batch.append(data)
            priorities.append(priority)
            idxs.append(idx)

        sampling_probabilities = np.array(priorities) / self.tree.total_priority
        self.beta = min(1.0, self.beta + self.beta_increment_per_sampling)
        weights = np.power(self.capacity * sampling_probabilities, -self.beta)
        weights /= weights.max()  # Normalize for stability
        if self.plugin_manager:
            self.plugin_manager.notify_sample(batch)
        logging.debug("Sampled prioritized batch of size %d", batch_size)
        return idxs, batch, weights

    def update(self, idxs, errors):
        """
        Update the priorities of sampled experiences based on their errors.
        """
        for idx, error in zip(idxs, errors):
            priority = (abs(error) + self.epsilon) ** self.alpha
            self.tree.update(idx, priority)
            self.max_priority = max(self.max_priority, priority)
            logging.debug("Updated priority at index %d to %f", idx, priority)

    def __len__(self):
        return len([d for d in self.tree.data if d is not None])

# ------------------------------------------------------------------
# 7. Memory monitoring and dashboard tools
# ------------------------------------------------------------------
def monitor_memory_usage(interval: float = 1.0):
    """
    Periodically display system memory usage.
    """
    try:
        while True:
            mem = psutil.virtual_memory()
            logging.info("[Memory Monitor] Memory Usage: %.2f%% of %.2f GB",
                         mem.percent, psutil.virtual_memory().total / (1024**3))
            time.sleep(interval)
    except KeyboardInterrupt:
        logging.info("Memory monitoring stopped.")

def run_dashboard(replay_buffer, update_interval: float = 1.0):
    """
    Launch a simple dashboard using Streamlit to display the status of the experience buffer.
    To run the dashboard, install streamlit and execute:
      streamlit run memory.py
    """
    try:
        import streamlit as st
    except ImportError:
        raise ImportError("Streamlit is required for the dashboard. Install it via: pip install streamlit")
    st.title("Memory Dashboard")
    buffer_length = len(replay_buffer) if hasattr(replay_buffer, '__len__') else "Unknown"
    st.write(f"Number of stored experiences: {buffer_length}")
    if st.button("Refresh"):
        st.experimental_rerun()
    st.write("Add more charts/visualizations as needed.")

# ------------------------------------------------------------------
# 8. Demo and complete testing of the library
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Test the INFO class
    logging.info("==== Testing INFO Class ====")
    info = INFO()
    logging.info("\n%s", info.display_info())

    # Define a sample plugin for logging operations
    class LoggerPlugin(MemoryPlugin):
        def on_experience_stored(self, experience):
            logging.info("LoggerPlugin: Experience stored: %s", experience)
        def on_sample(self, batch):
            logging.info("LoggerPlugin: Sampled a batch of %d experiences.", len(batch))

    plugin_manager = PluginManager()
    logger_plugin = LoggerPlugin()
    plugin_manager.register_plugin(logger_plugin)

    # Test uniform ExperienceReplay buffer
    logging.info("==== Testing Uniform ExperienceReplay ====")
    replay_buffer = ExperienceReplay(capacity=1000, plugin_manager=plugin_manager)
    for i in range(50):
        state = np.random.randn(4)
        action = random.choice([0, 1])
        reward = random.random()
        next_state = np.random.randn(4)
        done = random.choice([True, False])
        replay_buffer.store(state, action, reward, next_state, done)
    try:
        sample_batch = replay_buffer.sample(5)
        logging.info("Uniform sample batch: %s", sample_batch)
    except ValueError as e:
        logging.error("Error sampling from uniform buffer: %s", e)

    # Test PrioritizedExperienceReplay buffer
    logging.info("==== Testing PrioritizedExperienceReplay ====")
    prioritized_buffer = PrioritizedExperienceReplay(capacity=1000, plugin_manager=plugin_manager)
    for i in range(50):
        state = np.random.randn(4)
        action = random.choice([0, 1])
        reward = random.random()
        next_state = np.random.randn(4)
        done = random.choice([True, False])
        prioritized_buffer.store(state, action, reward, next_state, done)
    try:
        idxs, batch, weights = prioritized_buffer.sample(5)
        logging.info("Prioritized sample batch: %s", batch)
        logging.info("Importance sampling weights: %s", weights)
    except ValueError as e:
        logging.error("Error sampling from prioritized buffer: %s", e)

    # Optionally, run memory monitoring in a separate thread:
    # monitor_thread = threading.Thread(target=monitor_memory_usage, args=(2,), daemon=True)
    # monitor_thread.start()

    # Optionally, run the dashboard (uncomment the following line to use Streamlit):
    # run_dashboard(replay_buffer)

    # Test the memoize decorator
    @memoize(ttl=5)
    def expensive_computation(x):
        logging.info("Performing expensive computation for x = %s", x)
        time.sleep(1)  # Simulate heavy computation
        return x * x

    logging.info("==== Testing memoize decorator ====")
    logging.info("Result: %s", expensive_computation(4))  # Computation performed
    logging.info("Result: %s", expensive_computation(4))  # Result fetched from cache
    time.sleep(6)
    logging.info("Result: %s", expensive_computation(4))  # TTL expired, computation performed again
