import sys
import os

import env_builder


os.environ.setdefault('selene_base_url', 'http://spielplatz.taocloud.org/sprint81/tao/Main/login')
env_builder.main(sys.argv[1:])