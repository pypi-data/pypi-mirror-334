import imy.docstrings


class Parent



docs = imy.docstrings.Docstring.from_string(
    docstring,
    key_sections=["key section"],
)


print(docs.key_sections["key section"])
