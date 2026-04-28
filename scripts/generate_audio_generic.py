r"""
generate_audio_generic.py
Usage:
    python scripts\generate_audio_generic.py --script <path> [--output <dir>] [--chunk-size <chars>]

    --script      Path to TTS-formatted .md script file (required)
    --output      Directory for MP3 clips (default: audio_clips/ next to script)
    --chunk-size  Max characters per API call (default: 500 ~ 30 seconds)
                  Splits at natural sentence boundaries — never mid-sentence.

Working directory: any repo root (all paths may be absolute or relative).

Sub-chunking strategy:
  Long blocks are split at sentence endings (. ? ! ...) into ~30-second pieces.
  Each sub-chunk gets its own API call and a lettered suffix: 01a, 01b, 02a, etc.
  The stitcher (ffmpeg) joins them in alphabetical order — seamless playback.

Environment:
  Requires OPENAI_API_KEY. If your shell does not have it, run .\env_setter.ps1 from your StudyBook repo first.
"""

import os
import sys
import re
import base64
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


# ── Voice override helpers ───────────────────────────────────────────────────

def parse_mapping_entries(raw_entries: list[str], label: str) -> dict[str, str]:
    """
    Parse repeated CLI entries like ["SEAN=cedar", "HOST=nova"] into a dictionary.
    """
    mapping: dict[str, str] = {}
    for entry in raw_entries:
        if "=" not in entry:
            raise ValueError(f"Invalid {label} entry '{entry}'. Expected format KEY=VALUE.")
        key, value = entry.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise ValueError(f"Invalid {label} entry '{entry}'. Empty key/value not allowed.")
        mapping[key] = value
    return mapping


def apply_voice_overrides(
    blocks: list[dict],
    speaker_voice_map: dict[str, str],
    voice_replace_map: dict[str, str],
) -> list[dict]:
    """
    Apply overrides in order:
      1) voice_replace_map: by existing voice token (e.g., onyx -> cedar)
      2) speaker_voice_map: by speaker name (e.g., SEAN -> cedar), highest priority
    """
    resolved = []
    for block in blocks:
        updated = dict(block)
        voice = updated["voice"]

        if voice in voice_replace_map:
            voice = voice_replace_map[voice]

        speaker = updated["speaker"]
        if speaker in speaker_voice_map:
            voice = speaker_voice_map[speaker]

        updated["voice"] = voice
        resolved.append(updated)
    return resolved


# ── Sentence boundary splitter ────────────────────────────────────────────────

def split_at_sentences(text: str, max_chars: int) -> list[str]:
    """
    Split text into chunks of at most max_chars.
    Always splits at a sentence boundary — never mid-sentence.
    Sentence endings: period, ellipsis, question mark, exclamation mark
    followed by a space or end of string.

    If a single sentence exceeds max_chars it is kept whole (not split mid-word).
    """
    if len(text) <= max_chars:
        return [text.strip()]

    # Split into sentences using a regex that keeps the delimiter attached
    sentence_pattern = re.compile(r'(?<=[.?!…])\s+|(?<=\.\.\.)\s+')
    raw_sentences = sentence_pattern.split(text)

    # Re-attach any trailing punctuation that got separated
    sentences = [s.strip() for s in raw_sentences if s.strip()]

    chunks = []
    current = ""

    for sentence in sentences:
        candidate = (current + " " + sentence).strip() if current else sentence
        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                chunks.append(current.strip())
            # If single sentence > max_chars, keep it whole — don't split words
            current = sentence

    if current:
        chunks.append(current.strip())

    return chunks


# ── Script parser ─────────────────────────────────────────────────────────────

def parse_script(script_path: Path) -> list[dict]:
    """
    Parse **[SPEAKER — voice: voice_name]** blocks.
    Returns list of {speaker, voice, text} dicts.
    """
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
        elif (current_speaker
              and line_stripped
              and not line_stripped.startswith("---")
              and "END OF SCRIPT" not in line_stripped
              and not line_stripped.startswith("## API")):
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


