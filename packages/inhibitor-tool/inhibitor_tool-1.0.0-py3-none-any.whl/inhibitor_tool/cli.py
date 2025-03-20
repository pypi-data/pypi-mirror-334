import argparse
from inhibitor_tool.inhibitor import inhibit


def main():
    parser = argparse.ArgumentParser(description="Send an inhibition request.")
    parser.add_argument(
        "content",
        type=str,
        help="Content to inhibit (at least 10 characters, no spaces).",
    )
    parser.add_argument(
        "ttl",
        type=int,
        nargs="?",
        default=3,
        help="TTL in hours (default: 3, max: 72).",
    )

    args = parser.parse_args()
    inhibit(args.content, args.ttl)


if __name__ == "__main__":
    main()
