# Unit 8 e-Portfolio Activity: Constituency Parse Trees

The trees use the following phrase labels: sentence (`S`), noun phrase (`NP`), verb phrase (`VP`), determiner (`Det`), noun (`N`), verb (`V`), adjective (`Adj`), preposition (`P`) and prepositional phrase (`PP`).

## 1. The government raised interest rates

```text
S
|-- NP
|   |-- Det: The
|   `-- N: government
`-- VP
    |-- V: raised
    `-- NP
        |-- N: interest
        `-- N: rates
```

Bracketed form:

```text
[S [NP [Det The] [N government]] [VP [V raised] [NP [N interest] [N rates]]]]
```

## 2. The internet gives everyone a voice

```text
S
|-- NP
|   |-- Det: The
|   `-- N: internet
`-- VP
    |-- V: gives
    |-- NP
    |   `-- N: everyone
    `-- NP
        |-- Det: a
        `-- N: voice
```

Here, `everyone` is the indirect object and `a voice` is the direct object of the ditransitive verb `gives`.

Bracketed form:

```text
[S [NP [Det The] [N internet]] [VP [V gives] [NP [N everyone]] [NP [Det a] [N voice]]]]
```

## 3. The man saw the dog with the telescope

This sentence has a prepositional-phrase attachment ambiguity. Its syntax permits at least two interpretations.

### Reading A: the man used the telescope

The `PP` modifies the verb phrase `saw`.

```text
S
|-- NP
|   |-- Det: The
|   `-- N: man
`-- VP
    |-- V: saw
    |-- NP
    |   |-- Det: the
    |   `-- N: dog
    `-- PP
        |-- P: with
        `-- NP
            |-- Det: the
            `-- N: telescope
```

```text
[S [NP [Det The] [N man]] [VP [V saw] [NP [Det the] [N dog]] [PP [P with] [NP [Det the] [N telescope]]]]]
```

### Reading B: the dog had the telescope

The `PP` modifies the noun phrase `the dog`.

```text
S
|-- NP
|   |-- Det: The
|   `-- N: man
`-- VP
    |-- V: saw
    `-- NP
        |-- Det: the
        |-- N: dog
        `-- PP
            |-- P: with
            `-- NP
                |-- Det: the
                `-- N: telescope
```

```text
[S [NP [Det The] [N man]] [VP [V saw] [NP [Det the] [N dog] [PP [P with] [NP [Det the] [N telescope]]]]]]
```

The two structures show why syntax alone may not resolve meaning. An intelligent agent may need semantic and contextual evidence to select the intended interpretation.