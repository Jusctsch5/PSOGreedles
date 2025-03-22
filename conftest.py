import logging

def pytest_configure(config):
    """Configure logging format and level for test runs"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logging.info("Pytest logging configured")  # Example log message

