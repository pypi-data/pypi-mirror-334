"""
    Helper for implementing model activity updates
"""

import os
import traceback
from typing import Optional
from logging import Logger
from time import sleep
from enum import Enum
import asyncio
from httpx import AsyncClient, Client, HTTPStatusError, RequestError, TimeoutException
from .sync_wrapper import sync_wrapper

CF_ACTIVITY_URL = os.getenv("CF_ACTIVITY_URL") or "https://white-bullfrog-c368f0-barking.azurewebsites.net/cosmicfrog/v0.2"

CFLIB_HTTPX_ACTIVITY_TIMEOUT = (
    os.getenv("CFLIB_HTTPX_ACTIVITY_TIMEOUT") or 30
)  # Connection timeout in seconds
CFLIB_HTTPX_RETRY_COUNT = os.getenv("CFLIB_HTTPX_RETRY_COUNT") or 3  # Retry count


class ActivityStatus(Enum):
    """
    Model activity statuses.
    PENDING -> STARTED -> Terminal(COMPLETED or FAILED)
    """

    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"


class ModelActivity:
    """
    Wraps model activity related Rest API
    """

    def __init__(
        self,
        logger: Logger,
        correlation_id: str,
        model_name: str,
        description: str,
        tags: str,
        app_key: str,
        account: Optional[object] = None
    ) -> None:
        # Fail fast if misconfigured
        assert CF_ACTIVITY_URL, "CF_ACTIVITY_URL is not configured"

        self.activity_id = None
        self.done = False
        self.logger = logger
        self.correlation_id = correlation_id
        self.model_name = model_name
        self.description = description
        self.tags = tags
        self.app_key = app_key

    def _get_api_header(self):
        return {"x-app-key": self.app_key, "correlation-id": self.correlation_id,
                "Content-Type": "application/json", "accept": "application/json"}

    async def create_activity_async(self) -> None:
        """
        Create a new activity
        """
        try:
            assert self.activity_id is None, "It is not possible to recreate an existing activity"

            self.logger.info(
                f"{self.correlation_id} Creating activity for model: {self.model_name}"
            )

            params = {
                "frogmodel_name": self.model_name,
                "description": self.description,
                "tags": self.tags,
            }

            attempt = 0
            max_attempts = CFLIB_HTTPX_RETRY_COUNT + 1

            async with AsyncClient() as client:
                while attempt < max_attempts:
                    try:
                        attempt += 1

                        response = await client.post(
                            f"{CF_ACTIVITY_URL}/activity",
                            headers=self._get_api_header(),
                            params=params,
                            timeout=CFLIB_HTTPX_ACTIVITY_TIMEOUT,
                        )

                        # If response == 200 then DONE
                        if response.status_code == 200:
                            result = response.json()
                            self.activity_id = result["ActivityId"]
                            self.logger.info(
                                f"{self.correlation_id} Activity ID created: {self.activity_id}"
                            )
                            return self.activity_id

                        response.raise_for_status()

                    except (HTTPStatusError, RequestError, TimeoutException) as e:
                        # Log any non-200 HTTP status as a failed attempt
                        self.logger.error(
                            f"{self.correlation_id} Attempt {attempt} failed with error: {str(e)}."
                        )
                        if attempt <= max_attempts:
                            await asyncio.sleep(
                                2 ** (attempt - 1)
                            )  # Exponential back-off (1s, 2s, 4s...)
                            continue
                        raise

        except Exception as e:
            # Ensure that an activity related failure does not stop the calling process
            trace_back = traceback.format_exc()
            self.logger.error(
                "%s Ignoring exception while creating activity: %s",
                self.correlation_id,
                e,
            )
            self.logger.debug(f"{self.correlation_id} {trace_back}")

    create_activity = sync_wrapper(create_activity_async)

    async def update_activity_async(
        self,
        activity_status: ActivityStatus,
        last_message: Optional[str] = None,
        progress: Optional[int] = None,
        tags: Optional[str] = None,
    ):
        """
        Update an existing activity
        """

        try:
            assert self.activity_id, "No activity_id. Check create_activity has been called"
            assert len(self.activity_id) == 36

            self.logger.info(f"activity_status: {activity_status}")
            self.logger.info(f"last_message: {last_message}")
            self.logger.info(f"progress: {progress}")

            if self.done:
                raise ValueError("Cannot update a closed activity")

            if activity_status in [ActivityStatus.COMPLETED, ActivityStatus.FAILED]:
                self.done = True

            params = {
                "frogmodel_name": self.model_name,
                "activity_id": self.activity_id,
                "activity_status": activity_status.value,
            }

            if tags:
                params["tags"] = tags

            if progress:
                params["progress"] = progress

            if last_message:
                # Also, automatically log messages on the sender side also
                self.logger.info(f"{self.correlation_id} {last_message}")
                params["last_message"] = last_message

            attempt = 0
            max_attempts = CFLIB_HTTPX_RETRY_COUNT + 1

            async with AsyncClient() as client:
                while attempt < max_attempts:
                    try:
                        attempt += 1

                        response = await client.put(
                            f"{CF_ACTIVITY_URL}/activity",
                            headers=self._get_api_header(),
                            params=params,
                            timeout=CFLIB_HTTPX_ACTIVITY_TIMEOUT,
                        )

                        # If response == 200 then DONE
                        if response.status_code == 200:
                            self.logger.info(
                                f"{self.correlation_id} Activity ID updated: {self.activity_id}"
                            )
                            return  # Successfully updated

                        # This line will raise an error for non-200 status and hence trigger the retry mechanism in the exception block below
                        response.raise_for_status()

                    except (HTTPStatusError, RequestError, TimeoutException) as e:
                        self.logger.error(
                            f"{self.correlation_id} Attempt {attempt} failed with error: {str(e)}."
                        )
                        if attempt == max_attempts:
                            raise ConnectionError(
                                f"{self.correlation_id} Unable to update activity: {response.status_code} {response.text}"
                            ) from None
                        await asyncio.sleep(
                            2 ** (attempt - 1)
                        )  # Exponential back-off (1s, 2s, 4s...)

        except Exception as e:
            # Ensure that an activity related failure does not stop the calling process
            trace_back = traceback.format_exc()
            self.logger.error(
                "%s Ignoring exception while updating activity: %s",
                self.correlation_id,
                e,
            )
            self.logger.debug(f"{self.correlation_id} {trace_back}")

    update_activity = sync_wrapper(update_activity_async)


