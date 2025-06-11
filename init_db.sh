#!/bin/bash

psql -U admin -d meshos -h localhost -f /tmp/init.sql
