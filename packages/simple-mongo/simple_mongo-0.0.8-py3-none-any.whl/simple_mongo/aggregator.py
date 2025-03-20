from .database import MongoDB
class Aggregator:
    def __init__(self, mongodb : MongoDB, collection_name : str):
        self._mongodb = mongodb
        self._aggregator = []
        self._collection_name = collection_name

    def join(self, 
            collection_name : str, 
            field : str, 
            foreign_field : str,
            as_field : str
            ):
        """
        Joins two collections
        """
        self._aggregator.append({
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
        self._aggregator.append({
            '$match': query
        })

        return self
    
    def aggregate(self):
        """
        Aggregates the collections
        """
        return self._mongodb.aggregate(self._collection_name, self._aggregator)