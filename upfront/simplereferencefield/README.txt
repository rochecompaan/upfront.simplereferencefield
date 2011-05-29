simplereferencefield is an Archeteyps reference field implementation
that stores the references directly on the object without indexing it in
the reference_catalog.

Create a document that references news.

  >>> self.loginAsPortalOwner()
  >>> self.portal.invokeFactory('Document', 'doc1')
  'doc1'
  >>> doc = self.portal['doc1']
  >>> doc.setRelatedItems(self.portal.news)
  >>> doc.reindexObject()
  >>> doc.getRelatedItems()
  [<ATFolder at /plone/news>]

The document has a relationship.  
  >>> doc.getRelationships()
  ['relatesTo']

Change relatedItems in the document content type's schema to be a 
SimpleReferenceField.

  >>> from Products.ATContentTypes.content.document import ATDocument
  >>> from upfront.simplereferencefield import SimpleReferenceField
  >>> ATDocument.schema['relatedItems'] = SimpleReferenceField(
  ...   'relatedItems', relationship='relatesTo', multiValued=1)
  >>> ATDocument.schema['relatedItems'].type
  'simplereference'

Create a document that references news.

  >>> self.portal.invokeFactory('Document', 'doc2')
  'doc2'
  >>> doc = self.portal['doc2']
  >>> doc.setRelatedItems(self.portal.news)
  >>> doc.reindexObject()
  >>> doc.getRelatedItems()
  [<ATFolder at /plone/news>]

The document has no relationships.  

  >>> doc.getRelationships()
  []

If we reference doc1 from doc2, doc1 will have doc2 set as back
reference.

  >>> self.portal.doc2.setRelatedItems(self.portal.doc1)
  >>> self.portal.doc2.getRelatedItems()
  [<ATDocument at /plone/doc1>]
  >>> self.portal.doc1.getRelatedItems()
  [<ATDocument at /plone/doc2>]

Setting back references are enabled by default but can be disabled.

  >>> ATDocument.schema['relatedItems'] = SimpleReferenceField(
  ...   'relatedItems', relationship='relatesTo', multiValued=1,
  ...   set_backreference=False)
  >>> self.portal.invokeFactory('Document', 'doc3')
  'doc3'
  >>> self.portal.doc3.setRelatedItems(self.portal.doc1)
  >>> self.portal.doc3.getRelatedItems()
  [<ATDocument at /plone/doc1>]
  >>> self.portal.doc1.getRelatedItems()
  [<ATDocument at /plone/doc2>]
