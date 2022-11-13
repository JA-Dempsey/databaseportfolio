from Data import Data
from flask_mysqldb import MySQL

class Database:

    def __init__(self, sql_object: MySQL, queries=[], tables=[]):
        """Initialize variables, need to give a MySQL
        object with app data given as the sql_object."""
        self._mysql = sql_object
        self._queries = queries
        self._results = Data()
        self._execute_dict = None

    def update_case(self, input: str) -> str:
        """Given a string as input, will ensure only
        the first letter is capitalized (to match
        case of table names in database)."""
        input.casefold()
        input.capitalize()

        return input

    def add_query(self, query: str):
        """Adds a manual query to the list of queries
        to execute. More complicated queries may need
        to use this method."""
        self._queries.append(query)

    def remove_query(self, index: int):
        """Removes the query at a given index from
        the list of queries."""
        self._queries.pop(index)

    def delete_queries(self):
        """Deletes all queries from Database object."""
        self._queries = []

    def get_queries(self):
        """Returns the list of current queries."""
        return self._queries

    def get_results(self):
        """Returns the results for the last list of queries
        that were run. Returns a Data Object."""
        return self._results

    def get_json(self):
        """Returns the results in JSON format."""
        return self._results.convert_to_json()

    def execute(self):
        """Executes the list of queries given to the Database Class."""
        cursor = self._mysql.connection.cursor()
        print("FAILED")
        for query in self._queries:
            if self._execute_dict is None:
                print("It is none")
                cursor.execute(query)
            else:
                print("attempt that one")
                cursor.execute(query, self._execute_dict)

        self._results.set_data(cursor.fetchall())
        self._queries = []

    def create_execution_dict(self, keys, values):
        """Creates a dictionary to pass to the execution function to 
        protect against injection."""
        self._execute_dict = {}
        for index in range(len(keys)):
            self._execute_dict[keys[index]] = values[index]

    def add_select(self, columns: list, table: str, append=''):
        """Adds a query to the list of queries with the given
        columns, table, and optional append (for things like WHERE)
        in case they are needed."""

        # Ensure proper table case
        table = self.update_case(table)

        # Build string of columns from columns list
        columns_str = ", ".join(columns)

        query = 'SELECT ' + columns_str + ' FROM ' + table

        if append != '':
            query += ' ' + append

        self._queries.append(query)

    def add_insert(self, table: str, columns: list, values: list, append=''):
        """Adds an insert query to the current list of queries given
        a table, columns, and values to insert. The append parameter
        given will be added on to the end of the query."""

        # Ensure proper table case
        table = self.update_case(table)

        self.create_execution_dict(columns, values)

        print(self._execute_dict)

        f_values = []
        for index in range(len(columns)):
            f_values.append(f'%({columns[index]})s')
    
        # Convert list values into strings
        columns_str = ','.join(columns)
        values_str = ','.join(f_values)


        # Build Insert query
        query = 'INSERT INTO ' + table.capitalize() + ' (' + columns_str + ') VALUES ' + '(' + values_str + ')'

        if append != '':
            query += ' ' + append

        self._queries.append(query)

        # Build append search to get only the item
        # added back from the SQL table

    def add_update(self, table: str, set_pairs: list, filter='', append=''):
        """Adds an UPDATE query to the current list of queries given
        a table, a string of set_pairs to update, a filter, and an optional
        append string."""

        # Ensure proper table case
        table = self.update_case(table)

        # Convert list values into strings
        set_pairs_str = ','.join(set_pairs)

        query = 'UPDATE ' + table + ' SET ' + set_pairs_str + ' WHERE ' + filter

        if append != '':
            query += ' ' + append

        self._queries.append(query)

        # BUILD SELECT to RETURN data UPDATED
        # -----------------------------------

        # Get keys for the set_pairs
        keys = get_keys(set_pairs, "=")

        # Build string from keys for SELECT columns
        keys_str = ','.join(keys)

        # Build append search for SELECT
        append = 'WHERE ' + filter

        # Add select to queries
        self.add_select(keys_str, table, append)

    def add_delete(self, table, filter):
        """Adds a DELETE query to the current list of queries given
        a table and a filter."""

        # Ensure proper table case
        table = self.update_case(table)

        query = 'DELETE FROM ' + table + ' WHERE ' + filter

        self._queries.append(query)

def get_keys(pairs: list, delimiter: str):
    """Extracts keys for a list of strings in the format key=pair as
    a single entry of the list as a string, where = can be any given
    delimeter."""
    keys = []

    for value in pairs:
        split_values = value.split(delimiter)
        keys.append(split_values[0])

    return keys
