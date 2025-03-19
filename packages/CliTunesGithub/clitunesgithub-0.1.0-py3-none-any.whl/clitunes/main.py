import os
import sys
import time
import random
import argparse
import curses
import threading
import json
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import numpy as np
import pygame
from pygame import mixer
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CONFIG_DIR = os.path.expanduser("~/.config/clitunes")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
CACHE_DIR = os.path.join(CONFIG_DIR, "cache")
DEFAULT_CONFIG = {
    "spotify": {
        "client_id": "",
        "client_secret": "",
        "redirect_uri": "http://localhost:8888/callback",
        "scope": "user-library-read user-read-playback-state user-modify-playback-state"
    },
    "music_dirs": [os.path.expanduser("~/Music")]
}

@dataclass
class Track:
    title: str
    artist: str
    album: str
    duration: int
    path: Optional[str] = None
    spotify_id: Optional[str] = None

class Player:
    def __init__(self):
        self.load_config()
        self.setup_dirs()
        self.current_track = None
        self.playlist: List[Track] = []
        self.playing = False
        self.paused = False
        self.volume = 0.7
        self.position = 0
        self.spotify = None
        self.visualizer = None
        self.setup_audio()
        self.setup_spotify()
        self.load_local_tracks()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            if not os.path.exists(CONFIG_DIR):
                os.makedirs(CONFIG_DIR)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(DEFAULT_CONFIG, f, indent=2)
            print(f"Created default config at {CONFIG_FILE}. Please add your Spotify credentials.")
        
        with open(CONFIG_FILE, 'r') as f:
            self.config = json.load(f)

    def setup_dirs(self):
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

    def setup_audio(self):
        pygame.init()
        mixer.init()

    def setup_spotify(self):
        spotify_config = self.config.get("spotify", {})
        if spotify_config.get("client_id") and spotify_config.get("client_secret"):
            try:
                self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id=spotify_config["client_id"],
                    client_secret=spotify_config["client_secret"],
                    redirect_uri=spotify_config["redirect_uri"],
                    scope=spotify_config["scope"],
                    cache_path=os.path.join(CACHE_DIR, "spotify_cache")
                ))
                print("Spotify connection established")
            except Exception as e:
                print(f"Spotify connection failed: {e}")
        else:
            print("Spotify credentials not found in config")

    def load_local_tracks(self):
        self.local_tracks = []
        for music_dir in self.config.get("music_dirs", []):
            if os.path.exists(music_dir):
                for root, _, files in os.walk(music_dir):
                    for file in files:
                        if file.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                            path = os.path.join(root, file)
                            title = os.path.splitext(file)[0]
                            artist = "Unknown"
                            album = "Unknown"
                            duration = 0
                            self.local_tracks.append(Track(
                                title=title,
                                artist=artist,
                                album=album,
                                duration=duration,
                                path=path
                            ))
        print(f"Loaded {len(self.local_tracks)} local tracks")

    def play_track(self, track: Track):
        if self.playing:
            mixer.music.stop()
        
        self.current_track = track
        
        if track.path:
            mixer.music.load(track.path)
            mixer.music.set_volume(self.volume)
            mixer.music.play()
            self.playing = True
            self.paused = False
        elif track.spotify_id and self.spotify:
            try:
                self.spotify.start_playback(uris=[f"spotify:track:{track.spotify_id}"])
                self.playing = True
                self.paused = False
            except Exception as e:
                print(f"Failed to play Spotify track: {e}")
        else:
            print("Track cannot be played (no path or Spotify ID)")

    def pause(self):
        if self.playing and not self.paused:
            if self.current_track.path:
                mixer.music.pause()
            elif self.current_track.spotify_id and self.spotify:
                self.spotify.pause_playback()
            self.paused = True

    def resume(self):
        if self.playing and self.paused:
            if self.current_track.path:
                mixer.music.unpause()
            elif self.current_track.spotify_id and self.spotify:
                self.spotify.start_playback()
            self.paused = False

    def stop(self):
        if self.playing:
            if self.current_track.path:
                mixer.music.stop()
            elif self.current_track.spotify_id and self.spotify:
                self.spotify.pause_playback()
            self.playing = False
            self.paused = False
            self.current_track = None

    def next_track(self):
        if not self.playlist:
            return
        
        if self.current_track in self.playlist:
            current_index = self.playlist.index(self.current_track)
            next_index = (current_index + 1) % len(self.playlist)
        else:
            next_index = 0
        
        self.play_track(self.playlist[next_index])

    def prev_track(self):
        if not self.playlist:
            return
        
        if self.current_track in self.playlist:
            current_index = self.playlist.index(self.current_track)
            prev_index = (current_index - 1) % len(self.playlist)
        else:
            prev_index = 0
        
        self.play_track(self.playlist[prev_index])

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, volume))
        if self.playing:
            if self.current_track.path:
                mixer.music.set_volume(self.volume)
            elif self.current_track.spotify_id and self.spotify:
                self.spotify.volume(int(self.volume * 100))

    def search_spotify(self, query: str) -> List[Track]:
        if not self.spotify:
            print("Spotify not configured")
            return []
        
        try:
            results = self.spotify.search(q=query, type='track', limit=10)
            tracks = []
            for item in results['tracks']['items']:
                track = Track(
                    title=item['name'],
                    artist=item['artists'][0]['name'] if item['artists'] else "Unknown",
                    album=item['album']['name'] if item['album'] else "Unknown",
                    duration=item['duration_ms'] // 1000,
                    spotify_id=item['id']
                )
                tracks.append(track)
            return tracks
        except Exception as e:
            print(f"Spotify search failed: {e}")
            return []

    def play_random(self):
        if not self.local_tracks:
            print("No local tracks available")
            return
        
        track = random.choice(self.local_tracks)
        self.play_track(track)

    def attach_visualizer(self, visualizer):
        self.visualizer = visualizer


