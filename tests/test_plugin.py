import os
import json
import subprocess
import socket

TIMEOUT = 5

import pytest


class TCPServer:
	def __init__(self, bind_interface="0.0.0.0", bind_port=0):
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._sock.settimeout(TIMEOUT)
		self._sock.bind((bind_interface, bind_port))
		self.port = self._sock.getsockname()[1]
		self._sock.listen(1)

	def accept_connection(self, timeout):
		'''Returns connected socket'''
		self._sock.settimeout(timeout)
		return self._sock.accept()[0]


@pytest.mark.integration
def test_integration():
	with open(os.path.join("src", "manifest.json"), "r") as file_:
		manifest = json.load(file_)

	plugin_path = os.path.join("src", manifest["script"])

	request = {
		"id": "3",
		"jsonrpc": "2.0",
		"method": "get_capabilities"
	}
	token = "token"
	server = TCPServer()
	result = subprocess.Popen(
		["python", plugin_path, token, str(server.port), "plugin.log"]
	)

	plugin_socket = server.accept_connection(TIMEOUT)
	plugin_socket.settimeout(TIMEOUT)
	plugin_socket.sendall((json.dumps(request) + "\n").encode("utf-8"))
	response = json.loads(plugin_socket.recv(4096))
	print(response)
	assert response["result"]["platform_name"] == "psx"
	assert set(response["result"]["features"]) == set([
		'ImportOwnedGames',
		# 'ImportSubscriptions',
		# 'ImportSubscriptionGames',
	])
	assert response["result"]["token"] == token

	plugin_socket.close()
	result.wait(TIMEOUT)
	assert result.returncode == 0

@pytest.mark.asyncio
async def test_get_game_titles_from_ps_now(
		backend_client
):
	# games = await backend_client.get_game_titles_from_ps_now()
	# with open(os.path.join("tests", "games.json"), "w") as file_:
	# 	json.dump(games, file_, indent=4, sort_keys=True)

	with open(os.path.join("tests", "games.json"), "r") as file_:
		assert json.load(file_) == await backend_client.get_game_titles_from_ps_now()


@pytest.mark.asyncio
async def test_get_games(
		backend_client
):
	with open(os.path.join("tests", "games.json"), "r") as file_:
		game_titles = await backend_client.get_games()
		games = list(map(lambda game: game.game_title, game_titles))
		assert json.load(file_) == games
