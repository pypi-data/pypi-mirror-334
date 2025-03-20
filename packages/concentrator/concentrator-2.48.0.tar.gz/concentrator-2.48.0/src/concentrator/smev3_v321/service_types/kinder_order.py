#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Apr 14 15:15:26 2021 by generateDS.py version 2.38.6.
# Python 3.6.5 (default, Sep  2 2019, 21:07:57)  [GCC 8.3.0]
#
# Command line options:
#   ('-o', '/home/boris/PycharmProjects/concentrator/src/concentrator/smev3_v321/service_types/kinder_order.py')
#   ('-s', '/home/boris/PycharmProjects/concentrator/src/concentrator/smev3_v321/service_types/kinder_order_subs.py')
#
# Command line arguments:
#   /home/boris/PycharmProjects/concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd
#
# Command line:
#   /home/boris/.virtualenvs/edukndg/bin/generateDS -o "/home/boris/PycharmProjects/concentrator/src/concentrator/smev3_v321/service_types/kinder_order.py" -s "/home/boris/PycharmProjects/concentrator/src/concentrator/smev3_v321/service_types/kinder_order_subs.py" /home/boris/PycharmProjects/concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd
#
# Current working directory (os.getcwd()):
#   edukndg
#

import sys


try:
    ModulenotfoundExp_ = ModuleNotFoundError
except NameError:
    ModulenotfoundExp_ = ImportError
import base64
import datetime as datetime_
import decimal as decimal_
import os
import re as re_

from six.moves import (
    zip_longest,
)


try:
    from lxml import (
        etree as etree_,
    )
except ModulenotfoundExp_:
    from xml.etree import (
        ElementTree as etree_,
    )


Validate_simpletypes_ = True
SaveElementTreeNode = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str


def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc


def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element


#
# Namespace prefix definition table (and other attributes, too)
#
# The module generatedsnamespaces, if it is importable, must contain
# a dictionary named GeneratedsNamespaceDefs.  This Python dictionary
# should map element type names (strings) to XML schema namespace prefix
# definitions.  The export method for any class for which there is
# a namespace prefix definition, will export that definition in the
# XML representation of that element.  See the export method of
# any generated element type class for an example of the use of this
# table.
# A sample table is:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceDefs = {
#         "ElementtypeA": "http://www.xxx.com/namespaceA",
#         "ElementtypeB": "http://www.xxx.com/namespaceB",
#     }
#
# Additionally, the generatedsnamespaces module can contain a python
# dictionary named GenerateDSNamespaceTypePrefixes that associates element
# types with the namespace prefixes that are to be added to the
# "xsi:type" attribute value.  See the exportAttributes method of
# any generated element type and the generation of "xsi:type" for an
# example of the use of this table.
# An example table:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceTypePrefixes = {
#         "ElementtypeC": "aaa:",
#         "ElementtypeD": "bbb:",
#     }
#

try:
    from generatedsnamespaces import (
        GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_,
    )
except ModulenotfoundExp_:
    GenerateDSNamespaceDefs_ = {}
try:
    from generatedsnamespaces import (
        GenerateDSNamespaceTypePrefixes as GenerateDSNamespaceTypePrefixes_,
    )
except ModulenotfoundExp_:
    GenerateDSNamespaceTypePrefixes_ = {}

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#
try:
    from generatedscollector import (
        GdsCollector as GdsCollector_,
    )
except ModulenotfoundExp_:

    class GdsCollector_(object):
        def __init__(self, messages=None):
            if messages is None:
                self.messages = []
            else:
                self.messages = messages

        def add_message(self, msg):
            self.messages.append(msg)

        def get_messages(self):
            return self.messages

        def clear_messages(self):
            self.messages = []

        def print_messages(self):
            for msg in self.messages:
                print('Warning: {}'.format(msg))

        def write_messages(self, outstream):
            for msg in self.messages:
                outstream.write('Warning: {}\n'.format(msg))


#
# The super-class for enum types
#

try:
    from enum import (
        Enum,
    )
except ModulenotfoundExp_:
    Enum = object

#
# The root super-class for element type classes
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import (
        GeneratedsSuper,
    )
except ModulenotfoundExp_ as exp:

    class GeneratedsSuper(object):
        __hash__ = object.__hash__
        tzoff_pattern = re_.compile(r'(\+|-)((0\d|1[0-3]):[0-5]\d|14:00)$')

        class _FixedOffsetTZ(datetime_.tzinfo):
            def __init__(self, offset, name):
                self.__offset = datetime_.timedelta(minutes=offset)
                self.__name = name

            def utcoffset(self, dt):
                return self.__offset

            def tzname(self, dt):
                return self.__name

            def dst(self, dt):
                return None

        def gds_format_string(self, input_data, input_name=''):
            return input_data

        def gds_parse_string(self, input_data, node=None, input_name=''):
            return input_data

        def gds_validate_string(self, input_data, node=None, input_name=''):
            if not input_data:
                return ''
            else:
                return input_data

        def gds_format_base64(self, input_data, input_name=''):
            return base64.b64encode(input_data)

        def gds_validate_base64(self, input_data, node=None, input_name=''):
            return input_data

        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % input_data

        def gds_parse_integer(self, input_data, node=None, input_name=''):
            try:
                ival = int(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires integer value: %s' % exp)
            return ival

        def gds_validate_integer(self, input_data, node=None, input_name=''):
            try:
                value = int(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires integer value')
            return value

        def gds_format_integer_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)

        def gds_validate_integer_list(self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    int(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of integer values')
            return values

        def gds_format_float(self, input_data, input_name=''):
            return ('%.15f' % input_data).rstrip('0')

        def gds_parse_float(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires float or double value: %s' % exp)
            return fval_

        def gds_validate_float(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires float value')
            return value

        def gds_format_float_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)

        def gds_validate_float_list(self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of float values')
            return values

        def gds_format_decimal(self, input_data, input_name=''):
            return_value = '%s' % input_data
            if '.' in return_value:
                return_value = return_value.rstrip('0')
                if return_value.endswith('.'):
                    return_value = return_value.rstrip('.')
            return return_value

        def gds_parse_decimal(self, input_data, node=None, input_name=''):
            try:
                decimal_value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return decimal_value

        def gds_validate_decimal(self, input_data, node=None, input_name=''):
            try:
                value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return value

        def gds_format_decimal_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return ' '.join([self.gds_format_decimal(item) for item in input_data])

        def gds_validate_decimal_list(self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    decimal_.Decimal(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of decimal values')
            return values

        def gds_format_double(self, input_data, input_name=''):
            return '%s' % input_data

        def gds_parse_double(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires double or float value: %s' % exp)
            return fval_

        def gds_validate_double(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires double or float value')
            return value

        def gds_format_double_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)

        def gds_validate_double_list(self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of double or float values')
            return values

        def gds_format_boolean(self, input_data, input_name=''):
            return ('%s' % input_data).lower()

        def gds_parse_boolean(self, input_data, node=None, input_name=''):
            if input_data in ('true', '1'):
                bval = True
            elif input_data in ('false', '0'):
                bval = False
            else:
                raise_parse_error(node, 'Requires boolean value')
            return bval

        def gds_validate_boolean(self, input_data, node=None, input_name=''):
            if input_data not in (
                True,
                1,
                False,
                0,
            ):
                raise_parse_error(node, 'Requires boolean value (one of True, 1, False, 0)')
            return input_data

        def gds_format_boolean_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)

        def gds_validate_boolean_list(self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                value = self.gds_parse_boolean(value, node, input_name)
                if value not in (
                    True,
                    1,
                    False,
                    0,
                ):
                    raise_parse_error(node, 'Requires sequence of boolean values (one of True, 1, False, 0)')
            return values

        def gds_validate_datetime(self, input_data, node=None, input_name=''):
            return input_data

        def gds_format_datetime(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue

        @classmethod
        def gds_parse_datetime(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(tzoff, results.group(0))
                    input_data = input_data[:-6]
            time_parts = input_data.split('.')
            if len(time_parts) > 1:
                micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
                input_data = '%s.%s' % (
                    time_parts[0],
                    '{}'.format(micro_seconds).rjust(6, '0'),
                )
                dt = datetime_.datetime.strptime(input_data, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(input_data, '%Y-%m-%dT%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt

        def gds_validate_date(self, input_data, node=None, input_name=''):
            return input_data

        def gds_format_date(self, input_data, input_name=''):
            _svalue = '%04d-%02d-%02d' % (
                input_data.year,
                input_data.month,
                input_data.day,
            )
            try:
                if input_data.tzinfo is not None:
                    tzoff = input_data.tzinfo.utcoffset(input_data)
                    if tzoff is not None:
                        total_seconds = tzoff.seconds + (86400 * tzoff.days)
                        if total_seconds == 0:
                            _svalue += 'Z'
                        else:
                            if total_seconds < 0:
                                _svalue += '-'
                                total_seconds *= -1
                            else:
                                _svalue += '+'
                            hours = total_seconds // 3600
                            minutes = (total_seconds - (hours * 3600)) // 60
                            _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            except AttributeError:
                pass
            return _svalue

        @classmethod
        def gds_parse_date(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(tzoff, results.group(0))
                    input_data = input_data[:-6]
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
            dt = dt.replace(tzinfo=tz)
            return dt.date()

        def gds_validate_time(self, input_data, node=None, input_name=''):
            return input_data

        def gds_format_time(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%02d:%02d:%02d' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%02d:%02d:%02d.%s' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue

        def gds_validate_simple_patterns(self, patterns, target):
            # pat is a list of lists of strings/patterns.
            # The target value must match at least one of the patterns
            # in order for the test to succeed.
            found1 = True
            for patterns1 in patterns:
                found2 = False
                for patterns2 in patterns1:
                    mo = re_.search(patterns2, target)
                    if mo is not None and len(mo.group(0)) == len(target):
                        found2 = True
                        break
                if not found2:
                    found1 = False
                    break
            return found1

        @classmethod
        def gds_parse_time(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(tzoff, results.group(0))
                    input_data = input_data[:-6]
            if len(input_data.split('.')) > 1:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt.time()

        def gds_check_cardinality_(self, value, input_name, min_occurs=0, max_occurs=1, required=None):
            if value is None:
                length = 0
            elif isinstance(value, list):
                length = len(value)
            else:
                length = 1
            if required is not None:
                if required and length < 1:
                    self.gds_collector_.add_message(
                        'Required value {}{} is missing'.format(input_name, self.gds_get_node_lineno_())
                    )
            if length < min_occurs:
                self.gds_collector_.add_message(
                    'Number of values for {}{} is below the minimum allowed, expected at least {}, found {}'.format(
                        input_name, self.gds_get_node_lineno_(), min_occurs, length
                    )
                )
            elif length > max_occurs:
                self.gds_collector_.add_message(
                    'Number of values for {}{} is above the maximum allowed, expected at most {}, found {}'.format(
                        input_name, self.gds_get_node_lineno_(), max_occurs, length
                    )
                )

        def gds_validate_builtin_ST_(
            self, validator, value, input_name, min_occurs=None, max_occurs=None, required=None
        ):
            if value is not None:
                try:
                    validator(value, input_name=input_name)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))

        def gds_validate_defined_ST_(
            self, validator, value, input_name, min_occurs=None, max_occurs=None, required=None
        ):
            if value is not None:
                try:
                    validator(value)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))

        def gds_str_lower(self, instring):
            return instring.lower()

        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = '/'.join(path_list)
            return path

        Tag_strip_pattern_ = re_.compile(r'\{.*\}')

        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)

        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if 'xsi' in node.nsmap:
                classname = node.get('{%s}type' % node.nsmap['xsi'])
                if classname is not None:
                    names = classname.split(':')
                    if len(names) == 2:
                        classname = names[1]
                    class_obj2 = globals().get(classname)
                    if class_obj2 is not None:
                        class_obj1 = class_obj2
            return class_obj1

        def gds_build_any(self, node, type_name=None):
            # provide default value in case option --disable-xml is used.
            content = ''
            content = etree_.tostring(node, encoding='unicode')
            return content

        @classmethod
        def gds_reverse_node_mapping(cls, mapping):
            return dict(((v, k) for k, v in mapping.items()))

        @staticmethod
        def gds_encode(instring):
            if sys.version_info.major == 2:
                if ExternalEncoding:
                    encoding = ExternalEncoding
                else:
                    encoding = 'utf-8'
                return instring.encode(encoding)
            else:
                return instring

        @staticmethod
        def convert_unicode(instring):
            if isinstance(instring, str):
                result = quote_xml(instring)
            elif sys.version_info.major == 2 and isinstance(instring, unicode):
                result = quote_xml(instring).encode('utf8')
            else:
                result = GeneratedsSuper.gds_encode(str(instring))
            return result

        def __eq__(self, other):
            def excl_select_objs_(obj):
                return obj[0] != 'parent_object_' and obj[0] != 'gds_collector_'

            if type(self) != type(other):
                return False
            return all(
                x == y
                for x, y in zip_longest(
                    filter(excl_select_objs_, self.__dict__.items()), filter(excl_select_objs_, other.__dict__.items())
                )
            )

        def __ne__(self, other):
            return not self.__eq__(other)

        # Django ETL transform hooks.
        def gds_djo_etl_transform(self):
            pass

        def gds_djo_etl_transform_db_obj(self, dbobj):
            pass

        # SQLAlchemy ETL transform hooks.
        def gds_sqa_etl_transform(self):
            return 0, None

        def gds_sqa_etl_transform_db_obj(self, dbobj):
            pass

        def gds_get_node_lineno_(self):
            if hasattr(self, 'gds_elementtree_node_') and self.gds_elementtree_node_ is not None:
                return ' near line {}'.format(self.gds_elementtree_node_.sourceline)
            else:
                return ''

    def getSubclassFromModule_(module, class_):
        """Get the subclass of a class from a specific module."""
        name = class_.__name__ + 'Sub'
        if hasattr(module, name):
            return getattr(module, name)
        else:
            return None


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = ''
# Set this to false in order to deactivate during export, the use of
# name space prefixes captured from the input document.
UseCapturedNS_ = True
CapturedNsmap_ = {}
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r'[\n\r\s]+')
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r'<!\[CDATA\[.*?\]\]>', re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Support/utility functions.
#


def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write('    ')


def quote_xml(inStr):
    "Escape markup chars, but do not modify CDATA sections."
    if not inStr:
        return ''
    s1 = isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr
    s2 = ''
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos : mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start() : mo.end()]
        pos = mo.end()
    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_attrib(inStr):
    s1 = isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', '&quot;')
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1


def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        if prefix == 'xml':
            namespace = 'http://www.w3.org/XML/1998/namespace'
        else:
            namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get(
                '{%s}%s'
                % (
                    namespace,
                    name,
                )
            )
    return value


def encode_str_2_3(instr):
    return instr


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    if node is not None:
        msg = '%s (element %s/line %d)' % (
            msg,
            node.tag,
            node.sourceline,
        )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    TypeBase64 = 8

    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value

    def getCategory(self):
        return self.category

    def getContenttype(self, content_type):
        return self.content_type

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def export(self, outfile, level, name, namespace, pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:  # category == MixedContainer.CategoryComplex
            self.value.export(outfile, level, namespace, name_=name, pretty_print=pretty_print)

    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeBase64:
            outfile.write('<%s>%s</%s>' % (self.name, base64.b64encode(self.value), self.name))

    def to_etree(self, element, mapping_=None, nsmap_=None):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                if len(element) > 0:
                    if element[-1].tail is None:
                        element[-1].tail = self.value
                    else:
                        element[-1].tail += self.value
                else:
                    if element.text is None:
                        element.text = self.value
                    else:
                        element.text += self.value
        elif self.category == MixedContainer.CategorySimple:
            subelement = etree_.SubElement(element, '%s' % self.name)
            subelement.text = self.to_etree_simple()
        else:  # category == MixedContainer.CategoryComplex
            self.value.to_etree(element)

    def to_etree_simple(self, mapping_=None, nsmap_=None):
        if self.content_type == MixedContainer.TypeString:
            text = self.value
        elif self.content_type == MixedContainer.TypeInteger or self.content_type == MixedContainer.TypeBoolean:
            text = '%d' % self.value
        elif self.content_type == MixedContainer.TypeFloat or self.content_type == MixedContainer.TypeDecimal:
            text = '%f' % self.value
        elif self.content_type == MixedContainer.TypeDouble:
            text = '%g' % self.value
        elif self.content_type == MixedContainer.TypeBase64:
            text = '%s' % base64.b64encode(self.value)
        return text

    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n'
                % (self.category, self.content_type, self.name, self.value)
            )
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n'
                % (self.category, self.content_type, self.name, self.value)
            )
        else:  # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s",\n'
                % (
                    self.category,
                    self.content_type,
                    self.name,
                )
            )
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0, optional=0, child_attrs=None, choice=None):
        self.name = name
        self.data_type = data_type
        self.container = container
        self.child_attrs = child_attrs
        self.choice = choice
        self.optional = optional

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_data_type(self, data_type):
        self.data_type = data_type

    def get_data_type_chain(self):
        return self.data_type

    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type

    def set_container(self, container):
        self.container = container

    def get_container(self):
        return self.container

    def set_child_attrs(self, child_attrs):
        self.child_attrs = child_attrs

    def get_child_attrs(self):
        return self.child_attrs

    def set_choice(self, choice):
        self.choice = choice

    def get_choice(self):
        return self.choice

    def set_optional(self, optional):
        self.optional = optional

    def get_optional(self):
        return self.optional


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)


#
# Data representation classes.
#


class EnvType(str, Enum):
    EPGU = 'EPGU'
    DEV = 'DEV'
    UAT = 'UAT'
    EXUAT = 'EXUAT'
    SVCDEV = 'SVCDEV'
    TCOD = 'TCOD'


class DataElementType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, code=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.code = _cast(None, code)
        self.code_nsprefix_ = None
        self.valueOf_ = valueOf_

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, DataElementType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DataElementType.subclass:
            return DataElementType.subclass(*args_, **kwargs_)
        else:
            return DataElementType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code

    def get_valueOf_(self):
        return self.valueOf_

    def set_valueOf_(self, valueOf_):
        self.valueOf_ = valueOf_

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_50(self, value):
        # Validate type tns:string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False

    def hasContent_(self):
        if 1 if type(self.valueOf_) in [int, float] else self.valueOf_:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='DataElementType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DataElementType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DataElementType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DataElementType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(
                outfile, level + 1, namespaceprefix_, namespacedef_, name_='DataElementType', pretty_print=pretty_print
            )
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DataElementType'):
        if self.code is not None and 'code' not in already_processed:
            already_processed.add('code')
            outfile.write(
                ' code=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.code), input_name='code')),)
            )

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='DataElementType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        pass

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('code', node)
        if value is not None and 'code' not in already_processed:
            already_processed.add('code')
            self.code = value
            self.validate_string_50(self.code)  # validate type string-50

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass


# end class DataElementType


class DocInfoType(GeneratedsSuper):
    """Описание документа"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, DocIssueDate=None, DocIssued=None, DocExpirationDate=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        if isinstance(DocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = DocIssueDate
        self.DocIssueDate = initvalue_
        self.DocIssueDate_nsprefix_ = 'tns'
        self.DocIssued = DocIssued
        self.validate_string_256(self.DocIssued)
        self.DocIssued_nsprefix_ = 'tns'
        if isinstance(DocExpirationDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DocExpirationDate, '%Y-%m-%d').date()
        else:
            initvalue_ = DocExpirationDate
        self.DocExpirationDate = initvalue_
        self.DocExpirationDate_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, DocInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DocInfoType.subclass:
            return DocInfoType.subclass(*args_, **kwargs_)
        else:
            return DocInfoType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_DocIssueDate(self):
        return self.DocIssueDate

    def set_DocIssueDate(self, DocIssueDate):
        self.DocIssueDate = DocIssueDate

    def get_DocIssued(self):
        return self.DocIssued

    def set_DocIssued(self, DocIssued):
        self.DocIssued = DocIssued

    def get_DocExpirationDate(self):
        return self.DocExpirationDate

    def set_DocExpirationDate(self, DocExpirationDate):
        self.DocExpirationDate = DocExpirationDate

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if self.DocIssueDate is not None or self.DocIssued is not None or self.DocExpirationDate is not None:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='DocInfoType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DocInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DocInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DocInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile, level + 1, namespaceprefix_, namespacedef_, name_='DocInfoType', pretty_print=pretty_print
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DocInfoType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='DocInfoType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DocIssueDate is not None:
            namespaceprefix_ = (
                self.DocIssueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DocIssueDate_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sDocIssueDate>%s</%sDocIssueDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.DocIssueDate, input_name='DocIssueDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.DocIssued is not None:
            namespaceprefix_ = self.DocIssued_nsprefix_ + ':' if (UseCapturedNS_ and self.DocIssued_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sDocIssued>%s</%sDocIssued>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.DocIssued), input_name='DocIssued')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.DocExpirationDate is not None:
            namespaceprefix_ = (
                self.DocExpirationDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DocExpirationDate_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sDocExpirationDate>%s</%sDocExpirationDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.DocExpirationDate, input_name='DocExpirationDate'),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DocIssueDate = dval_
            self.DocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'DocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocIssued')
            value_ = self.gds_validate_string(value_, node, 'DocIssued')
            self.DocIssued = value_
            self.DocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.DocIssued)
        elif nodeName_ == 'DocExpirationDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DocExpirationDate = dval_
            self.DocExpirationDate_nsprefix_ = child_.prefix


# end class DocInfoType


class PersonInfoType(GeneratedsSuper):
    """Сведения о заявителе"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        PersonSurname=None,
        PersonName=None,
        PersonMiddleName=None,
        PersonPhone=None,
        PersonEmail=None,
        Parents=None,
        OtherRepresentative=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.PersonSurname = PersonSurname
        self.validate_string_256(self.PersonSurname)
        self.PersonSurname_nsprefix_ = 'tns'
        self.PersonName = PersonName
        self.validate_string_256(self.PersonName)
        self.PersonName_nsprefix_ = 'tns'
        self.PersonMiddleName = PersonMiddleName
        self.validate_string_256(self.PersonMiddleName)
        self.PersonMiddleName_nsprefix_ = 'tns'
        self.PersonPhone = PersonPhone
        self.validate_string_14(self.PersonPhone)
        self.PersonPhone_nsprefix_ = 'tns'
        self.PersonEmail = PersonEmail
        self.validate_string_256(self.PersonEmail)
        self.PersonEmail_nsprefix_ = 'tns'
        self.Parents = Parents
        self.Parents_nsprefix_ = 'tns'
        self.OtherRepresentative = OtherRepresentative
        self.OtherRepresentative_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, PersonInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PersonInfoType.subclass:
            return PersonInfoType.subclass(*args_, **kwargs_)
        else:
            return PersonInfoType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_PersonSurname(self):
        return self.PersonSurname

    def set_PersonSurname(self, PersonSurname):
        self.PersonSurname = PersonSurname

    def get_PersonName(self):
        return self.PersonName

    def set_PersonName(self, PersonName):
        self.PersonName = PersonName

    def get_PersonMiddleName(self):
        return self.PersonMiddleName

    def set_PersonMiddleName(self, PersonMiddleName):
        self.PersonMiddleName = PersonMiddleName

    def get_PersonPhone(self):
        return self.PersonPhone

    def set_PersonPhone(self, PersonPhone):
        self.PersonPhone = PersonPhone

    def get_PersonEmail(self):
        return self.PersonEmail

    def set_PersonEmail(self, PersonEmail):
        self.PersonEmail = PersonEmail

    def get_Parents(self):
        return self.Parents

    def set_Parents(self, Parents):
        self.Parents = Parents

    def get_OtherRepresentative(self):
        return self.OtherRepresentative

    def set_OtherRepresentative(self, OtherRepresentative):
        self.OtherRepresentative = OtherRepresentative

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_14(self, value):
        result = True
        # Validate type string-14, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 14:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-14'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.PersonSurname is not None
            or self.PersonName is not None
            or self.PersonMiddleName is not None
            or self.PersonPhone is not None
            or self.PersonEmail is not None
            or self.Parents is not None
            or self.OtherRepresentative is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='PersonInfoType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PersonInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PersonInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PersonInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile, level + 1, namespaceprefix_, namespacedef_, name_='PersonInfoType', pretty_print=pretty_print
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PersonInfoType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='PersonInfoType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PersonSurname is not None:
            namespaceprefix_ = (
                self.PersonSurname_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonSurname_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sPersonSurname>%s</%sPersonSurname>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.PersonSurname), input_name='PersonSurname')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.PersonName is not None:
            namespaceprefix_ = self.PersonName_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sPersonName>%s</%sPersonName>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.PersonName), input_name='PersonName')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.PersonMiddleName is not None:
            namespaceprefix_ = (
                self.PersonMiddleName_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonMiddleName_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sPersonMiddleName>%s</%sPersonMiddleName>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.PersonMiddleName), input_name='PersonMiddleName')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.PersonPhone is not None:
            namespaceprefix_ = (
                self.PersonPhone_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonPhone_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sPersonPhone>%s</%sPersonPhone>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.PersonPhone), input_name='PersonPhone')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.PersonEmail is not None:
            namespaceprefix_ = (
                self.PersonEmail_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonEmail_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sPersonEmail>%s</%sPersonEmail>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.PersonEmail), input_name='PersonEmail')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.Parents is not None:
            namespaceprefix_ = self.Parents_nsprefix_ + ':' if (UseCapturedNS_ and self.Parents_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sParents>%s</%sParents>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_boolean(self.Parents, input_name='Parents'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.OtherRepresentative is not None:
            namespaceprefix_ = (
                self.OtherRepresentative_nsprefix_ + ':'
                if (UseCapturedNS_ and self.OtherRepresentative_nsprefix_)
                else ''
            )
            self.OtherRepresentative.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_='',
                name_='OtherRepresentative',
                pretty_print=pretty_print,
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PersonSurname':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonSurname')
            value_ = self.gds_validate_string(value_, node, 'PersonSurname')
            self.PersonSurname = value_
            self.PersonSurname_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.PersonSurname)
        elif nodeName_ == 'PersonName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonName')
            value_ = self.gds_validate_string(value_, node, 'PersonName')
            self.PersonName = value_
            self.PersonName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.PersonName)
        elif nodeName_ == 'PersonMiddleName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonMiddleName')
            value_ = self.gds_validate_string(value_, node, 'PersonMiddleName')
            self.PersonMiddleName = value_
            self.PersonMiddleName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.PersonMiddleName)
        elif nodeName_ == 'PersonPhone':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonPhone')
            value_ = self.gds_validate_string(value_, node, 'PersonPhone')
            self.PersonPhone = value_
            self.PersonPhone_nsprefix_ = child_.prefix
            # validate type string-14
            self.validate_string_14(self.PersonPhone)
        elif nodeName_ == 'PersonEmail':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PersonEmail')
            value_ = self.gds_validate_string(value_, node, 'PersonEmail')
            self.PersonEmail = value_
            self.PersonEmail_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.PersonEmail)
        elif nodeName_ == 'Parents':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'Parents')
            ival_ = self.gds_validate_boolean(ival_, node, 'Parents')
            self.Parents = ival_
            self.Parents_nsprefix_ = child_.prefix
        elif nodeName_ == 'OtherRepresentative':
            obj_ = OtherRepresentativeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.OtherRepresentative = obj_
            obj_.original_tagname_ = 'OtherRepresentative'


