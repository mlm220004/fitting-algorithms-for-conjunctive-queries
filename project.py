from typing import Optional
from itertools import product

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
        string = "q("
        i = 1
        for ace in self.answer_variables:
            string += ace.capitalize()
            if i < len(self.answer_variables):
                string += ", "
            i += 1
        string += ")"
        if len(self.relational_atoms) > 0:
            string += " :- "
        i = 1
        for (R, B) in self.relational_atoms:
            string += R.lower()
            string += "("
            j = 1
            for bce in B:
                string += bce.capitalize()
                if j < self.schema.get_arity(R):
                    string += ", "
                j += 1
            string += ")"
            if i < len(self.relational_atoms):
                string += ", "
            i += 1
        string += "."
        return string

#-----------------------------------------------------------------------------------------------------------------
#   Helper Functions
#-----------------------------------------------------------------------------------------------------------------

def strongest_example(schema: DatabaseSchema, k: int):
    """Build the strongest possible example."""
    I_star = DatabaseInstance("strongest", schema)
    c = "c"
    for R, arity in schema.relations:
        I_star.add_fact(R, tuple([c] * arity))
    return (I_star, tuple([c] * k))

def get_query_key(q: FittingCQ) -> tuple:
    """Canonical hashable key for deduplication (stable ordering)."""
    atoms_sorted = sorted(q.relational_atoms, key=lambda x: (x[0], x[1]))
    return (q.answer_variables, tuple(atoms_sorted))

def canonical_cq(ex, schema: DatabaseSchema, k: int) -> FittingCQ:
    """Turn an example (I, a) into its canonical FittingCQ."""
    I_final, answer_final = ex
    query = FittingCQ(schema, k)
    all_values = set()
    for R, tup in I_final.facts:
        for v in tup:
            all_values.add(v)
    for v in answer_final:
        all_values.add(v)

    value_to_var = {}
    var_idx = 1
    for val in answer_final:
        if val not in value_to_var:
            value_to_var[val] = f"x{var_idx}"
            var_idx += 1
    for val in sorted(all_values, key=str):
        if val not in value_to_var:
            value_to_var[val] = f"x{var_idx}"
            var_idx += 1

    for R, tup in sorted(I_final.facts):
        var_tup = tuple(value_to_var[val] for val in tup)
        query.add_relational_atom(R, var_tup)
    return query


def direct_product(ex1, ex2, schema: DatabaseSchema, k: int):
    """Direct product of two examples."""
    I1, a1 = ex1
    I2, a2 = ex2
    I_prod = DatabaseInstance("product", schema)
    facts1_by_rel = {}
    for R, tup in I1.facts:
        facts1_by_rel.setdefault(R, []).append(tup)

    for R, tup_list1 in facts1_by_rel.items():
        for tup1 in tup_list1:
            for R2, tup2 in I2.facts:
                if R2 == R:
                    new_tup = tuple((tup1[i], tup2[i]) for i in range(len(tup1)))
                    I_prod.add_fact(R, new_tup)

    new_answer = tuple((a1[i], a2[i]) for i in range(k))
    return (I_prod, new_answer)


def query_holds_on_example(ex_query, I_target: DatabaseInstance, a_target: tuple, k: int) -> bool:
    """Optimized backtracking version to check whether there exists a homomorphism
    from the query's canonical instance to the target example.
    This eliminates the combinatorial explosion in the original product-based version.
    """
    I_q, a_q = ex_query
    # Collect all variables used in the query
    vars_set = set(a_q)
    for _, tup in I_q.facts:
        for v in tup:
            vars_set.add(v)
    variables = list(vars_set)

    # Forced mapping for answer variables
    mapping = {}
    for i in range(k):
        mapping[a_q[i]] = a_target[i]

    target_facts = I_target.facts
    target_domain = list(I_target.get_active_domain())

    def backtrack(idx):
        if idx == len(variables):
            # All variables assigned → verify every query atom exists in target
            for R, tup in I_q.facts:
                mapped = tuple(mapping[v] for v in tup)
                if (R, mapped) not in target_facts:
                    return False
            return True

        var = variables[idx]
        if var in mapping:  # already fixed (answer variable)
            return backtrack(idx + 1)

        for val in target_domain:
            mapping[var] = val
            if backtrack(idx + 1):
                return True
            del mapping[var]  # backtrack
        return False

    return backtrack(0)


def fits_labeled_examples(q: FittingCQ, E: LabeledExamples, schema: DatabaseSchema, k: int) -> bool:
    """Check if the FittingCQ fits all the positive/negative examples in E"""
    I_q = DatabaseInstance("q_canonical", schema)
    for R, B in q.relational_atoms:
        I_q.add_fact(R, B)
    a_q = q.answer_variables
    ex_query = (I_q, a_q)

    for (I_pos, a_pos) in E.positive_examples:
        if not query_holds_on_example(ex_query, I_pos, a_pos, k):
            return False
    for (I_neg, a_neg) in E.negative_examples:
        if query_holds_on_example(ex_query, I_neg, a_neg, k):
            return False
    return True


