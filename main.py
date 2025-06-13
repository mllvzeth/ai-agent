import os
import sys
from dotenv import load_dotenv
from google import genai
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    try:
        if len(sys.argv) < 2:
            console.print(
                Panel("[bold red]Usage:[/bold red] python main.py <PROMPT>"),
                style="red"
            )
            sys.exit(1)

        prompt = " ".join(sys.argv[1:])
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            console.print(
                Panel("[bold red]Error:[/bold red] GEMINI_API_KEY not found in environment."),
                style="red"
            )
            sys.exit(1)

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", contents=prompt,
        )
        console.print(Panel(response.text, title="Gemini Response", style="green"))
        if hasattr(response, "usage_metadata"):
            if hasattr(response.usage_metadata, "prompt_token_count"):
                console.print(f"[bold]Prompt tokens:[/bold] {response.usage_metadata.prompt_token_count}")
            if hasattr(response.usage_metadata, "candidates_token_count"):
                console.print(f"[bold]Response tokens:[/bold] {response.usage_metadata.candidates_token_count}")
        sys.exit(0)

    except Exception as e:
        console.print(
            Panel(f"[bold red]Error during API call:[/bold red] {e}", style="red"),
            file=sys.stderr
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
