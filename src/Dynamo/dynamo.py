import boto3

class DynamoTable:
    def __init__(self, tableName):
        self.tableName = tableName
        self.dynamoDB = boto3.resource('dynamodb', region_name = 'ap-southeast-2')
        self.table = self.dynamoDB.Table(tableName)

    def get_everything(self):
        return self.table.scan()["Items"]

    def get_item(self, item):
        response = table.query()
    def insert_item(self, item):
        print(item)
        self.table.put_item(Item = item)

    def update_item(self, category, path, value):
        response = self.table.update_item(
            Key = {
                'Category': category 
            },
            UpdateExpression = "set " + path + " = :v",
            ExpressionAttributeValues = {
                ':v': value    
            },
            ReturnValues = "UPDATED_NEW"
        )

        return response

    def delete_item(self):
        print('deleting')

    def read_item(self):
        print('reading')

    def create_item(self, item):
        print(item)
        self.table.put_item(Item = item)
