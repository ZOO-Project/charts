#!/bin/bash
#
# Author : Gérald FENOY
#
# Copyright 2021 GeoLabs SARL. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

mkdir -p /tmp/zTmp/statusInfos

CMD="curl -o /tmp/toto.out {{ include "zoo-project-dru.rabbitmq.serviceName" . }}:15672"
$CMD

if [ -e /tmp/toto.out ]; then echo "Should start" ; else echo wait; sleep 1; $CMD ; fi 

while [ ! -e /tmp/toto.out ]; do echo wait; sleep 1; $CMD ;  done

{{- if not .Values.keda.enabled }}
echo "START FPM in 5 seconds"
sleep 5
{{- end }}
rm toto.out

touch /var/log/zoofpm.log

if [ "$(id -u)" = "0" ]; then
	su www-data -s /bin/bash -c "cd /usr/lib/cgi-bin; ./zoo_loader_fpm ./main.cfg 2> /var/log/zoofpm.log >> /var/log/zoofpm.log"
else
	cd /usr/lib/cgi-bin
	./zoo_loader_fpm ./main.cfg 2> /var/log/zoofpm.log >> /var/log/zoofpm.log
fi
