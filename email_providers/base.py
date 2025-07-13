from abc import ABC, abstractmethod

class BaseEmailProvider(ABC):
    @abstractmethod
    def send_email(self, subject: str, to_email: str, from_email: str,
                   plain_text: str, html_content: str) -> bool:
        pass
