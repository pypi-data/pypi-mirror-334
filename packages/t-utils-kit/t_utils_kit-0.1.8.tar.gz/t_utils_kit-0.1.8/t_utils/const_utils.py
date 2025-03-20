"""Constants Module.

This module manages environment variables and imports for running RPA tasks.
It checks the environment to determine whether the process is running locally
or in production, and retrieves relevant work item data from Robocorp's WorkItems
API if not running locally.

Imports:
    os: Provides access to environment variables.
    WorkItems (from RPA.Robocorp.WorkItems): Used to interact with work items in Robocorp's RPA framework.
        Import is attempted and handled if not available.
"""
import os

try:
    from RPA.Robocorp.WorkItems import WorkItems
except ImportError:
    ...

IN_PRODUCTION = bool(os.environ.get("THOUGHTFUL_PRODUCTION"))
LOCAL_RUN = os.environ.get("RC_PROCESS_RUN_ID") is None

if not LOCAL_RUN:
    work_items = WorkItems()
    work_items.get_input_work_item()
    work_item = work_items.get_work_item_variables()

    fabric_variables = work_item.get("variables", dict())
    EMPOWER_RUN_LINK = fabric_variables.get("processRunUrl", "unknown")
    EMPOWER_RUN_ID = EMPOWER_RUN_LINK.split("/")[-1]
else:
    work_item = {}
    fabric_variables = dict()
    EMPOWER_RUN_LINK = None
    EMPOWER_RUN_ID = None
