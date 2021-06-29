# standard setup for copy2scratch

inDS=$(cat ../data_dids.txt | tr "\n" "," | sed 's/,$//')

prun --containerImage /cvmfs/unpacked.cern.ch/registry.hub.docker.com/nikolaihartmann/physlite-experiments:6f11b90 \
     --exec="python -m physlite_experiments.scripts.run_analysis_example --max-chunksize 100000 %IN" \
     --inDS="$inDS" \
     --outDS=user.nihartma.test_physlite_analysis_GCP_100p_copy2scratch_2021-06-28_1130 \
     --nFilesPerJob 30 \
     --site=GOOGLE100 \
     --forceStaged --forceStagedSecondary \
     --destSE=GOOGLE_EU
