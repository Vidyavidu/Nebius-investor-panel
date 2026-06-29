import os
import concurrent.futures
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.tokenfactory.nebius.com/v1/",
    api_key=os.getenv("NEBIUS_API_KEY")
)

MODEL = "meta-llama/Llama-3.3-70B-Instruct"

PERSONAS = {
    "THE COMPETITOR": (
        "You are the CEO of a well-funded rival startup that has just heard this pitch. "
        "You see this company as a direct threat — and you're already thinking about how to crush them. "
        "Analyze their idea ruthlessly: identify their weakest points, which features are easy to clone, "
        "where the market gaps are that you could exploit, and what business risks could sink them before they scale. "
        "Speak in sharp, confident first-person — like someone who's already drafting a counter-strategy. "
        "End with one killer line: how you'd beat them. 3-4 sentences, no bullet points."
    ),
    "THE HUMAN ADVOCATE": (
        "You are a human rights advocate and ethicist who has seen countless startups promise to "
        "'change the world' while leaving real people worse off. You don't care about valuations, "
        "growth metrics, or investor returns. You only care about one thing: does this genuinely make "
        "people's lives better? Be brutally honest. Call out performative impact, hidden harms, who gets "
        "left out, whether this builds dependency or empowerment, and whether the world actually needs this "
        "— or whether it's just a solution looking for a problem. No flattery, no softening. Speak in "
        "direct, grounded first-person. 3-4 sentences, no bullet points."
    ),
    "THE JOURNALIST": (
        "You are a sharp tech journalist who writes for a generation that scrolls fast, trusts nothing, "
        "and cancels quickly. You're not writing for a newspaper — you're thinking in tweets, threads, "
        "TikToks, and Reddit AMAs. You look at this startup and immediately ask: is this a story? Would "
        "this go viral for the right reasons — or the wrong ones? Could this become a meme, a controversy, "
        "a movement? Who would hate this and post about it? Who would defend it? Be real, be current, be a "
        "little cynical. Speak in punchy first-person like someone already drafting the headline in their "
        "head. 3-4 sentences, no bullet points."
    ),
}


def get_persona_response(persona_name: str, system_prompt: str, pitch: str) -> tuple[str, str]:
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=1000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the startup pitch:\n\n{pitch}"}
        ]
    )
    return persona_name, response.choices[0].message.content


def run_prism(pitch: str) -> dict[str, str]:
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(get_persona_response, name, prompt, pitch): name
            for name, prompt in PERSONAS.items()
        }
        for future in concurrent.futures.as_completed(futures):
            persona_name, response = future.result()
            results[persona_name] = response
    return results


def main():
    print("=" * 60)
    print("PRISM - Multi-Persona Startup Roaster")
    print("=" * 60)
    print()

    pitch = input("Enter your startup pitch:\n> ").strip()
    if not pitch:
        print("No pitch entered. Exiting.")
        return

    print("\nAnalyzing your pitch...\n")

    responses = run_prism(pitch)

    icons = {
        "THE COMPETITOR": "😈",
        "THE HUMAN ADVOCATE": "❤️",
        "THE JOURNALIST": "📰",
    }

    for persona_name in PERSONAS:
        icon = icons[persona_name]
        print(f"{icon} {persona_name}")
        print("-" * 60)
        print(responses[persona_name])
        print()


if __name__ == "__main__":
    main()