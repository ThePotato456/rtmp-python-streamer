#!./.venv/bin/python

import ffmpeg, dotenv, subprocess, io, os, argparse

from colorama import init, just_fix_windows_console, Fore, Style
printi = lambda *a, **kw: print(f' {Style.BRIGHT}[{Fore.CYAN}i{Fore.RESET}]{Style.RESET_ALL}', *a, **kw)
printe = lambda *a, **kw: print(f' {Style.BRIGHT}[{Fore.LIGHTRED_EX}-{Fore.RESET}]', *a, **kw)
prints = lambda *a, **kw: print(f' {Style.BRIGHT}[{Fore.LIGHTGREEN_EX}+{Fore.RESET}]', *a, **kw)


def stream_mp4_to_rtmp(input_file, rtmp_url):
    try:
        ffmpeg.input(input_file, ).output(rtmp_url, format='flv', vcodec='libx264').run(capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode('utf-8')}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

import subprocess

def stream_to_owncast(input_file, rtmp_server_url, stream_key, video_bitrate=1800, audio_bitrate=48000):
    ffmpeg_cmd = [
        'ffmpeg',
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
        type=argparse.FileType('r')
    )
    args = parser.parse_args()
    
    if not args.input_file:
        printe(F"No file specified!")
        exit()
    
    input_file: io.TextIOWrapper = args.input_file
    file_name = input_file.name
    
    if input_file is None:
        printe('[main] no file specified')
        exit(2)
    try:
        printi(f"Streaming {file_name} to owncast server...")
        stream_to_owncast(
            input_file=f"{file_name}",
            rtmp_server_url='127.0.0.1:1935',
            stream_key=os.getenv('OWNCAST_STREAMKEY'))
    except KeyboardInterrupt as ke:
        print(f'\n {Style.BRIGHT}[{Fore.LIGHTGREEN_EX}-{Fore.RESET}] Goodbye!')
        exit(1)