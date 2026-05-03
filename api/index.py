"""
Vercel FastAPI entrypoint
--------------------------

This module exposes a FastAPI ``app`` object that wraps the existing backend
application from this project. Vercel automatically discovers Python
applications by looking for a top‑level ``app`` instance in supported
entrypoints such as ``index.py`` or ``app.py``. By importing the existing
backend app here, we avoid duplicating any logic and keep the codebase
organized.  The backend code lives in the ``backend`` package alongside
``predictor.py`` and the various data source connectors.  Adjustments to the
prediction logic or endpoints should be made in ``backend/main.py``.

The import path uses ``sys.path.append`` to include the project root so that
Python can locate the ``backend`` package when deployed on Vercel.  This
technique is necessary because Vercel executes functions from within the
``api`` directory, which means relative imports like ``from backend.main``
would normally fail without adding the parent directory to ``sys.path``.

For more details on deploying FastAPI apps to Vercel, see the official
documentation which explains that Vercel looks for a ``FastAPI`` instance
named ``app`` in entrypoint files such as ``index.py``【865630093623360†L45-L58】.

"""

import os
import sys

# Add the parent directory to the Python path so that the ``backend`` package
# can be imported when this file is executed in Vercel's serverless
# environment.  Without this, ``from backend.main`` would fail because
# ``backend`` is a sibling of ``api`` and not in the default sys.path.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, os.pardir))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

# Import the FastAPI app from the backend.  The ``app`` instance is defined
# in ``backend/main.py`` where all routes and middleware are registered.
from backend.main import app  # noqa: E402  # import after modifying sys.path

__all__ = ["app"]