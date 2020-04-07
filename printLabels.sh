#!/bin/sh -xeu

# プリンタの設定
lpoptions -p Brother_QL_720NW -o PageSize=29x90mm
lpoptions -p Brother_QL_720NW -o cupsPrintQuality=Normal

# ホストの環境とプリンタの設定を表示
sw_vers
lpstat -s
lpoptions -p Brother_QL_720NW -l

# ラベルを印刷
lpr -o landscape -P Brother_QL_720NW Labels/*.pdf
