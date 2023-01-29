#!/bin/sh
brctl addbr xenbr0
ifconfig xenbr0 192.168.1.101/24
ifconfig xenbr0 up

