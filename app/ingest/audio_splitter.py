#Сие была восьмая попытка а может и деветая попытка нармально поделить (прошу не бить пока не придумал как красиво разбивать аудио)

import argparse
import torch
import numpy as np
from pydub import AudioSegment


SAMPLE_RATE = 16000
MAX_CHUNK_MS = 7000        
EDGE_MS = 250              
MIN_SAVE_MS = 300          


def rms_energy(samples: np.ndarray) -> float:
    return np.sqrt(np.mean(samples ** 2))


def adaptive_trim(chunk: AudioSegment) -> AudioSegment:

    samples = np.array(chunk.get_array_of_samples(), dtype=np.float32) / 32768.0
    if len(samples) == 0:
        return chunk

    total_energy = rms_energy(samples)
    thresh = total_energy * 0.4  
    sr = chunk.frame_rate
    edge_samples = int(sr * EDGE_MS / 1000)

    start_energy = rms_energy(samples[:edge_samples])
    end_energy = rms_energy(samples[-edge_samples:])

    start_cut = EDGE_MS if start_energy < thresh else 0
    end_cut = EDGE_MS if end_energy < thresh else 0

    return chunk[start_cut: len(chunk) - end_cut]


def split_audio_vad(path: str):
    audio = AudioSegment.from_file(path)
    audio = audio.set_frame_rate(SAMPLE_RATE).set_channels(1)

    samples = torch.tensor(
        audio.get_array_of_samples(),
        dtype=torch.float32
    ) / 32768.0

    model, utils = torch.hub.load(
        "snakers4/silero-vad",
        "silero_vad",
        trust_repo=True
    )

    (get_speech_timestamps, _, _, _, _) = utils

    speech_segments = get_speech_timestamps(
        samples,
        model,
        sampling_rate=SAMPLE_RATE,
        min_speech_duration_ms=300,
        min_silence_duration_ms=200
    )

    idx = 0

    for seg in speech_segments:
        start_ms = int(seg["start"] / SAMPLE_RATE * 1000)
        end_ms = int(seg["end"] / SAMPLE_RATE * 1000)

        segment = audio[start_ms:end_ms]

        for offset in range(0, len(segment), MAX_CHUNK_MS):
            part = segment[offset:offset + MAX_CHUNK_MS]

            part = adaptive_trim(part)

            if len(part) >= MIN_SAVE_MS:
                part.export(f"chunk_{idx:04}.wav", format="wav")
                idx += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Maximum-quality audio splitting (VAD + adaptive energy)"
    )
    parser.add_argument(
        "audio",
        help="Path to input audio file (wav/mp3/ogg)"
    )

    args = parser.parse_args()
    split_audio_vad(args.audio)
