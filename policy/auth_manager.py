"""
Authentication Manager

Responsible for:
1. Password Verification
2. Failed Attempt Tracking
3. Resetting Attempts
"""

from config import DEFAULT_PASSWORD, MAX_FAILED_ATTEMPTS
from logger import PolicyLogger


class AuthManager:

    def __init__(
        self,
        password=DEFAULT_PASSWORD,
        max_attempts=MAX_FAILED_ATTEMPTS
    ):
        self.correct_password = password
        self.max_attempts = max_attempts
        self.failed_attempts = 0

    def authenticate(self, entered_password):
        """
        Returns True if authentication succeeds.
        Otherwise increments failed attempts.
        """

        if entered_password == self.correct_password:

            PolicyLogger.info("Authentication Successful")

            self.failed_attempts = 0

            return True

        self.failed_attempts += 1

        PolicyLogger.warning(
            f"Authentication Failed "
            f"({self.failed_attempts}/{self.max_attempts})"
        )

        return False

    def attempts_remaining(self):
        """
        Returns remaining authentication attempts.
        """

        return self.max_attempts - self.failed_attempts

    def limit_reached(self):
        """
        Returns True if failure limit reached.
        """

        return self.failed_attempts >= self.max_attempts

    def reset(self):
        """
        Reset failed attempts.
        """

        self.failed_attempts = 0

        PolicyLogger.info("Authentication Counter Reset")


