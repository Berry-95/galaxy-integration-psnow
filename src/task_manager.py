import asyncio


class TaskManager:

	def __init__(self, plugin, games_cache):
		self.plugin = plugin
		self.games_cache = games_cache
		self.check_for_new_games_task = None
		self.check_for_removed_games_task = None

	def tick(self):
		if self.check_for_new_games_task is None:
			self.check_for_new_games_task = asyncio.create_task(self.check_for_new_games())
		if self.check_for_removed_games_task is None:
			self.check_for_removed_games_task = asyncio.create_task(self.check_for_removed_games())

	async def check_for_new_games(self):
		games = await self.plugin.get_owned_games()
		self.games_cache.add(games)
		self.check_for_new_games_task = None

	async def check_for_removed_games(self):
		games = await self.plugin.get_owned_games()
		self.games_cache.remove(games)
		self.check_for_removed_games_task = None
