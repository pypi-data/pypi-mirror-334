#
# Blob Object Dumper - pretty print json/html/xml and others in the future.
#
import sys
import json
import warnings
from typing import Any, Callable

import requests
from bs4 import BeautifulSoup as bs
import bs4.formatter as bs_fmt
from bs4 import GuessedAtParserWarning
warnings.filterwarnings('ignore', category=GuessedAtParserWarning)

__version__ = "1.0.3"
__copyright__ = "Copyright 2025, Aaron Edwards"
__license__ = "MIT"

# hack to make the root module callable - thanks https://stackoverflow.com/questions/1060796/callable-modules
class CallModule(sys.modules[__name__].__class__):
    def __call__(self, *args, **kwargs):  # module callable
        return _bod(*args, **kwargs)

sys.modules[__name__].__class__ = CallModule

def _bod(*args, **kwargs):
    return dmp(*args, **kwargs)

# actual module
def dmp(data: Any, indent: str | int=4, sort_keys: bool=True, output: Callable[[str], Any]=print) -> str | None:
    """
    Converts and formats the given data into a human-readable form. This function can handle various types
    of input data including JSON, HTML, bytes, and other Python objects. The formatted output can either
    be returned as a string or passed to a callable output function like `print`.

    :param data: Input data to be processed. It can be of any type and is formatted into a readable form.
    :param indent: The number of spaces or characters used for indentation in the formatted output.
    :param sort_keys: When set to True, sorts dictionaries in the JSON output by their keys.
    :param output: A callable function that processes the formatted output. If None, the function returns
        the formatted output as a string.
    :return: Returns the formatted output as a string if the `output` parameter is set to None. Otherwise,
        returns None when the output is directly passed to the specified callable.
    """
    final_output = None
    final_decision = False

    # first check for requests.Response
    try:
        working_data = data.content
    except (TypeError, ValueError, AttributeError):
        working_data = data

    # quick check for bytes, decode to string.
    if isinstance(working_data, bytes):
        working_data = working_data.decode('utf-8')

    # check if is str, if so - parse based on how it's interpreted
    if isinstance(working_data, str):
        # check if JSON serializable
        try:
            working_data_parsed = json.loads(working_data)
            final_output = json.dumps(working_data_parsed, indent=indent, sort_keys=sort_keys)
            final_decision = True
        except json.JSONDecodeError:
            soup = bs(working_data)
            my_fmt = bs_fmt.Formatter(indent=indent)
            final_output = soup.prettify(formatter=my_fmt)
            final_decision = True

    if not final_decision:
        # got here, it's not a string or byte

        try:
            # attempt json dump the object. If it's a dict-type or list-type - this works.
            final_output = json.dumps(working_data, indent=indent, sort_keys=sort_keys)
            final_decision = True
        except (TypeError, ValueError, AttributeError):
            # it didn't like it - just print whatever we got!
            final_output = working_data
            final_decision = True

    # output the data
    if output is not None:
        output(final_output)
        return None
    else:
        # no output, return the data.
        return final_output

