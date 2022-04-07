.. _release_history:

Release and Version History
==============================================================================


0.0.4 (TODO)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.3 (Planned)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Support Named source policy styled permission
- Support more resource type like ``DataFilter``, ``DataLocation``

**Minor Improvements**

**Bugfixes**

- each ``Resource`` object should have a ``Catalog Id`` field. We cannot imply that it is equal to the boto session account id. Because it could be shared from another AWS Account.

**Miscellaneous**


0.0.2 (2022-04-04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First working version! allow you to manage LakeFormation Tag, Data lake permission and LF Tag attachment as code.
- Colorful logging like ``terraform plan``
- Allow dry run.


0.0.1 (2022-04-02)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- PyPI Place Holder release
