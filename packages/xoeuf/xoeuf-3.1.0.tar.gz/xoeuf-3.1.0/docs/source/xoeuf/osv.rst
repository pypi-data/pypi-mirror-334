=========================================
 :mod:`xoeuf.osv` -- General DB services
=========================================

.. module:: xoeuf.osv

.. autofunction:: savepoint


:mod:`xoeuf.osv.orm` -- OpenERP's Basic ORM extensions and utilities
====================================================================

.. module:: xoeuf.osv.orm

.. autofunction:: CREATE_RELATED(**values)

.. autofunction:: UPDATE_RELATED(id, **values)

.. autofunction:: REMOVE_RELATED(id)

.. autofunction:: FORGET_RELATED(id)

.. autofunction:: LINK_RELATED(id)

.. autofunction:: UNLINKALL_RELATED()

.. autofunction:: REPLACEWITH_RELATED(*ids)


:mod:`xoeuf.osv.expression` -- Working with Odoo domains
========================================================

.. module:: xoeuf.osv.expression

.. autoclass:: Domain
   :members: first_normal_form, second_normal_form, simplified,
             distribute_not, AND, OR, asfilter, walk

   .. data:: TRUE

      The domain which is True.  Implemented as ``[(1, '=', 1)]``.

   .. data:: FALSE

      The domain which is False.  Implemented as ``[(0, '=', 1)]``.
