# split_config.py
from enum import Enum
import os
import sys
from splitio import get_factory
from splitio.exceptions import TimeoutException
import importlib

# For now this is the best way forward
# in the future we'll just remove legacy stuff and move everything here
from .frog_activity_old import activity_signal as legacy_activity_signal
from .frog_notifications import activity_signal as notification_activity_signal


class ActivityStatus(Enum):
    """
    Model activity statuses.
    PENDING -> STARTED -> Terminal(COMPLETED or FAILED)
    """

    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


config = {"impressionsMode": "none"}
splitio_key = os.getenv("SPLITIO_SDK_KEY", "NO_KEY_FOUND")

# Override split with environment variable
# value should be either "old" or "new" otherwise
# defaults back to split logic
DEV_OVERRIDE = os.getenv("DEV_OVERRIDE_SPLIT", "default")

factory = None
split = None

if splitio_key != "NO_KEY_FOUND":
    factory = get_factory(splitio_key, config=config)
    try:
        factory.block_until_ready(5)
    except TimeoutException:
        sys.exit()

    split = factory.client()


class ModelActivity:
    def __new__(cls, *args, **kwargs):
        # Try to get logger and correlation_id from args
        # default to None if something goes wrong
        try:
            logger = args[0]
            correlation_id = args[1]
            logger.debug(
                "ModelActivity logger initialized, correlation_id: " + correlation_id
            )
        except:
            logger = None
            correlation_id = None

        # Check the DEV_OVERRIDE value to determine the module
        if DEV_OVERRIDE == "old":
            module_name = "cosmicfrog.frog_activity_old"
        elif DEV_OVERRIDE == "new":
            module_name = "cosmicfrog.frog_notifications"
        else:
            # Default behavior based on Split.io
            try:
                assert split is not None
                account = args[-1]
                split_value = split.get_treatment(
                    account.get("email"), "PlatformNotificationsService"
                )
                if logger is not None and correlation_id is not None:
                    logger.info(
                        f"Split value: {split_value}, correlation_id: {correlation_id}"
                    )
                # Determine which module to import
                if split_value == "on":
                    module_name = "cosmicfrog.frog_notifications"
                else:
                    module_name = "cosmicfrog.frog_activity_old"
            except:
                if logger is not None and correlation_id is not None:
                    logger.info(
                        f"Split failed, defaulting to old module, correlation_id: {correlation_id}"
                    )
                module_name = "cosmicfrog.frog_activity_old"

        # Dynamically import the module
        module = importlib.import_module(module_name)
        actual_class = getattr(module, "ModelActivity")
        instance = actual_class(*args, **kwargs)

        return instance


class AsyncFrogActivityHandler:
    def __new__(cls, *args, **kwargs):
        # Try to get logger and correlation_id from args
        # default to None if something goes wrong
        try:
            logger = args[0]
            correlation_id = args[1]
            logger.debug(
                "AsyncFrogActivityHandler logger initialized, correlation_id: "
                + correlation_id
            )
        except:
            logger = None
            correlation_id = None

        # Check the DEV_OVERRIDE value to determine the module
        if DEV_OVERRIDE == "old":
            module_name = "cosmicfrog.frog_activity_old"
        elif DEV_OVERRIDE == "new":
            module_name = "cosmicfrog.frog_notifications"
        else:
            # Default behavior based on Split.io
            try:
                assert split is not None
                account = args[-1]
                split_value = split.get_treatment(
                    account.get("email"), "PlatformNotificationsService"
                )
                if logger is not None and correlation_id is not None:
                    logger.info(
                        f"Split value: {split_value}, correlation_id: {correlation_id}"
                    )
                # Determine which module to import
                if split_value == "on":
                    module_name = "cosmicfrog.frog_notifications"
                else:
                    module_name = "cosmicfrog.frog_activity_old"
            except:
                if logger is not None and correlation_id is not None:
                    logger.info(
                        f"Split failed, defaulting to old module, correlation_id: {correlation_id}"
                    )
                module_name = "cosmicfrog.frog_activity_old"

        # Dynamically import the module
        module = importlib.import_module(module_name)
        actual_class = getattr(module, "AsyncFrogActivityHandler")
        instance = actual_class(*args, **kwargs)

        return instance


# TODO - after migration away from legacy stuff some things need to be refactored
#        currently the message being sent is a string and not a dict bercause of old API
#        but in the new API we can send fully fledged JSON meaning we can get the dict
#        and send it in one go without json.dumps logic across the services and moreover
#        brittle string parsing to JSON is not a good idea
def activity_signal(logger, message, **kwargs):
    correlation_id = kwargs.get("correlation_id")

    # Check the DEV_OVERRIDE value to determine which signal to use
    if DEV_OVERRIDE == "old":
        logger.debug("DEV_OVERRIDE set to 'old', using legacy_activity_signal")
        return legacy_activity_signal(logger, message, **kwargs)
    elif DEV_OVERRIDE == "new":
        logger.debug("DEV_OVERRIDE set to 'new', using notification_activity_signal")
        return notification_activity_signal(logger, message, **kwargs)

    # Default behavior based on Split.io
    try:
        # throw as soon as possible if split didn't succeed
        assert split != None
        logger.debug("Split module found (or instantiated)")
        email = kwargs.get("email")
        split_value = split.get_treatment(email, "PlatformNotificationsService")
        if split_value == "on":
            logger.debug("Split treatment is on")
            return notification_activity_signal(logger, message, **kwargs)
        else:
            logger.debug("Split treatment is off")
            return legacy_activity_signal(logger, message, **kwargs)
    except:
        logger.debug(
            "Split failed, defaulting to old module, correlation_id: " + correlation_id
        )
        return legacy_activity_signal(logger, message, **kwargs)
