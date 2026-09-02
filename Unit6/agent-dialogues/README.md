# Alice and Bob KQML/KIF Dialogue

This Unit 6 e-Portfolio project implements a short dialogue between:

- **Alice**, a procurement agent seeking information about 50-inch televisions.
- **Bob**, a warehouse agent controlling stock-level information.

Alice sends two KQML `ask-one` messages. Their content is expressed as KIF
logical statements using the shared `warehouse-stock` ontology. Bob answers each
request with a correlated KQML `tell` message.

## Run the dialogue

```bash
python3 agent_dialogue.py
```

The transcript shows four messages:

1. Alice asks how many 50-inch televisions are available.
2. Bob reports that 18 are available.
3. Alice asks how many HDMI slots those televisions have.
4. Bob reports that they have 4 HDMI slots.

## Run the tests

```bash
python3 -m unittest -v
```

The implementation uses only the Python standard library. It demonstrates the
separation between the KQML communication act (`ask-one` or `tell`) and the KIF
content describing the warehouse fact being queried or reported.
