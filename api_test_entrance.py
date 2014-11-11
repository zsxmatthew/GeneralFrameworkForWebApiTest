"""
  usage: %prog [options] args
  -s, --server=SERVER         :  server environment e.g. rdtest1, production, staging
  -m, --musicserver=MUSICSERVER  : music FE server
  -t, --testplan=TESTPLAN     :  testplan file
  -v, --clientversion=VERSION :  OviStore client version e.g. /stateless/26/
  -x, --timeout=TIMEOUT       :  Socket timeout value in case it needs to be extended
  -j, --jobname=JOBNAME       :  Specify the job name from Husdon environment
  -y, --useproxy              :  True/False flag to indicate if internet proxy is used or not.
  -d, --download              :  flag to enable or disable content download after purchase, default false
  -b, --buildno=BUILDNO       :  jenkins buildno passed to report
"""
import sys, time, unittest
import htmlreport
import TestSample
    
OPE_SERVER = 'payment.ovi.com'

if __name__=='__main__':
    mainsuite = unittest.TestSuite()  # create unittest suite
    htmlreport.CONSOLE_OUTPUT = True
    fp = file('%s_report.html'%(time.strftime('%Y%m%d%H%M')), 'wb')
    runner = htmlreport.HTMLTestRunner(          # create unitest html testsuite runner
                stream = fp,
                title='API general testing report: ',
                description='''This is a report automatically created by Pytusk Automation testing tool. \
                            Click 'pass', 'fail', or 'error' below for details.''',
                verbosity = 2,
                attrs = {}
                )
    mainsuite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSample.SampleTC))
    result = None
    print ""
    print "===================================================================" 
    res=runner.run(mainsuite,True,result)
    print "Runner completed!  Check result html file."
    print "Exiting with code:",res.failure_count+res.error_count
    sys.exit(res.failure_count+res.error_count)