# end class PersonInfoType


class OtherRepresentativeType(GeneratedsSuper):
    """Сведения о документе, подтверждающем полномочия заявителя"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        OtherRepresentativeDocName=None,
        OtherRepresentativeDocSeries=None,
        OtherRepresentativeDocNumber=None,
        OtherRepresentativeDocDate=None,
        OtherRepresentativeDocIssued=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.OtherRepresentativeDocName = OtherRepresentativeDocName
        self.validate_string_256(self.OtherRepresentativeDocName)
        self.OtherRepresentativeDocName_nsprefix_ = 'tns'
        self.OtherRepresentativeDocSeries = OtherRepresentativeDocSeries
        self.validate_string_10(self.OtherRepresentativeDocSeries)
        self.OtherRepresentativeDocSeries_nsprefix_ = 'tns'
        self.OtherRepresentativeDocNumber = OtherRepresentativeDocNumber
        self.validate_string_10(self.OtherRepresentativeDocNumber)
        self.OtherRepresentativeDocNumber_nsprefix_ = 'tns'
        if isinstance(OtherRepresentativeDocDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(OtherRepresentativeDocDate, '%Y-%m-%d').date()
        else:
            initvalue_ = OtherRepresentativeDocDate
        self.OtherRepresentativeDocDate = initvalue_
        self.OtherRepresentativeDocDate_nsprefix_ = 'tns'
        self.OtherRepresentativeDocIssued = OtherRepresentativeDocIssued
        self.validate_string_256(self.OtherRepresentativeDocIssued)
        self.OtherRepresentativeDocIssued_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, OtherRepresentativeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OtherRepresentativeType.subclass:
            return OtherRepresentativeType.subclass(*args_, **kwargs_)
        else:
            return OtherRepresentativeType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_OtherRepresentativeDocName(self):
        return self.OtherRepresentativeDocName

    def set_OtherRepresentativeDocName(self, OtherRepresentativeDocName):
        self.OtherRepresentativeDocName = OtherRepresentativeDocName

    def get_OtherRepresentativeDocSeries(self):
        return self.OtherRepresentativeDocSeries

    def set_OtherRepresentativeDocSeries(self, OtherRepresentativeDocSeries):
        self.OtherRepresentativeDocSeries = OtherRepresentativeDocSeries

    def get_OtherRepresentativeDocNumber(self):
        return self.OtherRepresentativeDocNumber

    def set_OtherRepresentativeDocNumber(self, OtherRepresentativeDocNumber):
        self.OtherRepresentativeDocNumber = OtherRepresentativeDocNumber

    def get_OtherRepresentativeDocDate(self):
        return self.OtherRepresentativeDocDate

    def set_OtherRepresentativeDocDate(self, OtherRepresentativeDocDate):
        self.OtherRepresentativeDocDate = OtherRepresentativeDocDate

    def get_OtherRepresentativeDocIssued(self):
        return self.OtherRepresentativeDocIssued

    def set_OtherRepresentativeDocIssued(self, OtherRepresentativeDocIssued):
        self.OtherRepresentativeDocIssued = OtherRepresentativeDocIssued

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_10(self, value):
        result = True
        # Validate type string-10, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-10'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.OtherRepresentativeDocName is not None
            or self.OtherRepresentativeDocSeries is not None
            or self.OtherRepresentativeDocNumber is not None
            or self.OtherRepresentativeDocDate is not None
            or self.OtherRepresentativeDocIssued is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='OtherRepresentativeType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OtherRepresentativeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OtherRepresentativeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OtherRepresentativeType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='OtherRepresentativeType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OtherRepresentativeType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='OtherRepresentativeType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.OtherRepresentativeDocName is not None:
            namespaceprefix_ = (
                self.OtherRepresentativeDocName_nsprefix_ + ':'
                if (UseCapturedNS_ and self.OtherRepresentativeDocName_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sOtherRepresentativeDocName>%s</%sOtherRepresentativeDocName>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(
                            quote_xml(self.OtherRepresentativeDocName), input_name='OtherRepresentativeDocName'
                        )
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.OtherRepresentativeDocSeries is not None:
            namespaceprefix_ = (
                self.OtherRepresentativeDocSeries_nsprefix_ + ':'
                if (UseCapturedNS_ and self.OtherRepresentativeDocSeries_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sOtherRepresentativeDocSeries>%s</%sOtherRepresentativeDocSeries>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(
                            quote_xml(self.OtherRepresentativeDocSeries), input_name='OtherRepresentativeDocSeries'
                        )
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.OtherRepresentativeDocNumber is not None:
            namespaceprefix_ = (
                self.OtherRepresentativeDocNumber_nsprefix_ + ':'
                if (UseCapturedNS_ and self.OtherRepresentativeDocNumber_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sOtherRepresentativeDocNumber>%s</%sOtherRepresentativeDocNumber>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(
                            quote_xml(self.OtherRepresentativeDocNumber), input_name='OtherRepresentativeDocNumber'
                        )
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.OtherRepresentativeDocDate is not None:
            namespaceprefix_ = (
                self.OtherRepresentativeDocDate_nsprefix_ + ':'
                if (UseCapturedNS_ and self.OtherRepresentativeDocDate_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sOtherRepresentativeDocDate>%s</%sOtherRepresentativeDocDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.OtherRepresentativeDocDate, input_name='OtherRepresentativeDocDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.OtherRepresentativeDocIssued is not None:
            namespaceprefix_ = (
                self.OtherRepresentativeDocIssued_nsprefix_ + ':'
                if (UseCapturedNS_ and self.OtherRepresentativeDocIssued_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sOtherRepresentativeDocIssued>%s</%sOtherRepresentativeDocIssued>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(
                            quote_xml(self.OtherRepresentativeDocIssued), input_name='OtherRepresentativeDocIssued'
                        )
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'OtherRepresentativeDocName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OtherRepresentativeDocName')
            value_ = self.gds_validate_string(value_, node, 'OtherRepresentativeDocName')
            self.OtherRepresentativeDocName = value_
            self.OtherRepresentativeDocName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.OtherRepresentativeDocName)
        elif nodeName_ == 'OtherRepresentativeDocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OtherRepresentativeDocSeries')
            value_ = self.gds_validate_string(value_, node, 'OtherRepresentativeDocSeries')
            self.OtherRepresentativeDocSeries = value_
            self.OtherRepresentativeDocSeries_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.OtherRepresentativeDocSeries)
        elif nodeName_ == 'OtherRepresentativeDocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OtherRepresentativeDocNumber')
            value_ = self.gds_validate_string(value_, node, 'OtherRepresentativeDocNumber')
            self.OtherRepresentativeDocNumber = value_
            self.OtherRepresentativeDocNumber_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.OtherRepresentativeDocNumber)
        elif nodeName_ == 'OtherRepresentativeDocDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.OtherRepresentativeDocDate = dval_
            self.OtherRepresentativeDocDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'OtherRepresentativeDocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'OtherRepresentativeDocIssued')
            value_ = self.gds_validate_string(value_, node, 'OtherRepresentativeDocIssued')
            self.OtherRepresentativeDocIssued = value_
            self.OtherRepresentativeDocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.OtherRepresentativeDocIssued)


# end class OtherRepresentativeType


class PersonIdentityDocInfoType(GeneratedsSuper):
    """Паспортные данные заявителя"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        IdentityDocName=None,
        IdentityDocSeries=None,
        IdentityDocNumber=None,
        IdentityDocIssueDate=None,
        IdentityDocIssueCode=None,
        IdentityDocIssued=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.IdentityDocName = IdentityDocName
        self.IdentityDocName_nsprefix_ = 'tns'
        self.IdentityDocSeries = IdentityDocSeries
        self.validate_string_10(self.IdentityDocSeries)
        self.IdentityDocSeries_nsprefix_ = 'tns'
        self.IdentityDocNumber = IdentityDocNumber
        self.validate_string_10(self.IdentityDocNumber)
        self.IdentityDocNumber_nsprefix_ = 'tns'
        if isinstance(IdentityDocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(IdentityDocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = IdentityDocIssueDate
        self.IdentityDocIssueDate = initvalue_
        self.IdentityDocIssueDate_nsprefix_ = 'tns'
        self.IdentityDocIssueCode = IdentityDocIssueCode
        self.validate_string_6(self.IdentityDocIssueCode)
        self.IdentityDocIssueCode_nsprefix_ = 'tns'
        self.IdentityDocIssued = IdentityDocIssued
        self.validate_string_256(self.IdentityDocIssued)
        self.IdentityDocIssued_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, PersonIdentityDocInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PersonIdentityDocInfoType.subclass:
            return PersonIdentityDocInfoType.subclass(*args_, **kwargs_)
        else:
            return PersonIdentityDocInfoType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_IdentityDocName(self):
        return self.IdentityDocName

    def set_IdentityDocName(self, IdentityDocName):
        self.IdentityDocName = IdentityDocName

    def get_IdentityDocSeries(self):
        return self.IdentityDocSeries

    def set_IdentityDocSeries(self, IdentityDocSeries):
        self.IdentityDocSeries = IdentityDocSeries

    def get_IdentityDocNumber(self):
        return self.IdentityDocNumber

    def set_IdentityDocNumber(self, IdentityDocNumber):
        self.IdentityDocNumber = IdentityDocNumber

    def get_IdentityDocIssueDate(self):
        return self.IdentityDocIssueDate

    def set_IdentityDocIssueDate(self, IdentityDocIssueDate):
        self.IdentityDocIssueDate = IdentityDocIssueDate

    def get_IdentityDocIssueCode(self):
        return self.IdentityDocIssueCode

    def set_IdentityDocIssueCode(self, IdentityDocIssueCode):
        self.IdentityDocIssueCode = IdentityDocIssueCode

    def get_IdentityDocIssued(self):
        return self.IdentityDocIssued

    def set_IdentityDocIssued(self, IdentityDocIssued):
        self.IdentityDocIssued = IdentityDocIssued

    def validate_string_10(self, value):
        result = True
        # Validate type string-10, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-10'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_6(self, value):
        result = True
        # Validate type string-6, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-6'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.IdentityDocName is not None
            or self.IdentityDocSeries is not None
            or self.IdentityDocNumber is not None
            or self.IdentityDocIssueDate is not None
            or self.IdentityDocIssueCode is not None
            or self.IdentityDocIssued is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='PersonIdentityDocInfoType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PersonIdentityDocInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PersonIdentityDocInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PersonIdentityDocInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='PersonIdentityDocInfoType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(
        self, outfile, level, already_processed, namespaceprefix_='', name_='PersonIdentityDocInfoType'
    ):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='PersonIdentityDocInfoType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.IdentityDocName is not None:
            namespaceprefix_ = (
                self.IdentityDocName_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityDocName_nsprefix_) else ''
            )
            self.IdentityDocName.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='IdentityDocName', pretty_print=pretty_print
            )
        if self.IdentityDocSeries is not None:
            namespaceprefix_ = (
                self.IdentityDocSeries_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityDocSeries_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sIdentityDocSeries>%s</%sIdentityDocSeries>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.IdentityDocSeries), input_name='IdentityDocSeries')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.IdentityDocNumber is not None:
            namespaceprefix_ = (
                self.IdentityDocNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityDocNumber_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sIdentityDocNumber>%s</%sIdentityDocNumber>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.IdentityDocNumber), input_name='IdentityDocNumber')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.IdentityDocIssueDate is not None:
            namespaceprefix_ = (
                self.IdentityDocIssueDate_nsprefix_ + ':'
                if (UseCapturedNS_ and self.IdentityDocIssueDate_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sIdentityDocIssueDate>%s</%sIdentityDocIssueDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.IdentityDocIssueDate, input_name='IdentityDocIssueDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.IdentityDocIssueCode is not None:
            namespaceprefix_ = (
                self.IdentityDocIssueCode_nsprefix_ + ':'
                if (UseCapturedNS_ and self.IdentityDocIssueCode_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sIdentityDocIssueCode>%s</%sIdentityDocIssueCode>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.IdentityDocIssueCode), input_name='IdentityDocIssueCode')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.IdentityDocIssued is not None:
            namespaceprefix_ = (
                self.IdentityDocIssued_nsprefix_ + ':' if (UseCapturedNS_ and self.IdentityDocIssued_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sIdentityDocIssued>%s</%sIdentityDocIssued>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.IdentityDocIssued), input_name='IdentityDocIssued')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'IdentityDocName':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.IdentityDocName = obj_
            obj_.original_tagname_ = 'IdentityDocName'
        elif nodeName_ == 'IdentityDocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdentityDocSeries')
            value_ = self.gds_validate_string(value_, node, 'IdentityDocSeries')
            self.IdentityDocSeries = value_
            self.IdentityDocSeries_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.IdentityDocSeries)
        elif nodeName_ == 'IdentityDocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdentityDocNumber')
            value_ = self.gds_validate_string(value_, node, 'IdentityDocNumber')
            self.IdentityDocNumber = value_
            self.IdentityDocNumber_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.IdentityDocNumber)
        elif nodeName_ == 'IdentityDocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.IdentityDocIssueDate = dval_
            self.IdentityDocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'IdentityDocIssueCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdentityDocIssueCode')
            value_ = self.gds_validate_string(value_, node, 'IdentityDocIssueCode')
            self.IdentityDocIssueCode = value_
            self.IdentityDocIssueCode_nsprefix_ = child_.prefix
            # validate type string-6
            self.validate_string_6(self.IdentityDocIssueCode)
        elif nodeName_ == 'IdentityDocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'IdentityDocIssued')
            value_ = self.gds_validate_string(value_, node, 'IdentityDocIssued')
            self.IdentityDocIssued = value_
            self.IdentityDocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.IdentityDocIssued)


