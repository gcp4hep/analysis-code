# convert to parquet with copy2scratch and 1 file per job
# (currently no way to do n-input -> n-output files jobs)

prun --containerImage /cvmfs/unpacked.cern.ch/registry.hub.docker.com/nikolaihartmann/physlite-experiments:6f11b90 \
     --exec="python -m physlite_experiments.scripts.to_parquet %IN output.parquet --zip --max-partition-size 50000" \
     --outputs=output.parquet \
     --inDS=data17_13TeV.00338183.physics_Main.deriv.DAOD_PHYSLITE.r10258_p3399_p4309_tid22958105_00 \
     --outDS=user.nihartma.physlite_to_parquet_gcp.00338183.r10258_p3399_p4309_tid22958105_00 \
     --nFilesPerJob 1 \
     --site=GOOGLE100 \
     --forceStaged --forceStagedSecondary \
     --destSE=GOOGLE_EU
