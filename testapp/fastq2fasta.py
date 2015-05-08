#!/usr/bin/python
import sys
import argparse
import screed


def get_parser():
    parser = argparse.ArgumentParser(
        description='Converts FASTQ format (.fq) files to FASTA format (.fa).',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('input_sequence', help='The name of the input'
                        ' FASTQ sequence file.')
    parser.add_argument('-d', '--directory')
    parser.add_argument('-o', '--output', metavar="filename",
                        help='The name of the output'
                        ' FASTA sequence file.',
                        type=argparse.FileType('w'),
                        default=sys.stdout)
    parser.add_argument('-n', '--n_keep', default=False, action='store_true',
                        help='Option to drop reads containing \'N\'s in ' +
                        'input_sequence file.')
    return parser


def main():
    args = get_parser().parse_args()
    print >> sys.stderr, ('fastq from ', args.input_sequence)

    n_count = 0
    for n, record in enumerate(screed.open(args.input_sequence,
                                           parse_description=False)):
        if n % 10000 == 0:
            print>>sys.stderr, '...', n

        sequence = record['sequence']
        name = record['name']

        if 'N' in sequence:
            if not args.n_keep:
                n_count += 1
                continue

        args.output.write('>' + name + '\n')
        args.output.write(sequence + '\n')

    print >> sys.stderr, '\n' + 'lines from ' + args.input_sequence

    if not args.n_keep:
        print >> sys.stderr, str(n_count) + ' lines dropped.'

    else:
        print >> sys.stderr, 'No lines dropped from file.'

    print >> sys.stderr, 'Wrote output to', args.output

if __name__ == '__main__':
    main()
