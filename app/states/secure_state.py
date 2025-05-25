import reflex as rx
from typing import Dict


class SecureState(rx.State):
    counter: int = 0
    _secret_token: str = "don't leak me"

    def to_json(self) -> Dict:
        """
        Only serialize attributes that don't start with "_".
        Reflex will use this to send state -> client.
        """
        base = super().to_json()
        return {
            k: v
            for k, v in base.items()
            if not k.startswith("_")
        }

    @classmethod
    def apply_patch(cls, state, patch: Dict):
        """
        Intercept any client -> server patch.
        Strip out any private keys before applying.
        """
        safe_patch = {
            k: v
            for k, v in patch.items()
            if not k.startswith("_")
        }
        return super().apply_patch(state, safe_patch)

    @rx.event
    def increment_secure_counter(self):
        self.counter += 1