def text_based_ui():
    player = Player()
    
    print("\nCliTunes - Terminal Music Player")
    print("================================")
    
    if not player.local_tracks:
        print("No local tracks found. Please add music files to your configured directories.")
        print(f"Current music directories: {player.config.get('music_dirs', [])}")
        return
    
    print("\nAvailable Tracks:")
    for i, track in enumerate(player.local_tracks):
        print(f"{i+1}. {track.title} - {track.artist}")
    
    currently_playing = None
    
    while True:
        if player.current_track:
            status = "▶" if player.playing and not player.paused else "⏸"
            print(f"\nNow {status}: {player.current_track.title} - {player.current_track.artist}")
            print(f"Volume: {int(player.volume * 100)}%")
        
        print("\nCommands:")
        print("  [number] - Play track by number")
        print("  n - Next track")
        print("  p - Previous track")
        print("  r - Play random track")
        print("  + - Volume up")
        print("  - - Volume down")
        print("  l - List tracks")
        print("  s [query] - Search Spotify")
        print("  q - Quit")
        
        choice = input("\nEnter command: ").strip().lower()
        
        if choice == 'q':
            if player.playing:
                player.stop()
            break
        elif choice == 'r':
            player.play_random()
            print(f"Playing: {player.current_track.title}")
        elif choice == ' ' or choice == 'space':
            if player.playing:
                if player.paused:
                    player.resume()
                    print("Playback resumed")
                else:
                    player.pause()
                    print("Playback paused")
            elif player.current_track:
                player.resume()
                print("Playback resumed")
            elif player.local_tracks:
                player.playlist = player.local_tracks.copy()
                player.play_track(player.playlist[0])
                print(f"Playing: {player.current_track.title}")
        elif choice == 'n':
            if player.playing:
                player.next_track()
                if player.current_track:
                    print(f"Playing: {player.current_track.title}")
            else:
                print("No active playback")
        elif choice == 'p':
            if player.playing:
                player.prev_track()
                if player.current_track:
                    print(f"Playing: {player.current_track.title}")
            else:
                print("No active playback")
        elif choice == '+':
            new_volume = min(1.0, player.volume + 0.1)
            player.set_volume(new_volume)
            print(f"Volume: {int(player.volume * 100)}%")
        elif choice == '-':
            new_volume = max(0.0, player.volume - 0.1)
            player.set_volume(new_volume)
            print(f"Volume: {int(player.volume * 100)}%")
        elif choice == 'l':
            print("\nAvailable Tracks:")
            for i, track in enumerate(player.local_tracks):
                print(f"{i+1}. {track.title} - {track.artist}")
        elif choice.startswith('s '):
            query = choice[2:].strip()
            if query:
                print(f"Searching Spotify for: {query}")
                tracks = player.search_spotify(query)
                if tracks:
                    print("\nSpotify Search Results:")
                    for i, track in enumerate(tracks):
                        print(f"{i+1}. {track.title} - {track.artist} ({track.album})")
                    
                    try:
                        track_choice = input("\nSelect track number to play (or Enter to cancel): ").strip()
                        if track_choice.isdigit():
                            idx = int(track_choice) - 1
                            if 0 <= idx < len(tracks):
                                player.playlist = tracks
                                player.play_track(tracks[idx])
                                print(f"Playing: {player.current_track.title}")
                    except ValueError:
                        pass
                else:
                    print("No tracks found or Spotify not configured")
            else:
                print("Please provide a search query")
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(player.local_tracks):
                if player.local_tracks[idx] not in player.playlist:
                    player.playlist.append(player.local_tracks[idx])
                player.play_track(player.local_tracks[idx])
                print(f"Playing: {player.current_track.title}")
            else:
                print("Invalid track number")
        else:
            print("Unknown command")

