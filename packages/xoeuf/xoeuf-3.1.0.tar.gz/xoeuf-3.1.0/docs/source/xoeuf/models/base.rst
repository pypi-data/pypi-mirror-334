============================================
 :mod:`xoeuf.models` - Utilities for models
============================================

The package
===========

.. module:: xoeuf.models

This module imports all of ``odoo.models`` into its namespace.  It also
re-exports the functions in `xoeuf.models.base`:mod:

.. class:: BaseModel

   This is the same as ``odoo.models.BaseModel`` with some extensions
   injected:

   .. property:: reference_repr

      The string representation compatible for Reference fields

   .. method:: iter_descendant_models(find_inherited=True, find_delegated=True, allow_abstract=False, allow_transient=False, exclude_self=True)

      Return a iterable of `(model_name, model)` of models inheriting from `self`.

      If `find_inherited` is True find models which use ``_inherit`` from
      `self`.  If `find_delegated` is True find models which use ``_inherits``
      (or ``delegate=True``) from `self`.

      If `allow_abstract` is True, yield models which are AbstractModels.  If
      `allow_transient` is True, yield transient models.

      If `exclude_self` is True, don't yield `self`.

      .. seealso:: xoeuf.models.base.iter_descendant_models

      .. versionadded:: 1.2.0

   .. method:: iter_pages(domain, order=None, *, page_size: int = 1000, show_progress: bool = True, progress_kwargs: Optional[dict] = None)

      Return an iterator over _pages_ of the given `domain`.

      This allows to process large models in chunks (pages).  If `order` is
      not given, use 'id'.

      Each iteration returns a recordset with at most `page_size` records.  If
      `show_progress` is true, use ``tqdm`` to show a progress bar, in this
      case, ``**progress_kwargs`` is passed to the function ``tqdm``.


Basic extensions
================

.. automodule:: xoeuf.models.base
   :members: get_modelname, ViewModel, iter_descendant_models
