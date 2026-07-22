"""
Authentication Manager

Responsible for:
1. Password Verification
2. Failed Attempt Tracking
3. Resetting Attempts
"""

from config import MAX_FAILED_ATTEMPTS
from logger import PolicyLogger


class AuthManager:

    def __init__(self, password="admin123"):
        self.correct_password = password
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
            f"({self.failed_attempts}/{MAX_FAILED_ATTEMPTS})"
        )

        return False

    def attempts_remaining(self):
        """
        Returns remaining authentication attempts.
        """

        return MAX_FAILED_ATTEMPTS - self.failed_attempts

    def limit_reached(self):
        """
        Returns True if failure limit reached.
        """

        return self.failed_attempts >= MAX_FAILED_ATTEMPTS

    def reset(self):
        """
        Reset failed attempts.
        """

        self.failed_attempts = 0

        PolicyLogger.info("Authentication Counter Reset")

if __name__ == "__main__":

    auth = AuthManager()

    print(auth.authenticate("abc"))
    print(auth.authenticate("xyz"))
    print(auth.authenticate("hello"))

    print("Attempts Remaining:", auth.attempts_remaining())

    print("Limit Reached:", auth.limit_reached())

    print(auth.authenticate("admin123"))