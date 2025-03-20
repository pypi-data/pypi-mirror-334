import uuid

class StatusMessage:
    """Represents a status message."""
    def __init__(self, message: str):
        self.id = uuid.uuid4()  # Unique ID
        self.message = message
        self.stale = False  # Initially set to False
        self.finished = False  # Must be explicitly set

    def mark_stale(self):
        """Mark message as stale."""
        self.stale = True

    def mark_finished_safely(self, status_updater):
        """Mark message as finished only if it's the topmost in the queue, otherwise mark stale."""
        with status_updater.lock:
            if status_updater.active_message == self:
                self.finished = True  # Set finished if this is the active message
            else:
                self.stale = True  # Otherwise, mark as stale