class XmlDataProvider:
    def get_xml_data(self, data: str) -> str:
        name, id_ = data.split(":")
        return f"<user><name>{name}</name><id>{id_}</id></user>"


class Client:
    def get_report(self, provider: XmlDataProvider, raw_data: str):
        # Client is forced to understand XML 
        xml = provider.get_xml_data(raw_data)

        # Manual parsing inside client (bad)
        name = xml.split("<name>")[1].split("</name>")[0]
        id_ = xml.split("<id>")[1].split("</id>")[0]

        json_data = f'{{"name": "{name}", "id": {id_}}}'

        print("Processed JSON:", json_data)


if __name__ == "__main__":
    provider = XmlDataProvider()
    client = Client()

    client.get_report(provider, "Alice:42")


# problems :

"""
1. client has to understand the XML format and manually parse it, which is not ideal.
2. If the XML format changes, the client code will break, leading to maintenance issues.
3. The client is tightly coupled to the XML data provider, making it less flexible and harder to adapt to other data formats in the future.
4. client has to know XML structure, parsing logic and data format very difficult
"""