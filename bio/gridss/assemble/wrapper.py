"""Snakemake wrapper for gridss assemble"""

__author__ = "Christopher Schröder"
__copyright__ = "Copyright 2020, Christopher Schröder"
__email__ = "christopher.schroede@tu-dortmund.de"
__license__ = "MIT"

from snakemake.shell import shell
from os import path

# Creating log
log = snakemake.log_fmt_shell(stdout=True, stderr=True)

# Placeholder for optional parameters
extra = snakemake.params.get("extra", "")

# Check inputs/arguments.
reference = snakemake.input.get("reference")
dictionary = snakemake.input.get("dictionary")
if not snakemake.params.workingdir:
    raise ValueError("Please set params.workingdir to provide a working directory.")

if not snakemake.input.reference:
    raise ValueError("Please set input.reference to provide reference genome.")

for ending in (".amb", ".ann", ".bwt", ".pac", ".sa"):
    if not path.exists(f"{reference}{ending}"):
        raise ValueError(
            f"{reference}{ending} missing. Please make sure the reference was properly indexed by bwa."
        )

if not path.exists(f"{dictionary}"):
    raise ValueError(
        f"{reference}{ending} missing. Please make sure the reference dictionary was properly created. This can be accomplished for example by CreateSequenceDictionary.jar from Picard"
    )

shell(
    "(gridss -s assemble "  # Tool
    "--reference {reference} "  # Reference
    "--threads {snakemake.threads} "  # Threads
    "--workingdir {snakemake.params.workingdir} "  # Working directory
    "--assembly {snakemake.output.assembly} "  # Assembly output
    "{snakemake.input.bams} "
    "{extra}) {log}"
)
