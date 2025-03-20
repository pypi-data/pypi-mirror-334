"""Constants Module."""
import os
import time
from datetime import datetime, timedelta
from typing import Any

from t_utils.const_utils import LOCAL_RUN
from t_utils.lib_utils.logger import logger

try:
    from RPA.Robocorp.Storage import Storage
    from robocorp.storage import AssetNotFound
except ImportError:
    logger.warning("rpaframework is not installed, please install the library to use all methods from robocloud_utils.")


RC_ORGANIZATION_ID = os.environ.get("RC_ORGANIZATION_ID")
RC_WORKSPACE_ID = os.environ.get("RC_WORKSPACE_ID")
RC_RUNTIME_ID = os.environ.get("RC_RUNTIME_ID")
RC_PROCESS_ID = os.environ.get("RC_PROCESS_ID")
RC_PROCESS_NAME = os.environ.get("RC_PROCESS_NAME")
RC_PROCESS_RUN_ID = os.environ.get("RC_PROCESS_RUN_ID")
RC_PROCESS_RUN_NUMBER = os.environ.get("RC_PROCESS_RUN_NUMBER")
RC_ACTIVITY_ID = os.environ.get("RC_ACTIVITY_ID")
RC_ACTIVITY_NAME = os.environ.get("RC_ACTIVITY_NAME")
RC_ACTIVITY_RUN_ID = os.environ.get("RC_ACTIVITY_RUN_ID")
RC_ACTIVITY_RUN_NUMBER = os.environ.get("RC_ACTIVITY_RUN_NUMBER")
RC_WORKITEM_ID = os.environ.get("RC_WORKITEM_ID")


class AssetsKeyBooking:
    """Class that manages booking and unbooking of keys in Robocloud Assets."""

    def __init__(self, key: str, wait_time: int = 660, expire_time: int = 600):
        """Class that manages booking and unbooking of keys in Robocloud Assets.

        May be used as a context manager.

        Args:
            key (str): String key that will be booked.
            wait_time (int, optional): Time to wait for the key to become available. Defaults to 660.
            expire_time (int, optional): Time in seconds after which the key booking will expire. Defaults to 600.
        """
        self.key = key
        self.wait_time = wait_time
        self.expire_time = expire_time
        self.asset_name = f"{RC_PROCESS_NAME} (Booked Keys)"
        self.storage = Storage()

    def __get_assets(self) -> dict:
        """Gets the assets from Robocloud."""
        exception = Exception()
        for _ in range(3):
            try:
                return self.storage.get_json_asset(self.asset_name)
            except ValueError as ex:
                exception = ex
                time.sleep(5)  # Wait for assets to be available, the creating in progress.
        raise exception

    def is_key_available(self) -> bool:
        """Checks if the key is available."""
        try:
            assets = self.__get_assets()
        except AssetNotFound:
            assets = {}
            self.storage.set_json_asset(self.asset_name, assets)

        if self.key not in assets:
            return True

        booking_time = datetime.strptime(assets[self.key]["datetime"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() - booking_time > timedelta(seconds=self.expire_time):
            self.unbook_key()
            return True

        return False

    def _is_booked_by_current_activity(self, assets: dict) -> bool:
        """Checks if the key is booked by the current activity."""
        return assets.get(self.key, {}).get("activity_id") == RC_ACTIVITY_RUN_ID

    def book_key(self) -> None:
        """Books the key."""
        assets = self.__get_assets()
        assets[self.key] = {"datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "activity_id": RC_ACTIVITY_RUN_ID}
        self.storage.set_json_asset(self.asset_name, assets)

        time.sleep(5)
        assets_updated = self.__get_assets()
        if not self._is_booked_by_current_activity(assets_updated):
            raise RuntimeError(f"{self.key} already booked by another process.")
        logger.info(f"Booking key '{self.key}' in assets for activity '{RC_ACTIVITY_RUN_ID}'.")

    def unbook_key(self) -> None:
        """Unbooks the key."""
        logger.info(f"Unbooking key '{self.key}' in assets.")
        assets = self.__get_assets()
        if self._is_booked_by_current_activity(assets):
            del assets[self.key]
            self.storage.set_json_asset(self.asset_name, assets)

    def __enter__(self):
        """Enters the context manager, ensuring the key is booked."""
        if not LOCAL_RUN:
            start_time = time.time()
            logger.info(f"Waiting for key '{self.key}' to become available.")
            while True:
                if time.time() - start_time >= self.wait_time:
                    raise TimeoutError(f"Timeout waiting for key '{self.key}' to become available.")

                if self.is_key_available():
                    try:
                        self.book_key()
                        break
                    except RuntimeError:
                        continue  # Booked by another process. Waiting for key to become available.
                else:
                    time.sleep(5)

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any):
        """Ensures the key is unbooked on exit, even on exceptions."""
        if not LOCAL_RUN:
            self.unbook_key()
