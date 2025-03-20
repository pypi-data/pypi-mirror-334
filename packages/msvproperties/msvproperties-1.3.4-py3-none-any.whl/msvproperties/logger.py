import logging


class ProcessLogger:
    def __init__(self, log_file):
        if log_file:
            self.logger = logging.getLogger("ProcessLogger")
            self.logger.setLevel(logging.ERROR)

            if not self.logger.handlers:
                formatter = logging.Formatter(
                    "%(asctime)s | Address: %(address)s | Cause: %(cause)s | Source: %(source)s | Is Auction: %(is_auction)s | User: %(user)s"
                )
                file_handler = logging.FileHandler(log_file + "/process.log")
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)

    def log_failure(self, address, cause, source_name, is_auction, user):
        extra = {
            "address": address,
            "cause": cause,
            "source": source_name,
            "is_auction": is_auction,
            "user": user,
        }
        self.logger.error("Processing failure logged.", extra=extra)
