"""Qualify the separate application profile without changing historical pins."""
import sys
from qualify_hero import qualify

if __name__ == '__main__':
    qualify(sys.argv[1], manifest_name='release-application-sources-v1.json', test_folder='application_tests',
            receipt_name='application-qualification.json', schema='cohesion-application-sources/1',
            hypnosis_extras='application,models', claim='installed application/process composition; POSIX native and Windows synthetic')
