from typing import Any

import html5lib

from ._parse import _prepare_context, _recursive_parse


def html_type(document, rule, rule_file_path=None) -> dict[str, Any]:
    """
    use this function if page is html

    :param rule_file_path:
        :type rule_file_path: str

    :param rule:
        :type rule: Rule

    :param document: Document to be parsed
        :type document: Document

    :rtype: OrderedDict
    """

    context = html5lib.parse(
        document.content,
        treebuilder="lxml",
        namespaceHTMLElements=document.namespace,
    )

    context = _prepare_context(context, document.url)

    return _recursive_parse(context, rule, "html", rule_file_path)
