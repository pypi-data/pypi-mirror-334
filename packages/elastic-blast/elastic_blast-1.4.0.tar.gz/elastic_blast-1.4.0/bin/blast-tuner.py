#!/usr/bin/env python3
#                           PUBLIC DOMAIN NOTICE
#              National Center for Biotechnology Information
#  
# This software is a "United States Government Work" under the
# terms of the United States Copyright Act.  It was written as part of
# the authors' official duties as United States Government employees and
# thus cannot be copyrighted.  This software is freely available
# to the public for use.  The National Library of Medicine and the U.S.
# Government have not placed any restriction on its use or reproduction.
#   
# Although all reasonable efforts have been taken to ensure the accuracy
# and reliability of the software and data, the NLM and the U.S.
# Government do not and cannot warrant the performance or results that
# may be obtained by using this software or data.  The NLM and the U.S.
# Government disclaim all warranties, express or implied, including
# warranties of performance, merchantability or fitness for any particular
# purpose.
#   
# Please cite NCBI in any work or product based on this material.
"""
blast-tuner.py - See DESC constant below

Author: Christiam Camacho (camacho@ncbi.nlm.nih.gov)
Created: Tue 21 Apr 2020 12:07:42 PM EDT
"""
import os
import argparse
import json
import logging
from elastic_blast import VERSION
from elastic_blast.config import configure
from elastic_blast.util import ElbSupportedPrograms, UserReportError
from elastic_blast.util import get_query_batch_size, config_logging
from elastic_blast.tuner import DbData, SeqData, MTMode, MolType
from elastic_blast.tuner import get_mt_mode, get_num_cpus, get_batch_length
from elastic_blast.tuner import get_machine_type, get_mem_limit
from elastic_blast.base import DBSource, PositiveInteger, MemoryStr
from elastic_blast.constants import CFG_CLOUD_PROVIDER, CFG_CP_AWS_REGION, CFG_CP_GCP_REGION
from elastic_blast.constants import ELB_DFLT_GCP_REGION, ELB_DFLT_AWS_REGION
from elastic_blast.constants import CFG_BLAST, CFG_CLUSTER
from elastic_blast.constants import CFG_BLAST_DB, CFG_BLAST_PROGRAM, CFG_BLAST_BATCH_LEN
from elastic_blast.constants import CFG_BLAST_OPTIONS, CFG_CLUSTER_NUM_CPUS
from elastic_blast.constants import CFG_CLUSTER_MACHINE_TYPE
from elastic_blast.constants import CFG_BLAST_MEM_LIMIT, ELB_BLASTDB_MEMORY_MARGIN
from elastic_blast.constants import MolType, INPUT_ERROR, CSP, BLASTDB_ERROR
from elastic_blast.db_metadata import get_db_metadata


DESC = r"""This application's purpose is to provide suggestions to run help run
BLAST efficiently. It is meant to be used in conjunction with BLAST+ and
ElasticBLAST."""


