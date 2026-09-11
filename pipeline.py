from agent import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain
)


def run_research_pipeline(topic: str) -> dict:

    state = {}

    # STEP 1 - Search Agent
    print("\n" + "=" * 50)
    print("STEP 1 - Search agent is working...")
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [
            (
                "user",
                f"Find recent, reliable and detailed information about: {topic}"
            )
        ]
    })

    state["search_result"] = search_result["messages"][-1].content

    print("\nSearch Result:\n")
    print(state["search_result"])

    # STEP 2 - Reader Agent
    print("\n" + "=" * 50)
    print("STEP 2 - Reader agent is scraping top results...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"""
Based on the following search results about '{topic}',

pick the most relevant URL and scrape it for deeper content.

Search Results:
{state['search_result'][:800]}
"""
            )
        ]
    })

    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped Content:\n")
    print(state["scraped_content"])

    # STEP 3 - Writer Chain
    print("\n" + "=" * 50)
    print("STEP 3 - Writer is drafting the report...")
    print("=" * 50)

    research_report = (
        f"SEARCH RESULTS:\n{state['search_result']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "Research": research_report
    })

    print("\nFINAL REPORT:\n")
    print(state["report"])

    # STEP 4 - Critic Chain
    print("\n" + "=" * 50)
    print("STEP 4 - Critic is reviewing the report...")
    print("=" * 50)

    state["Feedback"] = critic_chain.invoke({
        "REPORT": state["report"]
    })

    print("\nCRITIC REPORT:\n")
    print(state["Feedback"])

    return state


if __name__ == "__main__":

    topic = input("Enter the topic for research: ")

    state = run_research_pipeline(topic)