# end class PersonIdentityDocInfoType


class ChildInfoType(GeneratedsSuper):
    """Сведения о ребёнке"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        ChildSurname=None,
        ChildName=None,
        ChildMiddleName=None,
        ChildBirthDate=None,
        ChildBirthDocRF=None,
        ChildBirthDocForeign=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.ChildSurname = ChildSurname
        self.validate_string_256(self.ChildSurname)
        self.ChildSurname_nsprefix_ = 'tns'
        self.ChildName = ChildName
        self.validate_string_256(self.ChildName)
        self.ChildName_nsprefix_ = 'tns'
        self.ChildMiddleName = ChildMiddleName
        self.validate_string_256(self.ChildMiddleName)
        self.ChildMiddleName_nsprefix_ = 'tns'
        if isinstance(ChildBirthDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ChildBirthDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ChildBirthDate
        self.ChildBirthDate = initvalue_
        self.ChildBirthDate_nsprefix_ = 'tns'
        self.ChildBirthDocRF = ChildBirthDocRF
        self.ChildBirthDocRF_nsprefix_ = 'tns'
        self.ChildBirthDocForeign = ChildBirthDocForeign
        self.ChildBirthDocForeign_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, ChildInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ChildInfoType.subclass:
            return ChildInfoType.subclass(*args_, **kwargs_)
        else:
            return ChildInfoType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_ChildSurname(self):
        return self.ChildSurname

    def set_ChildSurname(self, ChildSurname):
        self.ChildSurname = ChildSurname

    def get_ChildName(self):
        return self.ChildName

    def set_ChildName(self, ChildName):
        self.ChildName = ChildName

    def get_ChildMiddleName(self):
        return self.ChildMiddleName

    def set_ChildMiddleName(self, ChildMiddleName):
        self.ChildMiddleName = ChildMiddleName

    def get_ChildBirthDate(self):
        return self.ChildBirthDate

    def set_ChildBirthDate(self, ChildBirthDate):
        self.ChildBirthDate = ChildBirthDate

    def get_ChildBirthDocRF(self):
        return self.ChildBirthDocRF

    def set_ChildBirthDocRF(self, ChildBirthDocRF):
        self.ChildBirthDocRF = ChildBirthDocRF

    def get_ChildBirthDocForeign(self):
        return self.ChildBirthDocForeign

    def set_ChildBirthDocForeign(self, ChildBirthDocForeign):
        self.ChildBirthDocForeign = ChildBirthDocForeign

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.ChildSurname is not None
            or self.ChildName is not None
            or self.ChildMiddleName is not None
            or self.ChildBirthDate is not None
            or self.ChildBirthDocRF is not None
            or self.ChildBirthDocForeign is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='ChildInfoType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ChildInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ChildInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ChildInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile, level + 1, namespaceprefix_, namespacedef_, name_='ChildInfoType', pretty_print=pretty_print
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ChildInfoType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='ChildInfoType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ChildSurname is not None:
            namespaceprefix_ = (
                self.ChildSurname_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildSurname_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildSurname>%s</%sChildSurname>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.ChildSurname), input_name='ChildSurname')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildName is not None:
            namespaceprefix_ = self.ChildName_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildName>%s</%sChildName>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.ChildName), input_name='ChildName')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildMiddleName is not None:
            namespaceprefix_ = (
                self.ChildMiddleName_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildMiddleName_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildMiddleName>%s</%sChildMiddleName>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.ChildMiddleName), input_name='ChildMiddleName')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDate is not None:
            namespaceprefix_ = (
                self.ChildBirthDate_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDate_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDate>%s</%sChildBirthDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.ChildBirthDate, input_name='ChildBirthDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDocRF is not None:
            namespaceprefix_ = (
                self.ChildBirthDocRF_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocRF_nsprefix_) else ''
            )
            self.ChildBirthDocRF.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='ChildBirthDocRF', pretty_print=pretty_print
            )
        if self.ChildBirthDocForeign is not None:
            namespaceprefix_ = (
                self.ChildBirthDocForeign_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocForeign_nsprefix_)
                else ''
            )
            self.ChildBirthDocForeign.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_='',
                name_='ChildBirthDocForeign',
                pretty_print=pretty_print,
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ChildSurname':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildSurname')
            value_ = self.gds_validate_string(value_, node, 'ChildSurname')
            self.ChildSurname = value_
            self.ChildSurname_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildSurname)
        elif nodeName_ == 'ChildName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildName')
            value_ = self.gds_validate_string(value_, node, 'ChildName')
            self.ChildName = value_
            self.ChildName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildName)
        elif nodeName_ == 'ChildMiddleName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildMiddleName')
            value_ = self.gds_validate_string(value_, node, 'ChildMiddleName')
            self.ChildMiddleName = value_
            self.ChildMiddleName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildMiddleName)
        elif nodeName_ == 'ChildBirthDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ChildBirthDate = dval_
            self.ChildBirthDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChildBirthDocRF':
            obj_ = ChildBirthDocRFType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChildBirthDocRF = obj_
            obj_.original_tagname_ = 'ChildBirthDocRF'
        elif nodeName_ == 'ChildBirthDocForeign':
            obj_ = ChildBirthDocForeignType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChildBirthDocForeign = obj_
            obj_.original_tagname_ = 'ChildBirthDocForeign'


# end class ChildInfoType


class ChildBirthDocRFType(GeneratedsSuper):
    """Свидетельство о рождении РФ"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        ChildBirthDocSeries=None,
        ChildBirthDocNumber=None,
        ChildBirthDocIssueDate=None,
        ChildBirthDocActNumber=None,
        ChildBirthDocActDate=None,
        ChildBirthDocIssued=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.ChildBirthDocSeries = ChildBirthDocSeries
        self.validate_string_10(self.ChildBirthDocSeries)
        self.ChildBirthDocSeries_nsprefix_ = 'tns'
        self.ChildBirthDocNumber = ChildBirthDocNumber
        self.validate_string_10(self.ChildBirthDocNumber)
        self.ChildBirthDocNumber_nsprefix_ = 'tns'
        if isinstance(ChildBirthDocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ChildBirthDocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ChildBirthDocIssueDate
        self.ChildBirthDocIssueDate = initvalue_
        self.ChildBirthDocIssueDate_nsprefix_ = 'tns'
        self.ChildBirthDocActNumber = ChildBirthDocActNumber
        self.validate_string_21(self.ChildBirthDocActNumber)
        self.ChildBirthDocActNumber_nsprefix_ = 'tns'
        if isinstance(ChildBirthDocActDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ChildBirthDocActDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ChildBirthDocActDate
        self.ChildBirthDocActDate = initvalue_
        self.ChildBirthDocActDate_nsprefix_ = 'tns'
        self.ChildBirthDocIssued = ChildBirthDocIssued
        self.validate_string_256(self.ChildBirthDocIssued)
        self.ChildBirthDocIssued_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, ChildBirthDocRFType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ChildBirthDocRFType.subclass:
            return ChildBirthDocRFType.subclass(*args_, **kwargs_)
        else:
            return ChildBirthDocRFType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_ChildBirthDocSeries(self):
        return self.ChildBirthDocSeries

    def set_ChildBirthDocSeries(self, ChildBirthDocSeries):
        self.ChildBirthDocSeries = ChildBirthDocSeries

    def get_ChildBirthDocNumber(self):
        return self.ChildBirthDocNumber

    def set_ChildBirthDocNumber(self, ChildBirthDocNumber):
        self.ChildBirthDocNumber = ChildBirthDocNumber

    def get_ChildBirthDocIssueDate(self):
        return self.ChildBirthDocIssueDate

    def set_ChildBirthDocIssueDate(self, ChildBirthDocIssueDate):
        self.ChildBirthDocIssueDate = ChildBirthDocIssueDate

    def get_ChildBirthDocActNumber(self):
        return self.ChildBirthDocActNumber

    def set_ChildBirthDocActNumber(self, ChildBirthDocActNumber):
        self.ChildBirthDocActNumber = ChildBirthDocActNumber

    def get_ChildBirthDocActDate(self):
        return self.ChildBirthDocActDate

    def set_ChildBirthDocActDate(self, ChildBirthDocActDate):
        self.ChildBirthDocActDate = ChildBirthDocActDate

    def get_ChildBirthDocIssued(self):
        return self.ChildBirthDocIssued

    def set_ChildBirthDocIssued(self, ChildBirthDocIssued):
        self.ChildBirthDocIssued = ChildBirthDocIssued

    def validate_string_10(self, value):
        result = True
        # Validate type string-10, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-10'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_21(self, value):
        result = True
        # Validate type string-21, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 21:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-21'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.ChildBirthDocSeries is not None
            or self.ChildBirthDocNumber is not None
            or self.ChildBirthDocIssueDate is not None
            or self.ChildBirthDocActNumber is not None
            or self.ChildBirthDocActDate is not None
            or self.ChildBirthDocIssued is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='ChildBirthDocRFType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ChildBirthDocRFType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ChildBirthDocRFType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ChildBirthDocRFType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='ChildBirthDocRFType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ChildBirthDocRFType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='ChildBirthDocRFType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ChildBirthDocSeries is not None:
            namespaceprefix_ = (
                self.ChildBirthDocSeries_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocSeries_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocSeries>%s</%sChildBirthDocSeries>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.ChildBirthDocSeries), input_name='ChildBirthDocSeries')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDocNumber is not None:
            namespaceprefix_ = (
                self.ChildBirthDocNumber_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocNumber_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocNumber>%s</%sChildBirthDocNumber>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.ChildBirthDocNumber), input_name='ChildBirthDocNumber')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDocIssueDate is not None:
            namespaceprefix_ = (
                self.ChildBirthDocIssueDate_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocIssueDate_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocIssueDate>%s</%sChildBirthDocIssueDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.ChildBirthDocIssueDate, input_name='ChildBirthDocIssueDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDocActNumber is not None:
            namespaceprefix_ = (
                self.ChildBirthDocActNumber_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocActNumber_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocActNumber>%s</%sChildBirthDocActNumber>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(
                            quote_xml(self.ChildBirthDocActNumber), input_name='ChildBirthDocActNumber'
                        )
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDocActDate is not None:
            namespaceprefix_ = (
                self.ChildBirthDocActDate_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocActDate_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocActDate>%s</%sChildBirthDocActDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.ChildBirthDocActDate, input_name='ChildBirthDocActDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDocIssued is not None:
            namespaceprefix_ = (
                self.ChildBirthDocIssued_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocIssued_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocIssued>%s</%sChildBirthDocIssued>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.ChildBirthDocIssued), input_name='ChildBirthDocIssued')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ChildBirthDocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocSeries')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocSeries')
            self.ChildBirthDocSeries = value_
            self.ChildBirthDocSeries_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.ChildBirthDocSeries)
        elif nodeName_ == 'ChildBirthDocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocNumber')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocNumber')
            self.ChildBirthDocNumber = value_
            self.ChildBirthDocNumber_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.ChildBirthDocNumber)
        elif nodeName_ == 'ChildBirthDocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ChildBirthDocIssueDate = dval_
            self.ChildBirthDocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChildBirthDocActNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocActNumber')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocActNumber')
            self.ChildBirthDocActNumber = value_
            self.ChildBirthDocActNumber_nsprefix_ = child_.prefix
            # validate type string-21
            self.validate_string_21(self.ChildBirthDocActNumber)
        elif nodeName_ == 'ChildBirthDocActDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ChildBirthDocActDate = dval_
            self.ChildBirthDocActDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChildBirthDocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocIssued')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocIssued')
            self.ChildBirthDocIssued = value_
            self.ChildBirthDocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildBirthDocIssued)


