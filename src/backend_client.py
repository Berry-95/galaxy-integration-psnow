import logging
import re

from galaxy.api.consts import LicenseType
from galaxy.api.types import Game, LicenseInfo
from galaxy.http import create_client_session, handle_exception

from datetime import date, timedelta


class BackendClient:
	GAMES_LIST_URL = "https://www.playstation.com/en-us/explore/playstation-now/games/#allgames"

	@staticmethod
	def calculate_next_games_list_update_date():
		today = date.today()
		first_tuesday_of_next_month = date(today.year, today.month + 1, 1)
		while first_tuesday_of_next_month.weekday() != 1:
			first_tuesday_of_next_month += timedelta(days=1)
		return first_tuesday_of_next_month

	def __init__(self, games_cache):
		self.games_cache = games_cache
		self._session = create_client_session()
		self.next_game_titles_update_date = date.today()

	async def close(self):
		await self._session.close()

	async def request(self, method, url, *args, **kwargs):
		return await self._session.request(method, url, *args, **kwargs)

	async def get_games(self):
		if self.next_game_titles_update_date <= date.today() or len(self.games_cache) == 0:
			game_titles = await self.get_game_titles_from_ps_now()
			games = self.resolve_games(game_titles)
			self.next_game_titles_update_date = BackendClient.calculate_next_games_list_update_date()

		return games

	async def get_game_titles_from_ps_now(self):
		response = await self._session.get(self.GAMES_LIST_URL)
		game_titles = re.findall('<li class="game-title">(.*)</li>', await response.text())
		logging.info("Updated %d games included with Playstation Now", len(game_titles))
		return game_titles

	@staticmethod
	def resolve_games(game_titles):
		return list(map(lambda title: Game(title, title, [], LicenseInfo(LicenseType.SinglePurchase)), game_titles))


def main():
	print(BackendClient.calculate_next_games_list_update_date())


if __name__ == "__main__":
	main()
