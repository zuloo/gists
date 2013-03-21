0.4.5 (2013/03/21)
------------------

* Fix bug #9 with some non-ascii characters (https://github.com/jdevesa/gists/issues/9)
** https://github.com/jdevesa/gists/commit/5100520eb0c6750292ee3d49a682c985c9417152
    
* Remove all '--credentials' arguments and use the prompt via 'getpass.getpass(string)'.
** https://github.com/jdevesa/gists/commit/e32b957bf78401537fdd7f06a05412ed0940ef54

0.4 (2012/30/12)
----------------

 * Add 'star/unstar' functionality 
 ** https://github.com/jdevesa/gists/commit/2724b0fe5bfa0e17e28abc969e63435f38c01686
 ** https://github.com/jdevesa/gists/commit/0417b00e22ef39d162459a6d8f9885a633072c4c

0.3 (2012/11/06)
----------------

 * Add 'fork' functionality 
 ** https://github.com/jdevesa/gists/commit/a0a68d771d36131c6c6dd720bd0046d291e5d33c

 * Create or update gist with multiple files at the same time 
 ** https://github.com/jdevesa/gists/commit/4813c2a1e58740d580ccec8c45a407a625f989b3

0.2 (2012/09/17)
----------------

 * Authentication based on OAuth 
 ** https://github.com/jdevesa/gists/commit/2e1e4dcd6237d37721e0509be46225ec2baac274

 * Adding 'version' command 
 ** https://github.com/jdevesa/gists/commit/ed1f0f5b849ce74be6d7cf32f6f7f0f8af250903

 * Pin the version of the dependences - 
 ** https://github.com/jdevesa/gists/commit/4a8df4d791c0360f09a1b580a3bf630202831910

0.1 (2012/09/07)
----------------

 * Initial version of the package. 
 * Basic gists functionallity: create, get, show, update, delete gists, BasicAuth authentication
