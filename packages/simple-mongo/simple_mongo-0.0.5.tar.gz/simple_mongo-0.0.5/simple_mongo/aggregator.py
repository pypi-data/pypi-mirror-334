from .database import MongoDB
class Aggregator:
    def __init__(self, mongodb : MongoDB, collection_name : str):
        self.mongodb = mongodb
        self.aggregator = []
        self.collection_name = collection_name

    def join(self, 
            collection_name : str, 
            field : str, 
            foreign_field : str,
            as_field : str
            ):
        """
        Joins two collections
        """
        self.aggregator.append({
            '$lookup': {
                'from': collection_name,
                'localField': field,
                'foreignField': foreign_field,
                'as': as_field
            }
        })
        return self
    
    def match(self, query : dict):
        """
        Filters the collection
        """
        self.aggregator.append({
            '$match': query
        })
    
    def aggregate(self):
        """
        Aggregates the collections
        """
        return self.mongodb.aggregate(self.collection_name, self.aggregator)