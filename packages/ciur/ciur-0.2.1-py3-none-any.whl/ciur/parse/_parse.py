"""
parse page based on ciur rules and page type (xml, html ...)

NOTE:
    local convention for all public paring function is `[a-z]+[a-z0-9_]+_type`
    is should end with "_type"
"""
from typing import Any, Dict

import sys

from collections import OrderedDict
import logging
import decimal

# noinspection PyProtectedMember
from lxml.etree import _Element as EtreeElement
from lxml.cssselect import CSSSelector
from lxml import etree

from ciur.exceptions import CiurBaseException

LOG = logging.getLogger(__name__)


NOT_NULL_TYPES = (bool, float, str, decimal.Decimal)


def _is_list(value):
    """
    check if is list
    :param value:
    :type value: str
    :rtype bool
    """
    return value.endswith("_list")


def _is_dict(value):
    """
    check if is dict
    :param value:
    :type value: str
    :rtype bool
    """
    return value.endswith("_dict")


def _type_list_casting(type_list, res, url):
    for fun, args in type_list[:-1]:
        tmp = []

        if getattr(fun, "process_list", None):
            res = [fun(None, res, *args)]
        else:
            for res_i in res:
                if fun.__name__.startswith("fn_"):
                    res_i = fun(None, res_i, *args)
                elif fun.__name__ == "url_":
                    res_i = fun(res_i, url)
                else:
                    try:
                        res_i = fun(res_i, *args)
                    except (TypeError,) as type_error:
                        print(type_error, file=sys.stderr)
                        # TODO fix this

                # filter null results
                if res_i not in [None, ""]:
                    tmp.append(res_i)

            res = tmp

    return res


def _evaluate_xpath(rule, context_, doctype, rule_file_path):
    selector = rule.selector

    if rule.selector_type == "xpath":
        xpath = selector
    elif rule.selector_type == "css":
        css = CSSSelector(
            selector,
            translator=doctype,
            namespaces=context_.nsmap
        )
        xpath = css.path
    else:
        assert False, "unknown rule.selector_type `%s`" % rule.selector_type

    try:
        return context_.xpath(xpath)
    except (etree.XPathEvalError,) as xpath_eval_error:
        raise CiurBaseException(xpath_eval_error, {
            "rule.name": rule.name,
            "rule.selector": rule.selector,
            "rule_file_path": rule_file_path
        })


def _shrink(res, it_list):
    if not it_list and isinstance(res, list) and len(res) == 1:
        return _shrink(res[0], it_list)

    return res


def _stretch(res):
    if isinstance(res, NOT_NULL_TYPES):
        res = [res]

    return res


def _name_colon(res, name):
    rule_name_list = name.split(":")
    if _is_list(rule_name_list[-1]):
        rule_name_list = [
            i if _is_list(i) else i + "_list" for i in rule_name_list
        ]

    return OrderedDict((i, res) for i in rule_name_list)


def _size_match_assert(res, rule, url, size, args):
    # do size match check
    try:
        size(len(res), *args)
    except (AssertionError,) as assert_error:
        raise CiurBaseException({
            "rule.name": rule.name,
            "rule.selector": rule.selector,
            "url": url
        }, "size-match error -> %s, on rule `%s` %s but got %s element" % (
            assert_error, rule.name, args, len(res)
        ))


def _recursive_parse(context_, rule, doctype, rule_file_path=None):
    """
    recursive parse embedded rules
    :param: context_:
        :type: context_: lxml.etree._ElementTree
    """

    res = _evaluate_xpath(rule, context_, doctype, rule_file_path)

    res = _stretch(res)
    res = _type_list_casting(rule.type_list, res, context_.base)

    if isinstance(res, list) and len(res) and isinstance(res[0], EtreeElement):
        tmp_list = []
        if rule.rule:
            for res_i in res:
                tmp_ordered_dict = OrderedDict()
                for rule_i in rule.rule:
                    data = _recursive_parse(
                        res_i,
                        rule_i,
                        doctype,
                        rule_file_path=rule_file_path
                    )
                    if len(data):
                        tmp_ordered_dict.update(data)

                if tmp_ordered_dict:
                    tmp_list.append(tmp_ordered_dict)

            res = tmp_list

    # filter empty items
    res = [i for i in res if i != ""]

    res = _stretch(res)

    if _is_dict(rule.name):

        # pylint: disable=redefined-variable-type
        res = OrderedDict((i.pop(rule.rule[0].name), i) for i in res)

    _size_match_assert(res, rule, context_.base, *rule.type_list[-1])

    res = _shrink(res, _is_list(rule.name))

    if rule.rule and (
            isinstance(res, NOT_NULL_TYPES) or
            res and isinstance(res, list) and
            isinstance(res[0], NOT_NULL_TYPES)
    ):
        import sys
        sys.stderr.write("[WARN] there are children that were ignored on"
                         " rule.name=`%s`\n" % rule.name)

    if isinstance(res, etree._Element):
        return res
    elif not res and not isinstance(res, NOT_NULL_TYPES):
        return res
    else:
        if res == "":
            return None

        if ":" not in rule.name:
            return {rule.name: res}

        return _name_colon(res, rule.name)


def _prepare_context(context_, url=None):
    if isinstance(context_, EtreeElement):
        pass
    else:
        context_ = context_.getroot()

    if url:
        context_.base = url

    return context_
