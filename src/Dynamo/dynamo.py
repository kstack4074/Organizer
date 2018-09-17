import boto3

class DynamoTable:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamoDB = boto3.resource('dynamodb', region_name = 'ap-southeast-2')
        self.table = self.dynamoDB.Table(table_name)

    def get_everything(self):
        return self.table.scan()["Items"]

    def create_item(self, path, value):
        split_path = path.split('.')
        table_key = split_path[0]
        path_length = len(split_path)
        if path_length == 1:
            item = {'Key': path}
            item.update(value)
            self.table.put_item(Item = item)
        elif path_length == 2:
            response = self.table.update_item(
            Key = {
                'Key': table_key 
            },
            UpdateExpression = "set " + split_path[1] + " = :v",
            ExpressionAttributeValues = {
                ':v': value    
            },
            ReturnValues = "UPDATED_NEW"
        )
        else:
            #Read what already exists
            new_key = split_path[-1]
            existing_path = split_path[:path_length - 1]
            existing_value = self.read_item('.'.join(existing_path))
            try:
                existing_value.update({new_key:value})
            except:
                existing_value = {existing_path[-1]: existing_value}
                existing_value.update({new_key: value})
            #Update the database value with the new value object
            self.update_element('.'.join(existing_path), existing_value)
            
    def read_item(self, path):
        split_path = path.split('.')
        table_key = split_path[0]
        data_path = '.'.join(split_path[1:])

        response = self.table.get_item(
            Key = {
                'Key': table_key
            }
        )

        item = response['Item']
        
        #Navigate to the data under path
        for key in split_path[1:]:
            item = item.get(key)
            if item == None:
                print('Key does not exist')
                return {'Error': key + ' does not exist'}
        return item

    def update_element(self, path, value):
        split_path = path.split('.')
        table_key = split_path[0]
        if len(split_path) > 1:
            data_path = '.'.join(split_path[1:])
        else:
            data_path = ''
        response = self.table.update_item(
            Key = {
                'Key': table_key 
            },
            UpdateExpression = "set " + data_path + " = :v",
            ExpressionAttributeValues = {
                ':v': value    
            },
            ReturnValues = "UPDATED_NEW"
        )

        return response['Attributes'][split_path[-1]]

    def delete_element(self, path):
        split_path = path.split('.')
        path_length = len(split_path)

        if path_length == 1:
            #Delete everything
            self.table.delete_item(
                Key = {
                    'Key': split_path[0]
                }
            )
        else:
            #Delete nested data
            response = self.table.update_item(
                Key = {
                    'Key': split_path[0]
                },
                UpdateExpression = "remove " + '.'.join(split_path[1:])
            )

            return response

