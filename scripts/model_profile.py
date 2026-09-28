"""List, inspect or select a local model profile. No API requests or credential reads."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Make invocation independent of the shell's cwd and PYTHONPATH.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.ai.model_profiles import (  # noqa: E402
    CONFIG_DIR,
    ProfileError,
    get_profile,
    load_profiles,
    select_profile,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config-dir", type=Path, default=CONFIG_DIR)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="List configured profile names and settings")
    commands.add_parser("show", help="Show the active profile")
    use = commands.add_parser("use", help="Save the active profile in the local config")
    use.add_argument("profile")
    args = parser.parse_args(argv)
    try:
        if args.command == "use":
            profile = select_profile(args.profile, args.config_dir)
            print(f"Active profile: {args.profile}")
            if any(target.model is None for target in profile.targets):
                print(
                    "Selection saved. Set actual model IDs in model_profiles.local.json before chat."
                )
            return 0
        config = load_profiles(args.config_dir)
        if args.command == "show":
            # Deliberate allowlist; do not dump arbitrary config data or descriptions.
            profile = get_profile(config)
            print(
                json.dumps(
                    {
                        "active_profile": config.active_profile,
                        "primary": profile.primary.model_dump(),
                        "fallbacks": [target.model_dump() for target in profile.fallbacks],
                        "temperature": profile.temperature,
                        "max_output_tokens": profile.max_output_tokens,
                        "structured_output": profile.structured_output,
                        "allow_artifacts": profile.allow_artifacts,
                    },
                    indent=2,
                )
            )
        else:
            for name, profile in config.profiles.items():
                marker = "*" if name == config.active_profile else " "
                model = profile.primary.model or "<configure model ID>"
                print(
                    f"{marker} {name}: {profile.primary.provider} / {model}; "
                    f"tokens={profile.max_output_tokens}; JSON={profile.structured_output}; "
                    f"fallbacks={len(profile.fallbacks)}; artifacts={profile.allow_artifacts}"
                )
        return 0
    except ProfileError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
