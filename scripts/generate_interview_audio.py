import os
import re
import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

def generate_audio():
    # Load environment variables (mostly for OPENAI_API_KEY)
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY is missing from .env file.")
        return

    client = OpenAI(api_key=api_key)

    script_path = Path(r"D:\StudyBook\temp\jobsearch\data\interview_prep\audio_prep\toyota_ramya_2026-04-23\Toyota_Interview_Audio_Script_v2.md")
    output_dir = script_path.parent / "audio_clips"
    output_dir.mkdir(exist_ok=True)

    with open(script_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    blocks = []
    current_speaker = None
    current_voice = None
    current_text = []

    for line in lines:
        line = line.strip()
        
        # Match speaker headers like **[RAMYA — voice: nova]**
        speaker_match = re.match(r"\*\*\[(.*?)\s*—\s*voice:\s*(.*?)\]\*\*", line)
        
        if speaker_match:
            # Save previous block if it exists
            if current_speaker and current_text:
                blocks.append({
                    "speaker": current_speaker,
                    "voice": current_voice,
                    "text": " ".join(current_text).strip()
                })
            
            # Start new block
            current_speaker = speaker_match.group(1)
            current_voice = speaker_match.group(2)
            current_text = []
        elif current_speaker and line and not line.startswith("---") and "END OF SCRIPT" not in line:
            current_text.append(line)

    # Add the last block
    if current_speaker and current_text:
        text = " ".join(current_text).strip()
        if text:
            blocks.append({
                "speaker": current_speaker,
                "voice": current_voice,
                "text": text
            })

    print(f"Found {len(blocks)} dialogue blocks. Generating audio...")

    for i, block in enumerate(blocks):
        idx = i + 1
        speaker = block["speaker"]
        voice = block["voice"]
        text = block["text"]
        
        if not text:
            continue

        filename = output_dir / f"{idx:02d}_{speaker}.mp3"
        print(f"Processing block {idx}/{len(blocks)}: {speaker} (Voice: {voice})")

        # Skip if file already exists (allows you to resume if script fails midway)
        if filename.exists():
            print(f"  -> {filename.name} already exists, skipping.")
            continue

        try:
            # We provide the text to be spoken in the user prompt.
            # Using gpt-4o-mini-audio-preview chat completions with audio modality.
            response = client.chat.completions.create(
                model="gpt-4o-mini-audio-preview",
                modalities=["text", "audio"],
                audio={"voice": voice, "format": "mp3"},
                messages=[
                    {
                        "role": "user",
                        "content": f"Please read the following text aloud:\n\n{text}"
                    }
                ]
            )
            
            # Extract the raw base64 audio and decode it to binary
            audio_data_b64 = response.choices[0].message.audio.data
            audio_bytes = base64.b64decode(audio_data_b64)
            
            with open(filename, "wb") as f:
                f.write(audio_bytes)
                
            print(f"  -> Saved {filename.name}")
        except Exception as e:
            print(f"  -> Error generating block {idx}: {e}")

if __name__ == "__main__":
    generate_audio()
