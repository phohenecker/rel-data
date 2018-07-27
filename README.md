rel-data
========


From a developers point of view, working with relational data or knowledge graphs is frequently cumbersome, and often
connected with considerable coding effort.
Therefore, this repository provides a Python package, `reldata`, which implements tools for creating knowledge graphs
as well as reading and writing them to and from disk, respectively.
Although `reldata` has originally been implemented to be used in the context of relational machine learning, the offered
tools are useful for working with relational data in general, and not tied to this particular use case.

**There is one caveat**, though: all functionality provided by `reldata` is confined to knowledge graphs that make use
of unary and binary predicates, i.e., classes and relations, only.
Any predicates of an arity greater than two cannot be handled by this package.


Installation
------------

The package `reldata` can be installed from PyPI:

```
pip install git+http://git.paho.at/phohenecker/rel-data
```


Data Format
-----------

Along with the code in this repository, I introduce a novel format for storing relational data, which I simply refer to
as *rel-data format*.
The reason for this is that, in my humble opinion, existing data formats are not just hard to read and interpret by
humans, but also impractical for applications like machine learning.
In contrast to this, data that is stored as rel-data is easily understood, and, by means of the package provided in this
repository, easy to read and write as well.
More importantly, however, it allows for a distinction between factual, inferable, and just predictable data.
This differs from most other formats, which are intended to store facts only, while everything else has to be inferred,
for example, by means of symbolic reasoning.

In the rel-data format, every knowledge graph is split into 13 different text files.
While this might seem inordinate at first sight, each of these files has a very clear and simple structure, and thus
achieves a maximum level of readability.
To advertise that the files together describe one single knowledge graph, they all share the same basic filename, which
I simply refer to as the *base name*, but exhibit different suffixes.
For example, the following files specify a knowledge graph with base name `kg-01`: 

```
kg-01.classes
kg-01.classes.data
kg-01.classes.data.inf
kg-01.classes.data.pred
kg-01.individuals
kg-01.literals
kg-01.literals.data
kg-01.literals.data.inf
kg-01.literals.data.pred
kg-01.relations
kg-01.relations.data
kg-01.relations.data.inf
kg-01.relations.data.pred
```

In the next few sections, I describe all of the 13 files in detail.


### Vocabulary

*`.individuals` / `.classes` / `.relations` / `.literals`*

These four files specify the vocabulary that is used to describe the knowledge graph, including individuals, classes
(i.e., unary predicates), relations (i.e., binary predicates), and literals.
They all have the same format: every line defines a single element as a pair of an unique numeric ID together with
a unique name:

```
<ID> <NAME>
```

There are a few aspects to keep in mind, though.
IDs are non-negative integers, and have to be assigned consecutively starting from 0.
For example, if `.classes` specifies *n*+1 different classes, then it has to look like this:

```
0 class-0
1 class-1
...
n class-n
```

This means that IDs correspond with line indices (starting from 0), and are thus actually superfluous.
Nevertheless, they have to be specified in order to improve readability.
Names are unique non-empty strings that do not contain any whitespaces, and are separated from the corresponding IDs by
an arbitrary number of tabs or blanks (or both).


### Facts

*`.classes.data` / `.relations.data` / `.literals.data`*

All of the facts that are known about a knowledge graph are specified in these three files.

- `.classes.data`:
  This file stores information about specified class memberships, and contains one line for each individual specified in
  `.individuals` ordered by index.
  To that end, every line describes a three-valued incidence vector that indicates the membership states of the
  according individual with respect to all classes that are defined in `.classes`:

  ```
  <INDICATOR CLASS 0> <INDICATOR CLASS 1> <INDICATOR CLASS 2> ...
  ```
  
  For instance, suppose that we are facing a knowledge graph that contains two individuals and three classes, and
  `.classes.data` looks like this:
  
  ```
  1 0 -1
  0 1  0
  ```
  
  This file specifies that the individual with index 0 is a member of the class with index 0, but not so of the class
  with index 2.
  In contrast to this, however, the `0` at the second position of the first line indicates that we do not have any
  knowledge of the individual's membership status with respect to the class with index 1.
  Similarly, the second line tells that the individual with index 1 is a member of the class with index 1, which is the
  only detail that is known about this individual.

- `.relations.data`:
  This file specifies all facts about relations that (not) exist in a knowledge graph.
  Thereby, every line describes one such relation in the common triple format, such that each of the three components is
  identified by means of its ID.
  Additionally, every triple is preceded by either `+` or `-`, which indicates whether the statement is positive or
  negative, i.e., whether the triple exists or is known to not exist:

  ```
  <+|-> <SUBJECT-ID> <PREDICATE-ID> <OBJECT-ID>
  ```
  
  As an example, consider the following version of `.relations.data`:
  
  ```
  + 1 0 2
  - 2 1 0
  ```
  
  The first line of this example states that the according knowledge graph contains the relation described by the
  predicate
  *relation-0*(*individual-1*, *individual-2*)
  or, written as triple,
  (*individual-1*, *relation-0*, *individual-2*).
  In contrast to this, line two clarifies the absence of a relation, which can be interpreted as the negated predicate
  *~relation-1*(*individual-2*, *individual-0*).

- `.literals.data`:
  Finally, this file describes all specified literals that exist as facts in the knowledge graph.
  Like relations before, literals are specified as triples.
  Notice, however, that there is no support for negated literals: 

  ```
  <INDIVIDUAL-ID> <LITERAL-ID> <VALUE>
  ```
  
  Note further that, unlike everything that we have seen before, the value of a literal may contain tabs or blanks.
  For example, the line
  
  ```
  1 3 Donald Duck
  ```
  
  specifies that the individual with index 1 is associated with the value `Donald Duck`, and the type of this value is
  identified by the literal with index 3.


### Inferences and Predictions

*`.classes.data.inf`  / `.relations.data.inf`  / `.literals.data.inf`*  
*`.classes.data.pred` / `.relations.data.pred` / `.literals.data.pred`*

As mentioned earlier already, the rel-data format offers the possibility to explicitly store information that is
actually supposed to be inferred from or predicted based on the facts in a knowledge graph (as described in the
previous section).
In fact, we make a clear distinction between these two kinds of data:

- *Inferable* information refers to any (possibly negated) class memberships, relations, or literals that may be derived
  from the facts in the knowledge graph with certainty.
  Therefore, this category comprises, for example, details that can be inferred by means of symbolic reasoning,
  logic programs, rule-based systems, etc.
  
- In contrast to this, *predictions* describe details that are not derivable in the sense used above, but are supposed
  to be predicted based on the facts (and possibly inferable data) available.
  This covers many tasks that are encountered in the context of machine learning.

Files that specify inferences exhibit the file extension `.inf`, and those describing predictions are marked with
`.pred`.
Furthermore, just like for facts, we use separate files for classes, relations, and literals. 


User Guide
----------

The user guide for the package `reldata` is still being developed, and will be uploaded as soon as it is ready.
Meanwhile, please refer to the documentation that is provided as part of the source code.
