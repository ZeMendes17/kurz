import logging
import colorlog

TRACE_LEVEL = 15
logging.addLevelName(TRACE_LEVEL, "TRACE")

def trace(self, message, *args, **kwargs):
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kwargs)

logging.Logger.trace = trace  # Add TRACE method to logger class

logger = logging.getLogger("kurz_vid")
logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Define log format
# Define color formatter (Only coloring the level name)
formatter = colorlog.ColoredFormatter(
    "%(asctime)s - %(log_color)s%(levelname)-8s%(reset)s - %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    },
    reset=True,
    style="%",
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

def separator():
    logger.trace("-" * 60)

def log_section(title):
    separator()
    logger.trace(f"{title.center(60)}")
    separator()

def log_subsection(title):
    """Creates a subsection with smaller dashes."""
    line = f"-- {title} --".center(60, "-")  # Format: ---- TITLE ----
    logger.trace(line)

