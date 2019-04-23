#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import DecisionMaker

if __name__ == "__main__":
    ip = '127.0.0.1'
    port = {"follow":8887, "avoid":8888, "motor":8889}
    decision_maker = DecisionMaker.DecisionMaker("Decison Maker", ip, port)
    decision_maker.start()
    pass