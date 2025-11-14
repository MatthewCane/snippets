from dataclasses import dataclass


class TemplateError(Exception):
    pass


template = """
# {title}

{body}

---

{footer}
""".strip()


@dataclass
class Article:
    title: str
    body: str
    footer: str
    other: str | None = None

    def apply_to_template(self, template: str) -> str:
        try:
            return template.format(**self.__dict__)
        except KeyError as e:
            raise TemplateError("Failed to apply template: ", e) from e


format_article = Article(
    title="Python String Formatting",
    body="String formatting is for formatting strings",
    footer="For more info, see the docs",
)

print(format_article.apply_to_template(template))
