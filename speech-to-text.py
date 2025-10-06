import os
from pydub import AudioSegment
from faster_whisper import WhisperModel

# ---------------- CONFIGURAZIONE ----------------
AUDIO_FILE = "input_file.wav"    # file di input
MODEL_SIZE = "small"              # small/medium/large
OUTPUT_FILE = "trascrizione_completa.txt"
MAX_SEGMENT_DURATION_MS = 30 * 60 * 1000  # 30 minuti in ms
LANGUAGE = "it"
# ------------------------------------------------

# Carica modello
model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="float32")

# Carica audio
audio = AudioSegment.from_file(AUDIO_FILE)

audio_length_ms = len(audio)

# Funzione per spezzare audio senza tagliare a metà frase
def split_audio_by_silence(audio, min_silence_len=700, silence_thresh=-40):
    """
    Restituisce una lista di AudioSegment spezzati sui silenzi.
    min_silence_len: durata minima di silenzio per considerarlo pausa (ms)
    silence_thresh: dB sotto il volume massimo per considerare silenzio
    """
    from pydub.silence import split_on_silence
    segments = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=500  # mantiene mezzo secondo di silenzio alla fine
    )
    return segments

# Spezza audio sui silenzi
print("Spezzando audio sui silenzi...")
segments = split_audio_by_silence(audio)
print(f"Numero di segmenti rilevati: {len(segments)}")

# Trascrizione
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    total_time_ms = 0
    for i, segment in enumerate(segments):
        # Salva segmento temporaneo
        temp_file = f"temp_segment_{i}.mp3"
        segment.export(temp_file, format="mp3")
        print(f"Trascrivo segmento {i+1}/{len(segments)}...")

        # Trascrizione
        segs, info = model.transcribe(temp_file, language=LANGUAGE)

        # Scrivi testo nel file
        for seg in segs:
            f.write(seg.text.strip() + " ")

            # Aggiorna tempo totale
            total_time_ms += (seg.end - seg.start) * 1000

            # Inserisci timestamp ogni 30 minuti
            if total_time_ms >= MAX_SEGMENT_DURATION_MS:
                minutes = int(total_time_ms // 60000)
                f.write(f"\n\n[Tempo: {minutes} minuti]\n\n")
                total_time_ms = 0

        f.write("\n\n")
        os.remove(temp_file)

print("Trascrizione completata!")
