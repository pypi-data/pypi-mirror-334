import threading
import queue
import time
from typing import Callable, Optional
from StatusMessage import StatusMessage

class StatusUpdater:
	"""Handles concurrent message updates using a queue and a user-defined callable."""
	def __init__(self, on_message: Callable[[str], None]):
		"""
		:param on_message: A callable that processes messages.
		"""
		self.message_queue = queue.Queue()
		self.on_message = on_message  # User-defined callable for processing messages
		self.running = threading.Event()
		self.running.set()
		self.active_message: Optional[StatusMessage] = None  # Track the current active message
		self.lock = threading.Lock()  # Ensure thread safety

		self.consumer_thread = threading.Thread(target=self._consume_messages, daemon=True)
		self.consumer_thread.start()

	def add_message(self, message: str) -> StatusMessage:
		"""Creates and queues a new message."""
		msg = StatusMessage(message)
		self.message_queue.put(msg)
		return msg  # Return reference for potential stale marking

	def _consume_messages(self):
		"""Continuously processes messages from the queue."""
		while self.running.is_set():
			with self.lock:
				if not self.active_message or self.active_message.finished or self.active_message.stale:
					try:
						# Fetch the next message
						self.active_message = self.message_queue.get_nowait()

						if not self.active_message.stale and not self.active_message.finished:
							self.on_message(self.active_message.message)  # Call user-defined function
					except queue.Empty:
						self.on_message("Ready")  # Indicate that the queue is waiting for messages
						time.sleep(1)  # Avoid excessive CPU usage
			time.sleep(0.1)  # Avoid busy-waiting

	def stop(self):
		"""Stops the consumer thread."""
		self.running.clear()
		self.consumer_thread.join()

# Example usage
if __name__ == "__main__":
    # Example user-defined function for handling messages
	def handle_message(message: str):
		print(message)
    
	updater = StatusUpdater(handle_message)

	msg1 = updater.add_message("First update")
	msg2 = updater.add_message("Second update")
	msg3 = updater.add_message("Third update")
    
	time.sleep(1)  # Simulate delay

	msg1.mark_finished_safely(updater)  # Marks first message as finished
	time.sleep(1)  # Allow processing

	msg2.mark_finished_safely(updater)  # Marks second message as finished
	time.sleep(1)  # Allow processing

	msg3.mark_finished_safely(updater)  # Marks third message as finished
	time.sleep(1)  # Allow processing

updater.stop()