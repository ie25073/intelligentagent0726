# Alice and Bob KQML/KIF Dialogue

This Unit 6 e-Portfolio project implements a short dialogue between:

- **Alice**, a procurement agent seeking information about 50-inch televisions.
- **Bob**, a warehouse agent controlling stock-level information.

Alice sends two KQML `ask-one` messages. Their content is expressed as formal
KIF conjunctions using variables and the shared `warehouse-stock` ontology.
Bob answers each request with a correlated KQML `tell` message. Every message
also carries the same conversation ID so the complete exchange can be tracked.

## Run the dialogue

```bash
python3 agent_dialogue.py
```

The enhanced transcript provides numbered stages, a plain-English explanation
of each KQML/KIF message and a final procurement summary. It shows four messages:

1. Alice asks how many 50-inch televisions are available.
2. Bob reports that 18 are available.
3. Alice asks how many HDMI slots those televisions have.
4. Bob reports that they have 4 HDMI slots.

To demonstrate Bob's error handling, request a size that is not in the sample
warehouse inventory:

```bash
python3 agent_dialogue.py --size 55
```

Bob responds with the KQML `sorry` performative and KIF content explaining that
the requested television size is unknown.

## Run the tests

```bash
python3 -m unittest -v
```

The implementation uses only the Python standard library. It demonstrates the
separation between the KQML communication act (`ask-one`, `tell` or `sorry`) and
the KIF content describing the warehouse fact being queried or reported.
