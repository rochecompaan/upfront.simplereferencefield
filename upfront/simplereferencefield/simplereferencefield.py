# -*- coding: utf-8 -*-
#
# Copyright (c) 2009 by Upfront Systems
#
# GNU General Public License (GPL)
#

__author__ = """Roché Compaan <roche@upfrontsystems.co.za>"""
__docformat__ = 'plaintext'

from types import ListType, TupleType
from zope.interface import implements
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import Field, ObjectField, \
    ReferenceWidget, AnnotationStorage
from Products.Archetypes.utils import shasattr
from Products.Archetypes.Field import STRING_TYPES
from Products.Archetypes.config import REFERENCE_CATALOG
from interfaces import ISimpleReferenceField

class SimpleReferenceField(ObjectField):
    """ A reference field that simply stores UIDs on the object
    """
    security = ClassSecurityInfo()

    implements(ISimpleReferenceField)

    _properties = Field._properties.copy()
    _properties.update({
        'type': 'simplereference',
        'default': None,
        'widget': ReferenceWidget,
        'storage': AnnotationStorage(),
        'relationship': None, # required
        'set_backreference': True,
        })


    security.declarePrivate('get')
    def get(self, instance, aslist=False, **kwargs):
        objects = []
        rc = getToolByName(instance, REFERENCE_CATALOG)
        uids = ObjectField.get(self, instance, **kwargs)

        if uids is None:
            uids = []

        for uid in uids:
            if uid:
                objects.append(rc.lookupObject(uid))

        if objects:
            if not self.multiValued:
                return objects[0]
            else:
                return objects

        return []

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        if value is None:
            value = ()

        if not isinstance(value, (ListType, TupleType)):
            value = value,
        elif not self.multiValued and len(value) > 1:
            raise ValueError, \
                  "Multiple values given for single valued field %r" % self

        # Convert objects to uids if necessary. Compute new references
        # as well.
        original_uids = []
        if not kwargs.get('_initializing_'):
            original_uids = self.getRaw(instance, aslist=True)
        new_uids = []
        uids = []
        for v in value:
            if type(v) in STRING_TYPES:
                uid = v
            else:
                uid = v.UID()

            # Update lists
            if uid not in original_uids:
                new_uids.append(uid)                
            if uid not in uids:
                uids.append(uid)

        ObjectField.set(self, instance, uids)

        if not self.set_backreference or kwargs.get('backref'):
            return
       
        # Maintain back references
        if kwargs.get('_initializing_'):
            return

        # Compute removed references
        removed_uids = set(original_uids) - set(uids)

        # Scan the target portal type for a field with a matching
        # relationship

        backref_field_map = {}
        def get_backref_field(ob):

            def filter_function(f):
                return (f.type in ('reference', 'simplereference')) \
                    and (f.relationship == self.relationship)

            portal_type = ob.portal_type
            field = None
            if backref_field_map.has_key(self.relationship):
                field = backref_field_map[self.relationship]
            else:
                fields = ob.Schema().filterFields(filter_function)
                if fields:
                    field = fields[0]
                    backref_field_map[self.relationship] = field
            return field

        rc = getToolByName(instance, REFERENCE_CATALOG)

        # Set new back references
        for uid in new_uids:        
            ob = rc.lookupObject(uid)
            field = get_backref_field(ob)
            if field is not None:
                field.set(
                    ob,                     
                    list(field.getRaw(ob, aslist=True)+[instance.UID()]),
                    backref=True,
                )

        # Remove old back references
        for uid in removed_uids:
            ob = rc.lookupObject(uid)
            field = get_backref_field(ob)
            if field is not None:
                field.set(
                    ob, 
                    list(set(field.getRaw(ob, aslist=True)) - 
                         set([instance.UID()])),
                    backref=True,
                )


    security.declarePrivate('getRaw')
    def getRaw(self, instance, aslist=False, **kwargs):
        """Return the list of UIDs referenced under this fields
        relationship
        """
        objects = []
        uids = ObjectField.get(self, instance, **kwargs)

        if uids is None:
            uids = []

        if not self.multiValued and not aslist:
            if uids:
                uids = uids[0]
            else:
                uids = None
        return uids
