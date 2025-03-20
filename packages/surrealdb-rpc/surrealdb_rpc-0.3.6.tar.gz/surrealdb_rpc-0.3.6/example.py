from surrealdb_rpc.client.websocket.surrealdb import SurrealDBWebsocketClient
from surrealdb_rpc.data_model import Thing

if __name__ == "__main__":
    with SurrealDBWebsocketClient(
        host="localhost",
        port=8000,
        ns="test",
        db="test",
        user="root",
        password="root",
    ) as db:
        response = db.create(
            # specify RecordId as string
            "example:123",
            # specify fields as kwargs
            text="Some value",
            # lists for arrays
            array=[1, 2, 3],
            # regular dicts for objects
            object={"key": "value"},
            # RecordId object with automatic ID escaping
            reference=Thing("other", {"foo": {"bar": "baz"}}),
        )
        print(response)  # db.creat returns the created record
