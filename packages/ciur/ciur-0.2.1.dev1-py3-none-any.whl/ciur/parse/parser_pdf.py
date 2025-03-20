from pdfminer.pdfdevice import TagExtractor
from pdfminer.pdfinterp import PDFResourceManager, process_pdf

from io import BytesIO, StringIO

from ciur.models import Document
from .parse_xml import xml_type


def pdf_type(document, rule, rule_file_path=None):
    """
    use this function if page is pdf
    TODO: do not forget to document this

    :param rule_file_path:
        :type rule_file_path: str

    :param rule:
        :type rule: Rule

    :param document: Document to be parsed
        :type document: Document

    :rtype: OrderedDict
    """

    class MyIO(StringIO):
        encoding = "utf-8"

    resource_manager = PDFResourceManager()

    out_fp = MyIO()
    in_fp = BytesIO(document.content)

    device = TagExtractor(resource_manager, out_fp)

    process_pdf(resource_manager, device, in_fp)

    out_fp.seek(0)  # reset the buffer position to the beginning

    xml = Document(
        out_fp.read(),
        namespace=document.namespace,
        url=document.url
    )
    return xml_type(xml, rule, rule_file_path)
