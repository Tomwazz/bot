import copy
import datetime
import json
import logging

import os
import sys
from discord.ext import commands
from commandss.prefix import get_prefix, change_prefix

from rich.logging import RichHandler
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from twitchAPI.types import AuthScope

log_level = logging.DEBUG if "dev".lower() in sys.argv else logging.INFO


log = logging.getLogger()


logging.basicConfig(
    level=log_level,
    format="%(name)s - %(message)s",
    datefmt="%X",
    handlers=[RichHandler()],
)


def path_exists(filename):
    return os.path.join(".", f"{filename}")


if not os.path.exists(path_exists("config.json")):
    print("\n--------------------------")
    print("\nwhat's your Twitch Bot's name?")
    bot_name = input(
        "Type your Bot's name, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")
    print("\nwhat will your prefix be? (example: !, ?, $)")
    prefix = input("Type your prefix, then press `ENTER`. (You can change this later) ")
    print("\n--------------------------")
    print("\nwhat's your Twitch Channel's name?")
    channel = input(
        "Type your Channel's name, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")

    with open("config.json", "a") as config_file:
        config_file.write(
            json.dumps({"nickname": bot_name, "prefix": prefix, "channels": [channel]})
        )

if not os.path.exists(path_exists(".env")):
    print("\n⚠⚠⚠⚠⚠ WARNING: DO NOT SHOW THE FOLLOWING ON STREAM. ⚠⚠⚠⚠⚠" * 10)
    input("\nPress `ENTER` if this is not showing on stream.")

    print("\n" * 100)
    print("Cool, now let's get to the boring stuff...")
    print("\n--------------------------")
    print("\nlet's set up the bot's token")
    token = input(
        "You can get this token from a site like https://twitchapps.com/tmi/.\nJust copy and paste the OAuth token into here.\nType token, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")
    print("\nlet's setup the Twitch Client ID")
    client_id = input(
        "You can get this by going to https://dev.twitch.tv/console/apps/create, signing in, creating a 'Chat Bot' application (the OAuth redirect URLs NEED to be 'http://localhost:17563/' and 'http://localhost:17563')\nNow just copy and paste the Client ID into here.\nType the Client ID, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")
    print("\nlet's setup the Twitch Client Secret")
    client_secret = input(
        'You can get this by scrolling down on your application, and clicking the "New Secret" button.\nNow just copy and paste the Client Secret into here.\nType the Client Secret, then press `ENTER`. (You can change this later) '
    )
    print("\n--------------------------")
    channel_points_reward = input(
        "If you are going to use TwitchTunes with channel points, then what is your Channel Point reward name?\nType the Channel Point reward name, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")
    print("\nlets setup the Spotify Client ID")
    spotify_client_id = input(
        "You can get this by going to https://developer.spotify.com/dashboard/applications, signing in, then creating an application.\nJust paste in the Client ID into here now.\nType Spotify's Client ID, then press `ENTER`. (You can change this later)"
    )
    print("\n--------------------------")
    print("\nlet's setup the Spotify Client Secret")
    spotify_secret = input(
        "You can get this by going to that application page, then clicking the 'SHOW CLIENT SECRET' button.\nNow just paste the Client Secret here.\nType Spotify Client Secret, then press `ENTER`. (You can change this later) "
    )
    print("\n--------------------------")
    print("\nlet's setup the Spotify Website/Redirect URI")
    input(
        "All you have to do, is hit the settings button, then in BOTH the Website field, AND the Redirect URIs field, but 'http://localhost:8080'\nPress `ENTER` once you have completed this step."
    )

    with open(".env", "a") as env_file:
        env_file.write(
            f"TOKEN={token}\n"
            + "# Twitch IRC token\n"
            + f"client_id={client_id}\n"
            + "# Twitch Client ID from dev.twitch.tv\n"
            + f"client_secret={client_secret}\n"
            + "# Twitch Client Secret from dev.twitch.tv\n"
            + f"channel_points_reward={channel_points_reward}\n"
            + "# Channel Point reward name\n"
            + f"\nspotify_client_id={spotify_client_id}\n"
            + "# Get this from the Spotify console https://developer.spotify.com/dashboard/applications\n"
            + f"spotify_secret={spotify_secret}\n"
            + "# Get this from the Spotify console https://developer.spotify.com/dashboard/applications\n"
            + "spotify_redirect_uri=http://localhost:8080\n"
            + "# Set your 'redirect_uri' and 'website' on your Spotify application to 'http://localhost:8080' (Don't change the spotify_redirect_uri in .env)"
        )

