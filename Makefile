#
# @author: jldupont
#
all: client_bridge

client_bridge:
	python tools/process_client_bridge.py
	
install:
	pip install pyyaml
