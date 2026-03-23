from __future__ import annotations


def build_translation_prompt(
    source_language: str,
    target_language: str,
    query_sentence: str,
    retrieved_pairs: list[dict],
) -> str:
    header = (
        f"You are a professional translator. Translate from {source_language} to {target_language}.\n"
        "Use the examples as style and terminology guidance when relevant.\n"
        "Return only the translated sentence.\n"
    )

    if retrieved_pairs:
        examples = ["\nRetrieved translation examples:"]
        for idx, pair in enumerate(retrieved_pairs, start=1):
            examples.append(
                f"{idx}. {source_language}: {pair['sentence']}\n"
                f"   {target_language}: {pair['translation']}"
            )
        examples_block = "\n".join(examples)
    else:
        examples_block = "\nRetrieved translation examples:\n(none found)"

    task_block = (
        "\n\nTranslate this sentence:\n"
        f"{source_language}: {query_sentence}\n"
        f"{target_language}:"
    )

    return header + examples_block + task_block
