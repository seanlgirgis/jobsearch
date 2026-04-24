"""
generate_audio_generic.py
Usage:
    python scripts/generate_audio_generic.py --script <path_to_audio_script.md> [--output <output_dir>]

    --script   Path to the TTS-formatted .md script file (required)
    --output   Directory to save MP3 clips (optional — defaults to audio_clips/ next to script)

Reads **[SPEAKER — voice: voice_name]** blocks from the script.
Calls gpt-4o-mini-tts (or gpt-4o-mini-audio-preview fallback) per block.
Saves numbered MP3s. Skips existing files so you can resume on failure.

Pipeline:
  1. Generate A1 script (via Codex/Gemini using A1 prompt from learning_artifact_prompt_template.md)
  2. Save script to: data/interview_prep/audio_prep/{topic_slug}/audio_script_{topic_slug}.md
  3. Run: python scripts/generate_audio_generic.py --script <path>
  4. Stitch MP3s in output dir (use Audacity, ffmpeg concat, or similar)

Environment:
  Requires OPENAI_API_KEY in .env or environment.
  Run env_setter.ps1 first if not already loaded.
"""

import os
import re
import base64
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


def parse_script(script_path: Path) -> list[dict]:
    """Parse **[SPEAKER — voice: voice_name]** blocks from script file."""
    blocks = []
    current_speaker = None
    current_voice = None
    current_text = []

    with open(script_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        line_stripped = line.strip()
        speaker_match = re.match(r"\*\*\[(.*?)\s*[—-]\s*voice:\s*(.*?)\]\*\*", line_stripped)

        if speaker_match:
            if current_speaker and current_text:
                text = " ".join(current_text).strip()
                if text:
                    blocks.append({
                        "speaker": current_speaker,
                        "voice": current_voice,
                        "text": text
                    })
            current_speaker = speaker_match.group(1).strip()
            current_voice = speaker_match.group(2).strip()
            current_text = []
        elif current_speaker and line_stripped and not line_stripped.startswith("---") and "END OF SCRIPT" not in line_stripped and not line_stripped.startswith("## API"):
            current_text.append(line_stripped)

    # Flush last block
    if current_speaker and current_text:
        text = " ".join(current_text).strip()
        if text:
            blocks.append({
                "speaker": current_speaker,
                "voice": current_voice,
                "text": text
            })

    return blocks


def generate_audio(script_path: Path, output_dir: Path):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found. Run env_setter.ps1 first.")
        return

    client = OpenAI(api_key=api_key)
    output_dir.mkdir(parents=True, exist_ok=True)

    blocks = parse_script(script_path)
    if not blocks:
        print("ERROR: No speaker blocks found in script. Check format: **[SPEAKER — voice: voice_name]**")
        return

    print(f"Script: {script_path.name}")
    print(f"Output: {output_dir}")
    print(f"Blocks found: {len(blocks)}")
    print()

    for i, block in enumerate(blocks):
        idx = i + 1
        speaker = block["speaker"]
        voice = block["voice"]
        text = block["text"]

        filename = output_dir / f"{idx:02d}_{speaker.replace(' ', '_')}.mp3"
        print(f"[{idx:02d}/{len(blocks)}] {speaker} ({voice}) — {len(text)} chars")

        if filename.exists():
            print(f"         -> EXISTS, skipping: {filename.name}")
            continue

        # Try gpt-4o-mini-tts first, fall back to audio-preview
        for model in ["gpt-4o-mini-tts", "gpt-4o-mini-audio-preview"]:
            try:
                response = client.chat.completions.create(
                    model=model,
                    modalities=["text", "audio"],
                    audio={"voice": voice, "format": "mp3"},
                    messages=[
                        {
                            "role": "user",
                            "content": f"Please read the following text aloud:\n\n{text}"
                        }
                    ]
                )
                audio_b64 = response.choices[0].message.audio.data
                audio_bytes = base64.b64decode(audio_b64)
                with open(filename, "wb") as f:
                    f.write(audio_bytes)
                print(f"         -> Saved: {filename.name} (model: {model})")
                break
            except Exception as e:
                print(f"         -> {model} failed: {e}")
                if model == "gpt-4o-mini-audio-preview":
                    print(f"         -> Both models failed for block {idx}. Continuing.")

    print()
    print(f"Done. {len(list(output_dir.glob('*.mp3')))} MP3 files in {output_dir}")
    print(f"Next: stitch files in order with ffmpeg or Audacity.")
    print(f"  ffmpeg concat example:")
    print(f"    cd \"{output_dir}\"")
    print(f"    (for %f in (*.mp3) do @echo file '%f') > filelist.txt")
    print(f"    ffmpeg -f concat -safe 0 -i filelist.txt -c copy final_{script_path.stem}.mp3")


def main():
    parser = argparse.ArgumentParser(description="Generate GPT-4o TTS audio from a formatted script .md file.")
    parser.add_argument("--script", required=True, help="Path to the audio script .md file")
    parser.add_argument("--output", default=None, help="Output directory for MP3 clips (default: audio_clips/ next to script)")
    args = parser.parse_args()

    script_path = Path(args.script).resolve()
    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        return

    output_dir = Path(args.output).resolve() if args.output else script_path.parent / "audio_clips"
    generate_audio(script_path, output_dir)


if __name__ == "__main__":
    main()
