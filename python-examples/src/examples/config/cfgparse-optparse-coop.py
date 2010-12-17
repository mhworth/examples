#Uses cfgparse, available from http://cfgparse.sourceforge.net/
import cfgparse, optparse

#Create the parser
c = cfgparse.ConfigParser()
o = optparse.OptionParser()
#Add the options.  dest is the name that you will be able to use when retrieving the data,
#i.e., opts.<name>
o.add_option('-l',"--log-level",type="int", help="Provides a filter for the logging.", dest="log_level")
o.add_option("-c", "--config", type="string", help="Path to your config file", dest="config")
o.add_option('-v', "--verbose", type="int", help="Verbosity of console messages", dest="verbose")
c.add_option('log-level', dest="log_level")
c.add_option('config')
c.add_option('verbose')
c.add_file('cfgparse-optparse-coop.conf')

(opts,args) = c.parse(o)
#Print out what we got out of the config file
print 'loglevel: ' + str(opts.log_level)
print 'config: ' + str(opts.config)
print 'verbose: ' + str(opts.verbose)

