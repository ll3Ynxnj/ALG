#!/bin/sh -xeu

DIR_PATH=./Archives/`date "+%y%m%d-%H%M%S"`
mkdir ${DIR_PATH}
cp -r Labels ${DIR_PATH}
cp -r OrderLists ${DIR_PATH}
cp -r DataSource ${DIR_PATH}
cp -r ${DIR_PATH} ~/Public/ALGArchives/
rm Labels/*
rm OrderLists/*
rm DataSource/*
