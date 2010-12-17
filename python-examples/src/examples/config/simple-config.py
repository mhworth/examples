#Uses cfgparse, available from http://cfgparse.sourceforge.net/

import cfgparse

c = cfgparse.ConfigParser()
c.add_option('CARoot', type='string')
c.add_file('simple-config.conf')
opts = c.parse()
print 'CA Root Directory:',opts.CARoot
