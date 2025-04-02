import pygame

class Timer:
    def __init__(self, duration):
        """
        Initialize the timer.

        :param duration: Timer duration in milliseconds.
        """
        self.duration = duration
        self.start_time = None
        self.running = False
        self.loop = False

    def restart(self):
        self.stop()
        self.start()

    def start(self, loop=False):
        """
        Start the timer.

        :param loop: If True, the timer will restart automatically when it expires.
        """
        self.start_time = pygame.time.get_ticks()
        self.running = True
        self.loop = loop

    def stop(self):
        """Stop the timer."""
        self.start_time = None
        self.running = False
        self.loop = False

    def is_running(self):
        """
        Check if the timer is running.

        :return: True if the timer is running, otherwise False.
        """
        return self.running

    def has_expired(self):
        """
        Check if the timer has expired.

        :return: True if the timer has expired, otherwise False.
        """
        if not self.running:
            return False

        elapsed_time = pygame.time.get_ticks() - self.start_time
        if elapsed_time >= self.duration:
            if self.loop:
                self.start_time = pygame.time.get_ticks()  # Restart the timer
            else:
                self.stop()
            return True
        return False