# end class ChildBirthDocRFType


class ChildBirthDocForeignType(GeneratedsSuper):
    """Другой документ"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        ChildBirthDocName=None,
        ChildBirthDocSeries=None,
        ChildBirthDocNumber=None,
        ChildBirthDocIssueDate=None,
        ChildBirthDocIssued=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.ChildBirthDocName = ChildBirthDocName
        self.validate_string_256(self.ChildBirthDocName)
        self.ChildBirthDocName_nsprefix_ = 'tns'
        self.ChildBirthDocSeries = ChildBirthDocSeries
        self.validate_string_10(self.ChildBirthDocSeries)
        self.ChildBirthDocSeries_nsprefix_ = 'tns'
        self.ChildBirthDocNumber = ChildBirthDocNumber
        self.validate_string_50(self.ChildBirthDocNumber)
        self.ChildBirthDocNumber_nsprefix_ = 'tns'
        if isinstance(ChildBirthDocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(ChildBirthDocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = ChildBirthDocIssueDate
        self.ChildBirthDocIssueDate = initvalue_
        self.ChildBirthDocIssueDate_nsprefix_ = 'tns'
        self.ChildBirthDocIssued = ChildBirthDocIssued
        self.validate_string_256(self.ChildBirthDocIssued)
        self.ChildBirthDocIssued_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, ChildBirthDocForeignType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ChildBirthDocForeignType.subclass:
            return ChildBirthDocForeignType.subclass(*args_, **kwargs_)
        else:
            return ChildBirthDocForeignType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_ChildBirthDocName(self):
        return self.ChildBirthDocName

    def set_ChildBirthDocName(self, ChildBirthDocName):
        self.ChildBirthDocName = ChildBirthDocName

    def get_ChildBirthDocSeries(self):
        return self.ChildBirthDocSeries

    def set_ChildBirthDocSeries(self, ChildBirthDocSeries):
        self.ChildBirthDocSeries = ChildBirthDocSeries

    def get_ChildBirthDocNumber(self):
        return self.ChildBirthDocNumber

    def set_ChildBirthDocNumber(self, ChildBirthDocNumber):
        self.ChildBirthDocNumber = ChildBirthDocNumber

    def get_ChildBirthDocIssueDate(self):
        return self.ChildBirthDocIssueDate

    def set_ChildBirthDocIssueDate(self, ChildBirthDocIssueDate):
        self.ChildBirthDocIssueDate = ChildBirthDocIssueDate

    def get_ChildBirthDocIssued(self):
        return self.ChildBirthDocIssued

    def set_ChildBirthDocIssued(self, ChildBirthDocIssued):
        self.ChildBirthDocIssued = ChildBirthDocIssued

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_10(self, value):
        result = True
        # Validate type string-10, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 10:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-10'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_50(self, value):
        result = True
        # Validate type string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.ChildBirthDocName is not None
            or self.ChildBirthDocSeries is not None
            or self.ChildBirthDocNumber is not None
            or self.ChildBirthDocIssueDate is not None
            or self.ChildBirthDocIssued is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='ChildBirthDocForeignType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ChildBirthDocForeignType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ChildBirthDocForeignType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ChildBirthDocForeignType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='ChildBirthDocForeignType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(
        self, outfile, level, already_processed, namespaceprefix_='', name_='ChildBirthDocForeignType'
    ):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='ChildBirthDocForeignType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ChildBirthDocName is not None:
            namespaceprefix_ = (
                self.ChildBirthDocName_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildBirthDocName_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocName>%s</%sChildBirthDocName>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.ChildBirthDocName), input_name='ChildBirthDocName')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDocSeries is not None:
            namespaceprefix_ = (
                self.ChildBirthDocSeries_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocSeries_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocSeries>%s</%sChildBirthDocSeries>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.ChildBirthDocSeries), input_name='ChildBirthDocSeries')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDocNumber is not None:
            namespaceprefix_ = (
                self.ChildBirthDocNumber_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocNumber_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocNumber>%s</%sChildBirthDocNumber>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.ChildBirthDocNumber), input_name='ChildBirthDocNumber')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDocIssueDate is not None:
            namespaceprefix_ = (
                self.ChildBirthDocIssueDate_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocIssueDate_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocIssueDate>%s</%sChildBirthDocIssueDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.ChildBirthDocIssueDate, input_name='ChildBirthDocIssueDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildBirthDocIssued is not None:
            namespaceprefix_ = (
                self.ChildBirthDocIssued_nsprefix_ + ':'
                if (UseCapturedNS_ and self.ChildBirthDocIssued_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildBirthDocIssued>%s</%sChildBirthDocIssued>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.ChildBirthDocIssued), input_name='ChildBirthDocIssued')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ChildBirthDocName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocName')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocName')
            self.ChildBirthDocName = value_
            self.ChildBirthDocName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildBirthDocName)
        elif nodeName_ == 'ChildBirthDocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocSeries')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocSeries')
            self.ChildBirthDocSeries = value_
            self.ChildBirthDocSeries_nsprefix_ = child_.prefix
            # validate type string-10
            self.validate_string_10(self.ChildBirthDocSeries)
        elif nodeName_ == 'ChildBirthDocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocNumber')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocNumber')
            self.ChildBirthDocNumber = value_
            self.ChildBirthDocNumber_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.ChildBirthDocNumber)
        elif nodeName_ == 'ChildBirthDocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.ChildBirthDocIssueDate = dval_
            self.ChildBirthDocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'ChildBirthDocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildBirthDocIssued')
            value_ = self.gds_validate_string(value_, node, 'ChildBirthDocIssued')
            self.ChildBirthDocIssued = value_
            self.ChildBirthDocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildBirthDocIssued)


# end class ChildBirthDocForeignType


class AddressType(GeneratedsSuper):
    """Адрес"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        FullAddress=None,
        Index=None,
        Region=None,
        Area=None,
        City=None,
        CityArea=None,
        Place=None,
        Street=None,
        AdditionalArea=None,
        AdditionalStreet=None,
        House=None,
        Building1=None,
        Building2=None,
        Apartment=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.FullAddress = FullAddress
        self.validate_string_1024(self.FullAddress)
        self.FullAddress_nsprefix_ = 'tns'
        self.Index = Index
        self.validate_string_6(self.Index)
        self.Index_nsprefix_ = 'tns'
        self.Region = Region
        self.Region_nsprefix_ = 'tns'
        self.Area = Area
        self.Area_nsprefix_ = 'tns'
        self.City = City
        self.City_nsprefix_ = 'tns'
        self.CityArea = CityArea
        self.CityArea_nsprefix_ = 'tns'
        self.Place = Place
        self.Place_nsprefix_ = 'tns'
        self.Street = Street
        self.Street_nsprefix_ = 'tns'
        self.AdditionalArea = AdditionalArea
        self.AdditionalArea_nsprefix_ = 'tns'
        self.AdditionalStreet = AdditionalStreet
        self.AdditionalStreet_nsprefix_ = 'tns'
        self.House = House
        self.House_nsprefix_ = 'tns'
        self.Building1 = Building1
        self.validate_string_50(self.Building1)
        self.Building1_nsprefix_ = 'tns'
        self.Building2 = Building2
        self.validate_string_50(self.Building2)
        self.Building2_nsprefix_ = 'tns'
        self.Apartment = Apartment
        self.validate_string_50(self.Apartment)
        self.Apartment_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, AddressType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressType.subclass:
            return AddressType.subclass(*args_, **kwargs_)
        else:
            return AddressType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_FullAddress(self):
        return self.FullAddress

    def set_FullAddress(self, FullAddress):
        self.FullAddress = FullAddress

    def get_Index(self):
        return self.Index

    def set_Index(self, Index):
        self.Index = Index

    def get_Region(self):
        return self.Region

    def set_Region(self, Region):
        self.Region = Region

    def get_Area(self):
        return self.Area

    def set_Area(self, Area):
        self.Area = Area

    def get_City(self):
        return self.City

    def set_City(self, City):
        self.City = City

    def get_CityArea(self):
        return self.CityArea

    def set_CityArea(self, CityArea):
        self.CityArea = CityArea

    def get_Place(self):
        return self.Place

    def set_Place(self, Place):
        self.Place = Place

    def get_Street(self):
        return self.Street

    def set_Street(self, Street):
        self.Street = Street

    def get_AdditionalArea(self):
        return self.AdditionalArea

    def set_AdditionalArea(self, AdditionalArea):
        self.AdditionalArea = AdditionalArea

    def get_AdditionalStreet(self):
        return self.AdditionalStreet

    def set_AdditionalStreet(self, AdditionalStreet):
        self.AdditionalStreet = AdditionalStreet

    def get_House(self):
        return self.House

    def set_House(self, House):
        self.House = House

    def get_Building1(self):
        return self.Building1

    def set_Building1(self, Building1):
        self.Building1 = Building1

    def get_Building2(self):
        return self.Building2

    def set_Building2(self, Building2):
        self.Building2 = Building2

    def get_Apartment(self):
        return self.Apartment

    def set_Apartment(self, Apartment):
        self.Apartment = Apartment

    def validate_string_1024(self, value):
        result = True
        # Validate type string-1024, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 1024:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-1024'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_6(self, value):
        result = True
        # Validate type string-6, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 6:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-6'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_50(self, value):
        result = True
        # Validate type string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.FullAddress is not None
            or self.Index is not None
            or self.Region is not None
            or self.Area is not None
            or self.City is not None
            or self.CityArea is not None
            or self.Place is not None
            or self.Street is not None
            or self.AdditionalArea is not None
            or self.AdditionalStreet is not None
            or self.House is not None
            or self.Building1 is not None
            or self.Building2 is not None
            or self.Apartment is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='AddressType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressType', pretty_print=pretty_print
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='AddressType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.FullAddress is not None:
            namespaceprefix_ = (
                self.FullAddress_nsprefix_ + ':' if (UseCapturedNS_ and self.FullAddress_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sFullAddress>%s</%sFullAddress>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.FullAddress), input_name='FullAddress')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.Index is not None:
            namespaceprefix_ = self.Index_nsprefix_ + ':' if (UseCapturedNS_ and self.Index_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sIndex>%s</%sIndex>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.Index), input_name='Index')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.Region is not None:
            namespaceprefix_ = self.Region_nsprefix_ + ':' if (UseCapturedNS_ and self.Region_nsprefix_) else ''
            self.Region.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='Region', pretty_print=pretty_print
            )
        if self.Area is not None:
            namespaceprefix_ = self.Area_nsprefix_ + ':' if (UseCapturedNS_ and self.Area_nsprefix_) else ''
            self.Area.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='Area', pretty_print=pretty_print
            )
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            self.City.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='City', pretty_print=pretty_print
            )
        if self.CityArea is not None:
            namespaceprefix_ = self.CityArea_nsprefix_ + ':' if (UseCapturedNS_ and self.CityArea_nsprefix_) else ''
            self.CityArea.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='CityArea', pretty_print=pretty_print
            )
        if self.Place is not None:
            namespaceprefix_ = self.Place_nsprefix_ + ':' if (UseCapturedNS_ and self.Place_nsprefix_) else ''
            self.Place.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='Place', pretty_print=pretty_print
            )
        if self.Street is not None:
            namespaceprefix_ = self.Street_nsprefix_ + ':' if (UseCapturedNS_ and self.Street_nsprefix_) else ''
            self.Street.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='Street', pretty_print=pretty_print
            )
        if self.AdditionalArea is not None:
            namespaceprefix_ = (
                self.AdditionalArea_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalArea_nsprefix_) else ''
            )
            self.AdditionalArea.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='AdditionalArea', pretty_print=pretty_print
            )
        if self.AdditionalStreet is not None:
            namespaceprefix_ = (
                self.AdditionalStreet_nsprefix_ + ':' if (UseCapturedNS_ and self.AdditionalStreet_nsprefix_) else ''
            )
            self.AdditionalStreet.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='AdditionalStreet', pretty_print=pretty_print
            )
        if self.House is not None:
            namespaceprefix_ = self.House_nsprefix_ + ':' if (UseCapturedNS_ and self.House_nsprefix_) else ''
            self.House.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='House', pretty_print=pretty_print
            )
        if self.Building1 is not None:
            namespaceprefix_ = self.Building1_nsprefix_ + ':' if (UseCapturedNS_ and self.Building1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sBuilding1>%s</%sBuilding1>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.Building1), input_name='Building1')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.Building2 is not None:
            namespaceprefix_ = self.Building2_nsprefix_ + ':' if (UseCapturedNS_ and self.Building2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sBuilding2>%s</%sBuilding2>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.Building2), input_name='Building2')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.Apartment is not None:
            namespaceprefix_ = self.Apartment_nsprefix_ + ':' if (UseCapturedNS_ and self.Apartment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sApartment>%s</%sApartment>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.Apartment), input_name='Apartment')),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'FullAddress':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'FullAddress')
            value_ = self.gds_validate_string(value_, node, 'FullAddress')
            self.FullAddress = value_
            self.FullAddress_nsprefix_ = child_.prefix
            # validate type string-1024
            self.validate_string_1024(self.FullAddress)
        elif nodeName_ == 'Index':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Index')
            value_ = self.gds_validate_string(value_, node, 'Index')
            self.Index = value_
            self.Index_nsprefix_ = child_.prefix
            # validate type string-6
            self.validate_string_6(self.Index)
        elif nodeName_ == 'Region':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Region = obj_
            obj_.original_tagname_ = 'Region'
        elif nodeName_ == 'Area':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Area = obj_
            obj_.original_tagname_ = 'Area'
        elif nodeName_ == 'City':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.City = obj_
            obj_.original_tagname_ = 'City'
        elif nodeName_ == 'CityArea':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CityArea = obj_
            obj_.original_tagname_ = 'CityArea'
        elif nodeName_ == 'Place':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Place = obj_
            obj_.original_tagname_ = 'Place'
        elif nodeName_ == 'Street':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Street = obj_
            obj_.original_tagname_ = 'Street'
        elif nodeName_ == 'AdditionalArea':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdditionalArea = obj_
            obj_.original_tagname_ = 'AdditionalArea'
        elif nodeName_ == 'AdditionalStreet':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdditionalStreet = obj_
            obj_.original_tagname_ = 'AdditionalStreet'
        elif nodeName_ == 'House':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.House = obj_
            obj_.original_tagname_ = 'House'
        elif nodeName_ == 'Building1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Building1')
            value_ = self.gds_validate_string(value_, node, 'Building1')
            self.Building1 = value_
            self.Building1_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.Building1)
        elif nodeName_ == 'Building2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Building2')
            value_ = self.gds_validate_string(value_, node, 'Building2')
            self.Building2 = value_
            self.Building2_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.Building2)
        elif nodeName_ == 'Apartment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Apartment')
            value_ = self.gds_validate_string(value_, node, 'Apartment')
            self.Apartment = value_
            self.Apartment_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.Apartment)


