#!/usr/bin/env python3
"""
Super Investing AI Research Agent
Generates concise equity research briefs from corporate document packs.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# Ensure UTF-8 output encoding across all platforms (especially Windows)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

# Load environment variables
load_dotenv()

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("[ERROR] google-genai package not found.")
    print("Install with: pip install google-genai python-dotenv")
    sys.exit(1)


class ResearchAgent:
    """AI agent for equity research brief generation."""

    def __init__(self, api_key: str = None, model: str = None):
        """Initialize the research agent."""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = model or os.getenv('GEMINI_MODEL', 'gemini-3.5-flash')

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not found. Set it in .env file or environment variable."
            )

        self.client = genai.Client(api_key=self.api_key)
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """Load the system prompt from file."""
        prompt_path = Path(__file__).parent / 'system_prompt.txt'

        if not prompt_path.exists():
            raise FileNotFoundError(f"system_prompt.txt not found at {prompt_path}")

        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _find_research_pack_dir(self) -> Path:
        """Find the research pack directory (research_pack/ or files/)."""
        base_dir = Path(__file__).parent

        # Try research_pack first (official assignment structure)
        research_pack = base_dir / 'research_pack'
        if research_pack.exists() and research_pack.is_dir():
            return research_pack

        # Fallback to files/
        files_dir = base_dir / 'files'
        if files_dir.exists() and files_dir.is_dir():
            return files_dir

        raise FileNotFoundError(
            "No research pack directory found. Expected 'research_pack/' or 'files/'"
        )

    def _load_documents(self) -> List[Dict[str, str]]:
        """Load all markdown documents from the research pack."""
        research_dir = self._find_research_pack_dir()
        documents = []

        # Find all .md files
        md_files = sorted(research_dir.glob('*.md'))

        if not md_files:
            raise FileNotFoundError(f"No .md files found in {research_dir}")

        print(f"[INFO] Found {len(md_files)} documents in {research_dir.name}/")

        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract metadata from frontmatter if present
            source = "Unknown"
            published = "Unknown"

            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    for line in frontmatter.split('\n'):
                        if line.startswith('source:'):
                            source = line.split('source:', 1)[1].strip()
                        elif line.startswith('published:'):
                            published = line.split('published:', 1)[1].strip()

            documents.append({
                'filename': md_file.name,
                'source': source,
                'published': published,
                'content': content
            })

            print(f"  [OK] {md_file.name}")

        return documents

    def _format_documents_as_xml(self, documents: List[Dict[str, str]]) -> str:
        """Format documents with XML delimiters for clean context separation."""
        formatted = []

        for doc in documents:
            xml_doc = f"""<document filename="{doc['filename']}" source="{doc['source']}" published="{doc['published']}">
{doc['content']}
</document>"""
            formatted.append(xml_doc)

        return "\n\n".join(formatted)

    def generate_brief(self, ticker: str = "SRVCABLE") -> str:
        """Generate research brief for the given ticker."""
        print(f"\n[INFO] Generating research brief for NSE: {ticker}")
        print("=" * 60)

        # Load documents
        documents = self._load_documents()

        # Format as XML context
        formatted_docs = self._format_documents_as_xml(documents)

        # Construct the prompt
        user_prompt = f"""Analyze the following documents for **{ticker}** (NSE ticker) and generate a one-page research brief.

Reference date: 23 September 2026

{formatted_docs}

Generate the research brief following the exact structure specified in your instructions."""

        # Call Gemini API
        print(f"\n[INFO] Calling Gemini API (Model: {self.model})...")

        max_retries = 3
        retry_delay = 2

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[
                        types.Content(
                            role='user',
                            parts=[
                                types.Part(text=self.system_prompt),
                                types.Part(text=user_prompt)
                            ]
                        )
                    ],
                    config=types.GenerateContentConfig(
                        temperature=0.15,
                        top_p=0.95,
                        max_output_tokens=8192,
                    )
                )

                brief = response.text

                # Print token usage if available
                if hasattr(response, 'usage_metadata') and response.usage_metadata:
                    usage = response.usage_metadata
                    print(f"\n[STATS] Token usage:")
                    print(f"  Input tokens: {usage.prompt_token_count}")
                    print(f"  Output tokens: {usage.candidates_token_count}")
                    print(f"  Total tokens: {usage.total_token_count}")

                return brief

            except Exception as e:
                error_msg = str(e)
                if attempt < max_retries - 1 and ('503' in error_msg or 'UNAVAILABLE' in error_msg):
                    print(f"[WARN] Attempt {attempt + 1} failed: {e}")
                    print(f"[INFO] Retrying in {retry_delay} seconds...")
                    import time
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print(f"\n[ERROR] Error calling Gemini API: {e}")
                    raise

    def save_brief(self, brief: str, output_path: Path):
        """Save the generated brief to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(brief)

        print(f"\n[SUCCESS] Brief saved to: {output_path}")


def main():
    """Main execution function."""
    try:
        # Initialize agent
        agent = ResearchAgent()

        # Generate brief
        brief = agent.generate_brief(ticker="SRVCABLE")

        # Save output
        output_path = Path(__file__).parent / 'output' / 'SRVCABLE_brief.md'
        agent.save_brief(brief, output_path)

        print("\n" + "=" * 60)
        print("[COMPLETE] Research brief generation complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n[FATAL] Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
