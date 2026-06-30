from app.services.preprocessing.config import AudioPreprocessingConfig
from app.services.preprocessing.filter import (
    AudioLengthFilter,
    AudioNoiseReducer,
    AudioSilenceFilter,
)
from app.services.preprocessing.loader import LocalAudioLoader
from app.services.preprocessing.resampler import AudioResampler
from app.services.preprocessing.saver import AudioSaver
from app.services.model import PreprocessedAudio


def run_audio_preprocessing(path_audio, target_path) -> None:
    config = AudioPreprocessingConfig()

    loader = LocalAudioLoader()
    resampler = AudioResampler()
    length_filter = AudioLengthFilter()
    silence_filter = AudioSilenceFilter()
    noise_reducer = AudioNoiseReducer()
    saver = AudioSaver()

    audio_files = list(path_audio.glob("*.wav"))

    if not audio_files:
        print(f"No audio files found in: {path_audio}")
        return

    list_preprocessed_audio = []

    for audio_file in audio_files:
        print(f"Processing: {audio_file}")

        # Load audio
        audio, original_sample_rate = loader.load(audio_file)

        # Resample audio
        audio = resampler.resample(
            audio=audio,
            original_sample_rate=original_sample_rate,
            target_sample_rate=config.target_sample_rate,
        )

        # Apply filters (length, silence, noise reduction)
        if config.apply_length_filter:
            is_valid_length = length_filter.is_valid(
                audio=audio,
                sample_rate=config.target_sample_rate,
                min_duration_seconds=config.min_duration_seconds,
                max_duration_seconds=config.max_duration_seconds,
            )

            if not is_valid_length:
                print(f"Skipped because of length filter: {audio_file}")
                continue

        if config.apply_silence_filter:
            is_valid_signal = silence_filter.is_valid(
                audio=audio,
                silence_rms_threshold=config.silence_rms_threshold,
            )

            if not is_valid_signal:
                print(f"Skipped because of silence filter: {audio_file}")
                continue

        if config.apply_noise_reduction:
            audio = noise_reducer.reduce_noise(
                audio=audio,
                noise_reduction_strength=config.noise_reduction_strength,
            )

        # Save processed audio
        saved_path = saver.save(
            audio=audio,
            sample_rate=config.target_sample_rate,
            source_path=audio_file,
            output_dir=target_path,
        )

        uuid = saver.extract_uuid_from_filename(audio_file)

        preprocessed_audio = PreprocessedAudio(uuid=uuid, audio=audio)

        list_preprocessed_audio.append(preprocessed_audio)

        print(f"Saved: {saved_path}")

    return list_preprocessed_audio


if __name__ == "__main__":
    run_audio_preprocessing()
