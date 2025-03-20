# Copyright (c) 2024 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
from functools import partial
from pathlib import Path
import os, shutil, tempfile
import threading

from rich.pretty import pprint
pprint = partial(pprint, max_length=500)

here = Path(__file__).resolve().parent
data_dir = here/"data"


class PowerShellTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import pwsh
        cls.ps = pwsh.ps
        cls.lock = threading.Lock()

    @classmethod
    def tearDownClass(cls):
        cls.ps = None

    def setUp(self):
        self.lock.acquire()

    def tearDown(self):
        self.lock.release()

    def test_main(self):
        # https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_redirection?view=powershell-7.4
       #print(self.ps.Streams.Success)      # 1, Write-Output
        print(self.ps.Streams.Error)        # 2, Write-Error
        print(self.ps.Streams.Debug)        # 5, Write-Debug
        print(self.ps.Streams.Information)  # 6, Write-Information, Write-Host
        print(self.ps.Streams.Progress)     #
        print(self.ps.Streams.Warning)      # 3, Write-Warning
        print(self.ps.Streams.Verbose)      # 4, Write-Verbose

# Error       - Gets or sets the error buffer.       Powershell invocation writes the error    data into this buffer.
# Debug       - Gets or sets the debug buffer.       Powershell invocation writes the debug    data into this buffer. Can be null.
# Information - Gets or sets the information buffer. Powershell invocation writes the warning  data into this buffer. Can be null.
# Progress    - Gets or sets the progress buffer.    Powershell invocation writes the progress data into this buffer. Can be null.
# Warning     - Gets or sets the warning buffer.     Powershell invocation writes the warning  data into this buffer. Can be null.
# Verbose     - Gets or sets the verbose buffer.     Powershell invocation writes the verbose  data into this buffer. Can be null.
