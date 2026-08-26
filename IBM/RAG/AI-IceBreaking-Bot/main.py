"""Main script for running the Icebreaker Bot."""

import argparse
import logging
import sys
import time

import config
from modules.data_extraction import extract_linkedin_profile
from modules.data_processing import (
    create_vector_database,
    split_profile_data,
    verify_embeddings,
)
from modules.query_engine import answer_user_query, generate_initial_facts


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout)],
)
logger = logging.getLogger(__name__)


def process_linkedin(linkedin_url, api_key=None, mock=False):
    try:
        profile_data = extract_linkedin_profile(linkedin_url, api_key, mock=mock)
        if not profile_data:
            logger.error("Failed to retrieve profile data.")
            return

        nodes = split_profile_data(profile_data)
        vectordb_index = create_vector_database(nodes)
        if not vectordb_index:
            logger.error("Failed to create vector database.")
            return

        if not verify_embeddings(vectordb_index):
            logger.warning("Some embeddings may be missing or invalid.")

        print("\nHere are 3 interesting facts about this person:")
        print(generate_initial_facts(vectordb_index))
        chatbot_interface(vectordb_index)
    except Exception as error:
        logger.error("Error occurred: %s", error)


def chatbot_interface(index):
    print(
        "\nYou can now ask more in-depth questions about this person. "
        "Type 'exit', 'quit', or 'bye' to quit."
    )
    while True:
        user_query = input("You: ")
        if user_query.lower() in ["exit", "quit", "bye"]:
            print("Bot: Goodbye!")
            break

        print("Bot is typing...", end="")
        sys.stdout.flush()
        time.sleep(1)
        print("\r", end="")
        response = answer_user_query(index, user_query)
        answer = response.response if hasattr(response, "response") else response
        print(f"Bot: {answer.strip()}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Icebreaker Bot - LinkedIn Profile Analyzer"
    )
    parser.add_argument("--url", type=str, help="LinkedIn profile URL")
    parser.add_argument("--api-key", type=str, help="API key")
    parser.add_argument("--mock", action="store_true", help="Use mock data")
    parser.add_argument("--model", type=str, help="LLM model to use")
    args = parser.parse_args()

    linkedin_url = args.url or (
        "" if args.mock else input(
            "Enter LinkedIn profile URL (or press Enter to use mock data): "
        )
    )
    use_mock = args.mock or not linkedin_url

    if args.model:
        from modules.llm_interface import change_llm_model
        change_llm_model(args.model)

    api_key = args.api_key or config.PROXYCURL_API_KEY
    if not use_mock and not api_key:
        api_key = input("Enter ProxyCurl API key: ")
    if use_mock and not linkedin_url:
        linkedin_url = "https://www.linkedin.com/in/leonkatsnelson/"

    process_linkedin(linkedin_url, api_key, mock=use_mock)


if __name__ == "__main__":
    main()
