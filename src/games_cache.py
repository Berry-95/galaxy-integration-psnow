class GamesCache:
	def __init__(self, plugin):
		self.plugin = plugin
		self.owned_games_cache = []

	def add(self, games):
		for game in games:
			if game not in self.owned_games_cache:
				self.owned_games_cache.append(game)
				self.plugin.add_game(game)

	def remove(self, games):
		for game in self.owned_games_cache:
			if game not in games:
				self.owned_games_cache.remove(game)
				self.plugin.remove_game(game.game_id)

	def get_games(self):
		return self.owned_games_cache