# end class AddressType


class EntryParamsType(GeneratedsSuper):
    """Желаемые параметры зачисления"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self, EntryDate=None, Language=None, Schedule=None, AgreementOnFullDayGroup=None, gds_collector_=None, **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        if isinstance(EntryDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(EntryDate, '%Y-%m-%d').date()
        else:
            initvalue_ = EntryDate
        self.EntryDate = initvalue_
        self.EntryDate_nsprefix_ = 'tns'
        self.Language = Language
        self.Language_nsprefix_ = 'tns'
        self.Schedule = Schedule
        self.Schedule_nsprefix_ = 'tns'
        self.AgreementOnFullDayGroup = AgreementOnFullDayGroup
        self.AgreementOnFullDayGroup_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, EntryParamsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EntryParamsType.subclass:
            return EntryParamsType.subclass(*args_, **kwargs_)
        else:
            return EntryParamsType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_EntryDate(self):
        return self.EntryDate

    def set_EntryDate(self, EntryDate):
        self.EntryDate = EntryDate

    def get_Language(self):
        return self.Language

    def set_Language(self, Language):
        self.Language = Language

    def get_Schedule(self):
        return self.Schedule

    def set_Schedule(self, Schedule):
        self.Schedule = Schedule

    def get_AgreementOnFullDayGroup(self):
        return self.AgreementOnFullDayGroup

    def set_AgreementOnFullDayGroup(self, AgreementOnFullDayGroup):
        self.AgreementOnFullDayGroup = AgreementOnFullDayGroup

    def hasContent_(self):
        if (
            self.EntryDate is not None
            or self.Language is not None
            or self.Schedule is not None
            or self.AgreementOnFullDayGroup is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='EntryParamsType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EntryParamsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EntryParamsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EntryParamsType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile, level + 1, namespaceprefix_, namespacedef_, name_='EntryParamsType', pretty_print=pretty_print
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EntryParamsType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='EntryParamsType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.EntryDate is not None:
            namespaceprefix_ = self.EntryDate_nsprefix_ + ':' if (UseCapturedNS_ and self.EntryDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sEntryDate>%s</%sEntryDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.EntryDate, input_name='EntryDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.Language is not None:
            namespaceprefix_ = self.Language_nsprefix_ + ':' if (UseCapturedNS_ and self.Language_nsprefix_) else ''
            self.Language.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='Language', pretty_print=pretty_print
            )
        if self.Schedule is not None:
            namespaceprefix_ = self.Schedule_nsprefix_ + ':' if (UseCapturedNS_ and self.Schedule_nsprefix_) else ''
            self.Schedule.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='Schedule', pretty_print=pretty_print
            )
        if self.AgreementOnFullDayGroup is not None:
            namespaceprefix_ = (
                self.AgreementOnFullDayGroup_nsprefix_ + ':'
                if (UseCapturedNS_ and self.AgreementOnFullDayGroup_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sAgreementOnFullDayGroup>%s</%sAgreementOnFullDayGroup>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_boolean(self.AgreementOnFullDayGroup, input_name='AgreementOnFullDayGroup'),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'EntryDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.EntryDate = dval_
            self.EntryDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'Language':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Language = obj_
            obj_.original_tagname_ = 'Language'
        elif nodeName_ == 'Schedule':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Schedule = obj_
            obj_.original_tagname_ = 'Schedule'
        elif nodeName_ == 'AgreementOnFullDayGroup':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AgreementOnFullDayGroup')
            ival_ = self.gds_validate_boolean(ival_, node, 'AgreementOnFullDayGroup')
            self.AgreementOnFullDayGroup = ival_
            self.AgreementOnFullDayGroup_nsprefix_ = child_.prefix


# end class EntryParamsType


class AdaptationProgramType(GeneratedsSuper):
    """Направленность группы"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        AdaptationGroup=None,
        AdaptationGroupType=None,
        AgreementOnGeneralGroup=None,
        AgreementOnCareGroup=None,
        NeedSpecialCareConditions=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.AdaptationGroup = AdaptationGroup
        self.AdaptationGroup_nsprefix_ = 'tns'
        self.AdaptationGroupType = AdaptationGroupType
        self.AdaptationGroupType_nsprefix_ = 'tns'
        self.AgreementOnGeneralGroup = AgreementOnGeneralGroup
        self.AgreementOnGeneralGroup_nsprefix_ = 'tns'
        self.AgreementOnCareGroup = AgreementOnCareGroup
        self.AgreementOnCareGroup_nsprefix_ = 'tns'
        self.NeedSpecialCareConditions = NeedSpecialCareConditions
        self.NeedSpecialCareConditions_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, AdaptationProgramType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AdaptationProgramType.subclass:
            return AdaptationProgramType.subclass(*args_, **kwargs_)
        else:
            return AdaptationProgramType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_AdaptationGroup(self):
        return self.AdaptationGroup

    def set_AdaptationGroup(self, AdaptationGroup):
        self.AdaptationGroup = AdaptationGroup

    def get_AdaptationGroupType(self):
        return self.AdaptationGroupType

    def set_AdaptationGroupType(self, AdaptationGroupType):
        self.AdaptationGroupType = AdaptationGroupType

    def get_AgreementOnGeneralGroup(self):
        return self.AgreementOnGeneralGroup

    def set_AgreementOnGeneralGroup(self, AgreementOnGeneralGroup):
        self.AgreementOnGeneralGroup = AgreementOnGeneralGroup

    def get_AgreementOnCareGroup(self):
        return self.AgreementOnCareGroup

    def set_AgreementOnCareGroup(self, AgreementOnCareGroup):
        self.AgreementOnCareGroup = AgreementOnCareGroup

    def get_NeedSpecialCareConditions(self):
        return self.NeedSpecialCareConditions

    def set_NeedSpecialCareConditions(self, NeedSpecialCareConditions):
        self.NeedSpecialCareConditions = NeedSpecialCareConditions

    def hasContent_(self):
        if (
            self.AdaptationGroup is not None
            or self.AdaptationGroupType is not None
            or self.AgreementOnGeneralGroup is not None
            or self.AgreementOnCareGroup is not None
            or self.NeedSpecialCareConditions is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='AdaptationProgramType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AdaptationProgramType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AdaptationProgramType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AdaptationProgramType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='AdaptationProgramType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AdaptationProgramType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='AdaptationProgramType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AdaptationGroup is not None:
            namespaceprefix_ = (
                self.AdaptationGroup_nsprefix_ + ':' if (UseCapturedNS_ and self.AdaptationGroup_nsprefix_) else ''
            )
            self.AdaptationGroup.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='AdaptationGroup', pretty_print=pretty_print
            )
        if self.AdaptationGroupType is not None:
            namespaceprefix_ = (
                self.AdaptationGroupType_nsprefix_ + ':'
                if (UseCapturedNS_ and self.AdaptationGroupType_nsprefix_)
                else ''
            )
            self.AdaptationGroupType.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_='',
                name_='AdaptationGroupType',
                pretty_print=pretty_print,
            )
        if self.AgreementOnGeneralGroup is not None:
            namespaceprefix_ = (
                self.AgreementOnGeneralGroup_nsprefix_ + ':'
                if (UseCapturedNS_ and self.AgreementOnGeneralGroup_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sAgreementOnGeneralGroup>%s</%sAgreementOnGeneralGroup>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_boolean(self.AgreementOnGeneralGroup, input_name='AgreementOnGeneralGroup'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.AgreementOnCareGroup is not None:
            namespaceprefix_ = (
                self.AgreementOnCareGroup_nsprefix_ + ':'
                if (UseCapturedNS_ and self.AgreementOnCareGroup_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sAgreementOnCareGroup>%s</%sAgreementOnCareGroup>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_boolean(self.AgreementOnCareGroup, input_name='AgreementOnCareGroup'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.NeedSpecialCareConditions is not None:
            namespaceprefix_ = (
                self.NeedSpecialCareConditions_nsprefix_ + ':'
                if (UseCapturedNS_ and self.NeedSpecialCareConditions_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sNeedSpecialCareConditions>%s</%sNeedSpecialCareConditions>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_boolean(self.NeedSpecialCareConditions, input_name='NeedSpecialCareConditions'),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AdaptationGroup':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdaptationGroup = obj_
            obj_.original_tagname_ = 'AdaptationGroup'
        elif nodeName_ == 'AdaptationGroupType':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdaptationGroupType = obj_
            obj_.original_tagname_ = 'AdaptationGroupType'
        elif nodeName_ == 'AgreementOnGeneralGroup':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AgreementOnGeneralGroup')
            ival_ = self.gds_validate_boolean(ival_, node, 'AgreementOnGeneralGroup')
            self.AgreementOnGeneralGroup = ival_
            self.AgreementOnGeneralGroup_nsprefix_ = child_.prefix
        elif nodeName_ == 'AgreementOnCareGroup':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AgreementOnCareGroup')
            ival_ = self.gds_validate_boolean(ival_, node, 'AgreementOnCareGroup')
            self.AgreementOnCareGroup = ival_
            self.AgreementOnCareGroup_nsprefix_ = child_.prefix
        elif nodeName_ == 'NeedSpecialCareConditions':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'NeedSpecialCareConditions')
            ival_ = self.gds_validate_boolean(ival_, node, 'NeedSpecialCareConditions')
            self.NeedSpecialCareConditions = ival_
            self.NeedSpecialCareConditions_nsprefix_ = child_.prefix


# end class AdaptationProgramType


class MedicalReportWithoutFilesType(GeneratedsSuper):
    """Реквизиты документа, подтверждающего группу коменсирующей
    направленности"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        DocName=None,
        DocSeries=None,
        DocNumber=None,
        DocIssueDate=None,
        DocIssued=None,
        DocExpirationDate=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.DocName = DocName
        self.DocName_nsprefix_ = 'tns'
        self.DocSeries = DocSeries
        self.validate_string_20(self.DocSeries)
        self.DocSeries_nsprefix_ = 'tns'
        self.DocNumber = DocNumber
        self.validate_string_20(self.DocNumber)
        self.DocNumber_nsprefix_ = 'tns'
        if isinstance(DocIssueDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DocIssueDate, '%Y-%m-%d').date()
        else:
            initvalue_ = DocIssueDate
        self.DocIssueDate = initvalue_
        self.DocIssueDate_nsprefix_ = 'tns'
        self.DocIssued = DocIssued
        self.validate_string_256(self.DocIssued)
        self.DocIssued_nsprefix_ = 'tns'
        if isinstance(DocExpirationDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(DocExpirationDate, '%Y-%m-%d').date()
        else:
            initvalue_ = DocExpirationDate
        self.DocExpirationDate = initvalue_
        self.DocExpirationDate_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, MedicalReportWithoutFilesType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if MedicalReportWithoutFilesType.subclass:
            return MedicalReportWithoutFilesType.subclass(*args_, **kwargs_)
        else:
            return MedicalReportWithoutFilesType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_DocName(self):
        return self.DocName

    def set_DocName(self, DocName):
        self.DocName = DocName

    def get_DocSeries(self):
        return self.DocSeries

    def set_DocSeries(self, DocSeries):
        self.DocSeries = DocSeries

    def get_DocNumber(self):
        return self.DocNumber

    def set_DocNumber(self, DocNumber):
        self.DocNumber = DocNumber

    def get_DocIssueDate(self):
        return self.DocIssueDate

    def set_DocIssueDate(self, DocIssueDate):
        self.DocIssueDate = DocIssueDate

    def get_DocIssued(self):
        return self.DocIssued

    def set_DocIssued(self, DocIssued):
        self.DocIssued = DocIssued

    def get_DocExpirationDate(self):
        return self.DocExpirationDate

    def set_DocExpirationDate(self, DocExpirationDate):
        self.DocExpirationDate = DocExpirationDate

    def validate_string_20(self, value):
        result = True
        # Validate type string-20, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 20:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-20'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.DocName is not None
            or self.DocSeries is not None
            or self.DocNumber is not None
            or self.DocIssueDate is not None
            or self.DocIssued is not None
            or self.DocExpirationDate is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='MedicalReportWithoutFilesType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('MedicalReportWithoutFilesType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'MedicalReportWithoutFilesType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(
            outfile, level, already_processed, namespaceprefix_, name_='MedicalReportWithoutFilesType'
        )
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='MedicalReportWithoutFilesType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(
        self, outfile, level, already_processed, namespaceprefix_='', name_='MedicalReportWithoutFilesType'
    ):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='MedicalReportWithoutFilesType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.DocName is not None:
            namespaceprefix_ = self.DocName_nsprefix_ + ':' if (UseCapturedNS_ and self.DocName_nsprefix_) else ''
            self.DocName.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='DocName', pretty_print=pretty_print
            )
        if self.DocSeries is not None:
            namespaceprefix_ = self.DocSeries_nsprefix_ + ':' if (UseCapturedNS_ and self.DocSeries_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sDocSeries>%s</%sDocSeries>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.DocSeries), input_name='DocSeries')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.DocNumber is not None:
            namespaceprefix_ = self.DocNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.DocNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sDocNumber>%s</%sDocNumber>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.DocNumber), input_name='DocNumber')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.DocIssueDate is not None:
            namespaceprefix_ = (
                self.DocIssueDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DocIssueDate_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sDocIssueDate>%s</%sDocIssueDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.DocIssueDate, input_name='DocIssueDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.DocIssued is not None:
            namespaceprefix_ = self.DocIssued_nsprefix_ + ':' if (UseCapturedNS_ and self.DocIssued_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sDocIssued>%s</%sDocIssued>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.DocIssued), input_name='DocIssued')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.DocExpirationDate is not None:
            namespaceprefix_ = (
                self.DocExpirationDate_nsprefix_ + ':' if (UseCapturedNS_ and self.DocExpirationDate_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sDocExpirationDate>%s</%sDocExpirationDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_date(self.DocExpirationDate, input_name='DocExpirationDate'),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'DocName':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.DocName = obj_
            obj_.original_tagname_ = 'DocName'
        elif nodeName_ == 'DocSeries':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocSeries')
            value_ = self.gds_validate_string(value_, node, 'DocSeries')
            self.DocSeries = value_
            self.DocSeries_nsprefix_ = child_.prefix
            # validate type string-20
            self.validate_string_20(self.DocSeries)
        elif nodeName_ == 'DocNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocNumber')
            value_ = self.gds_validate_string(value_, node, 'DocNumber')
            self.DocNumber = value_
            self.DocNumber_nsprefix_ = child_.prefix
            # validate type string-20
            self.validate_string_20(self.DocNumber)
        elif nodeName_ == 'DocIssueDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DocIssueDate = dval_
            self.DocIssueDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'DocIssued':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DocIssued')
            value_ = self.gds_validate_string(value_, node, 'DocIssued')
            self.DocIssued = value_
            self.DocIssued_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.DocIssued)
        elif nodeName_ == 'DocExpirationDate':
            sval_ = child_.text
            dval_ = self.gds_parse_date(sval_)
            self.DocExpirationDate = dval_
            self.DocExpirationDate_nsprefix_ = child_.prefix


# end class MedicalReportWithoutFilesType


class EduOrganizationType(GeneratedsSuper):
    """Выбранный детский сад"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, code=None, PriorityNumber=None, valueOf_=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.code = _cast(None, code)
        self.code_nsprefix_ = None
        self.PriorityNumber = _cast(int, PriorityNumber)
        self.PriorityNumber_nsprefix_ = None
        self.valueOf_ = valueOf_

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, EduOrganizationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EduOrganizationType.subclass:
            return EduOrganizationType.subclass(*args_, **kwargs_)
        else:
            return EduOrganizationType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code

    def get_PriorityNumber(self):
        return self.PriorityNumber

    def set_PriorityNumber(self, PriorityNumber):
        self.PriorityNumber = PriorityNumber

    def get_valueOf_(self):
        return self.valueOf_

    def set_valueOf_(self, valueOf_):
        self.valueOf_ = valueOf_

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def validate_string_50(self, value):
        # Validate type tns:string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False

    def hasContent_(self):
        if 1 if type(self.valueOf_) in [int, float] else self.valueOf_:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='EduOrganizationType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EduOrganizationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EduOrganizationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EduOrganizationType')
        if self.hasContent_():
            outfile.write('>')
            outfile.write(self.convert_unicode(self.valueOf_))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='EduOrganizationType',
                pretty_print=pretty_print,
            )
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EduOrganizationType'):
        if self.code is not None and 'code' not in already_processed:
            already_processed.add('code')
            outfile.write(
                ' code=%s' % (self.gds_encode(self.gds_format_string(quote_attrib(self.code), input_name='code')),)
            )
        if self.PriorityNumber is not None and 'PriorityNumber' not in already_processed:
            already_processed.add('PriorityNumber')
            outfile.write(
                ' PriorityNumber="%s"' % self.gds_format_integer(self.PriorityNumber, input_name='PriorityNumber')
            )

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='EduOrganizationType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        pass

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        self.valueOf_ = get_all_text_(node)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('code', node)
        if value is not None and 'code' not in already_processed:
            already_processed.add('code')
            self.code = value
            self.validate_string_50(self.code)  # validate type string-50
        value = find_attr_value_('PriorityNumber', node)
        if value is not None and 'PriorityNumber' not in already_processed:
            already_processed.add('PriorityNumber')
            self.PriorityNumber = self.gds_parse_integer(value, node, 'PriorityNumber')

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        pass


# end class EduOrganizationType


class EduOrganizationsType(GeneratedsSuper):
    """Выбранные детские сады"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, EduOrganization=None, AllowOfferOther=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        if EduOrganization is None:
            self.EduOrganization = []
        else:
            self.EduOrganization = EduOrganization
        self.EduOrganization_nsprefix_ = 'tns'
        self.AllowOfferOther = AllowOfferOther
        self.AllowOfferOther_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, EduOrganizationsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if EduOrganizationsType.subclass:
            return EduOrganizationsType.subclass(*args_, **kwargs_)
        else:
            return EduOrganizationsType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_EduOrganization(self):
        return self.EduOrganization

    def set_EduOrganization(self, EduOrganization):
        self.EduOrganization = EduOrganization

    def add_EduOrganization(self, value):
        self.EduOrganization.append(value)

    def insert_EduOrganization_at(self, index, value):
        self.EduOrganization.insert(index, value)

    def replace_EduOrganization_at(self, index, value):
        self.EduOrganization[index] = value

    def get_AllowOfferOther(self):
        return self.AllowOfferOther

    def set_AllowOfferOther(self, AllowOfferOther):
        self.AllowOfferOther = AllowOfferOther

    def hasContent_(self):
        if self.EduOrganization or self.AllowOfferOther is not None:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='EduOrganizationsType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('EduOrganizationsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'EduOrganizationsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='EduOrganizationsType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='EduOrganizationsType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='EduOrganizationsType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='EduOrganizationsType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for EduOrganization_ in self.EduOrganization:
            namespaceprefix_ = (
                self.EduOrganization_nsprefix_ + ':' if (UseCapturedNS_ and self.EduOrganization_nsprefix_) else ''
            )
            EduOrganization_.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='EduOrganization', pretty_print=pretty_print
            )
        if self.AllowOfferOther is not None:
            namespaceprefix_ = (
                self.AllowOfferOther_nsprefix_ + ':' if (UseCapturedNS_ and self.AllowOfferOther_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sAllowOfferOther>%s</%sAllowOfferOther>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_boolean(self.AllowOfferOther, input_name='AllowOfferOther'),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'EduOrganization':
            obj_ = EduOrganizationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EduOrganization.append(obj_)
            obj_.original_tagname_ = 'EduOrganization'
        elif nodeName_ == 'AllowOfferOther':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'AllowOfferOther')
            ival_ = self.gds_validate_boolean(ival_, node, 'AllowOfferOther')
            self.AllowOfferOther = ival_
            self.AllowOfferOther_nsprefix_ = child_.prefix


# end class EduOrganizationsType


class BrotherSisterInfoType(GeneratedsSuper):
    """Сведения об обучении братьев или сестер ребенка в выбранных
    организациях"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        ChildSurname=None,
        ChildName=None,
        ChildMiddleName=None,
        EduOrganization=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.ChildSurname = ChildSurname
        self.validate_string_256(self.ChildSurname)
        self.ChildSurname_nsprefix_ = 'tns'
        self.ChildName = ChildName
        self.validate_string_256(self.ChildName)
        self.ChildName_nsprefix_ = 'tns'
        self.ChildMiddleName = ChildMiddleName
        self.validate_string_256(self.ChildMiddleName)
        self.ChildMiddleName_nsprefix_ = 'tns'
        self.EduOrganization = EduOrganization
        self.EduOrganization_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, BrotherSisterInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BrotherSisterInfoType.subclass:
            return BrotherSisterInfoType.subclass(*args_, **kwargs_)
        else:
            return BrotherSisterInfoType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_ChildSurname(self):
        return self.ChildSurname

    def set_ChildSurname(self, ChildSurname):
        self.ChildSurname = ChildSurname

    def get_ChildName(self):
        return self.ChildName

    def set_ChildName(self, ChildName):
        self.ChildName = ChildName

    def get_ChildMiddleName(self):
        return self.ChildMiddleName

    def set_ChildMiddleName(self, ChildMiddleName):
        self.ChildMiddleName = ChildMiddleName

    def get_EduOrganization(self):
        return self.EduOrganization

    def set_EduOrganization(self, EduOrganization):
        self.EduOrganization = EduOrganization

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.ChildSurname is not None
            or self.ChildName is not None
            or self.ChildMiddleName is not None
            or self.EduOrganization is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='BrotherSisterInfoType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BrotherSisterInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BrotherSisterInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BrotherSisterInfoType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='BrotherSisterInfoType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='BrotherSisterInfoType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='BrotherSisterInfoType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.ChildSurname is not None:
            namespaceprefix_ = (
                self.ChildSurname_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildSurname_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildSurname>%s</%sChildSurname>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.ChildSurname), input_name='ChildSurname')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildName is not None:
            namespaceprefix_ = self.ChildName_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildName>%s</%sChildName>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.ChildName), input_name='ChildName')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.ChildMiddleName is not None:
            namespaceprefix_ = (
                self.ChildMiddleName_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildMiddleName_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sChildMiddleName>%s</%sChildMiddleName>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(
                        self.gds_format_string(quote_xml(self.ChildMiddleName), input_name='ChildMiddleName')
                    ),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.EduOrganization is not None:
            namespaceprefix_ = (
                self.EduOrganization_nsprefix_ + ':' if (UseCapturedNS_ and self.EduOrganization_nsprefix_) else ''
            )
            self.EduOrganization.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='EduOrganization', pretty_print=pretty_print
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'ChildSurname':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildSurname')
            value_ = self.gds_validate_string(value_, node, 'ChildSurname')
            self.ChildSurname = value_
            self.ChildSurname_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildSurname)
        elif nodeName_ == 'ChildName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildName')
            value_ = self.gds_validate_string(value_, node, 'ChildName')
            self.ChildName = value_
            self.ChildName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildName)
        elif nodeName_ == 'ChildMiddleName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ChildMiddleName')
            value_ = self.gds_validate_string(value_, node, 'ChildMiddleName')
            self.ChildMiddleName = value_
            self.ChildMiddleName_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.ChildMiddleName)
        elif nodeName_ == 'EduOrganization':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EduOrganization = obj_
            obj_.original_tagname_ = 'EduOrganization'


