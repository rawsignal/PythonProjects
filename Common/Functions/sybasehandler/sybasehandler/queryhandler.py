from sybasehandler import Connection

class QueryHandler(object) :
    def __new__(self, database, connection, query) :
        self._database = database
        self._connection = connection
        self._query = query
        quer = self._connection.cursor()
        quer.execute(self._database)
        quer.execute(self._query)

        results = []

        for row in quer.fetchall() :
            for element in row :
                results.append(element)

        if not results :
            results.append("No results returned.")

        return results

