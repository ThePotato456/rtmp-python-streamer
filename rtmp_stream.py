#!./.venv/bin/python

import ffmpeg, dotenv, subprocess, io, os, argparse, json, time

from colorama import init, just_fix_windows_console, Fore, Style
printi = lambda *a, **kw: print(f' {Style.BRIGHT}[{Fore.CYAN}i{Fore.RESET}]{Style.RESET_ALL}', *a, **kw)
printe = lambda *a, **kw: print(f' {Style.BRIGHT}[{Fore.LIGHTRED_EX}-{Fore.RESET}]', *a, **kw)
prints = lambda *a, **kw: print(f' {Style.BRIGHT}[{Fore.LIGHTGREEN_EX}+{Fore.RESET}]', *a, **kw)

def load_playlist():
    queue = []
    if os.path.exists('./media'):
        movie_list = os.listdir('./media')
        
        for movie in movie_list:
            movie_path = os.path.abspath(os.path.join('./media', movie))
            movie_info = { 'name': movie, 'path': movie_path }
            
            queue.append(movie_info)
        return queue
    else:
        return False

def stream_to_owncast(input_file, rtmp_server_url, stream_key, video_bitrate=1800, audio_bitrate=86000):
    ffmpeg_cmd = [
        'ffmpeg.exe',
        '-hide_banner',
        '-loglevel',
        'error',
        '-re',
        '-i', input_file,
        '-c:v', 'libx264',
        '-b:v', f'{video_bitrate}k',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', str(audio_bitrate),
        '-f', 'flv',
        f'rtmp://{rtmp_server_url}/live/{stream_key}'
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        printe(f"Error: {e}")
        exit(1)
    except Exception as e:
        printe(f"An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    dotenv.load_dotenv()
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_file',
        help=f"Path of the file to be streamed.",
        default=None,
        nargs='?',
        type=argparse.FileType('r')
    )
    args = parser.parse_args()
    
    queue = []
    if args.input_file is None:
        printe(F"No file specified, defaulting to playlist in ./media/")
        queue = load_playlist()
        printi(f"Playlist with {len(queue)} movies loaded.")
        
        for movie in queue:
            printi(f"\t{movie['name']}")
    else:
        input_file: io.TextIOWrapper = args.input_file
        queue.append({ 'name': input_file.name, 'path': os.path.abspath(os.path.join('./media', input_file.name)) })
        
    #print(json.dumps(queue, indent=2))
    try:
        for movie in queue:
            try:
                printi(f"Streaming {movie['name']} to owncast server...")
                stream_to_owncast(
                    input_file=f"{movie['path']}",
                    rtmp_server_url='192.168.1.113:1935',
                    stream_key=os.getenv('OWNCAST_STREAMKEY'))
            except KeyboardInterrupt as ke:
                printe(f"Stopping stream of {movie['name']}, and streaming next. Please wait 1.5 minutes for next film")
                time.sleep(60*1.5)
    except KeyboardInterrupt as ke:
        print(f'\n {Style.BRIGHT}[{Fore.LIGHTGREEN_EX}-{Fore.RESET}] Goodbye!')
        exit(1)