# end class BrotherSisterInfoType


class BenefitInfoWithoutFilesType(GeneratedsSuper):
    """Сведения о документе, подтверждающем право на получение мер специальной
    поддержки"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, BenefitCategory=None, BenefitDocInfo=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.BenefitCategory = BenefitCategory
        self.BenefitCategory_nsprefix_ = 'tns'
        self.BenefitDocInfo = BenefitDocInfo
        self.BenefitDocInfo_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, BenefitInfoWithoutFilesType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if BenefitInfoWithoutFilesType.subclass:
            return BenefitInfoWithoutFilesType.subclass(*args_, **kwargs_)
        else:
            return BenefitInfoWithoutFilesType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_BenefitCategory(self):
        return self.BenefitCategory

    def set_BenefitCategory(self, BenefitCategory):
        self.BenefitCategory = BenefitCategory

    def get_BenefitDocInfo(self):
        return self.BenefitDocInfo

    def set_BenefitDocInfo(self, BenefitDocInfo):
        self.BenefitDocInfo = BenefitDocInfo

    def hasContent_(self):
        if self.BenefitCategory is not None or self.BenefitDocInfo is not None:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='BenefitInfoWithoutFilesType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('BenefitInfoWithoutFilesType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'BenefitInfoWithoutFilesType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='BenefitInfoWithoutFilesType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='BenefitInfoWithoutFilesType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(
        self, outfile, level, already_processed, namespaceprefix_='', name_='BenefitInfoWithoutFilesType'
    ):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='BenefitInfoWithoutFilesType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.BenefitCategory is not None:
            namespaceprefix_ = (
                self.BenefitCategory_nsprefix_ + ':' if (UseCapturedNS_ and self.BenefitCategory_nsprefix_) else ''
            )
            self.BenefitCategory.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='BenefitCategory', pretty_print=pretty_print
            )
        if self.BenefitDocInfo is not None:
            namespaceprefix_ = (
                self.BenefitDocInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.BenefitDocInfo_nsprefix_) else ''
            )
            self.BenefitDocInfo.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='BenefitDocInfo', pretty_print=pretty_print
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'BenefitCategory':
            obj_ = DataElementType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BenefitCategory = obj_
            obj_.original_tagname_ = 'BenefitCategory'
        elif nodeName_ == 'BenefitDocInfo':
            obj_ = DocInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BenefitDocInfo = obj_
            obj_.original_tagname_ = 'BenefitDocInfo'


# end class BenefitInfoWithoutFilesType


class ApplicationType(GeneratedsSuper):
    """Данные заявления на запись в дошкольную организацию"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        PersonInfo=None,
        PersonIdentityDocInfo=None,
        ChildInfo=None,
        Address=None,
        EntryParams=None,
        AdaptationProgram=None,
        MedicalReport=None,
        EduOrganizations=None,
        BrotherSisterInfo=None,
        BenefitInfo=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.PersonInfo = PersonInfo
        self.PersonInfo_nsprefix_ = 'tns'
        self.PersonIdentityDocInfo = PersonIdentityDocInfo
        self.PersonIdentityDocInfo_nsprefix_ = 'tns'
        self.ChildInfo = ChildInfo
        self.ChildInfo_nsprefix_ = 'tns'
        self.Address = Address
        self.Address_nsprefix_ = 'tns'
        self.EntryParams = EntryParams
        self.EntryParams_nsprefix_ = 'tns'
        self.AdaptationProgram = AdaptationProgram
        self.AdaptationProgram_nsprefix_ = 'tns'
        self.MedicalReport = MedicalReport
        self.MedicalReport_nsprefix_ = 'tns'
        self.EduOrganizations = EduOrganizations
        self.EduOrganizations_nsprefix_ = 'tns'
        if BrotherSisterInfo is None:
            self.BrotherSisterInfo = []
        else:
            self.BrotherSisterInfo = BrotherSisterInfo
        self.BrotherSisterInfo_nsprefix_ = 'tns'
        self.BenefitInfo = BenefitInfo
        self.BenefitInfo_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, ApplicationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ApplicationType.subclass:
            return ApplicationType.subclass(*args_, **kwargs_)
        else:
            return ApplicationType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_PersonInfo(self):
        return self.PersonInfo

    def set_PersonInfo(self, PersonInfo):
        self.PersonInfo = PersonInfo

    def get_PersonIdentityDocInfo(self):
        return self.PersonIdentityDocInfo

    def set_PersonIdentityDocInfo(self, PersonIdentityDocInfo):
        self.PersonIdentityDocInfo = PersonIdentityDocInfo

    def get_ChildInfo(self):
        return self.ChildInfo

    def set_ChildInfo(self, ChildInfo):
        self.ChildInfo = ChildInfo

    def get_Address(self):
        return self.Address

    def set_Address(self, Address):
        self.Address = Address

    def get_EntryParams(self):
        return self.EntryParams

    def set_EntryParams(self, EntryParams):
        self.EntryParams = EntryParams

    def get_AdaptationProgram(self):
        return self.AdaptationProgram

    def set_AdaptationProgram(self, AdaptationProgram):
        self.AdaptationProgram = AdaptationProgram

    def get_MedicalReport(self):
        return self.MedicalReport

    def set_MedicalReport(self, MedicalReport):
        self.MedicalReport = MedicalReport

    def get_EduOrganizations(self):
        return self.EduOrganizations

    def set_EduOrganizations(self, EduOrganizations):
        self.EduOrganizations = EduOrganizations

    def get_BrotherSisterInfo(self):
        return self.BrotherSisterInfo

    def set_BrotherSisterInfo(self, BrotherSisterInfo):
        self.BrotherSisterInfo = BrotherSisterInfo

    def add_BrotherSisterInfo(self, value):
        self.BrotherSisterInfo.append(value)

    def insert_BrotherSisterInfo_at(self, index, value):
        self.BrotherSisterInfo.insert(index, value)

    def replace_BrotherSisterInfo_at(self, index, value):
        self.BrotherSisterInfo[index] = value

    def get_BenefitInfo(self):
        return self.BenefitInfo

    def set_BenefitInfo(self, BenefitInfo):
        self.BenefitInfo = BenefitInfo

    def hasContent_(self):
        if (
            self.PersonInfo is not None
            or self.PersonIdentityDocInfo is not None
            or self.ChildInfo is not None
            or self.Address is not None
            or self.EntryParams is not None
            or self.AdaptationProgram is not None
            or self.MedicalReport is not None
            or self.EduOrganizations is not None
            or self.BrotherSisterInfo
            or self.BenefitInfo is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='ApplicationType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ApplicationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ApplicationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ApplicationType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile, level + 1, namespaceprefix_, namespacedef_, name_='ApplicationType', pretty_print=pretty_print
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ApplicationType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='ApplicationType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.PersonInfo is not None:
            namespaceprefix_ = self.PersonInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.PersonInfo_nsprefix_) else ''
            self.PersonInfo.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='PersonInfo', pretty_print=pretty_print
            )
        if self.PersonIdentityDocInfo is not None:
            namespaceprefix_ = (
                self.PersonIdentityDocInfo_nsprefix_ + ':'
                if (UseCapturedNS_ and self.PersonIdentityDocInfo_nsprefix_)
                else ''
            )
            self.PersonIdentityDocInfo.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_='',
                name_='PersonIdentityDocInfo',
                pretty_print=pretty_print,
            )
        if self.ChildInfo is not None:
            namespaceprefix_ = self.ChildInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.ChildInfo_nsprefix_) else ''
            self.ChildInfo.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='ChildInfo', pretty_print=pretty_print
            )
        if self.Address is not None:
            namespaceprefix_ = self.Address_nsprefix_ + ':' if (UseCapturedNS_ and self.Address_nsprefix_) else ''
            self.Address.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='Address', pretty_print=pretty_print
            )
        if self.EntryParams is not None:
            namespaceprefix_ = (
                self.EntryParams_nsprefix_ + ':' if (UseCapturedNS_ and self.EntryParams_nsprefix_) else ''
            )
            self.EntryParams.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='EntryParams', pretty_print=pretty_print
            )
        if self.AdaptationProgram is not None:
            namespaceprefix_ = (
                self.AdaptationProgram_nsprefix_ + ':' if (UseCapturedNS_ and self.AdaptationProgram_nsprefix_) else ''
            )
            self.AdaptationProgram.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='AdaptationProgram', pretty_print=pretty_print
            )
        if self.MedicalReport is not None:
            namespaceprefix_ = (
                self.MedicalReport_nsprefix_ + ':' if (UseCapturedNS_ and self.MedicalReport_nsprefix_) else ''
            )
            self.MedicalReport.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='MedicalReport', pretty_print=pretty_print
            )
        if self.EduOrganizations is not None:
            namespaceprefix_ = (
                self.EduOrganizations_nsprefix_ + ':' if (UseCapturedNS_ and self.EduOrganizations_nsprefix_) else ''
            )
            self.EduOrganizations.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='EduOrganizations', pretty_print=pretty_print
            )
        for BrotherSisterInfo_ in self.BrotherSisterInfo:
            namespaceprefix_ = (
                self.BrotherSisterInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.BrotherSisterInfo_nsprefix_) else ''
            )
            BrotherSisterInfo_.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='BrotherSisterInfo', pretty_print=pretty_print
            )
        if self.BenefitInfo is not None:
            namespaceprefix_ = (
                self.BenefitInfo_nsprefix_ + ':' if (UseCapturedNS_ and self.BenefitInfo_nsprefix_) else ''
            )
            self.BenefitInfo.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='BenefitInfo', pretty_print=pretty_print
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'PersonInfo':
            obj_ = PersonInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonInfo = obj_
            obj_.original_tagname_ = 'PersonInfo'
        elif nodeName_ == 'PersonIdentityDocInfo':
            obj_ = PersonIdentityDocInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.PersonIdentityDocInfo = obj_
            obj_.original_tagname_ = 'PersonIdentityDocInfo'
        elif nodeName_ == 'ChildInfo':
            obj_ = ChildInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.ChildInfo = obj_
            obj_.original_tagname_ = 'ChildInfo'
        elif nodeName_ == 'Address':
            obj_ = AddressType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.Address = obj_
            obj_.original_tagname_ = 'Address'
        elif nodeName_ == 'EntryParams':
            obj_ = EntryParamsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EntryParams = obj_
            obj_.original_tagname_ = 'EntryParams'
        elif nodeName_ == 'AdaptationProgram':
            obj_ = AdaptationProgramType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AdaptationProgram = obj_
            obj_.original_tagname_ = 'AdaptationProgram'
        elif nodeName_ == 'MedicalReport':
            obj_ = MedicalReportWithoutFilesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.MedicalReport = obj_
            obj_.original_tagname_ = 'MedicalReport'
        elif nodeName_ == 'EduOrganizations':
            obj_ = EduOrganizationsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.EduOrganizations = obj_
            obj_.original_tagname_ = 'EduOrganizations'
        elif nodeName_ == 'BrotherSisterInfo':
            obj_ = BrotherSisterInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BrotherSisterInfo.append(obj_)
            obj_.original_tagname_ = 'BrotherSisterInfo'
        elif nodeName_ == 'BenefitInfo':
            obj_ = BenefitInfoWithoutFilesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.BenefitInfo = obj_
            obj_.original_tagname_ = 'BenefitInfo'


