# twobee

## Introduction

`twobee` is sort of two things rolled into one: it's a Python-based [2bit
file](https://genome.ucsc.edu/FAQ/FAQformat.html#format7) reading library,
wrapped in a [Textual](https://textual.textualize.io/) UI to provide a (for
now anyway) very simple viewer. It is, it has to be said, of very little
utility. I'm mostly writing it as a proof-of concept and as another way to
test some of the performance edges and use cases of Textual.

Also... I wanted a test project to get to know the Textual [line
API](https://textual.textualize.io/guide/widgets/#line-api) and this seemed
like a good fit.

## Installing

The package can be installed with `pip` or related tools, for example:

```sh
$ pip install twobee
```

As well as the library (which I'll give some minimal documentation for below
-- hopefully more comprehensive documentation will follow eventually), a
command is also installed called `twobee`. This can be used load up and view
the contents of a 2bit file.

## It's early days

This is a very early release of this code, it's still very much a work in
progress. This means things may change and break; it's also sitting atop
Textual which is, of course, still undergoing rapid development. As much as
possible I'll try and ensure that it's always working with the latest stable
release of Textual.

Also, because it's early days... while I love the collaborative aspect of
FOSS, I'm highly unlikely to be accepting any non-trivial PRs at the moment.
Developing this is a learning exercise for me, it's a hobby project, and
it's also something to help me further test Textual (disclaimer for those
who may not have gathered, I am employed by
[Textualize](https://www.textualize.io/)).

On the other hand: I'm *very* open to feedback and suggestions so don't
hesitate to engage with me in Discussions, or if it's a bug,in Issues. I
can't and won't promise that I'll take everything on board (see above about
hobby project, etc), but helpful input should help make this as useful as
possible in the longer term.

## The library

While I've not written this package to provide a 2bit-reading library, I
wanted to write one anyway (I've written one in [Common
Lisp](https://github.com/davep/org-davep-2bit), and one in [Emacs
Lisp](https://github.com/davep/2bit.el), it felt only right I should write
one in Python too). So, on the off chance someone else may want to mess with
this...

The library is designed so that there will be different ways of accessing a
2bit file, but for the moment there is just the option to load from a local
file. To do this you want a `TwoBitFileReader`:

```python
>>> from twobee import TwoBitFileReader
```

then it can be used to open a file:

```python
>>> hg38 = TwoBitFileReader( "hg38.2bit" )
```

The property `sequences` contains all of the sequences names contained in
the file, for example:

```python
>>> [ seq for seq in hg38.sequences if "_" not in seq ]
[
    'chr1',
    'chr10',
    'chr11',
    'chr12',
    'chr13',
    'chr14',
    'chr15',
    'chr16',
    'chr17',
    'chr18',
    'chr19',
    'chr2',
    'chr20',
    'chr21',
    'chr22',
    'chr3',
    'chr4',
    'chr5',
    'chr6',
    'chr7',
    'chr8',
    'chr9',
    'chrM',
    'chrX',
    'chrY'
]
```

The reader object itself can be used as an iterator too:

```python
>>> [ seq for seq in hg38 if "_" not in seq ]
[
    'chr1',
    'chr10',
    'chr11',
    'chr12',
    'chr13',
    'chr14',
    'chr15',
    'chr16',
    'chr17',
    'chr18',
    'chr19',
    'chr2',
    'chr20',
    'chr21',
    'chr22',
    'chr3',
    'chr4',
    'chr5',
    'chr6',
    'chr7',
    'chr8',
    'chr9',
    'chrM',
    'chrX',
    'chrY'
]
```

The reader can then be used like an array to get a particular sequence, for
example:

```python
>>> chrX = hg38[ "chrX" ]
>>> chrX
TwoBitSequence('chrX', dna_file_location=781826420, dna_size=156040895, len(n_blocks)=34, len(mask_blocks)=189177)
```

The `TwoBitSequence` that is returned can then be used in a similar way to
get a collection of bases. For example:

```python
>>> chrX[ 10000:10010 ]
TwoBitBases('chrX:10000..10010', bases='CTAACCCTAA')
```

There are a few convenience methods and the like on `TwoBitBases` to make it
easy to work with, with a bunch more to come as I get time to tinker.

[//]: # (README.md ends here)
