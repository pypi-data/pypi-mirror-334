<div style="width:100%;text-align:center;">
<img src="https://gitlab.gwdg.de/MedBioinf/mtb/adagenes/-/raw/main/assets/adagenes_v450x650.png?inline=false" alt="adagenes" width="100" />
</div>

# AdaGenes

[![pipeline](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes/badges/main/pipeline.svg)](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes)
[![commits](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes/-/jobs/artifacts/main/raw/commits.svg?job=build_badges)](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes)
[![license](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes/-/jobs/artifacts/main/raw/license.svg?job=build_badges)](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes)
[![coverage](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes/badges/main/coverage.svg)](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes)
[![python_version](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes/-/jobs/artifacts/main/raw/python_version.svg?job=build_badges)](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes)
[![release](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes/-/badges/release.svg)](https://gitlab.gwdg.de/MedBioinf/mtb/adagenes)


AdaGenes is a generic toolkit for processing, annotating, filtering and transforming DNA polymorphism data.

## Main features:
- A powerful data object to store and edit DNA mutation data
- Functionality to read and write files in common genomics file formats, including VCF, MAF, CSV/TSV, XLSX and 
plain text files
- Effective variant filtering according to specific threshold or feature values
- Liftover genome positions between hg38/GRCh38, hg19/GRCh37 and T2T-CHM13 reference genomes
- Effective variant normalization in VCF and HGVS notation

## Installation

AdaGenes is both usable as a Python package or directly from the command line. 
You can install AdaGenes in Python directly via PyPI:

```bash
pip install adagenes
```

## Getting started

### Reading files
Start by reading in a data file in one of the supported file formats in a biomarker frame with 
the ```read_file()``` function. adagenes automatically identifies the file type and inititates the corresponding file reader. 
You may also manually inititate a file reader and call its ```read_file()``` function:

```python
import adagenes as ag

bframe = ag.read_file("data/somaticMutations.vcf")

# Print biomarker identifiers
print(bframe.get_ids())

# Print loaded variant data completely
print(bframe.data)
```

Instead of loading a variant file, you may also create a biomarker frame manually at genomic or protein level:
```python
import adagenes as ag

# create biomarker frame based on variants at genomic level
bframe = ag.BiomarkerFrame(data=["chr7:g.140753336A>T"])
```

If the variant data has been parsed correctly, the data of the biomarker frame should be a nested JSON dictionary:
```
{
'chr7:140753336A>T': {'variant_data': {'CHROM': '7', 'POS': '140753336', 'ID': '.', 'REF': 'A', 'ALT': 'T', 'QUAL': '100', ... },
'chr1:2556664C>.': {'variant_data': {'CHROM': '1', 'POS': '2556664', 'ID': '.', ... } }
}
```

### Liftover

Convert the genomic positions of variants between genome assemblies with the liftover function (GRCh37 / GRCh38 / T2T-CHM13):

For large variant files, you can use the AdaGenes `process_file()` function for stream-based processing:
```python
import adagenes as ag

infile = "somaticMutations.vcf"
outfile = "somaticMutations.t2t.vcf"

client = ag.LiftoverClient(genome_version="hg19", target_genome="t2t")
ag.process_file(infile, outfile, client)
```

For small to medium sized variant files, you can load and edit the variant data as a biomarker frame: 
```python
import adagenes as ag

# Load a biomarker frame by defining the genome version (hg19/hg38/t2t)
infile = "somaticMutations.vcf"
bframe = ag.read_file(infile, genome_version="hg38")

# Liftover to another genome assemly
bframe_t2t = ag.liftover(bframe, target_genome="t2t")

# Write the new biomarker frame in T2T to a file
ag.write_file("somaticMutations.t2t.vcf", bframe_t2t)
```

### Filter mutations





### Annotate variants

Use Onkopus to annotate variants from the command line, e.g. 
```python
import adagenes as ag
import onkopus as op

bframe = ag.read_file("somaticMutations.vcf", genome_version="hg38")

bframe.data = op.PathogenicityClient(genome_version="hg38").process_data(bframe.data)

ag.write_file(bframe, "somaticMutations.annotated.vcf")
```

For further details on how to annotate variants, check out the [Onkopus][1] documentation. 

[1]: https://gitlab.gwdg.de/MedBioinf/mtb/onkopus/onkopus            "Onkopus"

### Variant notations and normalization




### Visualization



### Annotate variants

You can easily annotate variant data by combining an AdaGenes biomarker frame with the Onkopus annotation framework:
```python
pip install onkopus
```

Annotate the variant data of a biomarker frame by calling an Onkopus client directly on the bframe.data:

```python3
import adageness as av
import onkopus as op

genome_version="hg38"
bframe = av.read_file("somaticMutations.vcf", genome_version="hg38")

# Annotate with all Onkopus modules
bframe.data = op.annotate(bframe.data)

# Annotate with specific modules
bframe.data = op.AlphaMissenseClient(genome_version=genome_version).process_data(bframe.data)
bframe.data = op.GENCODEClient(genome_version=genome_version).process_data(bframe.data)

av.write_file("somaticMutations.annotated.avf",bframe)
```


### Saving data

Write a biomarker frame to a file with ```write_file()``` in one of the supported file formats (.vcf,.maf,.csv):

```python
import adagenes as ag

ag.write_file("/data/somaticMutations.annotated.maf", bframe, file_type="csv")
```

## Dependencies

- scikit-learn
- pandas
- matplotlib
- plotly
- pyliftover
- blosum
- openpyxl
- requests

## License

GPLv3