def dmpdetail(data: Any, indent: str | int=4, sort_keys: bool=True, output: Callable[[str], Any]=print,
             sensitive: bool=False, sensitive_cookies: list[str] | None=None, sensitive_headers: list[str] | None=None
             ) -> str | None:
    """
    Generates a detailed log or formatted output of the provided data, particularly useful
    for logging HTTP request and response details while accounting for sensitive information
    in headers and cookies.

    This function supports customization in output format and anonymization of sensitive
    data. If the input is a Response object, details of the HTTP request and response
    will be extracted and formatted. Sensitive headers and cookies can be selectively
    redacted based on the given parameters. Additionally, it supports serialization of
    request/response bodies and arbitrary data structures into a formatted string for
    output or return.

    :param data: The input data to be detailed. Can be a Response object or any other
        data structure. If it is a Response object, request and response details
        are extracted specifically.
    :param indent: Number representing the indentation level for formatted output.
        Default is 4 for better readability. A string can also be passed for custom
        indentation.
    :param sort_keys: Boolean indicating if JSON objects should have their keys
        sorted while serializing request/response bodies or data structures. Useful
        for consistent formatting.
    :param output: A callable accepting a single string argument, used to handle
        the final output of the function. If not provided, `print` is used by default.
        Pass None if you expect the formatted output as a return value.
    :param sensitive: Boolean flag indicating whether sensitive data in headers and
        cookies should be redacted. When set to True, sensitive data is not redacted.
    :param sensitive_cookies: List of sensitive cookie names to redact. This list
        overrides the default sensitive cookie names of ['AUTH_TOKEN', 'X-AUTH-TOKEN'].
    :param sensitive_headers: List of sensitive header names to redact. This list
        overrides the default sensitive header names of ['Authorization', 'X-Auth-Token', 'JWT'].

    :return: A formatted string detailing the processed data, HTTP request/response
        information, or JSON data depending on the provided input. If the `output`
        callable is not None, the formatted string is passed to it, and the function
        returns None. If `output` is None, the formatted string is returned.
    """
    if isinstance(data, requests.Response):

        if sensitive_headers and isinstance(sensitive_cookies, list):
            s_headers = [header.lower() for header in sensitive_headers]
        else:
            s_headers = [header.lower() for header in ['Authorization', 'X-Auth-Token', 'JWT']]

        if sensitive_cookies and isinstance(sensitive_cookies, list):
            s_cookies = [cookie.lower() for cookie in sensitive_cookies]
        else:
            s_cookies = [cookie.lower() for cookie in ['AUTH_TOKEN', 'X-AUTH-TOKEN']]


        # try to be super verbose.
        final_output = f"REQUEST: {data.request.method} {data.request.path_url}\n"
        final_output += "REQUEST HEADERS:\n"
        for key, value in data.request.headers.items():
            # look for sensitive values
            if key.lower() in ['cookie'] and not sensitive:
                # we need to do some work to watch for the AUTH_TOKEN cookie. Split on cookie separator
                cookie_list = value.split('; ')
                muted_cookie_list = []
                for cookie in cookie_list:
                    # check if cookie starts with a permutation of AUTH_TOKEN/whitespace.
                    for s_cookie in s_cookies:
                        if cookie.lower().strip().startswith(f"{s_cookie}="): # s_cookie already lower()
                            # first 11 chars of cookie with whitespace removed + mute string.
                            new_cookie = cookie.strip()[:6] + "\"<SENSITIVE - NOT SHOWN BY DEFAULT>\""
                            muted_cookie_list.append(new_cookie)
                        else:
                            muted_cookie_list.append(cookie)
                # got list of cookies, muted as needed. recombine.
                muted_value = "; ".join(muted_cookie_list)
                final_output += f"\t{key}: {muted_value}\n"

            elif key.lower() in s_headers and not sensitive:
                final_output += f"\t{key}: <SENSITIVE - NOT SHOWN BY DEFAULT>\n"
            else:
                final_output += f"\t{key}: {value}\n"
        # if body not present, final_output blank.
        if not data.request.body:
            final_output += f"REQUEST BODY:\n{{}}\n\n"
        else:
            # Use formatting in main func.
            final_output += (f"REQUEST BODY:\n"
                       f"{_bod(data.request.body, indent=indent, sort_keys=sort_keys, output=None)}\n\n")
        final_output += f"RESPONSE: {data.status_code} {data.reason}\n"
        final_output += "RESPONSE HEADERS:\n"
        for key, value in data.headers.items():
            final_output += f"\t{key}: {value}\n"

        # format response data
        final_output += f"RESPONSE DATA:\n{_bod(data.content, indent=indent, sort_keys=sort_keys, output=None)}"

    else:
        # if we got here, not requests.Response. Just handle through non-detailed output. Other future handles go here.
        final_output = _bod(data, indent=indent, sort_keys=sort_keys, output=None)

    # output the data
    if output is not None:
        output(final_output)
        return None
    else:
        # no output, return the data.
        return final_output

# aliases
pretty = dmp
dump = dmp
detailed = dmpdetail