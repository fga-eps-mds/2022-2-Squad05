

import os
import sys
import importlib
from callback import Callback,import_all_callbacks
import inspect

def test_imports():
    
    import_all_callbacks(globals(),'../src')
    

    assert "Callback" in globals()
    assert "CallbackComDados" in globals()
    assert "CallbackSemDados" in globals()

    