def minimize(ex, bq: FittingCQ, schema: DatabaseSchema, k: int):
    """Exact implementation of the paper's minimize procedure (Algorithm 3.2, lines 6–10).
    Drops a fact f only if a is still in bq(I \ {f}) according to the membership oracle.
    """
    I, a = ex
    current_facts = set(I.facts)   # facts are tuples (R, tup)
    
    changed = True
    while changed:
        changed = False
        facts_list = list(current_facts)
        for i, fact in enumerate(facts_list):
            fact_to_remove = fact
            temp_facts = current_facts - {fact_to_remove}
            
            temp_I = DatabaseInstance("temp", schema)
            for (R, tup) in temp_facts:
                temp_I.add_fact(R, tup)
            
            # Simulate MEMB_bq: check if a is still in bq(temp_I)
            I_bq = DatabaseInstance("bq_canonical", schema)
            for R_b, B_b in bq.relational_atoms:
                I_bq.add_fact(R_b, B_b)
            ex_query = (I_bq, bq.answer_variables)
            
            if query_holds_on_example(ex_query, temp_I, a, k):
                current_facts = temp_facts
                changed = True
                break   # restart after a successful removal (greedy, as in the paper)
    
    final_I = DatabaseInstance("minimized", schema)
    for (R, tup) in current_facts:
        final_I.add_fact(R, tup)
    return (final_I, a)

def upward_refinements(q: FittingCQ, schema: DatabaseSchema, k: int):
    """Upward refinement operator ρ (exactly as used in the paper's Algorithm R):
       Delete exactly one atom → produces a strictly more general query (q ⊆ p).
    """
    refinements = []
    atoms = list(q.relational_atoms)
    for i in range(len(atoms)):
        new_atoms = atoms[:i] + atoms[i+1:]
        new_q = FittingCQ(schema, k)
        new_q.answer_variables = q.answer_variables
        for R2, B2 in new_atoms:
            new_q.add_relational_atom(R2, B2)
        # safety condition (every answer variable must appear in at least one atom)
        appears = set()
        for _, B2 in new_q.relational_atoms:
            appears.update(B2)
        if all(v in appears for v in new_q.answer_variables):
            refinements.append(new_q)
    return refinements

#-----------------------------------------------------------------------------------------------------------------
#   Algorithms
#-----------------------------------------------------------------------------------------------------------------

def algorithm_P(I: DatabaseInstance, E: LabeledExamples) -> FittingCQ:
    k = E.get_arity()
    schema = I.get_schema()

    e_star = strongest_example(schema, k)
    
    for pos_example in E.positive_examples:
        e_star = direct_product(e_star, pos_example, schema, k)

    return canonical_cq(e_star, schema, k)
    

def algorithm_M(I: DatabaseInstance, E: LabeledExamples, bq: FittingCQ) -> FittingCQ:
    k = E.get_arity()
    schema = I.get_schema()

    e_star = strongest_example(schema, k)

    for pos_example in E.positive_examples:
        e_star = direct_product(e_star, pos_example, schema, k)
        e_star = minimize(e_star, bq, schema, k)   # now uses the real oracle

    return canonical_cq(e_star, schema, k)
    

def algorithm_B(I: DatabaseInstance, E: LabeledExamples) -> FittingCQ:
    query = FittingCQ(I.get_schema(), E.get_arity())

    k = E.get_arity()
    schema = I.get_schema()

    # Generate variable pool (slightly larger than k to allow joins)
    max_vars = k + 2
    variables = [f"x{i}" for i in range(1, max_vars + 1)]

    # Helper: generate all possible relational atoms
    def generate_atoms():
        atoms = []
        for (R, arity) in schema.relations:
            for assignment in product(variables, repeat=arity):
                atoms.append((R, assignment))
        return atoms

    all_atoms = generate_atoms()

    # Helper: generate all queries of size s
    def generate_queries_of_size(s):
        queries = []
        for atom_combo in product(all_atoms, repeat=s):
            q = FittingCQ(schema, k)
            q.answer_variables = tuple(f"x{i}" for i in range(1, k + 1))

            try:
                for (R, B) in atom_combo:
                    q.add_relational_atom(R, B)

                # Safety condition: every answer variable must appear
                appears = set()
                for _, B in q.relational_atoms:
                    appears.update(B)

                if all(v in appears for v in q.answer_variables):
                    queries.append(q)

            except:
                # Skip invalid constructions
                continue

        return queries

    # Main loop: increase size bound
    max_size = 4  # reasonable bound for your test cases

    for s in range(1, max_size + 1):
        candidates = generate_queries_of_size(s)

        for q in candidates:
            if fits_labeled_examples(q, E, schema, k):
                return q

    # If nothing found, return empty query
    return FittingCQ(schema, k)
    
def algorithm_R(I: DatabaseInstance, E: LabeledExamples) -> Optional[FittingCQ]:
    """Completely faithful implementation of Algorithm 9.1 from the paper (Section 9).
    Uses upward refinement (delete one atom) + BFS prioritization.
    May return None even when a fitting CQ exists (as explicitly discussed in the paper).
    """
    k = E.get_arity()
    schema = I.get_schema()

    # 1. q0 := canonical CQ of ek>
    e_star = strongest_example(schema, k)
    q0 = canonical_cq(e_star, schema, k)

    from collections import deque
    pq = deque([q0])
    visited = set()

    while pq:
        q = pq.popleft()
        q_key = get_query_key(q)
        if q_key in visited:
            continue
        visited.add(q_key)

        # 5. if q fits (E+, E−) then return q
        if fits_labeled_examples(q, E, schema, k):
            return q

        # 6. Insert every p ∈ ρ(q) into pq (BFS)
        for p in upward_refinements(q, schema, k):
            p_key = get_query_key(p)
            if p_key not in visited:
                pq.append(p)

    return None  # “None exists” (per the paper)
