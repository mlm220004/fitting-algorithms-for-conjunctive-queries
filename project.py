from typing import Optional

class DatabaseSchema:

    def __init__(self, name: str):
        self.name = name
        self.relations = set()
        
    def add_relation(self, R: str, n: int):
        """
        Adds a new relation (table) to the schema,
        where R is the relation symbol (table name)
        and n is the arity (number of columns) of the relation symbol
        """
        self.relations.add((R, n))
        
    def relation_exists(self, R: str, n: int) -> bool:
        """
        Returns
        true if the schema has a relation R of arity n
        and false otherwise
        """
        return (R, n) in self.relations
        
    def get_arity(self, R: str) -> int:
        """
        Returns the arity (number of columns) in the relation R
        """
        for (R2, n) in self.relations:
            if R == R2:
                return n
        return 0
    
    def __str__(self) -> str:
        string = self.name
        string += " = {\n"
        i = 1
        for (R, n) in self.relations:
            string += "  ('"
            string += R
            string += "', "
            string += str(n)
            string += ")"
            if i < len(self.relations):
                string += ","
            string += "\n"
            i += 1
        string += "}"
        return string


class DatabaseInstance:
    
    def __init__(self, name: str, schema: DatabaseSchema):
        self.name = name
        self.schema = schema
        self.facts = set()
        
    def add_fact(self, R: str, A: tuple):
        """
        Adds a new fact to the database,
        where R is the relation symbol (table name),
        A is an n-tuple, and (R, n) is a relation
        """
        if not self.schema.relation_exists(R, len(A)):
            raise ValueError(f"Relation ({R}, {len(A)}) does not exist")
        self.facts.add((R, A))
        
    def get_schema(self) -> DatabaseSchema:
        """
        Returns the schema for the database
        """
        return self.schema
        
    def get_active_domain(self) -> set:
        """
        Returns the active domain of the database,
        i.e., the set of all constant values
        """
        active_domain = set()
        for (R, A) in self.facts:
            for v in A:
                active_domain.add(v)
        return active_domain
    
    def __str__(self) -> str:
        string = self.name
        string += " = {\n"
        i = 1
        for (R, A) in self.facts:
            string += "  ('"
            string += R
            string += "', "
            string += str(A)
            string += ")"
            if i < len(self.facts):
                string += ","
            string += "\n"
            i += 1
        string += "}"
        return string


class LabeledExamples:
    
    def __init__(self, k: int):
        self.arity = k
        self.positive_examples = set()
        self.negative_examples = set()
    
    def add_positive_example(self, I: DatabaseInstance, a: tuple):
        """
        Adds a new positive example for some database,
        where a is a k-tuple
        
        The new example must not already be a negative example
        in order to maintain disjointness
        """
        if len(a) != self.arity:
            raise ValueError()
        pair = (I, a)
        if pair in self.negative_examples:
            raise ValueError()
        self.positive_examples.add(pair)
        
    def add_negative_example(self, I: DatabaseInstance, a: tuple):
        """
        Adds a new negative example for some database,
        where a is a k-tuple
        
        The new example must not already be a positive example
        in order to maintain disjointness
        """
        if len(a) != self.arity:
            raise ValueError()
        pair = (I, a)
        if pair in self.positive_examples:
            raise ValueError()
        self.negative_examples.add(pair)
        
    def get_arity(self) -> int:
        """
        Returns the arity of the examples
        """
        return self.arity
    
    def __str__(self) -> str:
        string = "E+ = {"
        
        i = 1
        for (I, a) in self.positive_examples:
            string += "("
            string += I.name
            string += ", "
            string += str(a)
            string += ")"
            if i < len(self.positive_examples):
                string += ", "
            i += 1
        
        string += "},\nE- = {"
        
        i = 1
        for (I, a) in self.negative_examples:
            string += "("
            string += I.name
            string += ", "
            string += str(a)
            string += ")"
            if i < len(self.negative_examples):
                string += ", "
            i += 1
        
        string += "}"
        return string


class FittingCQ:
    
    def __init__(self, schema: DatabaseSchema, k: int):
        self.schema = schema
        self.arity = k
        a = list()
        for i in range(1, k+1):
            a.append("x" + str(i))
        self.answer_variables = tuple(a)
        self.relational_atoms = set()
    
    def add_relational_atom(self, R: str, B: tuple):
        """
        Adds a relational atom to the clause,
        where R is the relation symbol (table name),
        B is an n-tuple, and (R, n) is a relation
        """
        if len(B) != self.schema.get_arity(R):
            raise ValueError()
        if not all(isinstance(b, str) for b in B):
            raise ValueError()
        pair = (R, B)
        self.relational_atoms.add(pair)
    
    def __str__(self) -> str:
        string = "q"
        string += str(self.answer_variables)
        string += " :- "
        i = 1
        for (R, B) in self.relational_atoms:
            string += R
            string += str(B)
            if i < len(self.relational_atoms):
                string += ", "
            i += 1
        string += "."
        return string


def algorithm_P(I: DatabaseInstance, E: LabeledExamples) -> FittingCQ:
    query = FittingCQ(I.get_schema(), E.get_arity())
    
    # TODO
    
    return query
    
def algorithm_M(I: DatabaseInstance, E: LabeledExamples) -> FittingCQ:
    query = FittingCQ(I.get_schema(), E.get_arity())
    
    # TODO
    
    return query
    
def algorithm_B(I: DatabaseInstance, E: LabeledExamples) -> FittingCQ:
    query = FittingCQ(I.get_schema(), E.get_arity())
    
    # TODO
    
    return query
    
def algorithm_R(I: DatabaseInstance, E: LabeledExamples) -> Optional[FittingCQ]:
    
    # TODO
    
    return None
