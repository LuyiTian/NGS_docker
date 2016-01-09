## bwa.py
import os

def bwa_index(in_fasta, version_cfg):
    """
    """
    _ref_version = version_cfg["REF_VERSION"]
    _bwa_version = version_cfg["BWA_VERSION"]

    cmd1 = \
        """sudo docker create \
    -v /ref \
    --name {_ref_v} reference:{_ref_v}""".format(_ref_v=_ref_version)

    cmd2 = \
        """sudo docker run \
    --rm \
    --volumes-from {_ref_v} \
    -w /ref \
    bwa:{_bwa_v} \
    bash -c "mkdir -p index && cd index && bwa index /ref/{in_f}" """.format(
        in_f=in_fasta,
        _ref_v=_ref_version,
        _bwa_v=_bwa_version)

    return " && ".join([cmd1,cmd2]), None


'''
def bwa_mem(in_fq_list, version_cfg, args):
    """
    """
    _ref_version = version_cfg["REF_VERSION"]
    _bwa_version = version_cfg["BWA_VERSION"]
    #if in_fq_list[0][-3:] == ".gz":
    cmd = \
        """docker run \
    --rm \
    --volumes-from {_ref_v} \
    -w {tmp_d} \
    bwa:{_bwa_v} \
    bash -c "mkdir -p index && cd index && bwa index {in_f}" """.format(
        in_f=in_fasta,
        _ref_v=_ref_version,
        _bwa_v=_bwa_version)
    return cmd, None
'''
