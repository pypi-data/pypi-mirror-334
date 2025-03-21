# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
import numbers # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args
try:
    from dash.development.base_component import ComponentType # noqa: F401
except ImportError:
    ComponentType = typing.TypeVar("ComponentType", bound=Component)


class PdfViewer(Component):
    """A PdfViewer component.
Component description

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- highlights (list of dicts; optional):
    the highlights.

    `highlights` is a list of dicts with keys:

    - id (string; required)

    - position (dict; required)

        `position` is a dict with keys:

        - boundingRect (dict; required)

            `boundingRect` is a dict with keys:

            - x1 (number; required)

            - y1 (number; required)

            - x2 (number; required)

            - y2 (number; required)

            - width (number; required)

            - height (number; required)

            - pageNumber (number; optional)

        - rects (list of dicts; required)

            `rects` is a list of dicts with keys:

    - x1 (number; required)

    - y1 (number; required)

    - x2 (number; required)

    - y2 (number; required)

    - width (number; required)

    - height (number; required)

    - pageNumber (number; optional)

        - pageNumber (number; required)

        - usePdfCoordinates (boolean; optional)

    - content (dict; required)

        `content` is a dict with keys:

        - text (string; optional)

        - image (string; optional)

    - comment (dict; required)

        `comment` is a dict with keys:

        - text (string; required)

        - emoji (string; required)

- scrollTo (dict; optional):
    scroll to active highlight.

    `scrollTo` is a dict with keys:

    - id (string; required)

    - timestamp (dict; required)

        `timestamp` is a dict with keys:

        - toString (optional):
            Returns a string representation of an object.
            @,param,radix, ,Specifies a radix for converting numeric
            values to strings. This value is only used for numbers.

        - toFixed (required):
            Returns a string representing a number in fixed-point
            notation. @,param,fractionDigits, ,Number of digits after
            the decimal point. Must be in the range 0 - 20, inclusive.

        - toExponential (required):
            Returns a string containing a number represented in
            exponential notation. @,param,fractionDigits, ,Number of
            digits after the decimal point. Must be in the range 0 -
            20, inclusive.

        - toPrecision (required):
            Returns a string containing a number represented either in
            exponential or fixed-point notation with a specified
            number of digits. @,param,precision, ,Number of
            significant digits. Must be in the range 1 - 21,
            inclusive.

        - valueOf (optional):
            Returns the primitive value of the specified object.

        - toLocaleString (dict; optional):
            Converts a number to a string by using the current or
            specified locale. @,param,locales, ,A locale string or
            array of locale strings that contain one or more language
            or locale tags. If you include more than one locale
            string, list them in descending order of priority so that
            the first entry is the preferred locale. If you omit this
            parameter, the default locale of the JavaScript runtime is
            used. @,param,options, ,An object that contains one or
            more properties that specify comparison options.
            @,param,locales, ,A locale string, array of locale
            strings, Intl.Locale object, or array of Intl.Locale
            objects that contain one or more language or locale tags.
            If you include more than one locale string, list them in
            descending order of priority so that the first entry is
            the preferred locale. If you omit this parameter, the
            default locale of the JavaScript runtime is used.
            @,param,options, ,An object that contains one or more
            properties that specify comparison options.

            `toLocaleString` is a dict with keys:


- url (string; optional):
    The URL of the PDF file."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_pdf_highlighter'
    _type = 'PdfViewer'
    HighlightsPositionBoundingRect = TypedDict(
        "HighlightsPositionBoundingRect",
            {
            "x1": typing.Union[int, float, numbers.Number],
            "y1": typing.Union[int, float, numbers.Number],
            "x2": typing.Union[int, float, numbers.Number],
            "y2": typing.Union[int, float, numbers.Number],
            "width": typing.Union[int, float, numbers.Number],
            "height": typing.Union[int, float, numbers.Number],
            "pageNumber": NotRequired[typing.Union[int, float, numbers.Number]]
        }
    )

    HighlightsPositionRects = TypedDict(
        "HighlightsPositionRects",
            {
            "x1": typing.Union[int, float, numbers.Number],
            "y1": typing.Union[int, float, numbers.Number],
            "x2": typing.Union[int, float, numbers.Number],
            "y2": typing.Union[int, float, numbers.Number],
            "width": typing.Union[int, float, numbers.Number],
            "height": typing.Union[int, float, numbers.Number],
            "pageNumber": NotRequired[typing.Union[int, float, numbers.Number]]
        }
    )

    HighlightsPosition = TypedDict(
        "HighlightsPosition",
            {
            "boundingRect": "HighlightsPositionBoundingRect",
            "rects": typing.Sequence["HighlightsPositionRects"],
            "pageNumber": typing.Union[int, float, numbers.Number],
            "usePdfCoordinates": NotRequired[bool]
        }
    )

    HighlightsContent = TypedDict(
        "HighlightsContent",
            {
            "text": NotRequired[str],
            "image": NotRequired[str]
        }
    )

    HighlightsComment = TypedDict(
        "HighlightsComment",
            {
            "text": str,
            "emoji": str
        }
    )

    Highlights = TypedDict(
        "Highlights",
            {
            "id": str,
            "position": "HighlightsPosition",
            "content": "HighlightsContent",
            "comment": "HighlightsComment"
        }
    )

    ScrollToTimestampToLocaleString = TypedDict(
        "ScrollToTimestampToLocaleString",
            {

        }
    )

    ScrollToTimestamp = TypedDict(
        "ScrollToTimestamp",
            {
            "toString": NotRequired[typing.Any],
            "toFixed": typing.Any,
            "toExponential": typing.Any,
            "toPrecision": typing.Any,
            "valueOf": NotRequired[typing.Any],
            "toLocaleString": NotRequired["ScrollToTimestampToLocaleString"]
        }
    )

    ScrollTo = TypedDict(
        "ScrollTo",
            {
            "id": str,
            "timestamp": "ScrollToTimestamp"
        }
    )

    @_explicitize_args
    def __init__(
        self,
        url: typing.Optional[str] = None,
        highlights: typing.Optional[typing.Sequence["Highlights"]] = None,
        scrollTo: typing.Optional["ScrollTo"] = None,
        style: typing.Optional[typing.Any] = None,
        id: typing.Optional[typing.Union[str, dict]] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'highlights', 'scrollTo', 'style', 'url']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'highlights', 'scrollTo', 'style', 'url']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(PdfViewer, self).__init__(**args)
