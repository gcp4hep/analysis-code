# Convert to parquet for usage in Google BigQuery

Convert the physlite files with the following modifications

* replace `.` in column names with `__`
* remove `AnalysisHLT` collection (currently not used and makes trouble in BQ)
* remove triple-jagged arrays (`METAssoc_AnalysisMETAux.overlapIndices`, `METAssoc_AnalysisMETAux.overlapTypes`)
* remove egammaClusters since they are sometimes missing
* skip files that don't have all fields to ensure consistent schema (e.g. Electrons, should not happen too often)

Example commands for panda submission:

```
git submodule init
git submodule update

inTarBall=to_parquet_forBQ.tgz
tar cfz ../"$inTarBall" *
cd ..
prun --containerImage /cvmfs/unpacked.cern.ch/registry.hub.docker.com/nikolaihartmann/physlite-experiments:6f11b90 \
     --inTarBall="$inTarBall" \
     --exec="python -m physlite_experiments.scripts.to_parquet '%IN' output.parquet --zip --max-partition-size 100000" \
     --outputs=output.parquet \
     --inDS=data17_13TeV.periodK.physics_Main.PhysCont.DAOD_PHYSLITE.grp17_v01_p4309 \
     --outDS=user.nihartma.physlite_to_parquet_gcp.data17_13TeV.periodK.grp17_v01_p4309_v3 \
     --nFilesPerJob 10 \
     --site=GOOGLE100 \
     --forceStaged --forceStagedSecondary \
     --destSE=GOOGLE_EU
```
