# -*- coding: utf-8 -*-
"""
Created on Fri March 14 18:28:36 2025

@author: Javier S. Zurdo
@module: Check if Spyder is enabled or not.
"""

#%% ------------ Libraries -----------------
# ------------------------------------------
import os

#%% ------------ Classes -------------------
# ------------------------------------------
class Check_Spyder:
    def check(self, test_type:str='environment_variables')->bool:
        is_spyder = False
        # Checking environment variables
        if test_type == 'environment_variables':
            is_spyder = any('SPYDER' in name for name in os.environ)
        else:  # Using spyder kernel values
            try: # fails when not ipython
                ip_name = get_ipython().__class__.__name__
                is_spyder = ip_name == 'SpyderShell'
            except:
                is_spyder = False
        return is_spyder

    def __init__(self, test_type:str='environment_variables'):
        self.test_type = test_type
        self.is_spyder = self.check()
