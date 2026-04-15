from project import *

# PRESIDENTS

presidents_schema = DatabaseSchema("Presidents Schema")
presidents_schema.add_relation("Businessman", 1)
presidents_schema.add_relation("Economist", 1)
presidents_schema.add_relation("Democrat", 1)
presidents_schema.add_relation("Republican", 1)
presidents_schema.add_relation("Father", 2)

presidents_instance = DatabaseInstance("Presidents Instance", presidents_schema)
presidents_instance.add_fact("Businessman", ("donald", ))
presidents_instance.add_fact("Businessman", ("fred", ))
presidents_instance.add_fact("Businessman", ("james", ))
presidents_instance.add_fact("Economist", ("barack-sr", ))
presidents_instance.add_fact("Democrat", ("barack", ))
presidents_instance.add_fact("Democrat", ("franklin", ))
presidents_instance.add_fact("Republican", ("donald", ))
presidents_instance.add_fact("Father", ("barack-sr", "barack", ))
presidents_instance.add_fact("Father", ("fred", "donald", ))
presidents_instance.add_fact("Father", ("james", "franklin", ))

# CASE 1 - unary examples

presidents_examples_1 = LabeledExamples(1)
presidents_examples_1.add_positive_example(presidents_instance, ("franklin", ))
presidents_examples_1.add_positive_example(presidents_instance, ("barack", ))
presidents_examples_1.add_negative_example(presidents_instance, ("donald", ))

print("Testing algorithm P")
print(f"{algorithm_P(presidents_instance, presidents_examples_1)}")

"""
ANSWER

q = FittingCQ(presidents_schema, 1)
q.add_relational_atom("Democrat", ("x1", ))

because

("franklin") is a positive example

    ("franklin") in Democrat

("barack") is a positive example

    ("barack") in Democrat

("donald") is a negative example

    ("donald") not in Democrat

"""

# CASE 2 - unary examples

presidents_examples_2 = LabeledExamples(1)
presidents_examples_2.add_positive_example(presidents_instance, ("franklin", ))
presidents_examples_2.add_positive_example(presidents_instance, ("donald", ))
presidents_examples_2.add_negative_example(presidents_instance, ("barack", ))

"""
ANSWER

q = FittingCQ(presidents_schema, 1)
q.add_relational_atom("Father", ("x2", "x1"))
q.add_relational_atom("Businessman", ("x2", ))

because

("franklin") is a positive example

    ("james", "franklin") in Father
    ("james") in Businessman

("donald") is a positive example

    ("fred", "donald") in Father
    ("fred") in Businessman

("barack") is a negative example

    ("barack-sr", "barack") in Father
    ("barack-sr") not in Businessman

"""

# CASE 3 - unary examples with no fitting CQ
# (should only be run against algorithm R)

presidents_examples_3 = LabeledExamples(1)
presidents_examples_3.add_positive_example(presidents_instance, ("barack", ))
presidents_examples_3.add_positive_example(presidents_instance, ("donald", ))
presidents_examples_3.add_negative_example(presidents_instance, ("franklin", ))

"""
ANSWER

q = None

because

there is no fitting CQ where

    ("barack") and ("donald") are positive examples
    ("franklin") is a negative example

"""

# CASE 4 - binary examples

presidents_examples_4 = LabeledExamples(2)
presidents_examples_4.add_positive_example(presidents_instance, ("barack-sr", "barack"))
presidents_examples_4.add_negative_example(presidents_instance, ("fred", "donald"))

"""
ANSWER

q = FittingCQ(presidents_schema, 2)
q.add_relational_atom("Father", ("x1", "x2"))
q.add_relational_atom("Economist", ("x1", ))

because

("barack-sr", "barack") is a positive example

    ("barack-sr", "barack") in Father
    ("barack-sr") in Economist

("fred", "donald") is a negative example

    ("fred", "donald") in Father
    ("fred") not in Economist

"""

# CASE 5 - binary examples

presidents_examples_5 = LabeledExamples(2)
presidents_examples_5.add_positive_example(presidents_instance, ("fred", "donald"))
presidents_examples_5.add_negative_example(presidents_instance, ("barack-sr", "barack"))

"""
ANSWER

q = FittingCQ(presidents_schema, 2)
q.add_relational_atom("Father", ("x1", "x2"))
q.add_relational_atom("Republican", ("x2", ))

because

("fred", "donald") is a positive example

    ("fred", "donald") in Father
    ("donald") in Republican

("barack-sr", "barack") is a negative example

    ("barack-sr", "barack") in Father
    ("barack") not in Republican

"""

# CASE 6 - binary examples

presidents_examples_6 = LabeledExamples(2)
presidents_examples_6.add_positive_example(presidents_instance, ("james", "franklin"))
presidents_examples_6.add_negative_example(presidents_instance, ("barack-sr", "barack"))
presidents_examples_6.add_negative_example(presidents_instance, ("fred", "donald"))

"""
ANSWER

q = FittingCQ(presidents_schema, 2)
q.add_relational_atom("Father", ("x1", "x2"))
q.add_relational_atom("Businessman", ("x1", ))
q.add_relational_atom("Democrat", ("x2", ))

because

("james", "franklin") is a positive example

    ("james", "franklin") in Father
    ("james") in Businessman
    ("franklin") in Democrat

("barack-sr", "barack") is a negative example

    ("barack-sr", "barack") in Father
    ("barack-sr") not in Businessman
    ("barack") in Democrat

("fred", "donald") is a negative example

    ("fred", "donald") in Father
    ("fred") in Businessman
    ("donald") not in Democrat

"""