class ASCIIVisualizer:
    def __init__(self, player, stdscr):
        self.player = player
        self.stdscr = stdscr
        self.running = False
        self.thread = None
        self.fft_data = np.zeros(64)
        self.patterns = [
            self._pattern_bars,
            self._pattern_wave,
            self._pattern_spectrum
        ]
        self.current_pattern = 0
        self.colors = self._init_colors()

    def _init_colors(self):
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            for i in range(1, curses.COLORS):
                curses.init_pair(i, i, -1)
            return True
        return False

    def start(self):
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def _run(self):
        while self.running:
            if self.player.playing and not self.player.paused:
                self._update_fft_data()
                self._draw()
            time.sleep(0.05)

    def _update_fft_data(self):
        self.fft_data = np.random.rand(64) * 0.5
        for i in range(5):
            pos = random.randint(0, 63)
            self.fft_data[pos] = random.random() * 0.5 + 0.5

    def _draw(self):
        try:
            self.stdscr.erase()
            height, width = self.stdscr.getmaxyx()
            
            self._draw_header(height, width)
            
            if height > 6 and width > 10:
                pattern_func = self.patterns[self.current_pattern]
                pattern_func(height, width)
            
            self._draw_footer(height, width)
            
            self.stdscr.refresh()
        except curses.error:
            pass

    def _draw_header(self, height, width):
        if self.player.current_track:
            status = "▶" if self.player.playing and not self.player.paused else "⏸"
            title = f"{status} {self.player.current_track.title}"
            artist = f"♫ {self.player.current_track.artist}"
            vol = f"Vol: {int(self.player.volume * 100)}%"
            
            max_title = width - len(vol) - 3
            self.stdscr.addstr(0, 0, title[:max_title])
            self.stdscr.addstr(0, width - len(vol), vol)
            self.stdscr.addstr(1, 0, artist[:width-1])

    def _draw_footer(self, height, width):
        if height < 5 or width < 10:
            return
        
        if self.player.current_track and self.player.current_track.duration > 0:
            progress = self.player.position / self.player.current_track.duration
            bar_width = width - 10
            filled = int(bar_width * progress)
            progress_bar = "[" + "■" * filled + " " * (bar_width - filled) + "]"
            time_str = f"{self._format_time(self.player.position)} / {self._format_time(self.player.current_track.duration)}"
            self.stdscr.addstr(height-3, 0, progress_bar)
            self.stdscr.addstr(height-3, len(progress_bar)+1, time_str)
        
        controls = [
            "SPACE: Play/Pause",
            "N: Next",
            "P: Previous",
            "V: Visuals",
            "+/-: Volume",
            "Q: Quit"
        ]
        y = height - 2
        x = 0
        for control in controls:
            if x + len(control) < width - 1:
                self.stdscr.addstr(y, x, control)
                x += len(control) + 2

    def _format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def _pattern_bars(self, height, width):
        bar_count = min(width, len(self.fft_data))
        start_y = 3
        viz_height = height - 6
        
        for i in range(bar_count):
            amp = self.fft_data[i]
            bar_height = int(amp * viz_height)
            color = int(amp * 100) % (curses.COLORS - 1) + 1 if self.colors else 0
            
            for j in range(bar_height):
                y = start_y + viz_height - j - 1
                if y < height - 4:
                    char = '█' if j == bar_height - 1 else '░'
                    if color:
                        self.stdscr.addstr(y, i, char, curses.color_pair(color))
                    else:
                        self.stdscr.addstr(y, i, char)

    def _pattern_wave(self, height, width):
        start_y = 3
        viz_height = height - 6
        mid_y = start_y + viz_height // 2
        
        for i in range(width):
            amp = self.fft_data[i % len(self.fft_data)]
            y = int(mid_y + amp * (viz_height // 2 - 1))
            y = max(start_y, min(y, start_y + viz_height - 1))
            
            if self.colors:
                color = int(amp * 100) % (curses.COLORS - 1) + 1
                self.stdscr.addstr(y, i, '●', curses.color_pair(color))
            else:
                self.stdscr.addstr(y, i, '●')

    def _pattern_spectrum(self, height, width):
        start_y = 3
        viz_height = height - 6
        chars = ' ▁▂▃▄▅▆▇'
        
        for i in range(width):
            amp = self.fft_data[i % len(self.fft_data)]
            char_idx = min(int(amp * (len(chars) - 1)), len(chars) - 1)
            color = int(amp * 100) % (curses.COLORS - 1) + 1 if self.colors else 0
            
            for j in range(viz_height):
                y = start_y + viz_height - j - 1
                if j <= char_idx:
                    if color:
                        self.stdscr.addstr(y, i, chars[j], curses.color_pair(color))
                    else:
                        self.stdscr.addstr(y, i, chars[j])

    def next_pattern(self):
        self.current_pattern = (self.current_pattern + 1) % len(self.patterns)


def main_ui(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    
    player = Player()
    visualizer = ASCIIVisualizer(player, stdscr)
    player.attach_visualizer(visualizer)
    visualizer.start()
    
    running = True
    while running:
        try:
            key = stdscr.getch()
            
            if key == ord('q'):
                running = False
            elif key == ord(' '):
                if player.playing:
                    if player.paused:
                        player.resume()
                    else:
                        player.pause()
                elif player.playlist:
                    player.play_track(player.playlist[0])
                elif player.local_tracks:
                    player.playlist = player.local_tracks[:10]
                    player.play_track(player.playlist[0])
            elif key == ord('n'):
                player.next_track()
            elif key == ord('p'):
                player.prev_track()
            elif key == ord('v'):
                visualizer.next_pattern()
            elif key == ord('+'):
                player.set_volume(player.volume + 0.05)
            elif key == ord('-'):
                player.set_volume(player.volume - 0.05)
            elif key == ord('r'):
                player.play_random()
                
        except curses.error:
            pass
    
    visualizer.stop()
    player.stop()


def get_lyrics(artist, title):
    player = Player()
    lyrics = player.get_lyrics(artist, title)
    print(f"Lyrics for {title} by {artist}:\n")
    print(lyrics)


def play_random():
    def _handle_ui(stdscr):
        player = Player()
        visualizer = ASCIIVisualizer(player, stdscr)
        player.attach_visualizer(visualizer)
        visualizer.start()
        
        player.play_random()
        
        running = True
        while running:
            try:
                key = stdscr.getch()
                if key == ord('q'):
                    running = False
                elif key == ord(' '):
                    if player.paused:
                        player.resume()
                    else:
                        player.pause()
                elif key == ord('n'):
                    player.play_random()
                elif key == ord('v'):
                    visualizer.next_pattern()
            except curses.error:
                pass
        
        visualizer.stop()
        player.stop()
    
    curses.wrapper(_handle_ui)


def search_spotify(query):
    player = Player()
    tracks = player.search_spotify(query)
    
    if not tracks:
        print("No tracks found or Spotify not configured")
        return
    
    print(f"Search results for '{query}':")
    for i, track in enumerate(tracks):
        print(f"{i+1}. {track.title} - {track.artist} ({track.album})")
    
    try:
        choice = int(input("\nSelect a track to play (0 to cancel): "))
        if 1 <= choice <= len(tracks):
            def _handle_ui(stdscr):
                ui_player = Player()
                ui_player.playlist = tracks
                visualizer = ASCIIVisualizer(ui_player, stdscr)
                ui_player.attach_visualizer(visualizer)
                visualizer.start()
                
                ui_player.play_track(tracks[choice-1])
                
                running = True
                while running:
                    try:
                        key = stdscr.getch()
                        if key == ord('q'):
                            running = False
                        elif key == ord(' '):
                            if ui_player.paused:
                                ui_player.resume()
                            else:
                                ui_player.pause()
                        elif key == ord('n'):
                            ui_player.next_track()
                        elif key == ord('p'):
                            ui_player.prev_track()
                        elif key == ord('v'):
                            visualizer.next_pattern()
                    except curses.error:
                        pass
                
                visualizer.stop()
                ui_player.stop()
            
            curses.wrapper(_handle_ui)
    except ValueError:
        print("Invalid selection")


def parse_arguments():

    parser = argparse.ArgumentParser(description="CliTunes - Terminal-Based Music Player")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    play_parser = subparsers.add_parser("play", help="Play music with visualizer")
    random_parser = subparsers.add_parser("random", help="Play random track")
    lyrics_parser = subparsers.add_parser("lyrics", help="Fetch lyrics for a song")
    lyrics_parser.add_argument("title", help="Song title")
    lyrics_parser.add_argument("--artist", "-a", help="Artist name", default="")
    search_parser = subparsers.add_parser("search", help="Search for tracks on Spotify")
    search_parser.add_argument("query", help="Search query")
    
    return parser.parse_args()


def main():
    args = parse_arguments()
    
    if args.command == "play" or args.command is None:
        try:
            curses.wrapper(main_ui)
        except:
            text_based_ui()
    elif args.command == "random":
        try:
            play_random()
        except:
            print("Trying to play random track...")
            player = Player()
            if player.local_tracks:
                track = random.choice(player.local_tracks)
                print(f"Playing random track: {track.title}")
                player.play_track(track)
                print("Press Ctrl+C to stop")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\nStopping playback")
            else:
                print("No local tracks available")
    elif args.command == "lyrics":
        artist = args.artist if args.artist else ""
        get_lyrics(artist, args.title)
    elif args.command == "search":
        search_spotify(args.query)

if __name__ == "__main__":
    main()
