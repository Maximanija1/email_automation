from logger_setup import setup_logger

# Create the logger
logger = setup_logger()

# Test different log levels
print("***TESTING LOGGER***")

logger.debug("Debug")
logger.info("Info")
logger.warning("Warning")
logger.error("Error")
logger.critical("Critical")

print("Logger test complete")