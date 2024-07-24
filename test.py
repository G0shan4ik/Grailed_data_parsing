from pinecone import Pinecone

pc = Pinecone(api_key="afd305a0-e8fd-4c1b-bd1e-c79b1790d6aa")
index = pc.Index("test")


index.upsert(
    vectors=[
        {
            "id": "vec1",
            "values": [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
            "metadata": {"genre": "drama"}
        }, {
            "id": "vec2",
            "values": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
            "metadata": {"genre": "action"}
        }, {
            "id": "vec3",
            "values": [0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
            "metadata": {"genre": "drama"}
        }, {
            "id": "vec4",
            "values": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
            "metadata": {"genre": "action"}
        }
    ],
    namespace="ns1"
)