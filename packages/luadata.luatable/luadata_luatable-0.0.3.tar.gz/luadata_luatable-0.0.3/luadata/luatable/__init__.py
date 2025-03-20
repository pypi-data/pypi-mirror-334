# Define a LuaMapping class that inherits from the built-in dict class
try:
    from lupa.lua import lua_type, LuaRuntime
except ImportError:
    from lupa import lua_type, LuaRuntime


def _():
    # Import the serialize function from the luadata module
    from luadata import serialize as lua_ser

    # Import the lua_type function from the lupa.lua module
    runtime = None
    global GetRuntime, SetRuntime, LuaTable

    def GetRuntime():
        nonlocal runtime
        if runtime is None:
            runtime = LuaRuntime()
        return runtime

    def SetRuntime(_run):
        nonlocal runtime
        runtime = _run

    def newLuaTable():
        nonlocal runtime
        if runtime is None:
            runtime = LuaRuntime()
        return runtime.table_from({})

    def LuaTable(*args):
        len_args = len(args)
        if len_args > 1:
            return [LuaTable(i) for i in args]
        elif len_args == 0:
            _LuaMappingClass__lua_table = newLuaTable()
        else:
            _LuaMappingClass__lua_table = args[0]
        if lua_type(_LuaMappingClass__lua_table) != "table":
            # If so, return a LuaMapping object for the key
            return _LuaMappingClass__lua_table
        __lua_table = _LuaMappingClass__lua_table
        class LuaMappingClass(dict):
            # Initialize the LuaMapping object with the given argument
            def __init__(self):
                pass

            # Implement the __contains__ method
            def __contains__(self, key):
                return key in __lua_table.keys()

            # Implement the __getitem__ method to automatically declare LuaMapping objects for nested dictionaries
            def __getitem__(self, key):
                key = __lua_table[key]
                return LuaTable(key)

            def __setitem__(self, key, value):
                __lua_table[key] = value

            def __delitem__(self, key):
                del __lua_table[key]

            def get(self, key, default=None):
                if key in self:
                    return self[key]
                else:
                    return default

            def pop(self, key, default=None):
                dd = self.get(key, default)
                del self[key]
                return dd

            def update(self, *args, **kwargs):
                j = {}
                j.update(*args, **kwargs)
                tb = __lua_table
                for i in j:
                    tb[i] = j[i]

            def keys(self):
                j = list(__lua_table.keys())
                j.sort()
                return j

            def values(self):
                return map(lambda i: LuaTable(self[i]), self.keys())

            def items(self):
                return map(lambda i: [i, LuaTable(self[i])], self.keys())

            def __iter__(self):
                return iter(self.keys())

            def __len__(self):
                return len(list(__lua_table.keys()))

            def __repr__(self):
                return lua_ser(self, indent=" ", indent_level=1)

            def __getattr__(self, name):
                return self[name]

            def __setattr__(self, name, value):
                self[name] = value

            def __delattr__(self, name):
                del self[name]

        return LuaMappingClass()


_()
