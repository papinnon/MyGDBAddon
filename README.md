### gdb addons

#### piebreak
	(gdb)$ piebreak offset == (gdb)$ break * LoadAddr+Offset 
#### pbreak
	持久断点
	(gdb)$ pbreak [foo.c:12234/ offset(PIE) / address(等价于break *)]
	(gdb)$ showpbp #打印持久断点
	(gdb)$ delpbp #under develop
