"""
Base module for SynPro models.
"""

import contextlib
import numpy as np
import torch

@contextlib.contextmanager
def set_random_states(random_state, set_model_random_state):
    """Context manager for managing the random state.

    Args:
        random_state (int or tuple):
            The random seed or a tuple of (numpy.random.RandomState, torch.Generator).
        set_model_random_state (function):
            Function to set the random state on the model.
    """
    original_np_state = np.random.get_state()
    original_torch_state = torch.get_rng_state()

    random_np_state, random_torch_state = random_state

    np.random.set_state(random_np_state.get_state())
    torch.set_rng_state(random_torch_state.get_state())

    try:
        yield
    finally:
        current_np_state = np.random.RandomState()
        current_np_state.set_state(np.random.get_state())
        current_torch_state = torch.Generator()
        current_torch_state.set_state(torch.get_rng_state())
        set_model_random_state((current_np_state, current_torch_state))

        np.random.set_state(original_np_state)
        torch.set_rng_state(original_torch_state)


def random_state(function):
    """Set the random state before calling the function.

    This decorator uses the random_states saved in the synthesizer
    (numpy + torch) so that calls to .fit() or .sample() become reproducible.
    """
    def wrapper(self, *args, **kwargs):
        if self.random_states is None:
            return function(self, *args, **kwargs)
        else:
            with set_random_states(self.random_states, self.set_random_state):
                return function(self, *args, **kwargs)
    return wrapper


class BaseSynthesizer:
    """
    Base class for all Synthesizers in the SynPro package.
    """

    random_states = None

    def __getstate__(self):
        """Improve pickling state for the synthesizer.

        Convert to CPU device before pickling to allow
        loading the model in different environments.
        """
        device_backup = self._device
        self.set_device(torch.device('cpu'))
        state = self.__dict__.copy()
        self.set_device(device_backup)

        # store random states if present
        if (
            isinstance(self.random_states, tuple)
            and hasattr(self.random_states[0], "get_state")
            and isinstance(self.random_states[1], torch.Generator)
        ):
            state['_numpy_random_state'] = self.random_states[0].get_state()
            state['_torch_random_state'] = self.random_states[1].get_state()
            state.pop('random_states', None)

        return state

    def __setstate__(self, state):
        """Restore the state of a synthesizer."""
        if '_numpy_random_state' in state and '_torch_random_state' in state:
            np_state = state.pop('_numpy_random_state')
            torch_state = state.pop('_torch_random_state')

            current_torch_state = torch.Generator()
            current_torch_state.set_state(torch_state)

            current_numpy_state = np.random.RandomState()
            current_numpy_state.set_state(np_state)
            state['random_states'] = (current_numpy_state, current_torch_state)

        self.__dict__ = state
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.set_device(device)

    def save(self, path):
        """Save the model to the given `path`."""
        device_backup = self._device
        self.set_device(torch.device('cpu'))
        torch.save(self, path)
        self.set_device(device_backup)

    @classmethod
    def load(cls, path):
        """Load the model from the given `path`."""
        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        model = torch.load(path, weights_only=False)
        model.set_device(device)
        return model

    def set_random_state(self, random_state):
        """Set the random state."""
        if random_state is None:
            self.random_states = None
        elif isinstance(random_state, int):
            self.random_states = (
                np.random.RandomState(seed=random_state),
                torch.Generator().manual_seed(random_state)
            )
        elif (
            isinstance(random_state, tuple)
            and hasattr(random_state[0], "get_state")
            and isinstance(random_state[1], torch.Generator)
        ):
            self.random_states = random_state
        else:
            raise TypeError(
                f"`random_state` {random_state} expected to be an int or a tuple "
                "(`np.random.RandomState`, `torch.Generator`)"
            )

    def set_device(self, device):
        """Subclass can override to move the model to the specified device."""
        self._device = device