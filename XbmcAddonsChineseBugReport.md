# How to report xbmc-addons-chinese bug with xbmc.log file #

Typically users will report errors with descriptions that lack many important details. While we take all user reported errors seriously, it is sometimes difficult to help if problem description is not clear or without a proper debug-log. This guide will take you through the steps to create such a log.

As such, if you need help with the issue you must follow these steps.

1. Launch new XBMC session to capture the log information.

2. Perform the steps that have problem.

3. Exit XBMC program

4. Find your debug Log here:

  * Linux:
```
$HOME/.xbmc/temp/xbmc.log
```

  * Mac OSX:
```
$User/Library/Logs/xbmc.log
```

  * Windows 7 & Vista:
```
\Users\<UserName>\AppData\Roaming\XBMC\xbmc.log
```

5. Go to the link below and open a "New issue":
```
 * http://code.google.com/p/xbmc-addons-chinese/issues/list
```
6. Give a brief description of your system; a step by step on how to reproduce the problem; what you have observed and what is the expected output.

7. Attached the captured debug xbmc.log in (4). Do not upload part of the log, we need the entire xbmc.log.

If you have problems and need help, please post your question on the forum thread and we will help you. But do not report the problem in the forum thread.
```
 * http://bbs.htpc1.com/forum-225-1.html
 * http://forum.xbmc.org/showthread.php?t=64250
```