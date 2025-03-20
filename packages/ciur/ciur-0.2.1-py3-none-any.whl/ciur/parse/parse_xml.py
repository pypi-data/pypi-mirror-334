from lxml import etree
from ._parse import _prepare_context, _recursive_parse

def xml_type(document, rule, rule_file_path=None):
    """
    use this function if page is xml
    :param rule:
        :type rule: Rule

    :param document: Document to be parsed
        :type document: Document

    :param rule_file_path:
        :type rule_file_path: str

    :rtype: OrderedDict
    """

    context = etree.fromstring(document.content)

    context = _prepare_context(context, document.url)

    return _recursive_parse(context, rule, "xml", rule_file_path)
