from jsonToClass import TopSteamGames
import requests

steamTopGamesUrl = "https://api.steampowered.com/ISteamChartsService/GetGamesByConcurrentPlayers/v1/"
steamResponse = requests.get(steamTopGamesUrl).json()

top_games = TopSteamGames(**steamResponse)

with open("topgames.json", "w") as topGamesJson:
    topGamesJson.write(top_games.toJson())
