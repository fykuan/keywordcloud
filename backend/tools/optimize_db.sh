#!/usr/bin/env bash
#
MYSQLCHECK="/usr/bin/mysqlcheck"
SECRET=`cat .mysql`
echo ${SECRET}
${MYSQLCHECK} -uroot -p`cat .mysql` -Aov