# ── Sub-chunk expander ────────────────────────────────────────────────────────

def expand_blocks(blocks: list[dict], max_chars: int) -> list[dict]:
    """
    For any block longer than max_chars, split into sub-chunks at sentence boundaries.
    Labels: block 1 → 01a, 01b, 01c ...  block 2 → 02a, 02b ...
    Short blocks (fit in one chunk) get label suffix 'a' only.
    """
    expanded = []
    for block_idx, block in enumerate(blocks):
        chunks = split_at_sentences(block["text"], max_chars)
        suffixes = [chr(ord('a') + i) for i in range(len(chunks))]
        for chunk_text, suffix in zip(chunks, suffixes):
            expanded.append({
                "speaker":    block["speaker"],
                "voice":      block["voice"],
                "text":       chunk_text,
                "block_num":  block_idx + 1,
                "suffix":     suffix,
                "is_split":   len(chunks) > 1,
            })
    return expanded


# ── Audio generation ──────────────────────────────────────────────────────────

def generate_audio(
    script_path: Path,
    output_dir: Path,
    max_chars: int,
    request_timeout_seconds: float,
    fail_fast: bool,
    speaker_voice_map: dict[str, str],
    voice_replace_map: dict[str, str],
    sample_chunks: int,
) -> int:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found. Run .\\env_setter.ps1 from D:\\StudyBook\\ first.")
        return

    client = OpenAI(api_key=api_key, timeout=request_timeout_seconds)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_blocks = parse_script(script_path)
    if not raw_blocks:
        print("ERROR: No speaker blocks found. Check format: **[SPEAKER — voice: voice_name]**")
        return 2

    resolved_blocks = apply_voice_overrides(
        raw_blocks,
        speaker_voice_map=speaker_voice_map,
        voice_replace_map=voice_replace_map,
    )

    chunks = expand_blocks(resolved_blocks, max_chars)
    if sample_chunks > 0:
        chunks = chunks[:sample_chunks]

    failed_chunks = []

    # Report split summary
    split_count = sum(1 for c in chunks if c["is_split"])
    print(f"Script:       {script_path.name}")
    print(f"Output:       {output_dir}")
    print(f"Raw blocks:   {len(raw_blocks)}")
    print(f"Chunks total: {len(chunks)}  ({split_count} sub-chunked blocks)")
    print(f"Chunk limit:  {max_chars} chars (~30 sec)")
    if voice_replace_map:
        print(f"Voice map:    {voice_replace_map}")
    if speaker_voice_map:
        print(f"Speaker map:  {speaker_voice_map}")
    if sample_chunks > 0:
        print(f"Sample mode:  first {sample_chunks} chunk(s) only")
    print()

    total = len(chunks)
    for i, chunk in enumerate(chunks):
        block_num = chunk["block_num"]
        suffix    = chunk["suffix"]
        speaker   = chunk["speaker"]
        voice     = chunk["voice"]
        text      = chunk["text"]

        label    = f"{block_num:02d}{suffix}"
        filename = output_dir / f"{label}_{speaker.replace(' ', '_')}.mp3"

        char_count = len(text)
        split_tag  = f" [split {suffix}]" if chunk["is_split"] else ""
        print(f"[{i+1:02d}/{total}] Block {label} — {speaker} ({voice}) — {char_count} chars{split_tag}")

        if filename.exists():
            print(f"         -> EXISTS, skipping: {filename.name}")
            continue

        # chat.completions reliably supports audio-preview models in this flow.
        # Try audio-preview first to avoid repeated 404s from mini-tts.
        chunk_saved = False
        for model in ["gpt-4o-mini-audio-preview", "gpt-4o-mini-tts"]:
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
                audio_b64  = response.choices[0].message.audio.data
                audio_bytes = base64.b64decode(audio_b64)
                with open(filename, "wb") as f:
                    f.write(audio_bytes)
                print(f"         -> Saved: {filename.name}  (model: {model})")
                chunk_saved = True
                break
            except BaseException as e:
                print(f"         -> {model} failed: {e}")
                if model == "gpt-4o-mini-audio-preview":
                    # Fallback to the secondary model on next iteration.
                    continue

        if not chunk_saved:
            failed_chunks.append(label)
            print(f"         -> Both models failed for chunk {label}.")
            if fail_fast:
                print("ERROR: fail-fast is enabled. Stopping at first failed chunk.")
                return 3

    mp3_files = sorted(output_dir.glob("*.mp3"))
    print()
    print(f"Done. {len(mp3_files)} MP3 files in {output_dir}")
    if failed_chunks:
        print(f"ERROR: Failed chunks: {', '.join(failed_chunks)}")
        return 3
    print()
    print("Next — stitch in order (PowerShell from D:\\StudyBook\\):")
    print(f'  $clips = Get-ChildItem "{output_dir}" -Filter "*.mp3" | Sort-Object Name')
    print(f'  $clips | ForEach-Object {{ "file \'$($_.FullName)\'" }} | Out-File -Encoding utf8 "{output_dir}\\filelist.txt"')
    slug = script_path.stem.replace("audio_script_", "")
    print(f'  ffmpeg -f concat -safe 0 -i "{output_dir}\\filelist.txt" -c copy "{output_dir.parent}\\final_{slug}.mp3"')
    return 0


