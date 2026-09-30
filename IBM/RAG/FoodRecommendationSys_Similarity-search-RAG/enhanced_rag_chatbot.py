from shared_functions import *
import os


def create_watsonx_model():
    """Create Watsonx only when the user has supplied credentials."""
    api_key = os.getenv("WATSONX_API_KEY") or os.getenv("IBM_CLOUD_API_KEY")
    if not api_key:
        return None

    from ibm_watsonx_ai.foundation_models import ModelInference

    return ModelInference(
        model_id=os.getenv("WATSONX_MODEL_ID", "ibm/granite-4-h-small"),
        credentials={
            "url": os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
            "apikey": api_key,
        },
        params={"max_new_tokens": 400},
        project_id=os.getenv("WATSONX_PROJECT_ID", "skills-network"),
        verify=False,
    )


def local_response(query, results):
    """Return a useful response without an external LLM or API key."""
    if not results:
        return f"I could not find a close match for '{query}'. Try a different description."

    recommendations = ", ".join(result["food_name"] for result in results[:3])
    best = results[0]
    return (
        f"For '{query}', I recommend {recommendations}. "
        f"The closest match is {best['food_name']} ({best['similarity_score'] * 100:.1f}% match), "
        f"with {best['food_calories_per_serving']} calories per serving."
    )


def main():
    print("🍽️  Food Recommendation Chatbot")
    print("Type a food request, or 'quit' to exit.")

    food_items = load_food_data("FoodDataSet.json")
    collection = create_similarity_search_collection(
        "enhanced_food_search",
        {"description": "Food recommendation search"},
    )
    populate_similarity_collection(collection, food_items)

    model = create_watsonx_model()
    if model:
        print("Using IBM Watsonx for responses.")
    else:
        print("Using local mode. No API key required.")

    while True:
        query = input("\n🔍 What would you like to eat? ").strip()
        if query.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        if not query:
            continue

        results = perform_similarity_search(collection, query, 5)
        if model:
            prompt = (
                f"Recommend food based on this request: {query}. "
                f"Search results: {local_response(query, results)}"
            )
            try:
                print(f"\n🤖 {model.invoke(prompt)[0]}")
            except Exception as error:
                print(f"Watsonx request failed ({error}); using local mode instead.")
                print(f"\n🤖 {local_response(query, results)}")
        else:
            print(f"\n🤖 {local_response(query, results)}")


if __name__ == "__main__":
    main()
