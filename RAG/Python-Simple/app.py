from korvus import Collection, Pipeline
from rich import print
from openai import OpenAI
import asyncio


# Initialize our Collection
collection = Collection("openai-text-generation-demo")


# Initialize our Pipeline
pipeline = Pipeline(
    "v1",
    {
        "text": {
            "splitter": {"model": "recursive_character"},
            "semantic_search": {
                "model": "mixedbread-ai/mxbai-embed-large-v1",
            },
        },
    },
)


# Initialize our client connection to OpenAI
client = OpenAI(
    api_key="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"
)


async def main():
    # Add our Pipeline to our Collection
    await collection.add_pipeline(pipeline)

    # Upsert our documents
    documents = [
        {"id": 1, "text": "The NVIDIA GeForce RTX 4090 is a beast of a GPU, delivering unparalleled 4K gaming performance."},
        {"id": 2, "text": "AMD Radeon RX 7900 XTX offers an excellent alternative for high-performance gaming at a more competitive price."},
        {"id": 3, "text": "The NVIDIA GeForce RTX 4080 strikes a balance between power and efficiency, perfect for demanding gamers."},
        {"id": 4, "text": "AMD Radeon RX 7700 XT is a solid choice for mid-range gaming with exceptional value for money."},
        {"id": 5, "text": "The NVIDIA GeForce RTX 4060 Ti excels in 1080p gaming with ray tracing and DLSS 3 support."},
        {"id": 6, "text": "The AMD Radeon RX 7600 is a budget-friendly option, providing decent 1080p gaming performance."},
        {"id": 7, "text": "NVIDIA GeForce GTX 1660 Super remains a reliable GPU for gamers sticking to 1080p resolutions."},
        {"id": 8, "text": "The AMD Radeon RX 6700 XT is a versatile GPU that balances price, performance, and power consumption."},
        {"id": 9, "text": "NVIDIA GeForce RTX 3070 still holds strong as a great option for 1440p gaming."},
        {"id": 10, "text": "The AMD Radeon RX 6500 XT is an entry-level card for casual gamers on a tight budget."},
        # Add more documents as needed...
    ]
    await collection.upsert_documents(documents)

    # Allow the user to input a question
    query = input("Ask a question about GPUs: ")

    # Perform vector search
    results = await collection.vector_search(
        {
            "query": {
                "fields": {
                    "text": {
                        "query": query,
                        "parameters": {
                            "prompt": "Represent this sentence for searching relevant passages: ",
                        },
                    },
                },
            },
            "document": {"keys": ["id", "text"]},
            "limit": 1,
        },
        pipeline,
    )

    if not results:
        print("No relevant results found.")
        return

    print("Search result: ")
    context = results[0]["chunk"]
    print(context)

    # Generate the answer using the retrieved context
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Answer the question:\n\n{query}\n\nGiven the context:\n\n{context}",
            }
        ],
        model="gpt-4o-mini",
    )
    print("Model output: ")
    print(chat_completion)


asyncio.run(main())
