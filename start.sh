source miniconda3/bin/activate
conda activate whisper
python whisper_fastapi_online_server.py --host 0.0.0.0 --port 8000 --warmup-file ./jfk.wav
