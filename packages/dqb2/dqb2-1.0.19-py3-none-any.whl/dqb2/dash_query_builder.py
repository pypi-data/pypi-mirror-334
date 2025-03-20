# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class dash_query_builder(Component):
    """A dash_query_builder component.
The Dash Query Builder component

Keyword arguments:

- id (string; optional):
    Unique ID to identify this component in Dash callbacks.

- alwaysShowActionButtons (boolean; default True):
    Whether to show action buttons all the time or just on hover.

- clear (boolean; default False):
    Whether to clear the tree.

- config (boolean | number | string | dict | list; optional):
    The config object. See the
    [Config](https://github.com/ukrbublik/react-awesome-query-builder/blob/master/CONFIG.adoc
    docs).

- debounceTime (number; default 500):
    debounce time for dynamic update.

- dynamic (boolean; default True):
    Toggles whether the tree is updated automatically or through a
    button.

- elasticSearchFormat (dict; optional):
    ElasticSearch query object.

    `elasticSearchFormat` is a dict with keys:

    - constructor (optional):
        The initial value of Object.prototype.constructor is the
        standard built-in Object constructor.

    - toString (optional):
        Returns a string representation of an object.

    - toLocaleString (optional):
        Returns a date converted to a string using the current locale.

    - valueOf (optional):
        Returns the primitive value of the specified object.

    - hasOwnProperty (optional):
        Determines whether an object has a property with the specified
        name. @,param,v, ,A property name.

    - isPrototypeOf (optional):
        Determines whether an object exists in another object's
        prototype chain. @,param,v, ,Another object whose prototype
        chain is to be checked.

    - propertyIsEnumerable (optional):
        Determines whether a specified property is enumerable.
        @,param,v, ,A property name.

- fields (dict with strings as keys and values of type boolean | number | string | dict | list; required):
    The fields to populate the query builder. See the
    [Fields](https://github.com/ukrbublik/react-awesome-query-builder/blob/master/CONFIG.adoc#configfields)
    docs.

- jsonLogicFormat (dict; optional):
    JSONLogic object.

    `jsonLogicFormat` is a dict with keys:

    - constructor (optional):
        The initial value of Object.prototype.constructor is the
        standard built-in Object constructor.

    - toString (optional):
        Returns a string representation of an object.

    - toLocaleString (optional):
        Returns a date converted to a string using the current locale.

    - valueOf (optional):
        Returns the primitive value of the specified object.

    - hasOwnProperty (optional):
        Determines whether an object has a property with the specified
        name. @,param,v, ,A property name.

    - isPrototypeOf (optional):
        Determines whether an object exists in another object's
        prototype chain. @,param,v, ,Another object whose prototype
        chain is to be checked.

    - propertyIsEnumerable (optional):
        Determines whether a specified property is enumerable.
        @,param,v, ,A property name.

- loadFormat (a value equal to: 'tree', 'jsonLogicFormat', 'spelFormat'; default 'tree'):
    The load format string. Changes the tree based on the
    corresponding prop change.

- mongoDBFormat (dict; optional):
    MongoDB query object.

    `mongoDBFormat` is a dict with keys:

    - constructor (optional):
        The initial value of Object.prototype.constructor is the
        standard built-in Object constructor.

    - toString (optional):
        Returns a string representation of an object.

    - toLocaleString (optional):
        Returns a date converted to a string using the current locale.

    - valueOf (optional):
        Returns the primitive value of the specified object.

    - hasOwnProperty (optional):
        Determines whether an object has a property with the specified
        name. @,param,v, ,A property name.

    - isPrototypeOf (optional):
        Determines whether an object exists in another object's
        prototype chain. @,param,v, ,Another object whose prototype
        chain is to be checked.

    - propertyIsEnumerable (optional):
        Determines whether a specified property is enumerable.
        @,param,v, ,A property name.

- queryString (string; optional):
    Query string.

- spelFormat (string; optional):
    SPEL query string.

- sqlFormat (string; optional):
    The WHERE clause in SQL.

- theme (a value equal to: 'mui', 'material', 'antd', 'fluent', 'bootstrap', 'basic'; default 'mui'):
    The theme/styling used.

- tree (boolean | number | string | dict | list; default emptyTree):
    The JSON representation of the tree."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dqb2'
    _type = 'dash_query_builder'
    @_explicitize_args
    def __init__(self, tree=Component.UNDEFINED, sqlFormat=Component.UNDEFINED, jsonLogicFormat=Component.UNDEFINED, mongoDBFormat=Component.UNDEFINED, queryString=Component.UNDEFINED, elasticSearchFormat=Component.UNDEFINED, spelFormat=Component.UNDEFINED, fields=Component.REQUIRED, config=Component.UNDEFINED, dynamic=Component.UNDEFINED, clear=Component.UNDEFINED, debounceTime=Component.UNDEFINED, loadFormat=Component.UNDEFINED, alwaysShowActionButtons=Component.UNDEFINED, theme=Component.UNDEFINED, id=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'alwaysShowActionButtons', 'clear', 'config', 'debounceTime', 'dynamic', 'elasticSearchFormat', 'fields', 'jsonLogicFormat', 'loadFormat', 'mongoDBFormat', 'queryString', 'spelFormat', 'sqlFormat', 'theme', 'tree']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'alwaysShowActionButtons', 'clear', 'config', 'debounceTime', 'dynamic', 'elasticSearchFormat', 'fields', 'jsonLogicFormat', 'loadFormat', 'mongoDBFormat', 'queryString', 'spelFormat', 'sqlFormat', 'theme', 'tree']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['fields']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(dash_query_builder, self).__init__(**args)
