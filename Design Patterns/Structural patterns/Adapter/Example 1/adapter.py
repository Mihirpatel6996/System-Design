# Defining Target Interface

class IReports:
    def get_json_data(self, data: str) -> str:
        raise NotImplementedError

# legacy class (Adaptee) or existing class or adaptee class --> this is a class 3 party library or existing class which we cannot modify
class XmlDataProvider:
    def get_xml_data(self, data: str) -> str:
        name, id_ = data.split(":")
        return f"<user><name>{name}</name><id>{id_}</id></user>"


# Adapter class has-a relationship with the adaptee class and implements the target interface

class XmlDataProviderAdapter(IReports):
    def __init__(self, xml_provider: XmlDataProvider):
        self.xml_provider = xml_provider

    def get_json_data(self, data: str) -> str:
        # Step 1: Get XML from adaptee
        xml = self.xml_provider.get_xml_data(data)

        # Step 2: Parse XML (same logic, but now isolated)
        name = xml.split("<name>")[1].split("</name>")[0]
        id_ = xml.split("<id>")[1].split("</id>")[0]

        # Step 3: Convert to JSON
        return f'{{"name": "{name}", "id": {id_}}}'



# client code - very very clean 

class Client:
    def get_report(self, report: IReports, raw_data: str):
        print("Processed JSON:", report.get_json_data(raw_data))

# Execution flow 

if __name__ == "__main__":
    # Step 1: Create adaptee
    xml_provider = XmlDataProvider()

    # Step 2: Wrap it inside adapter
    xml_data_adapter = XmlDataProviderAdapter(xml_provider)

    # Step 3: Client uses adapter
    client = Client()
    client.get_report(xml_data_adapter, "Alice:42")


    