# ── Entry point ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate GPT-4o TTS audio from a formatted script .md file. "
                    "Splits long blocks at sentence boundaries (~30 sec each)."
    )
    parser.add_argument("--script",     required=True, help="Path to audio script .md file")
    parser.add_argument("--output",     default=None,  help="Output directory for MP3 clips")
    parser.add_argument("--chunk-size", type=int, default=500,
                        help="Max chars per API call (default 500 ~ 30 sec). Split at sentence boundaries.")
    parser.add_argument(
        "--request-timeout-seconds",
        type=float,
        default=120.0,
        help="Per-request timeout in seconds (default: 120).",
    )
    parser.add_argument(
        "--no-fail-fast",
        action="store_true",
        help="Continue processing after failed chunks (default behavior is fail-fast).",
    )
    parser.add_argument(
        "--speaker-voice",
        action="append",
        default=[],
        help="Override voice by speaker. Repeatable. Example: --speaker-voice SEAN=cedar",
    )
    parser.add_argument(
        "--voice-replace",
        action="append",
        default=[],
        help="Replace one voice token with another. Repeatable. Example: --voice-replace onyx=cedar",
    )
    parser.add_argument(
        "--sample-chunks",
        type=int,
        default=0,
        help="Generate only the first N chunks for quick A/B voice testing (default: 0 = full script).",
    )
    args = parser.parse_args()

    script_path = Path(args.script).resolve()
    if not script_path.exists():
        print(f"ERROR: Script not found: {script_path}")
        return
    try:
        speaker_voice_map = parse_mapping_entries(args.speaker_voice, "speaker-voice")
        voice_replace_map = parse_mapping_entries(args.voice_replace, "voice-replace")
    except ValueError as e:
        print(f"ERROR: {e}")
        return

    if args.sample_chunks < 0:
        print("ERROR: --sample-chunks must be >= 0")
        return

    output_dir = Path(args.output).resolve() if args.output else script_path.parent / "audio_clips"
    exit_code = generate_audio(
        script_path=script_path,
        output_dir=output_dir,
        max_chars=args.chunk_size,
        request_timeout_seconds=args.request_timeout_seconds,
        fail_fast=not args.no_fail_fast,
        speaker_voice_map=speaker_voice_map,
        voice_replace_map=voice_replace_map,
        sample_chunks=args.sample_chunks,
    )
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()


