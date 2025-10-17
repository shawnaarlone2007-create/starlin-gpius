import argparse
from .agent import Agent
from .tools import list_tools


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="replica-ai",
        description="Replica AI agent CLI (scaffold)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="Run the agent")
    run_p.add_argument(
        "-m",
        "--model",
        default="gpt-4o-mini",
        help="LLM model identifier to use",
    )
    run_p.add_argument(
        "-s",
        "--system-prompt",
        default=None,
        help="Override the default system prompt",
    )

    tools_p = sub.add_parser("tools", help="List available tools")

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        agent = Agent(model=args.model, system_prompt=args.system_prompt)
        agent.run()
        return

    if args.command == "tools":
        for tool in list_tools():
            name = tool.get("name", "unknown")
            desc = tool.get("description", "")
            print(f"{name}: {desc}")
        return

    parser.print_help()