def main():
    """ Entry point into this program. """
    try:
        parser = create_arg_parser()
        args = parser.parse_args()
        config_logging(args)

        options = '' if args.options is None else args.options
        SECTIONS = [ CFG_CLOUD_PROVIDER, CFG_BLAST, CFG_CLUSTER ]
        conf = { s : {} for s in SECTIONS }
        cloud_provider = CSP[args.csp_target]
        sp = ElbSupportedPrograms()

        db_source = DBSource[cloud_provider.name] if not args.db_source else DBSource[args.db_source]

        if args.db_mem_limit_factor is None:
            db_mem_limit_factor = 0.0 if cloud_provider == CSP.AWS else 1.1
        else:
            db_mem_limit_factor = args.db_mem_limit_factor

        if args.db is not None:
            try:
                db_metadata = get_db_metadata(args.db, sp.get_db_mol_type(args.program),
                                              db_source, gcp_prj=args.gcp_project)
            except FileNotFoundError:
                raise UserReportError(returncode=BLASTDB_ERROR,
                                      message=f'Metadata for BLAST database "{args.db}" was not found or database molecular type is not the same as required by BLAST program: "{args.program}"')
            db_data = DbData.from_metadata(db_metadata)
            conf[CFG_BLAST][CFG_BLAST_DB] = args.db

        if not args.region:
            if cloud_provider == CSP.AWS:
                args.region = ELB_DFLT_AWS_REGION
            else:
                args.region = ELB_DFLT_GCP_REGION

        if cloud_provider == CSP.AWS:
            conf[CFG_CLOUD_PROVIDER][CFG_CP_AWS_REGION] = args.region
        else:
            conf[CFG_CLOUD_PROVIDER][CFG_CP_GCP_REGION] = args.region

        query_data = None
        # The total_query_length argument is only relevant for small searches. If a query has fewer than 10k residues or 2.5M bases there is no need for MT mode 1. We could also reduce number of CPUs if there is not enough work for 15 or 16. The small searches will typically run pretty quickly, so this would be only tiny cost optimization.
        if args.total_query_length:
            query_data = SeqData(args.total_query_length,
                                 sp.get_query_mol_type(args.program))

        # MT mode is only used to inform selection of ElasticBLAST batch-length, memory,
        # and machine type as the best guess. BLAST+ selects MT mode.
        mt_mode = get_mt_mode(args.program, args.options, db_metadata, query_data)

        num_cpus = get_num_cpus(cloud_provider = cloud_provider,
                                program = args.program,
                                mt_mode = mt_mode,
                                query = query_data)
        conf[CFG_BLAST][CFG_BLAST_PROGRAM] = args.program
        task = ElbSupportedPrograms().get_task(args.program, args.options)
        conf[CFG_BLAST][CFG_BLAST_BATCH_LEN] = str(get_batch_length(cloud_provider = cloud_provider,
                                                          program = args.program,
                                                          task = task,
                                                          mt_mode = mt_mode,
                                                          num_cpus = num_cpus))

        if len(options) > 1:
           conf[CFG_BLAST][CFG_BLAST_OPTIONS] = options

        conf[CFG_CLUSTER][CFG_CLUSTER_NUM_CPUS] = str(num_cpus)

        if args.with_optimal:
            machine_type = 'optimal'
            if cloud_provider != CSP.AWS:
                raise UserReportError(INPUT_ERROR, f'The "optimal" instance type is only allowed for AWS')
        else:
            machine_type = get_machine_type(cloud_provider = cloud_provider,
                                            db = db_metadata,
                                            num_cpus = num_cpus,
                                            mt_mode = mt_mode,
                                            db_mem_margin = ELB_BLASTDB_MEMORY_MARGIN,
                                            region = args.region)

        conf[CFG_CLUSTER][CFG_CLUSTER_MACHINE_TYPE] = machine_type

        conf[CFG_BLAST][CFG_BLAST_MEM_LIMIT] = get_mem_limit(
                                                cloud_provider = cloud_provider,
                                                num_cpus = num_cpus,
                                                machine_type = machine_type,
                                                db = db_data,
                                                db_factor = db_mem_limit_factor)


        for section in SECTIONS:
            print(f'[{section}]', file=args.out)
            for key, value in sorted(conf[section].items(), key=lambda x: x[0]):
                print(f'{key} = {value}', file=args.out)
            print('', file=args.out)

        return 0
    except UserReportError as err:
        logging.error(err.message)
        return err.returncode


def create_arg_parser():
    """ Create the command line options parser object for this script. """
    DFLT_LOGFILE = 'stderr'
    parser = argparse.ArgumentParser(prog=os.path.basename(os.path.splitext(sys.argv[0])[0]), 
                                     description=DESC)
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument("--db", type=str, help="BLAST database to search", required=True)
    required.add_argument("--program", type=str, help="BLAST program to run",
                        choices=ElbSupportedPrograms().get(), required=True)
    required.add_argument("--csp-target", type=str, help="Which Cloud Service Provider to use, default: AWS", choices=['AWS', 'GCP'], default='AWS')
    required.add_argument('--out', type=argparse.FileType('w'), help='Save configuration in this file', default='-')

    optional.add_argument("--total-query-length", type=PositiveInteger,
                        help='Number of residues or bases in query sequecnes')
    optional.add_argument("--db-source", type=str, help="Where NCBI-provided databases are downloaded from, default: AWS", choices=['AWS', 'GCP', 'NCBI'])
    optional.add_argument("--region", type=str, help=f'Cloud Service Provider region. Defaults: {ELB_DFLT_AWS_REGION} for AWS; {ELB_DFLT_GCP_REGION} for GCP')
    optional.add_argument("--gcp-project", type=str, help=f'GCP project, required if --db-source or --csp-target is GCP')
    optional.add_argument("--options", type=str, help='BLAST options', default='')
    optional.add_argument("--db-mem-limit-factor", type=float,
                          help='This number times database bytes-to-cache will produce memory limit for a BLAST search. (default: 0.0: for AWS, 1.1 for GCP)')
    optional.add_argument("--with-optimal", action='store_true',
                         help='Use AWS optimal instance type')
    optional.add_argument('--version', action='version',
                        version='%(prog)s ' + VERSION)
    optional.add_argument("--logfile", default=DFLT_LOGFILE, type=str,
                        help="Default: " + DFLT_LOGFILE)
    optional.add_argument("--loglevel", default='INFO',
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    return parser


if __name__ == "__main__":
    import sys, traceback
    try:
        sys.exit(main())
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