# end class ApplicationType


class statusCodeType(GeneratedsSuper):
    """Статус заявления"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, orgCode=None, techCode=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.orgCode = orgCode
        self.validate_string_50(self.orgCode)
        self.orgCode_nsprefix_ = 'tns'
        self.techCode = techCode
        self.techCode_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, statusCodeType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if statusCodeType.subclass:
            return statusCodeType.subclass(*args_, **kwargs_)
        else:
            return statusCodeType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_orgCode(self):
        return self.orgCode

    def set_orgCode(self, orgCode):
        self.orgCode = orgCode

    def get_techCode(self):
        return self.techCode

    def set_techCode(self, techCode):
        self.techCode = techCode

    def validate_string_50(self, value):
        result = True
        # Validate type string-50, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 50:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-50'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if self.orgCode is not None or self.techCode is not None:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='statusCodeType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('statusCodeType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'statusCodeType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='statusCodeType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile, level + 1, namespaceprefix_, namespacedef_, name_='statusCodeType', pretty_print=pretty_print
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='statusCodeType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='statusCodeType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orgCode is not None:
            namespaceprefix_ = self.orgCode_nsprefix_ + ':' if (UseCapturedNS_ and self.orgCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sorgCode>%s</%sorgCode>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.orgCode), input_name='orgCode')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.techCode is not None:
            namespaceprefix_ = self.techCode_nsprefix_ + ':' if (UseCapturedNS_ and self.techCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%stechCode>%s</%stechCode>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_integer(self.techCode, input_name='techCode'),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orgCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'orgCode')
            value_ = self.gds_validate_string(value_, node, 'orgCode')
            self.orgCode = value_
            self.orgCode_nsprefix_ = child_.prefix
            # validate type string-50
            self.validate_string_50(self.orgCode)
        elif nodeName_ == 'techCode' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'techCode')
            ival_ = self.gds_validate_integer(ival_, node, 'techCode')
            self.techCode = ival_
            self.techCode_nsprefix_ = child_.prefix


# end class statusCodeType


class statusHistoryType(GeneratedsSuper):
    """Статус по заявлению"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self, statusCode=None, statusDate=None, statusComment=None, cancelAllowed=None, gds_collector_=None, **kwargs_
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.statusCode = statusCode
        self.statusCode_nsprefix_ = 'tns'
        if isinstance(statusDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(statusDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = statusDate
        self.statusDate = initvalue_
        self.statusDate_nsprefix_ = 'tns'
        self.statusComment = statusComment
        self.validate_string_4000(self.statusComment)
        self.statusComment_nsprefix_ = 'tns'
        self.cancelAllowed = cancelAllowed
        self.cancelAllowed_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, statusHistoryType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if statusHistoryType.subclass:
            return statusHistoryType.subclass(*args_, **kwargs_)
        else:
            return statusHistoryType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_statusCode(self):
        return self.statusCode

    def set_statusCode(self, statusCode):
        self.statusCode = statusCode

    def get_statusDate(self):
        return self.statusDate

    def set_statusDate(self, statusDate):
        self.statusDate = statusDate

    def get_statusComment(self):
        return self.statusComment

    def set_statusComment(self, statusComment):
        self.statusComment = statusComment

    def get_cancelAllowed(self):
        return self.cancelAllowed

    def set_cancelAllowed(self, cancelAllowed):
        self.cancelAllowed = cancelAllowed

    def validate_string_4000(self, value):
        result = True
        # Validate type string-4000, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 4000:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-4000'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.statusCode is not None
            or self.statusDate is not None
            or self.statusComment is not None
            or self.cancelAllowed is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='statusHistoryType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('statusHistoryType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'statusHistoryType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='statusHistoryType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='statusHistoryType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='statusHistoryType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='statusHistoryType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.statusCode is not None:
            namespaceprefix_ = self.statusCode_nsprefix_ + ':' if (UseCapturedNS_ and self.statusCode_nsprefix_) else ''
            self.statusCode.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='statusCode', pretty_print=pretty_print
            )
        if self.statusDate is not None:
            namespaceprefix_ = self.statusDate_nsprefix_ + ':' if (UseCapturedNS_ and self.statusDate_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sstatusDate>%s</%sstatusDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_datetime(self.statusDate, input_name='statusDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.statusComment is not None:
            namespaceprefix_ = (
                self.statusComment_nsprefix_ + ':' if (UseCapturedNS_ and self.statusComment_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sstatusComment>%s</%sstatusComment>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.statusComment), input_name='statusComment')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.cancelAllowed is not None:
            namespaceprefix_ = (
                self.cancelAllowed_nsprefix_ + ':' if (UseCapturedNS_ and self.cancelAllowed_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%scancelAllowed>%s</%scancelAllowed>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_boolean(self.cancelAllowed, input_name='cancelAllowed'),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'statusCode':
            obj_ = statusCodeType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.statusCode = obj_
            obj_.original_tagname_ = 'statusCode'
        elif nodeName_ == 'statusDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.statusDate = dval_
            self.statusDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'statusComment':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'statusComment')
            value_ = self.gds_validate_string(value_, node, 'statusComment')
            self.statusComment = value_
            self.statusComment_nsprefix_ = child_.prefix
            # validate type string-4000
            self.validate_string_4000(self.statusComment)
        elif nodeName_ == 'cancelAllowed':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'cancelAllowed')
            ival_ = self.gds_validate_boolean(ival_, node, 'cancelAllowed')
            self.cancelAllowed = ival_
            self.cancelAllowed_nsprefix_ = child_.prefix


# end class statusHistoryType


class statusHistoryListType(GeneratedsSuper):
    """Заявления"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, statusHistory=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        if statusHistory is None:
            self.statusHistory = []
        else:
            self.statusHistory = statusHistory
        self.statusHistory_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, statusHistoryListType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if statusHistoryListType.subclass:
            return statusHistoryListType.subclass(*args_, **kwargs_)
        else:
            return statusHistoryListType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_statusHistory(self):
        return self.statusHistory

    def set_statusHistory(self, statusHistory):
        self.statusHistory = statusHistory

    def add_statusHistory(self, value):
        self.statusHistory.append(value)

    def insert_statusHistory_at(self, index, value):
        self.statusHistory.insert(index, value)

    def replace_statusHistory_at(self, index, value):
        self.statusHistory[index] = value

    def hasContent_(self):
        if self.statusHistory:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='statusHistoryListType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('statusHistoryListType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'statusHistoryListType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='statusHistoryListType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='statusHistoryListType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='statusHistoryListType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='statusHistoryListType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for statusHistory_ in self.statusHistory:
            namespaceprefix_ = (
                self.statusHistory_nsprefix_ + ':' if (UseCapturedNS_ and self.statusHistory_nsprefix_) else ''
            )
            statusHistory_.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='statusHistory', pretty_print=pretty_print
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'statusHistory':
            obj_ = statusHistoryType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.statusHistory.append(obj_)
            obj_.original_tagname_ = 'statusHistory'


# end class statusHistoryListType


class CreateOrderRequestType(GeneratedsSuper):
    """Заявление"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(
        self,
        orderId_InfoRequest=None,
        requestDate=None,
        statusHistoryList=None,
        application=None,
        gds_collector_=None,
        **kwargs_,
    ):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.orderId_InfoRequest = orderId_InfoRequest
        self.orderId_InfoRequest_nsprefix_ = 'tns'
        if isinstance(requestDate, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(requestDate, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = requestDate
        self.requestDate = initvalue_
        self.requestDate_nsprefix_ = 'tns'
        self.statusHistoryList = statusHistoryList
        self.statusHistoryList_nsprefix_ = 'tns'
        self.application = application
        self.application_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, CreateOrderRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CreateOrderRequestType.subclass:
            return CreateOrderRequestType.subclass(*args_, **kwargs_)
        else:
            return CreateOrderRequestType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_orderId_InfoRequest(self):
        return self.orderId_InfoRequest

    def set_orderId_InfoRequest(self, orderId_InfoRequest):
        self.orderId_InfoRequest = orderId_InfoRequest

    def get_requestDate(self):
        return self.requestDate

    def set_requestDate(self, requestDate):
        self.requestDate = requestDate

    def get_statusHistoryList(self):
        return self.statusHistoryList

    def set_statusHistoryList(self, statusHistoryList):
        self.statusHistoryList = statusHistoryList

    def get_application(self):
        return self.application

    def set_application(self, application):
        self.application = application

    def hasContent_(self):
        if (
            self.orderId_InfoRequest is not None
            or self.requestDate is not None
            or self.statusHistoryList is not None
            or self.application is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='CreateOrderRequestType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CreateOrderRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CreateOrderRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreateOrderRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='CreateOrderRequestType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CreateOrderRequestType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='CreateOrderRequestType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId_InfoRequest is not None:
            namespaceprefix_ = (
                self.orderId_InfoRequest_nsprefix_ + ':'
                if (UseCapturedNS_ and self.orderId_InfoRequest_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sorderId_InfoRequest>%s</%sorderId_InfoRequest>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_integer(self.orderId_InfoRequest, input_name='orderId_InfoRequest'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.requestDate is not None:
            namespaceprefix_ = (
                self.requestDate_nsprefix_ + ':' if (UseCapturedNS_ and self.requestDate_nsprefix_) else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%srequestDate>%s</%srequestDate>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_datetime(self.requestDate, input_name='requestDate'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.statusHistoryList is not None:
            namespaceprefix_ = (
                self.statusHistoryList_nsprefix_ + ':' if (UseCapturedNS_ and self.statusHistoryList_nsprefix_) else ''
            )
            self.statusHistoryList.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='statusHistoryList', pretty_print=pretty_print
            )
        if self.application is not None:
            namespaceprefix_ = (
                self.application_nsprefix_ + ':' if (UseCapturedNS_ and self.application_nsprefix_) else ''
            )
            self.application.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='application', pretty_print=pretty_print
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId_InfoRequest' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId_InfoRequest')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId_InfoRequest')
            self.orderId_InfoRequest = ival_
            self.orderId_InfoRequest_nsprefix_ = child_.prefix
        elif nodeName_ == 'requestDate':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.requestDate = dval_
            self.requestDate_nsprefix_ = child_.prefix
        elif nodeName_ == 'statusHistoryList':
            obj_ = statusHistoryListType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.statusHistoryList = obj_
            obj_.original_tagname_ = 'statusHistoryList'
        elif nodeName_ == 'application':
            obj_ = ApplicationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.application = obj_
            obj_.original_tagname_ = 'application'


# end class CreateOrderRequestType


class UpdateOrderRequestType(GeneratedsSuper):
    """Заявление"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, orderId=None, statusHistoryList=None, application=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.orderId = orderId
        self.orderId_nsprefix_ = 'tns'
        self.statusHistoryList = statusHistoryList
        self.statusHistoryList_nsprefix_ = 'tns'
        self.application = application
        self.application_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, UpdateOrderRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UpdateOrderRequestType.subclass:
            return UpdateOrderRequestType.subclass(*args_, **kwargs_)
        else:
            return UpdateOrderRequestType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_orderId(self):
        return self.orderId

    def set_orderId(self, orderId):
        self.orderId = orderId

    def get_statusHistoryList(self):
        return self.statusHistoryList

    def set_statusHistoryList(self, statusHistoryList):
        self.statusHistoryList = statusHistoryList

    def get_application(self):
        return self.application

    def set_application(self, application):
        self.application = application

    def hasContent_(self):
        if self.orderId is not None or self.statusHistoryList is not None or self.application is not None:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='UpdateOrderRequestType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UpdateOrderRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UpdateOrderRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UpdateOrderRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='UpdateOrderRequestType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UpdateOrderRequestType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='UpdateOrderRequestType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sorderId>%s</%sorderId>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_integer(self.orderId, input_name='orderId'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.statusHistoryList is not None:
            namespaceprefix_ = (
                self.statusHistoryList_nsprefix_ + ':' if (UseCapturedNS_ and self.statusHistoryList_nsprefix_) else ''
            )
            self.statusHistoryList.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='statusHistoryList', pretty_print=pretty_print
            )
        if self.application is not None:
            namespaceprefix_ = (
                self.application_nsprefix_ + ':' if (UseCapturedNS_ and self.application_nsprefix_) else ''
            )
            self.application.export(
                outfile, level, namespaceprefix_, namespacedef_='', name_='application', pretty_print=pretty_print
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix
        elif nodeName_ == 'statusHistoryList':
            obj_ = statusHistoryListType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.statusHistoryList = obj_
            obj_.original_tagname_ = 'statusHistoryList'
        elif nodeName_ == 'application':
            obj_ = ApplicationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.application = obj_
            obj_.original_tagname_ = 'application'


# end class UpdateOrderRequestType


class OrderRequestType(GeneratedsSuper):
    """Запрос"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, env=None, CreateOrderRequest=None, UpdateOrderRequest=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.env = _cast(None, env)
        self.env_nsprefix_ = None
        self.CreateOrderRequest = CreateOrderRequest
        self.CreateOrderRequest_nsprefix_ = 'tns'
        self.UpdateOrderRequest = UpdateOrderRequest
        self.UpdateOrderRequest_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, OrderRequestType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OrderRequestType.subclass:
            return OrderRequestType.subclass(*args_, **kwargs_)
        else:
            return OrderRequestType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_CreateOrderRequest(self):
        return self.CreateOrderRequest

    def set_CreateOrderRequest(self, CreateOrderRequest):
        self.CreateOrderRequest = CreateOrderRequest

    def get_UpdateOrderRequest(self):
        return self.UpdateOrderRequest

    def set_UpdateOrderRequest(self, UpdateOrderRequest):
        self.UpdateOrderRequest = UpdateOrderRequest

    def get_env(self):
        return self.env

    def set_env(self, env):
        self.env = env

    def validate_EnvType(self, value):
        # Validate type tns:EnvType, a restriction on tns:string-16.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            value = value
            enumerations = ['EPGU', 'DEV', 'UAT', 'EXUAT', 'SVCDEV', 'TCOD']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on EnvType'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
            if len(value) > 16:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EnvType'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False

    def hasContent_(self):
        if self.CreateOrderRequest is not None or self.UpdateOrderRequest is not None:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='OrderRequestType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OrderRequestType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OrderRequestType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OrderRequestType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile, level + 1, namespaceprefix_, namespacedef_, name_='OrderRequestType', pretty_print=pretty_print
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OrderRequestType'):
        if self.env is not None and 'env' not in already_processed:
            already_processed.add('env')
            outfile.write(' env=%s' % (quote_attrib(self.env),))

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='OrderRequestType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CreateOrderRequest is not None:
            namespaceprefix_ = (
                self.CreateOrderRequest_nsprefix_ + ':'
                if (UseCapturedNS_ and self.CreateOrderRequest_nsprefix_)
                else ''
            )
            self.CreateOrderRequest.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_='',
                name_='CreateOrderRequest',
                pretty_print=pretty_print,
            )
        if self.UpdateOrderRequest is not None:
            namespaceprefix_ = (
                self.UpdateOrderRequest_nsprefix_ + ':'
                if (UseCapturedNS_ and self.UpdateOrderRequest_nsprefix_)
                else ''
            )
            self.UpdateOrderRequest.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_='',
                name_='UpdateOrderRequest',
                pretty_print=pretty_print,
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        value = find_attr_value_('env', node)
        if value is not None and 'env' not in already_processed:
            already_processed.add('env')
            self.env = value
            self.validate_EnvType(self.env)  # validate type EnvType

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CreateOrderRequest':
            obj_ = CreateOrderRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CreateOrderRequest = obj_
            obj_.original_tagname_ = 'CreateOrderRequest'
        elif nodeName_ == 'UpdateOrderRequest':
            obj_ = UpdateOrderRequestType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UpdateOrderRequest = obj_
            obj_.original_tagname_ = 'UpdateOrderRequest'


# end class OrderRequestType


class CreateOrderResponseType(GeneratedsSuper):
    """Ответ на создание заявления"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, code=None, message=None, orderId_InfoRequest=None, orderId=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.code = code
        self.code_nsprefix_ = 'tns'
        self.message = message
        self.validate_string_256(self.message)
        self.message_nsprefix_ = 'tns'
        self.orderId_InfoRequest = orderId_InfoRequest
        self.orderId_InfoRequest_nsprefix_ = 'tns'
        self.orderId = orderId
        self.orderId_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, CreateOrderResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if CreateOrderResponseType.subclass:
            return CreateOrderResponseType.subclass(*args_, **kwargs_)
        else:
            return CreateOrderResponseType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message

    def get_orderId_InfoRequest(self):
        return self.orderId_InfoRequest

    def set_orderId_InfoRequest(self, orderId_InfoRequest):
        self.orderId_InfoRequest = orderId_InfoRequest

    def get_orderId(self):
        return self.orderId

    def set_orderId(self, orderId):
        self.orderId = orderId

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if (
            self.code is not None
            or self.message is not None
            or self.orderId_InfoRequest is not None
            or self.orderId is not None
        ):
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='CreateOrderResponseType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('CreateOrderResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'CreateOrderResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='CreateOrderResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='CreateOrderResponseType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='CreateOrderResponseType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='CreateOrderResponseType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.code is not None:
            namespaceprefix_ = self.code_nsprefix_ + ':' if (UseCapturedNS_ and self.code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%scode>%s</%scode>%s'
                % (namespaceprefix_, self.gds_format_integer(self.code, input_name='code'), namespaceprefix_, eol_)
            )
        if self.message is not None:
            namespaceprefix_ = self.message_nsprefix_ + ':' if (UseCapturedNS_ and self.message_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%smessage>%s</%smessage>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.message), input_name='message')),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.orderId_InfoRequest is not None:
            namespaceprefix_ = (
                self.orderId_InfoRequest_nsprefix_ + ':'
                if (UseCapturedNS_ and self.orderId_InfoRequest_nsprefix_)
                else ''
            )
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sorderId_InfoRequest>%s</%sorderId_InfoRequest>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_integer(self.orderId_InfoRequest, input_name='orderId_InfoRequest'),
                    namespaceprefix_,
                    eol_,
                )
            )
        if self.orderId is not None:
            namespaceprefix_ = self.orderId_nsprefix_ + ':' if (UseCapturedNS_ and self.orderId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%sorderId>%s</%sorderId>%s'
                % (
                    namespaceprefix_,
                    self.gds_format_integer(self.orderId, input_name='orderId'),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'code' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'code')
            ival_ = self.gds_validate_integer(ival_, node, 'code')
            self.code = ival_
            self.code_nsprefix_ = child_.prefix
        elif nodeName_ == 'message':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'message')
            value_ = self.gds_validate_string(value_, node, 'message')
            self.message = value_
            self.message_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.message)
        elif nodeName_ == 'orderId_InfoRequest' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId_InfoRequest')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId_InfoRequest')
            self.orderId_InfoRequest = ival_
            self.orderId_InfoRequest_nsprefix_ = child_.prefix
        elif nodeName_ == 'orderId' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'orderId')
            ival_ = self.gds_validate_integer(ival_, node, 'orderId')
            self.orderId = ival_
            self.orderId_nsprefix_ = child_.prefix


# end class CreateOrderResponseType


class UpdateOrderResponseType(GeneratedsSuper):
    """Ответ на изменение заявления"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, code=None, message=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.code = code
        self.code_nsprefix_ = 'tns'
        self.message = message
        self.validate_string_256(self.message)
        self.message_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, UpdateOrderResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if UpdateOrderResponseType.subclass:
            return UpdateOrderResponseType.subclass(*args_, **kwargs_)
        else:
            return UpdateOrderResponseType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message

    def validate_string_256(self, value):
        result = True
        # Validate type string-256, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s is not of the correct base simple type (str)'
                    % {
                        'value': value,
                        'lineno': lineno,
                    }
                )
                return False
            if len(value) > 256:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message(
                    'Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on string-256'
                    % {'value': encode_str_2_3(value), 'lineno': lineno}
                )
                result = False
        return result

    def hasContent_(self):
        if self.code is not None or self.message is not None:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='UpdateOrderResponseType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('UpdateOrderResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'UpdateOrderResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='UpdateOrderResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='UpdateOrderResponseType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='UpdateOrderResponseType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='UpdateOrderResponseType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.code is not None:
            namespaceprefix_ = self.code_nsprefix_ + ':' if (UseCapturedNS_ and self.code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%scode>%s</%scode>%s'
                % (namespaceprefix_, self.gds_format_integer(self.code, input_name='code'), namespaceprefix_, eol_)
            )
        if self.message is not None:
            namespaceprefix_ = self.message_nsprefix_ + ':' if (UseCapturedNS_ and self.message_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write(
                '<%smessage>%s</%smessage>%s'
                % (
                    namespaceprefix_,
                    self.gds_encode(self.gds_format_string(quote_xml(self.message), input_name='message')),
                    namespaceprefix_,
                    eol_,
                )
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'code' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'code')
            ival_ = self.gds_validate_integer(ival_, node, 'code')
            self.code = ival_
            self.code_nsprefix_ = child_.prefix
        elif nodeName_ == 'message':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'message')
            value_ = self.gds_validate_string(value_, node, 'message')
            self.message = value_
            self.message_nsprefix_ = child_.prefix
            # validate type string-256
            self.validate_string_256(self.message)


# end class UpdateOrderResponseType


class OrderResponseType(GeneratedsSuper):
    """Ответ"""

    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None

    def __init__(self, CreateOrderResponse=None, UpdateOrderResponse=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = 'tns'
        self.CreateOrderResponse = CreateOrderResponse
        self.CreateOrderResponse_nsprefix_ = 'tns'
        self.UpdateOrderResponse = UpdateOrderResponse
        self.UpdateOrderResponse_nsprefix_ = 'tns'

    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(CurrentSubclassModule_, OrderResponseType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if OrderResponseType.subclass:
            return OrderResponseType.subclass(*args_, **kwargs_)
        else:
            return OrderResponseType(*args_, **kwargs_)

    factory = staticmethod(factory)

    def get_ns_prefix_(self):
        return self.ns_prefix_

    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix

    def get_CreateOrderResponse(self):
        return self.CreateOrderResponse

    def set_CreateOrderResponse(self, CreateOrderResponse):
        self.CreateOrderResponse = CreateOrderResponse

    def get_UpdateOrderResponse(self):
        return self.UpdateOrderResponse

    def set_UpdateOrderResponse(self, UpdateOrderResponse):
        self.UpdateOrderResponse = UpdateOrderResponse

    def hasContent_(self):
        if self.CreateOrderResponse is not None or self.UpdateOrderResponse is not None:
            return True
        else:
            return False

    def export(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='OrderResponseType',
        pretty_print=True,
    ):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('OrderResponseType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'OrderResponseType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write(
            '<%s%s%s'
            % (
                namespaceprefix_,
                name_,
                namespacedef_ and ' ' + namespacedef_ or '',
            )
        )
        already_processed = set()
        self.exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='OrderResponseType')
        if self.hasContent_():
            outfile.write('>%s' % (eol_,))
            self.exportChildren(
                outfile,
                level + 1,
                namespaceprefix_,
                namespacedef_,
                name_='OrderResponseType',
                pretty_print=pretty_print,
            )
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_,))

    def exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='OrderResponseType'):
        pass

    def exportChildren(
        self,
        outfile,
        level,
        namespaceprefix_='',
        namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        name_='OrderResponseType',
        fromsubclass_=False,
        pretty_print=True,
    ):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.CreateOrderResponse is not None:
            namespaceprefix_ = (
                self.CreateOrderResponse_nsprefix_ + ':'
                if (UseCapturedNS_ and self.CreateOrderResponse_nsprefix_)
                else ''
            )
            self.CreateOrderResponse.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_='',
                name_='CreateOrderResponse',
                pretty_print=pretty_print,
            )
        if self.UpdateOrderResponse is not None:
            namespaceprefix_ = (
                self.UpdateOrderResponse_nsprefix_ + ':'
                if (UseCapturedNS_ and self.UpdateOrderResponse_nsprefix_)
                else ''
            )
            self.UpdateOrderResponse.export(
                outfile,
                level,
                namespaceprefix_,
                namespacedef_='',
                name_='UpdateOrderResponse',
                pretty_print=pretty_print,
            )

    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self

    def buildAttributes(self, node, attrs, already_processed):
        pass

    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'CreateOrderResponse':
            obj_ = CreateOrderResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.CreateOrderResponse = obj_
            obj_.original_tagname_ = 'CreateOrderResponse'
        elif nodeName_ == 'UpdateOrderResponse':
            obj_ = UpdateOrderResponseType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.UpdateOrderResponse = obj_
            obj_.original_tagname_ = 'UpdateOrderResponse'


# end class OrderResponseType


GDSClassesMapping = {
    'OrderRequest': OrderRequestType,
    'OrderResponse': OrderResponseType,
}


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = GDSClassesMapping.get(tag)
    if rootClass is None:
        rootClass = globals().get(tag)
    return tag, rootClass


def get_required_ns_prefix_defs(rootNode):
    """Get all name space prefix definitions required in this XML doc.
    Return a dictionary of definitions and a char string of definitions.
    """
    nsmap = {prefix: uri for node in rootNode.iter() for (prefix, uri) in node.nsmap.items() if prefix is not None}
    namespacedefs = ' '.join(['xmlns:{}="{}"'.format(prefix, uri) for prefix, uri in nsmap.items()])
    return nsmap, namespacedefs


def parse(inFileName, silence=False, print_warnings=True):
    global CapturedNsmap_
    gds_collector = GdsCollector_()
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DataElementType'
        rootClass = DataElementType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(sys.stdout, 0, name_=rootTag, namespacedef_=namespacedefs, pretty_print=True)
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write(
            '----- Warnings -- count: {} -----\n'.format(
                len(gds_collector.get_messages()),
            )
        )
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseEtree(inFileName, silence=False, print_warnings=True, mapping=None, nsmap=None):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DataElementType'
        rootClass = DataElementType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if mapping is None:
        mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping, nsmap_=nsmap)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(rootElement, pretty_print=True, xml_declaration=True, encoding='utf-8')
        sys.stdout.write(str(content))
        sys.stdout.write('\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write(
            '----- Warnings -- count: {} -----\n'.format(
                len(gds_collector.get_messages()),
            )
        )
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False, print_warnings=True):
    """Parse a string, create the object tree, and export it.

    Arguments:
    - inString -- A string.  This XML fragment should not start
      with an XML declaration containing an encoding.
    - silence -- A boolean.  If False, export the object.
    Returns -- The root object in the tree.
    """
    parser = None
    rootNode = parsexmlstring_(inString, parser)
    gds_collector = GdsCollector_()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DataElementType'
        rootClass = DataElementType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout,
            0,
            name_=rootTag,
            namespacedef_='xmlns:tns="http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0"',
        )
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write(
            '----- Warnings -- count: {} -----\n'.format(
                len(gds_collector.get_messages()),
            )
        )
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseLiteral(inFileName, silence=False, print_warnings=True):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DataElementType'
        rootClass = DataElementType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from kinder_order import *\n\n')
        sys.stdout.write('import kinder_order as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write(
            '----- Warnings -- count: {} -----\n'.format(
                len(gds_collector.get_messages()),
            )
        )
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    # import pdb; pdb.set_trace()
    main()

RenameMappings_ = {}

#
# Mapping of namespaces to types defined in them
# and the file in which each is defined.
# simpleTypes are marked "ST" and complexTypes "CT".
NamespaceToDefMappings_ = {
    'http://epgu.gosuslugi.ru/concentrator/kindergarten-order/1.0.0': [
        ('string-6', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        ('string-10', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        ('string-14', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        ('string-16', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        ('string-20', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        ('string-21', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        ('string-50', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        ('string-256', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        ('string-1024', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        ('string-4000', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        ('EnvType', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'ST'),
        (
            'DataElementType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        ('DocInfoType', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'CT'),
        ('PersonInfoType', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'CT'),
        (
            'OtherRepresentativeType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'PersonIdentityDocInfoType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        ('ChildInfoType', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'CT'),
        (
            'ChildBirthDocRFType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'ChildBirthDocForeignType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        ('AddressType', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'CT'),
        (
            'EntryParamsType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'AdaptationProgramType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'MedicalReportWithoutFilesType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'EduOrganizationType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'EduOrganizationsType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'BrotherSisterInfoType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'BenefitInfoWithoutFilesType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'ApplicationType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        ('statusCodeType', '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd', 'CT'),
        (
            'statusHistoryType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'statusHistoryListType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'CreateOrderRequestType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'UpdateOrderRequestType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'OrderRequestType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'CreateOrderResponseType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'UpdateOrderResponseType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
        (
            'OrderResponseType',
            '../concentrator/src/concentrator/smev3_v321/templates/schema/kindergarten-order.xsd',
            'CT',
        ),
    ]
}

__all__ = [
    'AdaptationProgramType',
    'AddressType',
    'ApplicationType',
    'BenefitInfoWithoutFilesType',
    'BrotherSisterInfoType',
    'ChildBirthDocForeignType',
    'ChildBirthDocRFType',
    'ChildInfoType',
    'CreateOrderRequestType',
    'CreateOrderResponseType',
    'DataElementType',
    'DocInfoType',
    'EduOrganizationType',
    'EduOrganizationsType',
    'EntryParamsType',
    'MedicalReportWithoutFilesType',
    'OrderRequestType',
    'OrderResponseType',
    'OtherRepresentativeType',
    'PersonIdentityDocInfoType',
    'PersonInfoType',
    'UpdateOrderRequestType',
    'UpdateOrderResponseType',
    'statusCodeType',
    'statusHistoryListType',
    'statusHistoryType',
]
