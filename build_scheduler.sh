#!/usr/bin/env bash
javac -cp ${CLASSPATH} src/main/java/code/*.java 
java -cp "${CLASSPATH}:src/main/java" code.Scheduler


