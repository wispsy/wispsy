"""Qualify the independent balanced-session/checkpoint source profile."""
import sys
from qualify_hero import qualify

if __name__=='__main__':
    qualify(sys.argv[1],manifest_name='hero-sources-v2.json',test_folder='session_tests',
            receipt_name='session-qualification.json',schema='hero-session-sources/2')
