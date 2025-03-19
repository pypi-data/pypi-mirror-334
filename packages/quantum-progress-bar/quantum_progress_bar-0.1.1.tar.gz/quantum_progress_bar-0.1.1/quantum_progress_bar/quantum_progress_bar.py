import random
import time
import math
import sys
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Tuple, TypeVar, Union, cast, Generic

T = TypeVar('T')

class QuantumProgressBar(Generic[T]):
    """
    A progress bar that behaves according to quantum mechanics principles.
    The progress changes randomly when observed, and the estimated completion time
    has a high degree of uncertainty.
    
    This class can be used in multiple ways:
    
    1. As a standard progress bar:
       ```
       pb = QuantumProgressBar(total_steps=100)
       pb.quantum_progress()
       pb.update(10)
       ```
       
    2. As an iterator (tqdm-like):
       ```
       for item in QuantumProgressBar(range(100)):
           process(item)
       ```
       
    3. With a context manager:
       ```
       with QuantumProgressBar(total_steps=100) as pb:
           for i in range(100):
               process(i)
               pb.update()
       ```
    """
    def __init__(self, iterable: Optional[Iterable[T]] = None, total_steps=100, collapse_factor=0.2, uncertainty_level=0.8):
        """
        Initialize a quantum progress bar.
        
        Args:
            iterable (Optional[Iterable]): Optional iterable to wrap with the progress bar
            total_steps (int): Total number of steps to complete
            collapse_factor (float): How much the observation affects the state (0.0-1.0)
            uncertainty_level (float): Level of uncertainty in time estimates (0.0-1.0)
        """
        self.iterable = iterable
        
        # If iterable is provided and has a known length, use it for total_steps
        if iterable is not None:
            try:
                self.total_steps = len(iterable)  # type: ignore
            except (TypeError, AttributeError):
                # Iterable doesn't have a length, use the provided total_steps
                self.total_steps = total_steps
        else:
            self.total_steps = total_steps
            
        self.current_state = random.randint(0, self.total_steps // 3)  # Start with some progress
        self.collapse_factor = collapse_factor
        self.uncertainty_level = uncertainty_level
        self.start_time = datetime.now()
        self.observed_states = []
        self.entangled_state = None
        self.width = 50  # Default width for progress bar

    def _collapse_wavefunction(self):
        """
        Collapse the quantum state when observed, potentially changing the progress.
        """
        # Record the current state before collapsing
        self.observed_states.append(self.current_state)
        
        # Determine if progress goes forward or backward based on previous observations
        if len(self.observed_states) > 2:
            recent_trend = self.observed_states[-1] - self.observed_states[-2]
            # Probability of continuing in same direction is higher
            direction = 1 if random.random() < (0.5 + 0.1 * (1 if recent_trend > 0 else -1)) else -1
        else:
            direction = 1 if random.random() < 0.7 else -1  # Usually progress forward
        
        # Calculate the amount of change
        max_change = int(self.total_steps * self.collapse_factor)
        change = random.randint(0, max_change) * direction
        
        # Apply the change with constraints
        new_state = self.current_state + change
        self.current_state = max(0, min(self.total_steps, new_state))

    def quantum_progress(self, width=50, quantum_bars=True):
        """
        Display the current progress as a progress bar with quantum behavior.
        
        Args:
            width (int): Width of the progress bar
            quantum_bars (bool): Whether to use quantum-style bars that change
            
        Returns:
            int: Current progress percentage
        """
        self._collapse_wavefunction()
        
        progress_percent = int(100 * self.current_state / self.total_steps)
        
        # Create a progress bar with quantum-style characters
        if quantum_bars:
            bar_chars = ['▓', '▒', '░', '█', '▓', '▄', '▌']
            filled_length = int(width * self.current_state // self.total_steps)
            bar = ''
            for i in range(width):
                if i < filled_length:
                    bar += random.choice(bar_chars)
                else:
                    # Occasionally show quantum fluctuations in empty space
                    bar += random.choice(['░', ' ', ' ', ' ', ' ']) if random.random() < 0.1 else ' '
        else:
            # Traditional style bar
            filled_length = int(width * self.current_state // self.total_steps)
            bar = '█' * filled_length + ' ' * (width - filled_length)
            
        # Create a quantum noise in percentage display
        display_percent = progress_percent
        if random.random() < 0.2:  # Occasionally show quantum fluctuation in percentage
            noise = random.randint(-5, 5)
            display_percent = max(0, min(100, progress_percent + noise))
            
        sys.stdout.write(f'\r[{bar}] {display_percent}% ')
        sys.stdout.flush()
        
        return progress_percent

    def uncertainty_estimate(self):
        """
        Provide an uncertain estimate of remaining time to completion.
        
        Returns:
            str: A time estimate with uncertainty
        """
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        if not self.observed_states or self.current_state <= 0:
            return "Unknown ± ∞"
            
        # Calculate rate based on observations with some randomness
        observed_progress = self.current_state - self.observed_states[0]
        if observed_progress <= 0:
            # If no progress or negative progress
            return "∞ ± ∞ (Heisenberg is uncertain)"
            
        seconds_per_step = elapsed / observed_progress
        
        # Add quantum uncertainty
        uncertainty_factor = random.uniform(1 - self.uncertainty_level, 1 + self.uncertainty_level * 3)
        adjusted_rate = seconds_per_step * uncertainty_factor
        
        # Calculate remaining time
        steps_remaining = self.total_steps - self.current_state
        estimated_seconds = steps_remaining * adjusted_rate
        
        # Calculate uncertainty range
        min_estimate = max(1, estimated_seconds * (1 - self.uncertainty_level))
        max_estimate = estimated_seconds * (1 + self.uncertainty_level * 2)
        
        # Format the times
        def format_time(seconds):
            if seconds < 60:
                return f"{int(seconds)} seconds"
            elif seconds < 3600:
                return f"{int(seconds / 60)} minutes"
            else:
                return f"{seconds / 3600:.1f} hours"
                
        if random.random() < 0.05:  # Occasional joke estimate
            joke_units = ["light years", "eons", "quantum cycles", "galactic rotations", "CPU cycles"]
            return f"{random.randint(1, 42)} {random.choice(joke_units)} ± uncertainty principle"
        
        main_estimate = format_time(estimated_seconds)
        range_estimate = f"{format_time(min_estimate)} - {format_time(max_estimate)}"
        
        return f"{main_estimate} (probably between {range_estimate})"

    def entangle(self, other_progress_bar):
        """
        Entangle this progress bar with another, so their states become correlated.
        
        Args:
            other_progress_bar (QuantumProgressBar): Another progress bar to entangle with
        """
        self.entangled_state = other_progress_bar
        other_progress_bar.entangled_state = self
        print("⚛️ Progress bars are now quantum entangled! ⚛️")

    def update(self, steps=1):
        """
        Update the progress by a specific number of steps.
        In quantum mechanics, this is like forcing a measurement outcome.
        
        Args:
            steps (int): Number of steps to progress
        """
        self.current_state = min(self.total_steps, self.current_state + steps)
        
        # If entangled, affect the other progress bar
        if self.entangled_state:
            # Entangled system moves in opposite direction with some probability
            if random.random() < 0.7:
                entangled_change = -steps if random.random() < 0.5 else steps
                self.entangled_state.current_state = max(0, min(
                    self.entangled_state.total_steps,
                    self.entangled_state.current_state + entangled_change
                ))
                
    def __iter__(self) -> Iterator[T]:
        """
        Iterate over the wrapped iterable, updating the progress bar with each iteration.
        
        Returns:
            Iterator: An iterator over the wrapped iterable
            
        Raises:
            TypeError: If no iterable was provided during initialization
        """
        if self.iterable is None:
            raise TypeError("QuantumProgressBar requires an iterable when used as an iterator")
            
        # Reset progress bar state
        self.current_state = 0
        self.start_time = datetime.now()
        self.observed_states = []
        
        # Iterate over the wrapped iterable
        for item in self.iterable:
            # Update progress and display
            self.update(1)
            self.quantum_progress(width=self.width)
            
            # Yield the item
            yield item
            
        # Ensure we end at 100%
        self.current_state = self.total_steps
        self.quantum_progress(width=self.width)
        print()  # Add a newline after the progress bar
        
    def __call__(self, iterable: Iterable[T]) -> 'QuantumProgressBar[T]':
        """
        Wrap an iterable with this progress bar.
        
        Args:
            iterable: The iterable to wrap
            
        Returns:
            QuantumProgressBar: A new progress bar wrapping the iterable
        """
        return QuantumProgressBar(
            iterable=iterable,
            total_steps=self.total_steps,
            collapse_factor=self.collapse_factor,
            uncertainty_level=self.uncertainty_level
        )
        
    def __enter__(self) -> 'QuantumProgressBar':
        """
        Enter the context manager.
        
        Returns:
            QuantumProgressBar: This progress bar instance
        """
        return self
        
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit the context manager.
        
        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised
        """
        # Ensure we end at 100% if no exception occurred
        if exc_type is None:
            self.current_state = self.total_steps
            self.quantum_progress(width=self.width)
            print()  # Add a newline after the progress bar


# Convenience functions
def quantum_progress(total=100, width=50, delay=0.1, iterations=None):
    """
    Display a quantum progress bar that advances randomly when observed.
    
    Args:
        total (int): Total steps for completion
        width (int): Width of the progress bar
        delay (float): Delay between updates in seconds
        iterations (int): Number of iterations, or None for automatic completion
        
    Returns:
        int: Final progress percentage
    """
    pb = QuantumProgressBar(total_steps=total)
    
    if iterations is None:
        # Automatic mode: continue until we reach (or get close to) 100%
        max_iterations = total * 3  # Safety limit to prevent infinite loops
        i = 0
        progress = 0
        
        while progress < 95 and i < max_iterations:
            progress = pb.quantum_progress(width=width)
            time.sleep(delay)
            i += 1
            
            # Sometimes make real progress
            if random.random() < 0.3:
                pb.update(random.randint(1, 3))
    else:
        # Fixed iterations mode
        for i in range(iterations):
            pb.quantum_progress(width=width)
            time.sleep(delay)
            
            # Sometimes make real progress
            if random.random() < 0.3:
                pb.update(random.randint(1, 3))
    
    # Ensure we end at 100%
    pb.current_state = pb.total_steps
    final_progress = pb.quantum_progress(width=width)
    print()  # Add a newline after the progress bar
    return final_progress

def uncertainty_estimate():
    """
    Generate an uncertain time estimate that's too vague to be useful.
    
    Returns:
        str: A deliberately vague time estimate
    """
    pb = QuantumProgressBar()
    return pb.uncertainty_estimate()

def qqdm(iterable: Optional[Iterable[T]] = None, **kwargs) -> QuantumProgressBar[T]:
    """
    Quantum tqdm - A tqdm-like wrapper for iterables with quantum behavior.
    
    This function provides a tqdm-like interface for the QuantumProgressBar class,
    allowing you to wrap iterables with a quantum progress bar.
    
    Examples:
        >>> # Wrap a range
        >>> for i in qqdm(range(100)):
        >>>     process(i)
        >>>
        >>> # Wrap a list comprehension
        >>> results = [process(i) for i in qqdm(range(100))]
        >>>
        >>> # Use with a context manager
        >>> with qqdm(total_steps=100) as qbar:
        >>>     for i in range(100):
        >>>         process(i)
        >>>         qbar.update(1)
    
    Args:
        iterable: Optional iterable to wrap with the progress bar
        **kwargs: Additional keyword arguments to pass to QuantumProgressBar
        
    Returns:
        QuantumProgressBar: A progress bar instance
    """
    return QuantumProgressBar(iterable=iterable, **kwargs)

def quantum_loading(message="Loading quantum state", duration=5, width=50):
    """
    Display a quantum-style loading animation.
    
    Args:
        message (str): Message to display
        duration (float): Duration in seconds
        width (int): Width of the loading animation
    """
    start_time = time.time()
    iterations = 0
    
    while time.time() - start_time < duration:
        # Create a quantum-inspired loading animation
        bar_position = iterations % width
        uncertainty = random.randint(0, min(5, width // 10))
        
        bar = [' '] * width
        for i in range(bar_position - uncertainty, bar_position + uncertainty + 1):
            if 0 <= i < width:
                prob = 1 - abs(i - bar_position) / (uncertainty + 1) if uncertainty > 0 else 1
                if random.random() < prob:
                    bar[i] = random.choice(['▓', '▒', '░', '█', '▄', '▌'])
        
        sys.stdout.write(f'\r{message} [{"".join(bar)}]')
        sys.stdout.flush()
        
        time.sleep(0.1)
        iterations += 1
    
    sys.stdout.write('\r' + ' ' * (len(message) + width + 3) + '\r')
    sys.stdout.flush()


# Example usage
if __name__ == "__main__":
    print("🔬 Welcome to the Quantum Progress Bar 🔬")
    print("Where progress is uncertain until observed!")
    print("-" * 50)
    
    # Demonstrate quantum loading
    quantum_loading("Initializing quantum state", duration=3)
    
    print("Starting a task with quantum uncertainty...")
    print(f"Estimated time: {uncertainty_estimate()}")
    
    # Run a quantum progress bar
    quantum_progress(total=100, width=50, delay=0.2)
    
    print("Task completed with quantum efficiency!")
    print(f"Final time estimate: {uncertainty_estimate()}")
    print("-" * 50)
    
    # Demonstrate entanglement
    print("Demonstrating quantum entanglement between two progress bars:")
    pb1 = QuantumProgressBar(total_steps=50)
    pb2 = QuantumProgressBar(total_steps=50)
    pb1.entangle(pb2)
    
    for i in range(10):
        print(f"\nObservation {i+1}:")
        print("Progress Bar 1:", end=" ")
        pb1.quantum_progress(width=30)
        print("\nProgress Bar 2:", end=" ")
        pb2.quantum_progress(width=30)
        time.sleep(0.5)
    
    print("\n\nThanks for experiencing quantum computing without the expensive hardware!")
