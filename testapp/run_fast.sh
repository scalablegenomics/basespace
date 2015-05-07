#!/bin/bash
gunzip /data/input/samples/*
fastq2fasta.py /data/input/samples/* -o /data/output/appresults/output.fastq