if not os.path.exists(path_exists("blacklist.json")):
    with open("blacklist.json", "a") as blacklist_file:
        blacklist_file.write(json.dumps({"blacklist": []}))

if not os.path.exists(path_exists("blacklist_user.json")):
    with open("blacklist_user.json", "a") as blacklist_user_file:
        blacklist_user_file.write(json.dumps({"users": []}))


log.info("\n\nStarting 🎶TwitchTunes")

from pathlib import Path

import dotenv

import twitchio
from twitchio.ext import commands

cwd = Path(__file__).parents[0]
cwd = str(cwd)
import asyncio
import json
import re

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

with open("config.json") as config_file:
    config = json.load(config_file)

with open('nicknames.json', 'r') as file:
    nicknames = json.load(file)


dotenv.load_dotenv()


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ.get("spotify_client_id"),
        client_secret=os.environ.get("spotify_secret"),
        redirect_uri="http://localhost:8080",
        scope=[
            "user-modify-playback-state",
            "user-read-currently-playing",
            "user-read-playback-state",
            "user-read-recently-played",
        ],
    )
)

# Load prefixes from prefix.json
with open('prefix.json', 'r') as file:
    prefixes = json.load(file)

def read_json(filename):
    with open(f"{filename}.json") as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(f"{filename}.json", "w") as file:
        json.dump(data, file, indent=4)   

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ.get("TOKEN"),
            client_id=os.environ.get("client_id"),
            nick=config["nickname"],
            prefix=get_prefix,
            initial_channels=config["channels"],
        )  

        self.queue = []
        self.queue2 = []
        self.position_counter = 0
        self.prefixes = prefixes  # Store prefixes in a dictionary
        self.token = os.environ.get("SPOTIFY_AUTH")
        self.initial_channels = config["channels"]
        self.default_prefix = "<"  # Set the default prefix here
        self.channel_prefixes = {}  # Initialize an empty dictionary for channel prefixes
        self.afk_users = {}
        self.prefix = {}
        self.version = "1.4.0"
        self.user_counts = {}
        self.channel_prefixes = {}  # Initialize an empty dictionary for channel prefixes

        # Load the prefixes from the JSON file
        self.load_channel_prefixes()

        self.load_module("commandss.ping")
        self.load_module("commandss.afk")
        self.load_module("commandss.commands")
        self.load_module("commandss.moreinfo")
        self.load_module("commandss.s3s")
        self.load_module("commandss.helping")
        self.load_module("commandss.blacklistuser")
        self.load_module("commandss.unblacklistuser")
        self.load_module("commandss.pyramid")
        self.load_module("commandss.saying")
        self.load_module("commandss.spam")
        self.load_module("commandss.clock")
        self.load_module("commandss.send")
        self.load_module("commandss.send2")
        self.load_module("commandss.google")
        self.load_module("commandss.emotes")
        self.load_module("commandss.7tv")
        self.load_module("commandss.unique")
        self.load_module("commandss.nickname")
        self.load_module("commandss.number")
        self.load_module("commandss.bob")

    """a    sync def event_message(self, message):
        if message.author.name == "reformedmartass":
            content = message.content.strip()
            if content.lower().startswith("bobthe42"):
                content = content[len("bobthe42"):].strip()
            if re.search(r'bob.*', content, re.IGNORECASE):
                user = message.author.name
                target_channel = "omegalulingsomuch"
                if user not in self.user_counts:
                    self.user_counts[user] = 1
                else:
                    self.user_counts[user] += 1
                await self.send_message_to_channel(target_channel, f'Pingl te: ({user} count: {self.user_counts[user]})')
        if message.author.name == "reformedmartass" and re.search(r'tom.*', message.content, re.IGNORECASE):
            user = message.author.name
            target_channel = "omegalulingsomuch"  
            if user not in self.user_counts:
                self.user_counts[user] = 1
            else:
                self.user_counts[user] += 1
            await self.send_message_to_channel(target_channel, f'Pingl me: ({user} count: {self.user_counts[user]})')
        await self.handle_commands(message)"""

    """async def event_message(self, message):
        user_to_track = "fswref"  # Replace with the username you want to track
        channel_to_track = "bobthebuilder_98"  # Replace with the channel name you want to track

        if message.author.name == user_to_track and message.channel.name == channel_to_track:
            user = message.author.name
            channel_name = message.channel.name
            content = message.content
            await self.send_message_to_channel("omegalulingsomuch", f'{user} in {channel_name} typed: "{content}"')

    # Handle other events and commands
        await self.handle_commands(message)"""
    def metoda_queue(self):
        queue = sp.queue()
        self.queue2 = []
        for i in queue["queue"]:
            hdsbf = []
            for j in i["album"]["artists"]:
                hdsbf.append(j["name"])
            b = (i["external_urls"]["spotify"])
            c = (i["name"])
            self.queue2.append({c:[b, hdsbf]})
        # print(self.queue2[:5])

    def get_command_name(message_content, prefix):
        command = message_content[len(prefix):].strip().lower()
        return command

    def load_channel_prefixes(self):
        try:
            with open("prefix.json", "r") as file:
                self.channel_prefixes = json.load(file)
        except FileNotFoundError:
            print("prefix.json file not found. Using default prefixes.")

    async def event_message(self, message):
        await self.handle_commands(message)

    async def handle_commands(self, message):
        await asyncio.sleep(1)
        await super().handle_commands(message)

    async def send_message_to_channel(self, channel, message):
        target_channel = self.get_channel(channel)
        if target_channel:
            await target_channel.send(message)

    async def event_ready(self):
        log.info("\n" * 100)
        log.info(f"TwitchTunes ({self.version}) Ready, logged in as: {self.nick}")

    def is_owner(self, ctx):
        return ctx.author.id == "640348450"

    @commands.command(name='q', aliases=["queue"])
    async def q_command(self, ctx):
        self.metoda_queue()
        message = "Queue:\n"
        for index, item in enumerate(self.queue2[:5], start=1):
            c = list(item.keys())[0]
            hdsbf = item[c][1]
            message += f"{index}. {c} by {', '.join(hdsbf)} | "
        await ctx.send(message)

    @commands.command(name="prefix")
    async def change_prefix_command(self, ctx, new_prefix: str):
        if ctx.author.is_mod or ctx.author.is_broadcaster:
            change_prefix(ctx.channel.name, new_prefix)
            bot.prefix[ctx.channel.name] = new_prefix
            await ctx.send(f"Successfully changed prefix to {new_prefix}")
            await self.bot.send_message(ctx.channel.name, f"The prefix for this channel has been set to '{new_prefix}'")
        else:
            await ctx.send("You don't have permission to change the prefix for this channel.")

    @commands.command(name="blacklist", aliases=["blacklistsong", "blacklistadd"])
    async def blacklist_command(self, ctx, *, song_uri: str):
        if ctx.author.is_mod or self.is_owner(ctx):
            jscon = read_json("blacklist")

            song_uri = song_uri.replace("spotify:track:", "")

            if song_uri not in jscon["blacklist"]:
                if re.match(URL_REGEX, song_uri):
                    data = sp.track(song_uri)
                    song_uri = data["uri"]
                    song_uri = song_uri.replace("spotify:track:", "")

                track = sp.track(song_uri)

                track_name = track["name"]

                jscon["blacklist"].append(song_uri)

                write_json(jscon, "blacklist")

                await ctx.send(f"Added {track_name} to blacklist.")

            else:
                await ctx.send("Song is already blacklisted.")

        else:
            await ctx.send("You are not authorized to use this command.")
    
    @commands.command(
        name="unblacklist", aliases=["unblacklistsong", "blacklistremove"]
    )
    async def unblacklist_command(self, ctx, *, song_uri: str):
        if ctx.author.is_mod or self.is_owner(ctx):
            jscon = read_json("blacklist")

            song_uri = song_uri.replace("spotify:track:", "")

            if re.match(URL_REGEX, song_uri):
                data = sp.track(song_uri)
                song_uri = data["uri"]
                song_uri = song_uri.replace("spotify:track:", "")

            if song_uri in jscon["blacklist"]:
                jscon["blacklist"].remove(song_uri)
                write_json(jscon, "blacklist")
                await ctx.send("Removed that song from the blacklist.")

            else:
                await ctx.send("Song is not blacklisted.")
        else:
            await ctx.send("You are not authorized to use this command.")

    @commands.command(name="np", aliases=["nowplaying", "song"])
    async def np_command(self, ctx):
        data = sp.currently_playing()
        song_artists = data["item"]["artists"]
        song_artists_names = [artist["name"] for artist in song_artists]

        min_through = int(data["progress_ms"] / (1000 * 60) % 60)
        sec_through = int(data["progress_ms"] / (1000) % 60)
        time_through = f"{min_through} mins, {sec_through} secs"

        min_total = int(data["item"]["duration_ms"] / (1000 * 60) % 60)
        sec_total = int(data["item"]["duration_ms"] / (1000) % 60)
        time_total = f"{min_total} mins, {sec_total} secs"
        # Get the user's currently active device
        devices = sp.devices()
        active_device = next((device for device in devices['devices'] if device['is_active']), None)
        is_owner = "TOMWAZ"

    # Check if there is an active device
        if active_device:
        # Get the current volume of the active device
            current_volume = sp.current_playback()['device']['volume_percent']
        else:
            current_volume = "unknown"

        await ctx.send(
            f"🎶 Teď hraje: {data['item']['name']} by {', '.join(song_artists_names)} | {time_through} - {time_total} | {is_owner}'s volume: {current_volume}%")

    @commands.command(
        name="lastsong", aliases=["previoussongs", "last", "previousplayed"]
    )
    async def queue_command(self, ctx):
        queue = sp.current_user_recently_played(limit=10)
        songs = []

        for song in queue["items"]:
            # if the song artists include more than one artist: add all artist names to an artist list variable
            if len(song["track"]["artists"]) > 1:
                artists = [artist["name"] for artist in song["track"]["artists"]]
                song_artists = ", ".join(artists)
            # if the song artists only include one artist: add the artist name to the artist list variable
            else:
                song_artists = song["track"]["artists"][0]["name"]

            songs.append(song["track"]["name"] + " - " + song_artists)

        await ctx.send("Recently Played: " + " | ".join(songs))

    @commands.command(name="songrequest", aliases=["sr", "addsong", "ns"])
    async def songrequest_command(self, ctx, *, song: str):
        song_uri = None

        if (
            song.startswith("spotify:track:")
            or not song.startswith("spotify:track:")
            and re.match(URL_REGEX, song)
        ):
            song_uri = song
            await self.chat_song_request(ctx, song_uri, song_uri, album=False)
        else:
            await self.chat_song_request(ctx, song, song_uri, album=False)


    @commands.command(name="skip")
    async def skip_song_command(self, ctx):
        self.allowed_users = ["tomwaz"]
        if ctx.author.name in self.allowed_users:
            sp.next_track()
            await ctx.send(f":) Skipping song...")
        else: 
            await ctx.send(f":) gtfo")

    @commands.command(name="previous", aliases=["back"])
    async def previous_song_command(self, ctx):
        self.allowed_users = ["tomwaz"]
        if ctx.author.name in self.allowed_users:
            sp.previous_track()
            await ctx.send(f"Getting back... :)")
        else: 
            await ctx.send(f":) gtfo")

    # @commands.command(name="albumqueue")
    #     if ctx.author.is_mod or ctx.author.is_subscriber or self.is_owner(ctx):
    # async def albumqueue_command(self, ctx, *, album: str):
    #         album_uri = None

    #         if (
    #             album.startswith("spotify:album:")
    #             or not album.startswith("spotify:album:")
    #             and re.match(URL_REGEX, album)
    #         ):
    #             album_uri = album
    #         await self.album_request(ctx, album_uri)
    #     else:
    #         await ctx.send(f"🎶You don't have permission to do that! (Album queue is Sub Only!)")

    """
        DO NOT USE THE API REQUEST IT WONT WORK.
        the logic should still work iwth using the spotipy library, so thats why I'm keeping it, but don't do an API request
        - like this.
    """
    @commands.command(name='volume')
    async def volume_command(self, ctx, volume: int):
    # Get the user's current playback information
        playback = sp.current_playback()

    # Check if the user has an active playback
        if playback is not None and playback['is_playing']:
        # Get the active device
            active_device = playback['device']

        # Check if the active device belongs to the user
            if active_device['is_active'] and active_device['id'] == playback['device']['id']:
            # Toggle the volume
                sp.volume(volume, device_id=active_device['id'])
                await ctx.send(f'Spotify volume set to: {volume}%')
            else:
                await ctx.send('You do not have an active Spotify device.')
        else:
            await ctx.send('No active playback found.')

    # async def album_request(self, ctx, song):
    #     song = song.replace("spotify:album:", "")
    #     ALBUM_URL = f"https://api.spotify.com/v1/albums/{song}?market=US"
    #     async with request("GET", ALBUM_URL, headers={
    #                 "Content-Type": "application/json",
    #                 "Authorization": "Bearer " + self.token,
    #             }) as resp:
    #             data = await resp.json()
    #             songs_uris = [artist["uri"] for artist in data['tracks']['items']]

    #             for song_uris in songs_uris:
    #                 await self.song_request(ctx, song, song_uris, album=True)
    #             await ctx.send(f"Album Requested! {data['name']}")
    #             return

    async def chat_song_request(self, ctx, song, song_uri, album: bool):
        blacklisted_users = read_json("blacklist_user")["users"]
        if ctx.author.name.lower() in blacklisted_users:
            await ctx.send("You are blacklisted from requesting songs.")
        else:
            jscon = read_json("blacklist")

            if song_uri is None:
                data = sp.search(song, limit=1, type="track", market="US")
                song_uri = data["tracks"]["items"][0]["uri"]

            elif re.match(URL_REGEX, song_uri):
                data = sp.track(song_uri)
                song_uri = data["uri"]
                song_uri = song_uri.replace("spotify:track:", "")

            song_id = song_uri.replace("spotify:track:", "")

            if not album:
                data = sp.track(song_id)
                song_name = data["name"]
                song_artists = data["artists"]
                song_artists_names = [artist["name"] for artist in song_artists]
                duration = data["duration_ms"] / 60000

            if song_uri != "not found":
                if song_id in jscon["blacklist"]:
                    await ctx.send("That song is blacklisted.")

                elif duration > 17:
                    await ctx.send("Send a shorter song please! :)")
                else:
                    sp.add_to_queue(song_uri)
                    self.queue.append(song_id)
                    # Call the metoda_queue method to update the queue
                    self.metoda_queue()

                    channel_prefix = get_prefix(self, ctx.message)
                    await ctx.send(
                        f"@{ctx.author.name}, Your track: `{song_name}˙ is added. Check {channel_prefix}q"
                    )
                    self.metoda_queue()

