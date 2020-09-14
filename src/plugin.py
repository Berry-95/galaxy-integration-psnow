"""
Original example is taken from GOG Galaxy Python API documentation:
https://galaxy-integrations-python-api.readthedocs.io/en/latest/overview.html#basic-usage
"""
import asyncio
import sys

from galaxy.api.consts import Platform
from galaxy.api.plugin import Plugin, create_and_run_plugin
from galaxy.api.types import Authentication


sys.path.append('src')
from games_cache import GamesCache
from backend_client import BackendClient
from task_manager import TaskManager


# with open('manifest.json', 'r') as f:
#     __version__ = json.load(f)['version']

class PsNowPlugin(Plugin):

	def __init__(self, reader, writer, token):
		super().__init__(
			Platform.PlayStation,  # choose platform from available list
			"0.1",  # version
			reader,
			writer,
			token
		)
		self.games_cache = GamesCache(self)
		self.backend_client = BackendClient(self.games_cache)
		self.task_manager = TaskManager(self, self.games_cache)

	# required
	async def authenticate(self, stored_credentials=None):
		return Authentication()

	# required
	async def get_owned_games(self):
		return await self.backend_client.get_games()

	def tick(self):
		self.task_manager.tick()

	async def shutdown(self):
		await self.backend_client.close()


def main():
	create_and_run_plugin(PsNowPlugin, sys.argv)


# run plugin event loop
if __name__ == "__main__":
    main()