class AsyncFrogActivityHandler:
    """
    Async wrapper for Frog Model Activity notifications service

    Supports context manager style usage

    Can be used to create and update activities
    """

    # A new activity has:
    #
    # model_name: str =
    # Query(..., max_length=1024, description="The model the activity relates to"),
    #
    # description: str =
    # Query(..., max_length=1024, description="A short description of the activity"),
    #
    # tags: str = Query(..., max_length=1024, description="CSV tags for the activity"),

    def __init__(
        self,
        logger: Logger,
        correlation_id: str,
        model_name: str,
        description: str,
        tags: str,
        app_key: str,
        account: Optional[object] = None,
    ) -> None:
        self.activity_id = None
        self.activity = ModelActivity(
            logger, correlation_id, model_name, description, tags, app_key
        )

        self.logger = logger

    async def __aenter__(self):
        try:
            activity_id = await self.activity.create_activity_async()
            self.activity_id = activity_id
        except Exception as e:
            self.logger.debug(
                f"{self.activity.correlation_id} Failed to create activity due to exception"
            )
            raise e

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            # If this activity has already been closed, then close automatically
            if not self.activity.done:
                if exc_type is None and exc_val is None and exc_tb is None:
                    await self.activity.update_activity_async(ActivityStatus.COMPLETED)
                else:
                    await self.activity.update_activity_async(ActivityStatus.FAILED)
                    raise exc_val

                self.activity.done = True

        except Exception as e:
            self.logger.debug(
                f"{self.activity.correlation_id} Failed to close activity due to exception"
            )
            self.logger.error(traceback.format_exc())
            raise e

        return self

    async def update_activity_async(
        self,
        activity_status: ActivityStatus,
        last_message: Optional[str] = None,
        progress: Optional[int] = None,
        tags: Optional[str] = None,
    ):
        """
        Update activity while in context
        """
        await self.activity.update_activity_async(activity_status, last_message, progress, tags)


def activity_signal(
    logger: Logger,
    message: str,
    app_key: str,
    model_name: str = None,
    user_name: str = None,
    correlation_id: str = None,
    email: Optional[str] = None,
):

    assert logger, "Must supply Logger"

    assert model_name or user_name, "Must supply either model or user name"

    assert app_key, "Must supply a valid Optilogic app_key"

    assert message, "Must supply a valid service message"

    headers = {"X-App-KEY": app_key}

    if correlation_id:
        headers["correlation-id"] = correlation_id

    params = {"message": message}

    if model_name:
        params["frogmodel_name"] = model_name

    if user_name:
        params["user_target"] = user_name

    url = f"{CF_ACTIVITY_URL}/signal"

    attempt = 0
    max_attempts = CFLIB_HTTPX_RETRY_COUNT + 1
    target = model_name if model_name else user_name

    logger.info(f"Sending activity signal: {message} to {target}")

    try:
        with Client() as client:
            while attempt < max_attempts:
                try:
                    attempt += 1
                    response = client.post(
                        url,
                        headers=headers,
                        params=params,
                        timeout=CFLIB_HTTPX_ACTIVITY_TIMEOUT,
                    )

                    # If response == 200 then DONE
                    if response.status_code == 200:
                        logger.info(f"{target} Activity signal sent successfully.")
                        return response.status_code

                    response.raise_for_status()

                except (HTTPStatusError, RequestError, TimeoutException) as e:
                    logger.error(f"Attempt {attempt} failed with error: {str(e)}.")
                    if attempt >= max_attempts:
                        raise  # Re-raise the exception after max attempts
                    sleep(2 ** (attempt - 1))  # Exponential back-off

    except Exception:  # pylint: disable=broad-except
        logger.exception(
            f"{correlation_id} Exception attempting to send activity signal, ignoring",
            stack_info=True,
            exc_info=True,
        )