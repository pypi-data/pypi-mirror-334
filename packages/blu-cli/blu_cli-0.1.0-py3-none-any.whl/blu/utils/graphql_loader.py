import os


class GraphQLLoader:
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.MUT_DIR = os.path.join(
            os.path.dirname(__file__), "../constants/graphql/mutations"
        )
        self.QUERY_DIR = os.path.join(
            os.path.dirname(__file__), "../constants/graphql/queries"
        )

    def load_graphql_query(self, filename):
        """
        Load a GraphQL query/mutation from a .graphql file.

        :param filename: Name of the .graphql file (without extension).
        :return: GraphQL query/mutation string.
        """
        file_path = os.path.join(self.QUERY_DIR, f"{filename}.graphql")

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"GraphQL file '{filename}.graphql' not found in {self.QUERY_DIR}"
            )

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    def load_graphql_mutation(self, filename):
        """
        Load a GraphQL query/mutation from a .graphql file.

        :param filename: Name of the .graphql file (without extension).
        :return: GraphQL query/mutation string.
        """
        file_path = os.path.join(self.MUT_DIR, f"{filename}.graphql")

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"GraphQL file '{filename}.graphql' not found in {self.MUT_DIR}"
            )

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