def song_request(data, song, song_uri, album: bool):
    jscon = read_json("blacklist")
    if song_uri is None:
        data = sp.search(song, limit=1, type="track", market="US")
        song_uri = data["tracks"]["items"][0]["uri"]
    elif re.match(URL_REGEX, song_uri):
        data = sp.track(song_uri)
        song_uri = data["uri"]
        song_uri = song_uri.replace("spotify:track:", "")
    song_id = song_uri.replace("spotify:track:", "")
    if not album:
        data = sp.track(song_id)
        duration = data["duration_ms"] / 60000
    if song_uri != "not found":
        if song_id in jscon["blacklist"] or duration > 17:
            return
        else:
            sp.add_to_queue(song_uri)


def callback_channel_points(uuid, data: dict) -> None:
    if (
        data["data"]["redemption"]["reward"]["title"].lower()
        != os.environ.get("channel_points_reward").lower()
    ):
        return

    log.debug(data)

    song: str = data["data"]["redemption"]["user_input"]
    ctx = None
    blacklisted_users = read_json("blacklist_user")["users"]
    if data["data"]["redemption"]["user"]["login"] in blacklisted_users:
        return
    if (
        song.startswith("spotify:track:")
        or not song.startswith("spotify:track:")
        and re.match(URL_REGEX, song)
    ):
        song_uri = song
        song_request(ctx, song_uri, song_uri, album=False)
    else:
        song_request(ctx, song, song_uri, album=False)

if os.environ.get("channel_points_reward"):
    channel_points_reward = os.environ.get("channel_points_reward")
    twitch = Twitch(os.environ.get("client_id"), os.environ.get("client_secret"))
    twitch.authenticate_app([])
    target_scope: list = [AuthScope.CHANNEL_READ_REDEMPTIONS]
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    token, refresh_token = auth.authenticate()
    # add User authentication
    twitch.set_user_authentication(token, target_scope, refresh_token)

    user_id: str = twitch.get_users(logins=config["channels"])["data"][0]["id"]

    pubsub = PubSub(twitch)
    uuid = pubsub.listen_channel_points(user_id, callback_channel_points)
    pubsub.start()

bot = Bot()
bot.run()
