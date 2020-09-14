import pytest

from src.plugin import PsNowPlugin
from src.games_cache import GamesCache
from src.backend_client import BackendClient
from src.task_manager import TaskManager
from unittest.mock import MagicMock



@pytest.fixture()
def access_token():
	return "access_token"


@pytest.fixture()
def npsso():
	return "npsso"


@pytest.fixture()
def stored_credentials(npsso):
	return {"npsso": npsso}


@pytest.fixture()
def account_id():
	return "accountId"


@pytest.fixture()
def online_id():
	return "onlineId"


@pytest.fixture()
def user_profile(online_id, account_id):
	return {"profile": {"onlineId": online_id, "accountId": account_id}}


@pytest.fixture()
def psplus_active_status():
	return 1


@pytest.fixture()
def user_profile_psplus(psplus_active_status):
	return {"profile": {"plus": psplus_active_status}}


@pytest.fixture()
def psplus_name():
	return "PlayStation PLUS"


@pytest.fixture()
async def ps_now_plugin():
	plugin = PsNowPlugin(MagicMock(), MagicMock(), None)
	yield plugin

	await plugin.shutdown()

@pytest.fixture()
async def games_cache():
	cache = GamesCache()
	yield cache

@pytest.fixture()
async def backend_client():
	client = BackendClient(games_cache)
	yield client

	await client.close()

@pytest.fixture()
async def task_manager():
	manager = TaskManager(ps_now_plugin, games_cache)
	yield manager
