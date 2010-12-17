#Uses cfgparse, available from http://cfgparse.sourceforge.net/
import cfgparse

#Create the parser
c = cfgparse.ConfigParser()

#Add the options.  dest is the name that you will be able to use when retrieving the data,
#i.e., opts.<name>
c.add_option('opt1',dest="opt01", type='string',keys="Section 1")
c.add_option('opt2',dest="opt02", type='string',keys="Section 1")
c.add_option('opt1', dest="opt11",type='string',keys="Section 2")
c.add_option('opt2', dest="opt12", type='string',keys="Section 2")
c.add_file('cfgparse-more.conf')

opts = c.parse()

#Print out what we got out of the config file
print 'Section 1, opt1: ' + opts.opt01
print 'Section 2, opt1: ' + opts.opt11
print 'Section 1, opt2: ' + opts.opt02
print 'Section 2, opt2: ' + opts.opt12

