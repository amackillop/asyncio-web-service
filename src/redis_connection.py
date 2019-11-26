from rejson import Client, Path #type: ignore
from typing import Union


Json = Union[str, dict, list]


class ReJson:
    def __init__(self, host: str, port: Union[str, int]) -> None:
        """Instantiate a connection to ReJson.
        
        :param host: The hostname/ip of the Redis instance.
        :type host: str
        :param port: The port of the Redis instance.
        :type port: int
        """
        self._client = Client(host=host, port=port, decode_responses=True)
        self._client.

    def post(self, key: str, obj: Json) -> None:
        """Post a new Json object to the store.
        
        :param key: The key to store the Json at.
        :type key: str
        :param obj: What to store.
        :type obj: Json
        """
        self._client.jsonset(key, Path.rootPath(), obj)

    def get(self, key: str) -> Json:
        """[summary]
        
        :param key: The key that the Json object was stored at.
        :type key: str
        :return: The Json stored at `key`.
        :rtype: Json
        """
        return self._client.jsonget(key, Path.rootPath())

    def update(self, key: str, path: str, value: Json) -> None:
        """[summary]
        
        :param key: The key that the Json object was stored at.
        :type key: str
        :param path: A period seperated string of keys to traverse the Json.
        :type path: str
        :param value: The new value.
        :type value: Json
        """
        self._client.jsonset(key, Path(f".{path}"), value)

    def append(self, key: str, path: str, *values: Json) -> None:
        """Append to some array within a Json obejct.
        
        :param key: The key that the Json object was stored at.
        :type key: str
        :param path: A period seperated string of keys to traverse the Json.
        :type path: str
        """
        self._client.jsonarrappend(key, Path(f".{path}"), *values)

    def pop(self, key: str, path: str) -> Json:
        """Pop from from array within a Json object.

        :param key: The key that the Json object was stored at.
        :type key: str
        :param path: A period seperated string of keys to traverse the Json.
        :type path: str
        :return: The Json value popped from the array.
        :rtype: Json
        """
        return self._client.jsonarrpop(key, f".{path}")

    def remove(self, key: str, path: str, value: Json) -> None:
        """Remove something from some array within a Json object.
        
        :param key: The key that the Json object was stored at.
        :type key: str
        :param path: A period seperated string of keys to travers the Json.
        :type path: str
        :param value: The value to remove from the array.
        :type value: Json
        """        
        index = self._client.jsonarrindex(key, f'.{path}', value)
        self._client.jsondel(key, f'{path}[{index}]')
