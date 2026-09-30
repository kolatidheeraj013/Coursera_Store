from shared_functions import *


def test_result_limits():
    """Compare similarity-search results at different result limits."""
    print("📊 SIMILARITY SEARCH RESULT LIMITER")
    print("=" * 45)

    food_items = load_food_data('FoodDataSet.json')
    collection = create_similarity_search_collection("result_test")
    populate_similarity_collection(collection, food_items)

    query = "spicy chicken"
    print(f"🔍 Testing query: '{query}'\n")

    for limit in [1, 3, 5, 10]:
        print(f"📋 Getting top {limit} result(s):")
        print("-" * 30)
        results = perform_similarity_search(collection, query, limit)

        if not results:
            print("  No results found!")
            continue

        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['food_name']}")
            print(f"     Score: {result['similarity_score']:.3f}")
            print(f"     Cuisine: {result['cuisine_type']}")
            print(f"     Calories: {result['food_calories_per_serving']}")

        scores = [result['similarity_score'] for result in results]
        print(f"  📈 Average score: {sum(scores) / len(scores):.3f}")
        print(f"  🎯 Best score: {max(scores):.3f}")
        if len(scores) > 1:
            print(f"  📉 Worst score: {min(scores):.3f}")
        print("=" * 45)

    print("\n🎮 INTERACTIVE MODE:")
    print("Press Enter on the query prompt to exit.")
    while True:
        user_query = input("\nEnter search query: ").strip()
        if not user_query:
            break

        limit_input = input("How many results? (1-20): ").strip()
        try:
            limit = int(limit_input)
        except ValueError:
            limit = 5
        if not 1 <= limit <= 20:
            limit = 5

        results = perform_similarity_search(collection, user_query, limit)
        if results:
            print(f"Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result['food_name']} (Score: {result['similarity_score']:.3f})")
        else:
            print("No results found!")

    print("\n👋 Thanks for testing result limits!")


if __name__ == "__main__":
    test_result_limits()
