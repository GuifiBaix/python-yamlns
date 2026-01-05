# Compatibility abstractions

# This resolves pathlib in older Python versions
try:
	from pathlib2 import Path
except ImportError:
    from pathlib import Path

# Ensures that we get an unicode string, even in Py2
def text(data, encoding='utf8'):
	if type(data) is type(u''):
		return data
	if type(data) is type(b''):
		return data.decode(encoding)
	return type(u'')(data)

