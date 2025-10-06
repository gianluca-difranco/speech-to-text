# Trascrizione Audio con Python e Whisper / Faster-Whisper

Questo script permette di trascrivere **audio** (anche in italiano), suddividendo l’audio sui silenzi per evitare tagli a metà frase.

Lo script utilizza `faster-whisper` (o `whisper`) e `pydub` per gestire l’audio.

---

## 📝 Prerequisiti

1. **Python ≥ 3.8** installato.
2. **ffmpeg** installato e nel PATH di sistema.
   - Windows: scarica da [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
   - Assicurati che `ffmpeg.exe` e `ffprobe.exe` siano accessibili globalmente.
   - Verifica con:
     ```bash
     ffmpeg -version
     ```
3. Librerie Python:
   ```bash
   pip install faster-whisper pydub
   ```
4. **(Opzionale) GPU NVIDIA**: per velocizzare la trascrizione.
   - CUDA Toolkit compatibile
   - cuDNN compatibile
   - PATH aggiornato con le librerie CUDA/cuDNN
   - Verifica con:
     ```bash
     nvidia-smi
     ```

---

## ⚙️ Variabili d’ambiente per configurazione modello

Per rendere lo script flessibile, puoi usare due variabili d’ambiente:

| Variabile | Descrizione | Esempio |
|------------|------------|---------|
| `WHISPER_DEVICE` | Dispositivo su cui eseguire il modello (`cpu` o `cuda`) | `cpu` o `cuda` |
| `WHISPER_COMPUTE_TYPE` | Tipo di calcolo del modello (`float32`, `float16`, `int8`, ecc.) | `float32` per CPU, `float16` per GPU compatibile |

**Esempio su Windows (PowerShell):**
```powershell
setx WHISPER_DEVICE cpu
setx WHISPER_COMPUTE_TYPE float32
```

> Dopo aver impostato le variabili, **chiudi e riapri il terminale / PyCharm** per renderle effettive.

---

## 🖥️ Esempio di utilizzo

```bash
python speech-to-text.py
```

- L’audio di input deve essere posizionato nella stessa cartella dello script o specificato con il percorso corretto.
- Il file di output sarà generato come `trascrizione_completa.txt`.
- Lo script:
  - Spezza l’audio sui silenzi per non tagliare le frasi
  - Trascrive in italiano
  - Aggiunge un timestamp ogni 30 minuti

---

## 💡 Note Importanti

- Se non hai GPU o vuoi semplicità, usa `cpu` e `float32`.
- Se hai GPU compatibile e vuoi velocità, usa `cuda` e `float16`.
- Lo script funziona anche senza GPU, ma sarà più lento.
- ffmpeg è necessario per leggere/esportare audio in vari formati (`mp3`, `wav`, `m4a`).

---

## 📂 Struttura file suggerita

```
project/
│
├─ speech-to-text.py
├─ requirements.txt  
└─ README.md
```

