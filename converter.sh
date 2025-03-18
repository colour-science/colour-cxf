#!/bin/sh

export PATH="/usr/lib/jvm/java-8-openjdk/jre/bin/:$PATH"
exec java -jar ~/Downloads/jsonix-schema-compiler-full.jar -generateJsonSchema -p PO ./schema.xsd