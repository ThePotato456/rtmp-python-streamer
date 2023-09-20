# rtmp-python-streamer
Simple program that uses ffmpeg to stream a .mp4 file to Owncast's RTMP server inss

## Requirements
```bash
# Install FFMPEG
sudo apt-get update
sudo apt-get install ffmpeg -y

# Run setup.sh to create python venv and install requirements.
bash setup.sh
```

## Usage
```bash
./rtmp_stream.py input_file
```