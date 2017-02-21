from __future__ import unicode_literals

from . import undefined, null
from .internals import to_string
from .base import to_js, native_function, JSBase
from .jsobject import JSObject, JSObjectPrototype


class JSFunctionPrototype(JSObjectPrototype):

    def __init__(self, name, body, formal_args):
        if name is None and body is None and formal_args is None:
            # prototype
            super(JSFunctionPrototype, self).__init__()
            self.f_name = ''
            self.body = ''
        else:
            if isinstance(body, JSBase):
                super(JSFunctionPrototype, self).__init__(body.own)
                self.body = '[native code]'
            elif isinstance(body, native_function):
                super(JSFunctionPrototype, self).__init__()
                self.body = '[native code]'
            else:
                super(JSFunctionPrototype, self).__init__()
                body = to_js(body)
                self.body = to_string(body) if body is not undefined or body is not null else ''
            self.f_name = name
            self.arguments = list(formal_args)
            # FIXME: JSProtoBase sets body to '' instead of None
            # TODO check if self._args can be parsed as formal parameter list
            # TODO check if self._body can be parsed as function body
            # TODO set strict
            # TODO throw strict mode exceptions
            # (double argument, "eval" or "arguments" in arguments, function identifier is "eval" or "arguments")

    @property
    def _length(self):
        # Yeesh, I dare you to find anything like that in the python specification.
        return len([arg for arg, init in self.arguments if init is not None])

    @staticmethod
    def _constructor(arguments=None):
        return JSFunction.construct(arguments)

    def _to_string(self):
        if self.body is not None:
            body = '\n'
            body += '\t' + self.body if self.body else self.body
        else:
            body = ''
        return 'function %s(%s) {%s\n}' % (
            self.f_name,
            ', '.join(arg if init is None else arg + '=' + init for arg, init in self.arguments),
            body)

    def _apply(self, this_arg, arg_array):
        return 'function apply'

    def _call(self, this_arg, *args):
        return 'function call'

    def _bind(self, this_arg, *args):
        return 'function bind'

    jsclass = 'Function'
    own = {
        'length': 0,
        'constructor': _constructor,
        'toString': _to_string,
        'apply': _apply,
        'call': _call,
        'bind': _bind
    }


class JSFunction(JSObject):

    @staticmethod
    def call(formal_args=None):
        return JSFunction.construct(formal_args)

    @staticmethod
    def construct(formal_args=None):
        if formal_args is None:
            body = ''
            formal_args = []
        else:
            body = formal_args[-1] if formal_args else ''
            formal_args = formal_args[:-1]
        return JSFunctionPrototype('anonymous', body, formal_args)

    name = JSFunctionPrototype.jsclass
    own = {
        'length': 1,
        'prototype': JSFunctionPrototype(None, None, None)
    }
